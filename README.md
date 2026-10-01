# pokedata

> data science, engineering, and analytics with Pokemon in Python!

> A production-grade data platform built on Pokémon data. Every notebook is a deep
> standalone showcase of one discipline. The engineering pipeline is the foundation:
> analytics and science notebooks read from Gold/Silver Delta tables, never raw files.
> Mirrors how **Databricks**-heavy companies like **JP Morgan Chase**, **Walmart**,
> **John Deere**, and **Dow** operate

This workbook was built to help people (specifically **students**) **understand all three data roles and how they differ** and provides hands-on work to help **land jobs** in any or all of them

I aim to make these roles **interesting** by using **Pokemon data** to give a concrete glimpse of how each role works: stats become features, types become segments, and generations become time periods

- **Data engineering** builds and maintains the infrastructure that moves and stores data. You’ll work through async API ingestion (caching, retry, rate limiting), the medallion architecture (Bronze raw landing → Silver cleaned/conformed → Gold aggregated), Delta Lake (ACID, time travel, CDF), file formats (Parquet, JSON, CSV), ETL vs ELT, data quality rules, and pipeline testing. Beyond entry-level: streaming, orchestration, observability, and security
- **Data analytics** turns data into insights and recommendations. You’ll use SQL (GROUP BY, window functions, CTEs, query optimization), profiling (schema, missingness, cardinality), EDA (univariate, bivariate, outlier detection), hypothesis testing, and KPI frameworks. Beyond entry-level: cohort analysis, interactive dashboards, executive reports, and forecasting.
- **Data science** builds predictive and prescriptive models. You’ll cover feature engineering, classification (binary, multiclass, handling imbalance), regression, clustering, interpretability (SHAP, PDP, ICE), NLP (sentiment, topic modeling, text classification), and the full ML lifecycle. Beyond entry-level: hyperparameter tuning, ensembles, experiment tracking, and model cards for production.

> Each track has its own notebooks and together show how a real data platform works end-to-end

Practice the full spectrum of skills using Pokemon data — from async API ingestion and Delta Lake pipelines through SQL analytics to predictive modeling, NLP, and model interpretability. Built for **intern / co-op / new grad** portfolios, with stretch content for mid and senior roles.

**Runs locally with PySpark:** All notebooks (engineering, analytics, science) run on a local PySpark session by default. The architecture mirrors a Databricks-style lakehouse (Bronze/Silver/Gold), so you can later port this project to Databricks if you have a workspace.

## Notebook Structure

### Engineering (`notebooks/engineering/`) — 20 notebooks

**Core (intern/co-op/new grad):** 01–11

| # | Notebook | Skill Area |
|---|----------|------------|
| 01 | Ingestion | Async PokeAPI fetch, cache, retry, rate limiting |
| 02 | File Formats | Parquet vs JSON vs CSV, columnar vs row |
| 03 | Bronze | Raw landing zone, append-only, CDF |
| 04 | Data Modeling | Star schema, fact vs dimension, SCD |
| 05 | Silver | Cleaning, conforming, junction tables |
| 06 | Gold | Aggregations, partitioning, serving layer |
| 07 | ETL vs ELT | Architecture patterns, push-down |
| 08 | Warehouse Concepts | OLAP vs OLTP, lakehouse |
| 09 | Delta Patterns | MERGE, time travel, CDF, OPTIMIZE, ZORDER |
| 10 | Data Quality | DQ rules, quarantine, pipeline contracts |
| 11 | Pipeline Testing | Unit tests, integration tests, pytest |

**Beyond entry-level:** 12–20

| # | Notebook | Skill Area |
|---|----------|------------|
| 12 | distributed_systems | Shuffles, partitioning, skew, Spark internals |
| 13 | streaming | Structured Streaming, watermarks, stateful ops |
| 14 | storage_optimization | Z-ordering, bloom filters, liquid clustering |
| 15 | query_optimization | Explain plans, AQE, broadcast/skew joins |
| 16 | data_modeling_advanced | Data vault, OBT, medallion patterns |
| 17 | cdc_patterns | CDC beyond CDF, SCD Type 2, log-based |
| 18 | orchestration | DAG, DLT, incremental CDF, Workflows |
| 19 | observability | Monitoring, alerting, lineage |
| 20 | security_governance | PII, masking, Unity Catalog |

### Analytics (`notebooks/analytics/`) — 20 notebooks

**Core (intern/co-op/new grad):** 01–11

| # | Notebook | Skill Area |
|---|----------|------------|
| 01 | group_by | Aggregations, ROLLUP, CUBE, GROUPING SETS |
| 02 | window_functions | ROW_NUMBER, RANK, LAG/LEAD, running totals |
| 03 | advanced_queries | CTEs, recursive CTEs, joins, PIVOT/UNPIVOT |
| 04 | query_optimization | EXPLAIN, predicate pushdown, broadcast joins |
| 05 | business_sql | Translate business questions to SQL |
| 06 | profiling | Schema, missingno, cardinality, row counts |
| 07 | univariate | Histograms, KDE, box plots, distributions |
| 08 | bivariate | Correlation, scatter, violin, heatmaps |
| 09 | outlier_detection | IQR, Z-score, Mahalanobis |
| 10 | hypothesis_inventory | H0/H1, test selection, pre-registration |
| 11 | kpi_framework | KPI design, percentiles, Shannon entropy |

