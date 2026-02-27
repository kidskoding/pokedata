import asyncio
import aiohttp
import json
import os
import time
import uuid

from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

class AsyncPokeAPIFetcher:
    """
    Idempotent async fetcher for the PokeAPI.

    Design decisions:
    - Cache-first: always check local cache before hitting the network.
      This makes the pipeline idempotent — re-running never re-fetches
    - Semaphore(20): caps concurrent connections to respect PokeAPI fair use.
      In production you'd set this based on the API's rate limit headers
    - Exponential backoff: on 429/5xx, wait 1s→2s→4s before retrying
      Avoids thundering-herd problems when the API is temporarily degraded.
    """

    def __init__(
        self,
        cache_root: str | Path | None = None,
        manifest_path: str | Path | None = None,
        concurrency: int = 20,
        max_retries: int = 3,
    ):
        # Default to local data/cache (works without Databricks)
        _default_cache = Path(__file__).resolve().parent.parent / "data" / "cache"
        self.cache_root = Path(cache_root) if cache_root else _default_cache
        self.manifest_path = Path(manifest_path) if manifest_path else (self.cache_root / "manifest.json")
        self.semaphore = asyncio.Semaphore(concurrency)
        self.max_retries = max_retries
        self.manifest: Dict[str, Any] = self.load_manifest()
        self.run_id = str(uuid.uuid4())[:8]
        
    def load_manifest(self) -> Dict[str, Any]:
        if self.manifest_path.exists():
            with open(self.manifest_path) as f:
                return json.load(f)
        return {}
    
    def save_manifest(self):
        """Persist manifest to DBFS after each fetch"""
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.manifest_path, "w") as f:
            json.dump(self.manifest, f, indent=2)
    
    def manifest_key(self, endpoint: str, record_id: int) -> str:
        return f"{endpoint}/{record_id}"
    
    def is_cached(self, endpoint: str, record_id: int) -> bool:
        """Return True if both the file exists and was fetched successfully"""
        key = self.manifest_key(endpoint, record_id)
        cache_file = self.cache_root / endpoint / f"{record_id}.json"
        return (
            key in self.manifest
            and self.manifest[key].get("status") == 200
            and cache_file.exists()
        )
        
    async def fetch_one(
        self,
        session: aiohttp.ClientSession,
        endpoint: str,
        record_id: int,
        base_url: str,
    ) -> Tuple[bool, str]:
        """
        Fetch a single record. Returns (success, reason).
        Uses semaphore to cap concurrency and exponential backoff on failures
        """
        if self.is_cached(endpoint, record_id):
            return True, "cache_hit"

        url = f"{base_url}/{record_id}/"
        cache_file = self.cache_root / endpoint / f"{record_id}.json"
        cache_file.parent.mkdir(parents=True, exist_ok=True)

        async with self.semaphore:
            for attempt in range(self.max_retries):
                try:
                    start = time.time()
                    async with session.get(url) as resp:
                        status = resp.status

                        if status == 200:
                            data = await resp.json()
                            content = json.dumps(data).encode()
                            with open(cache_file, "wb") as f:
                                f.write(content)

                            self.manifest[self.manifest_key(endpoint, record_id)] = {
                                "status": 200,
                                "bytes": len(content),
                                "fetched_at": datetime.utcnow().isoformat(),
                                "retries": attempt,
                                "run_id": self.run_id,
                                "url": url,
                            }
                            return True, "fetched"

                        elif status in (429, 500, 502, 503, 504):
                            wait = 2 ** attempt
                            await asyncio.sleep(wait)
                            continue

                        else:
                            self.manifest[self.manifest_key(endpoint, record_id)] = {
                                "status": status,
                                "fetched_at": datetime.utcnow().isoformat(),
                                "retries": attempt,
                                "run_id": self.run_id,
                                "url": url,
                            }
                            return False, f"http_{status}"

                except aiohttp.ClientError as e:
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(2 ** attempt)
                    else:
                        self.manifest[self.manifest_key(endpoint, record_id)] = {
                            "status": "error",
                            "error": str(e),
                            "fetched_at": datetime.utcnow().isoformat(),
                            "retries": attempt,
                            "run_id": self.run_id,
                            "url": url,
                        }
                        return False, f"error: {e}"

        return False, "max_retries_exceeded"

    async def fetch_endpoint(
        self,
        endpoint: str,
        base_url: str,
        ids: list,
    ) -> Dict[str, int]:
        """
        Fetch all records for one endpoint concurrently
        Returns summary: {fetched, cached, failed}
        """
        try:
            from tqdm.asyncio import tqdm
        except ImportError:
            tqdm = None

        connector = aiohttp.TCPConnector(limit=50)
        timeout = aiohttp.ClientTimeout(total=30)

        results = {"fetched": 0, "cached": 0, "failed": 0}

        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            tasks = [
                self.fetch_one(session, endpoint, record_id, base_url)
                for record_id in ids
            ]

            if tqdm:
                iterator = tqdm.gather(*tasks, desc=f"  {endpoint}")
                outcomes = await iterator
            else:
                outcomes = await asyncio.gather(*tasks)

            for success, reason in outcomes:
                if reason == "cache_hit":
                    results["cached"] += 1
                elif success:
                    results["fetched"] += 1
                else:
                    results["failed"] += 1

        self.save_manifest()
        return results

    async def fetch_all(self, endpoints: Dict[str, Dict]) -> Dict[str, Dict]:
        """
        Fetch all endpoints sequentially (one at a time per endpoint,
        concurrent within each endpoint)

        Why sequential between endpoints rather than fully parallel?
        We want predictable resource usage and easier debugging.
        In production you might parallelize across endpoints too.
        """
        all_results = {}
        for name, config in endpoints.items():
            print(f"\n{'='*50}")
            print(f"Endpoint: {name} | Expected: {config['count']} records")
            ids = list(range(1, config["count"] + 1))
            result = await self.fetch_endpoint(name, config["url"], ids)
            all_results[name] = result
            print(f"  fetched={result['fetched']} cached={result['cached']} failed={result['failed']}")
        return all_results

    def validate_cache(self, endpoints: Dict[str, Dict]) -> bool:
        """
        Post-fetch validation: assert file counts match expected totals.
        This is a simple completeness check: a real DQ framework would
        also validate file sizes, JSON structure, etc
        """
        all_valid = True
        for endpoint, config in endpoints.items():
            cache_dir = self.cache_root / endpoint
            if not cache_dir.exists():
                print(f"  FAIL {endpoint}: directory missing")
                all_valid = False
                continue

            actual = len(list(cache_dir.glob("*.json")))
            expected = config["count"]

            tolerance = 50 if endpoint == "forms" else 5
            if abs(actual - expected) <= tolerance:
                print(f"  PASS {endpoint}: {actual} files (expected ~{expected})")
            else:
                print(f"  WARN {endpoint}: {actual} files (expected ~{expected})")
                if endpoint not in ("forms", "pokedexes"):
                    all_valid = False
        return all_valid

    def manifest_summary(self) -> Dict[str, int]:
        """Summarize the full manifest."""
        total = len(self.manifest)
        success = sum(1 for v in self.manifest.values() if v.get("status") == 200)
        failed = total - success
        total_bytes = sum(v.get("bytes", 0) for v in self.manifest.values())

        return {
            "total_records": total,
            "successful": success,
            "failed": failed,
            "total_mb": round(total_bytes / 1_000_000, 2),
        }