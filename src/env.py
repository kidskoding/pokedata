"""
Shared environment setup for pokedata notebooks.

Import this first in any notebook. Auto-detects local vs Databricks.
Usage:
    from src.env import project_root, CACHE_ROOT, cache_path, BENCH_PATH, get_spark
    spark = get_spark()
    pokemon_cache = cache_path("pokemon")
"""

import sys
from pathlib import Path

def find_project_root() -> Path:
    """Walk up from cwd until we find src/ (project root)"""
    
    cwd = Path.cwd()
    for candidate in [cwd, cwd.parent, cwd.parent.parent]:
        if (candidate / "src").exists():
            return candidate
    return cwd

def using_databricks() -> bool:
    import os
    return "DATABRICKS_RUNTIME_VERSION" in os.environ

if using_databricks():
    base = "/dbfs/FileStore/pokedata"
    # Repos: repo is at /Workspace/Repos/.../pokedata with src/ inside
    candidate = find_project_root()
    project_root = candidate if (candidate / "src").exists() else Path(base)
    CACHE_ROOT = Path(f"{base}/cache")
    CACHE_PATH = f"{base}/cache"
    BENCH_PATH = f"{base}/format_benchmark"
    DELTA_ROOT = f"{base}/delta"
else:
    project_root = find_project_root()
    data = project_root / "data"

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

if not using_databricks():
    CACHE_ROOT = data / "cache"
    CACHE_PATH = str(CACHE_ROOT)
    BENCH_PATH = str(data / "format_benchmark")
    DELTA_ROOT = str(data / "delta")

def cache_path(endpoint: str) -> str:
    """Path to cached JSON for an endpoint (e.g. 'pokemon', 'move')"""
    return f"{CACHE_PATH}/{endpoint}"

def get_spark():
    """Get SparkSession. Databricks only — Spark is pre-configured on the cluster."""
    if not using_databricks():
        raise RuntimeError(
            "Spark notebooks require Databricks. Connect your repo at community.cloud.databricks.com "
            "and run notebooks there. See README Quick Start."
        )
        
    from pyspark.sql import SparkSession
    session = SparkSession.getActiveSession()
    if session is not None:
        return session
    raise RuntimeError("No active Spark session. Attach a cluster to this notebook.")
