# pokedata

data science, engineering, and analytics with pokemon in Python!

Practice the full spectrum of data engineering, analytics, and data science skills
using Pokemon data — from async API ingestion and Delta Lake pipelines through SQL
analytics, predictive modeling, NLP, and model interpretability. These skills carry
directly to datathon competitions and real-world data work at companies like Dow.

All work runs on **Databricks** against Delta tables — the same stack used in industry.

## Notebook Structure

### Engineering (`notebooks/engineering/`) — 7 notebooks

| # | Notebook | Skill Area |
| --- | --- | --- |
| 00 | Ingestion | Async PokeAPI fetch, DBFS cache, retry logic |
| 01 | Bronze | PySpark ingestion → append-only Delta tables |
| 02 | Silver | Cleaning, typing, schema validation |
| 03 | Gold | Aggregations, feature engineering, wide tables |
| 04 | Delta Patterns | Change Data Feed, time travel, OPTIMIZE/ZORDER |
| 05 | Data Quality | DQ rule engine, assertions, HTML reports |
| 06 | Orchestration | Pipeline sequencing, logging, monitoring |

### Analytics (`notebooks/analytics/`) — 20 notebooks

| # | Notebook | Skill Area |
| --- | --- | --- |
| 00 | GROUP BY Mastery | Aggregation patterns, window functions |
| 01 | Window Functions | RANK, LAG/LEAD, running totals |
| 02 | Advanced Queries | CTEs, subqueries, self-joins |
| 03 | Query Optimization | EXPLAIN, Z-ordering, partition pruning |
| 04 | Business SQL | KPI queries, funnel analysis |
| 05 | Profiling | Missing values, distributions, outliers |
| 06 | Univariate EDA | Distributions, skewness, histograms |
| 07 | Bivariate EDA | Correlations, scatter plots, heatmaps |
| 08 | Outlier Detection | IQR, Z-score, isolation forest |
| 09 | Hypothesis Inventory | Structured hypothesis catalog |
| 10 | KPI Framework | Business metric design |
| 11 | Cohort Analysis | Generation cohorts, retention curves |
| 12 | Business Analogies | Pokemon-to-business domain mapping |
| 13 | Plotly Dashboard | Interactive charts and dashboards |
| 14 | Executive Report | Narrative storytelling, slide-ready output |
| 15 | Power Creep | Stat inflation over generations |
| 16 | Type Diversity | Type distribution analysis |
| 17 | Distribution Shifts | Cross-generation stat drift |
| 18 | Forecasting | ARIMA, trend decomposition, statsmodels |
| 19 | External Integration | Smogon data join, feature enrichment |

### Science (`notebooks/science/`) — 24 notebooks

| # | Notebook | Skill Area |
| --- | --- | --- |
| 00 | Feature Engineering | sklearn Pipeline, ColumnTransformer, OHE, splits |
| 01 | Binary Classification | Legendary prediction, class imbalance, SMOTE |
| 02 | Multiclass Classification | 18-class type prediction, per-class metrics |
| 03 | Additional Classification | is_evolved, evolution trigger, dual type |
| 04 | Interpretability | SHAP, PDP, ICE, permutation importance |
| 05 | BST Regression | Predict total base stat, regularization paths |
| 06 | Stat Regression | Multi-output regression, per-stat analysis |
| 07 | Additional Regression | Capture rate, base experience, movepool size |
| 08 | Feature Selection | VIF, RFE, Lasso path, mutual information |
| 09 | Stat Clustering | K-Means, DBSCAN, GMM, cluster validation |
| 10 | Cluster Profiling | Archetype labeling, radar charts, segment briefs |
| 11 | Dimensionality Reduction | PCA, t-SNE, UMAP |
| 12 | Full Feature Clustering | High-dim clustering, ARI, stability analysis |
| 13 | Text Preprocessing | spaCy pipeline, stopwords, lemmatization |
| 14 | TF-IDF Analysis | Word clouds, bigrams, co-occurrence networks |
| 15 | Sentiment | VADER, TextBlob, sentiment trends, t-tests |
| 16 | Text Classification | TF-IDF + ML, sentence transformers |
| 17 | Topic Modeling | LDA, coherence scores, pyLDAvis |
| 18 | Unified Evaluation | Cross-model comparison, McNemar's, Wilcoxon |
| 19 | Hyperparameter Tuning | RandomizedSearch, Optuna TPE, early stopping |
| 20 | Ensembles | Soft voting, stacking, calibration, ablation |
| 21 | Feature Selection Rigor | Boruta, permutation stability, minimal model |
| 22 | Experiment Tracking | JSONL logging, reproducibility, MLflow concepts |
| 23 | Model Cards | Fairness analysis, failure modes, production readiness |

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

1. Create a Databricks Community Edition cluster (Runtime 13.x LTS, single node)
2. Install cluster libraries: `aiohttp`, `tqdm`, `optuna`, `shap`, `imbalanced-learn`,
   `lightgbm`, `sentence-transformers`, `pyLDAvis`, `missingno`, `boruta`, `mord`
3. Upload `src/` to `dbfs:/FileStore/pokedata/src/`
4. Run `notebooks/engineering/` in order (00 → 06) to build the Delta pipeline
5. Then run any `analytics/` or `science/` notebook

## Project Structure

See [STRUCTURE.md](STRUCTURE.md) for the full directory layout and Pokemon-to-business domain mapping.

## Task Checklist

See [TODO.md](TODO.md) for the per-notebook task checklist.