**Beyond entry-level:** 12–20

| # | Notebook | Skill Area |
|---|----------|------------|
| 12 | cohort_analysis | Cohort definition, funnel, lifecycle |
| 13 | business_analogies | Executive communication, storytelling |
| 14 | plotly_dashboard | Interactive dashboards, HTML export |
| 15 | executive_report | Data storytelling, methodology appendix |
| 16 | power_creep | OLS trends, stratified analysis |
| 17 | type_diversity | Shannon entropy, before/after analysis |
| 18 | distribution_shifts | Hypothesis testing (15 tests), corrections |
| 19 | forecasting | ARIMA, Holt-Winters, prediction intervals |
| 20 | external_integration | Multi-source, fuzzy matching, enrichment |

### Science (`notebooks/science/`) — 24 notebooks

**Core (intern/co-op/new grad):** 01–11

| # | Notebook | Skill Area |
|---|----------|------------|
| 01 | feature_engineering | ColumnTransformer, Pipeline, train/val/test split |
| 02 | binary_classification | Baseline, class imbalance, ROC-AUC, calibration |
| 03 | multiclass_classification | Per-class metrics, confusion matrix |
| 04 | additional_classification | Multiple tasks, varying balance |
| 05 | interpretability | SHAP, PDP, ICE, permutation importance |
| 06 | bst_regression | Linear/tree regression, regularization, residuals |
| 07 | stat_regression | Multi-output, per-stat analysis |
| 08 | additional_regression | Non-stat targets, ordinal regression |
| 09 | feature_selection | VIF, RFE, Lasso path, mutual information |
| 10 | stat_clustering | K-Means, hierarchical, DBSCAN, GMM |
| 11 | cluster_profiling | Segment briefs, radar charts, cross-tabs |

**Beyond entry-level:** 12–24

| # | Notebook | Skill Area |
|---|----------|------------|
| 12 | dimensionality_reduction | PCA, t-SNE, UMAP |
| 13 | full_feature_clustering | High-dim clustering, ARI, stability |
| 14 | text_preprocessing | spaCy, lemmatization, vocabulary stats |
| 15 | tfidf_analysis | TF-IDF, word clouds, co-occurrence |
| 16 | sentiment | VADER, TextBlob, t-tests on sentiment |
| 17 | text_classification | TF-IDF + ML, sentence transformers |
| 18 | topic_modeling | LDA, coherence, pyLDAvis |
| 19 | unified_evaluation | McNemar, Wilcoxon, learning curves |
| 20 | hyperparameter_tuning | RandomizedSearchCV, Optuna |
| 21 | ensembles | Voting, stacking, calibration |
| 22 | feature_selection_rigor | Boruta, ablation, minimal model |
| 23 | experiment_tracking | JSONL logging, reproducibility |
| 24 | model_cards | Fairness, failure modes, production |

## Architecture - How all 3 roles flow together

```text
PokeAPI REST (18 endpoints, ~50,000+ records)
            │
            ▼  async aiohttp + semaphore + exponential backoff
Local cache (data/cache)  ← raw JSON, never re-fetched
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

**Local PySpark (recommended):** Everything runs on your machine using a local PySpark session. Engineering builds the pipeline; analytics and science read from the same Bronze/Silver/Gold data.

1. Install [uv](https://github.com/astral-sh/uv) and Python 3.10+ if you haven't already.
2. In this repo, run `uv sync` to create `.venv/` with all dependencies (including PySpark).
3. Start Jupyter: `uv run jupyter notebook`.
4. In Jupyter, open `notebooks/setup.ipynb` and run all cells once (per environment) — this installs `pokedata` as a package.
5. Run engineering notebooks in order (`engineering/01_ingestion` → `engineering/02_file_formats` → …).
6. Later, run analytics and science notebooks once Bronze/Silver/Gold data exists.

**Optional Databricks port:** If you have a Databricks workspace, you can clone this repo into Repos, point paths at Unity Catalog volumes in `src/env.py`, and reuse the same notebooks on a cluster.


## Project Structure

See [STRUCTURE.md](STRUCTURE.md) for the full directory layout and Pokemon-to-business domain mapping.

## Task Checklist

Per-notebook task checklists live in:
- [notebooks/engineering/TODO_ENGINEERING.md](notebooks/engineering/TODO_ENGINEERING.md)
- [notebooks/analytics/TODO_ANALYTICS.md](notebooks/analytics/TODO_ANALYTICS.md)
- [notebooks/science/TODO_SCIENCE.md](notebooks/science/TODO_SCIENCE.md)
