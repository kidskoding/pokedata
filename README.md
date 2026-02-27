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

**Beyond entry-level:** 11–19

| # | Notebook | Skill Area |
|---|----------|------------|
| 11 | distributed_systems | Shuffles, partitioning, skew, Spark internals |
| 12 | streaming | Structured Streaming, watermarks, stateful ops |
| 13 | storage_optimization | Z-ordering, bloom filters, liquid clustering |
| 14 | query_optimization | Explain plans, AQE, broadcast/skew joins |
| 15 | data_modeling_advanced | Data vault, OBT, medallion patterns |
| 16 | cdc_patterns | CDC beyond CDF, SCD Type 2, log-based |
| 17 | orchestration | DAG, DLT, incremental CDF, Workflows |
| 18 | observability | Monitoring, alerting, lineage |
| 19 | security_governance | PII, masking, Unity Catalog |

### Analytics (`notebooks/analytics/`) — 20 notebooks

**Core (intern/co-op/new grad):** 00–10

| # | Notebook | Skill Area |
|---|----------|------------|
| 00 | group_by | Aggregations, ROLLUP, CUBE, GROUPING SETS |
| 01 | window_functions | ROW_NUMBER, RANK, LAG/LEAD, running totals |
| 02 | advanced_queries | CTEs, recursive CTEs, joins, PIVOT/UNPIVOT |
| 03 | query_optimization | EXPLAIN, predicate pushdown, broadcast joins |
| 04 | business_sql | Translate business questions to SQL |
| 05 | profiling | Schema, missingno, cardinality, row counts |
| 06 | univariate | Histograms, KDE, box plots, distributions |
| 07 | bivariate | Correlation, scatter, violin, heatmaps |
| 08 | outlier_detection | IQR, Z-score, Mahalanobis |
| 09 | hypothesis_inventory | H0/H1, test selection, pre-registration |
| 10 | kpi_framework | KPI design, percentiles, Shannon entropy |

**Beyond entry-level:** 11–19

| # | Notebook | Skill Area |
|---|----------|------------|
| 11 | cohort_analysis | Cohort definition, funnel, lifecycle |
| 12 | business_analogies | Executive communication, storytelling |
| 13 | plotly_dashboard | Interactive dashboards, HTML export |
| 14 | executive_report | Data storytelling, methodology appendix |
| 15 | power_creep | OLS trends, stratified analysis |
| 16 | type_diversity | Shannon entropy, before/after analysis |
| 17 | distribution_shifts | Hypothesis testing (15 tests), corrections |
| 18 | forecasting | ARIMA, Holt-Winters, prediction intervals |
| 19 | external_integration | Multi-source, fuzzy matching, enrichment |

### Science (`notebooks/science/`) — 24 notebooks

**Core (intern/co-op/new grad):** 00–10

| # | Notebook | Skill Area |
|---|----------|------------|
| 00 | feature_engineering | ColumnTransformer, Pipeline, train/val/test split |
| 01 | binary_classification | Baseline, class imbalance, ROC-AUC, calibration |
| 02 | multiclass_classification | Per-class metrics, confusion matrix |
| 03 | additional_classification | Multiple tasks, varying balance |
| 04 | interpretability | SHAP, PDP, ICE, permutation importance |
| 05 | bst_regression | Linear/tree regression, regularization, residuals |
| 06 | stat_regression | Multi-output, per-stat analysis |
| 07 | additional_regression | Non-stat targets, ordinal regression |
| 08 | feature_selection | VIF, RFE, Lasso path, mutual information |
| 09 | stat_clustering | K-Means, hierarchical, DBSCAN, GMM |
| 10 | cluster_profiling | Segment briefs, radar charts, cross-tabs |

**Beyond entry-level:** 11–23

| # | Notebook | Skill Area |
|---|----------|------------|
| 11 | dimensionality_reduction | PCA, t-SNE, UMAP |
| 12 | full_feature_clustering | High-dim clustering, ARI, stability |
| 13 | text_preprocessing | spaCy, lemmatization, vocabulary stats |
| 14 | tfidf_analysis | TF-IDF, word clouds, co-occurrence |
| 15 | sentiment | VADER, TextBlob, t-tests on sentiment |
| 16 | text_classification | TF-IDF + ML, sentence transformers |
| 17 | topic_modeling | LDA, coherence, pyLDAvis |
| 18 | unified_evaluation | McNemar, Wilcoxon, learning curves |
| 19 | hyperparameter_tuning | RandomizedSearchCV, Optuna |
| 20 | ensembles | Voting, stacking, calibration |
| 21 | feature_selection_rigor | Boruta, ablation, minimal model |
| 22 | experiment_tracking | JSONL logging, reproducibility |
| 23 | model_cards | Fairness, failure modes, production |

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
