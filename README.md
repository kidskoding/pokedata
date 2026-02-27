# pokedata

Data science, engineering, and analytics with Pokemon in Python.

Practice the full spectrum of data engineering, analytics, and data science skills
using Pokemon data — from async API ingestion and Delta Lake pipelines through SQL
analytics, predictive modeling, NLP, and model interpretability. Designed for
**intern / co-op / new grad** portfolios, with stretch content for mid and senior roles.

> A production-grade data platform built on Pokémon data. Every notebook is a deep
> standalone showcase of one discipline. The engineering pipeline is the foundation:
> analytics and science notebooks read from Gold/Silver Delta tables, never raw files.
> Mirrors how **Databricks**-heavy companies like **JP Morgan Chase**, **Walmart**,
> **John Deere**, and **Dow** operate.

## Notebook Structure

### Engineering (`notebooks/engineering/`) — 20 notebooks

**Core (intern/co-op/new grad):** 00–10

| # | Notebook | Skill Area |
|---|----------|------------|
| 00 | Ingestion | Async PokeAPI fetch, cache, retry, rate limiting |
| 01 | File Formats | Parquet vs JSON vs CSV, columnar vs row |
| 02 | Bronze | Raw landing zone, append-only, CDF |
| 03 | Data Modeling | Star schema, fact vs dimension, SCD |
| 04 | Silver | Cleaning, conforming, junction tables |
| 05 | Gold | Aggregations, partitioning, serving layer |
| 06 | ETL vs ELT | Architecture patterns, push-down |
| 07 | Warehouse Concepts | OLAP vs OLTP, lakehouse |
| 08 | Delta Patterns | MERGE, time travel, CDF, OPTIMIZE, ZORDER |
| 09 | Data Quality | DQ rules, quarantine, pipeline contracts |
| 10 | Pipeline Testing | Unit tests, integration tests, pytest |

**Beyond entry-level:** 11–19 (Spark internals, streaming, storage/query optimization, CDC, orchestration, observability, security)

### Analytics (`notebooks/analytics/`) — 20 notebooks

**Core (intern/co-op/new grad):** 00–10 — GROUP BY, window functions, CTEs, query optimization, business SQL, profiling, univariate/bivariate EDA, outlier detection, hypothesis inventory, KPI framework

**Beyond entry-level:** 11–19 — Cohort analysis, business analogies, Plotly dashboards, executive reports, power creep, type diversity, hypothesis testing, forecasting, external integration

### Science (`notebooks/science/`) — 24 notebooks

**Core (intern/co-op/new grad):** 00–10 — Feature engineering, classification, interpretability, regression, feature selection, clustering, cluster profiling

**Beyond entry-level:** 11–23 — Dimensionality reduction, NLP, sentiment, text classification, topic modeling, unified evaluation, hyperparameter tuning, ensembles, experiment tracking, model cards

## Architecture

```text
PokeAPI REST (18 endpoints, ~50,000+ records)
            │
            ▼  async aiohttp + semaphore + exponential backoff
DBFS cache  ← raw JSON, never re-fetched
            │
            ▼  PySpark + StructType schemas
┌──────────────────────────────────────────┐
│  BRONZE  — append-only, immutable        │
│  18 tables, Change Data Feed enabled     │
└──────────────────────────────────────────┘
            │
            ▼  PySpark transforms + schema enforcement
┌──────────────────────────────────────────┐
│  SILVER  — cleaned, typed, validated     │
│  20 tables, junction tables              │
└──────────────────────────────────────────┘
            │
            ▼  aggregations + feature engineering
┌──────────────────────────────────────────┐
│  GOLD  — business-ready, query-optimized │
│  10 wide tables, ZORDERed, OPTIMIZE'd    │
└──────────────────────────────────────────┘
            │
     ┌──────┴──────┐
     ▼             ▼
Analytics      Data Science
(notebooks/    (notebooks/
 analytics/)    science/)
```

## Quick Start

**Local (uv + Jupyter):**
```bash
uv sync
uv run jupyter notebook
# Run notebooks/engineering/00_ingestion.ipynb first
```

**Databricks:**
1. Create a Community Edition cluster (Runtime 13.x LTS, single node)
2. Install cluster libraries: `aiohttp`, `tqdm`, `optuna`, `shap`, `imbalanced-learn`,
   `lightgbm`, `sentence-transformers`, `pyLDAvis`, `missingno`, `boruta`, `mord`
3. Upload `src/` to `dbfs:/FileStore/pokedata/src/`
4. Run `notebooks/engineering/` in order (00 → 19) to build the Delta pipeline
5. Then run any `analytics/` or `science/` notebook

## Project Structure

See [STRUCTURE.md](STRUCTURE.md) for the full directory layout and Pokemon-to-business domain mapping.

## Task Checklist

Per-notebook task checklists live in:
- [notebooks/engineering/TODO_ENGINEERING.md](notebooks/engineering/TODO_ENGINEERING.md)
- [notebooks/analytics/TODO_ANALYTICS.md](notebooks/analytics/TODO_ANALYTICS.md)
- [notebooks/science/TODO_SCIENCE.md](notebooks/science/TODO_SCIENCE.md)
