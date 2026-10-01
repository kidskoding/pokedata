"""
Shared environment setup for pokedata notebooks.

Import this first in any notebook.

Defaults:
- **Local:** uses a local PySpark session (`master=local[*]`) and the `data/` folder.
- **Databricks (optional):** if `DATABRICKS_RUNTIME_VERSION` is set, uses Unity Catalog
  style paths under `/Volumes/pokedata/default/pokedata`.

Usage:
    from src.env import project_root, CACHE_ROOT, cache_path, BENCH_PATH, get_spark
    spark = get_spark()
    pokemon_cache = cache_path("pokemon")
"""

import sys
from pathlib import Path


def find_project_root() -> Path:
    """Walk up from cwd until we find src/ (project root)."""

    cwd = Path.cwd()
    for candidate in [cwd, cwd.parent, cwd.parent.parent]:
        if (candidate / "src").exists():
            return candidate
    return cwd


def using_databricks() -> bool:
    """Return True when running on a Databricks cluster."""
    import os

    return "DATABRICKS_RUNTIME_VERSION" in os.environ


if using_databricks():
    import os

    # Catalog pokedata, schema default, volume pokedata. Override via POKEDATA_DBFS_PATH.
    base = os.environ.get("POKEDATA_DBFS_PATH", "/Volumes/pokedata/default/pokedata")
    candidate = find_project_root()
    project_root = candidate if (candidate / "src").exists() else Path(base)
    CACHE_ROOT = Path(f"{base}/cache")
    CACHE_PATH = f"{base}/cache"
    BENCH_PATH = f"{base}/format_benchmark"
    DELTA_ROOT = f"{base}/delta"
else:
    project_root = find_project_root()
    data = project_root / "data"
    CACHE_ROOT = data / "cache"
    CACHE_PATH = str(CACHE_ROOT)
    BENCH_PATH = str(data / "format_benchmark")
    DELTA_ROOT = str(data / "delta")


if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def cache_path(endpoint: str) -> str:
    """Path to cached JSON for an endpoint (e.g. 'pokemon', 'move')."""
    return f"{CACHE_PATH}/{endpoint}"


def get_spark():
    """
    Get a SparkSession.

    - **Local:** creates (or reuses) a `local[*]` PySpark session.
    - **Databricks:** returns the active cluster SparkSession.
    """
    from pyspark.sql import SparkSession

    if using_databricks():
        session = SparkSession.getActiveSession()
        if session is not None:
            return session
        raise RuntimeError("No active Spark session. Attach a cluster to this notebook.")

    # Local PySpark
    return (
        SparkSession.builder.appName("pokedata-local")
        .master("local[*]")
        .getOrCreate()
    )
