# TODO — Data Science, Engineering & Analytics with Pokemon

All work lives in Jupyter notebooks. Shared constants (TYPE_COLORS, paths, etc.)
and helper functions are defined inline in the notebooks that need them.

These skills carry directly to datathon competitions (UIUC Datathon, etc.)
and real-world data science work.

---

## Notebook 00 — Data Pipeline & Engineering

**Skills:** API data acquisition, ETL, data cleaning, feature engineering

- [ ] Define constants: TYPE_COLORS dict, STATS list, data paths
- [ ] Fetch all ~1025 Pokemon via pokebase with tqdm progress bar (id, name, height, weight, base_experience, types, 6 base stats, generation, is_legendary, is_mythical, capture_rate, growth_rate, color, shape)
- [ ] Fetch Pokedex flavor text (English) via pokemon-species endpoint
- [ ] Cache raw API responses to `data/cache/` so re-runs don't re-fetch
- [ ] Save raw data to `data/raw/pokemon_raw.csv` and `data/raw/flavor_text.csv`
- [ ] Load raw CSV into a SQLite database (`data/processed/pokemon.db`) for SQL practice
- [ ] Clean: handle missing values, convert units (decimeters to meters, hectograms to kg)
- [ ] Feature engineering: total_stats, offensive_power, defensive_bulk, physical_ratio, speed_tier, stat_variance, is_dual_type, stat_percentile
- [ ] Save processed data to `data/processed/pokemon_clean.csv`
- [ ] Validate: no nulls in critical columns, stat ranges 1-255, all 18 types present

---

## Notebook 01 — EDA & Data Profiling

**Skills:** Exploratory data analysis, Pandas, SQL queries, visualization

- [ ] Dataset shape, dtypes, missing value heatmap, duplicates check
- [ ] SQL queries against pokemon.db: aggregations, GROUP BY, JOINs, window functions
- [ ] Univariate: histograms + KDE for each stat, box plots, value counts for categoricals
- [ ] Bivariate: correlation heatmap, scatter matrix of 6 base stats, violin plots by type and generation
- [ ] Statistical summaries: mean, median, skew, kurtosis for each stat
- [ ] Outlier detection using IQR and z-scores
- [ ] Hypothesis generation for later notebooks (e.g., "Do later gens have higher stats?")

---

## Notebook 02 — Classification

**Skills:** Binary + multiclass classification, class imbalance handling, sklearn, XGBoost

- [ ] Binary: predict legendary status (~5% positive class, mirrors fraud/default detection)
- [ ] Handle class imbalance: SMOTE or class_weight
- [ ] Models: Logistic Regression, Random Forest, XGBoost, SVM
- [ ] Metrics: confusion matrix, accuracy, precision, recall, F1, ROC-AUC curve
- [ ] Multiclass: predict primary type (18 classes, mirrors customer segment classification)
- [ ] Feature importance analysis (permutation importance, built-in importances)
- [ ] 5-fold stratified cross-validation for all models

---

## Notebook 03 — Regression & Forecasting

**Skills:** Regression modeling, regularization, residual diagnostics

- [ ] Target: predict total_stats from non-stat features (type, generation, legendary, capture_rate, weight, height)
- [ ] Models: Linear Regression, Ridge, Lasso, Random Forest, XGBoost
- [ ] Metrics: R-squared, RMSE, MAE, residual plots
- [ ] Regularization analysis: Ridge/Lasso coefficient paths as a function of alpha
- [ ] Residual diagnostics: Q-Q plot, residuals vs fitted, heteroscedasticity check
- [ ] Interpret coefficients in business language (e.g., "capture_rate decrease of X predicts Y higher total_stats")

---

## Notebook 04 — Clustering & Segmentation

**Skills:** Unsupervised learning, dimensionality reduction, segment profiling

- [ ] Standardize 6 base stats (StandardScaler)
- [ ] K-Means: elbow method + silhouette analysis, optimal k
- [ ] Profile clusters as archetypes (Sweeper, Tank, Wall, Generalist)
- [ ] Hierarchical clustering + dendrogram
- [ ] PCA: reduce to 2 components, plot clusters, explain variance ratios
- [ ] t-SNE visualization (optional but impressive in presentations)
- [ ] Business-style segment recommendations (actionable profiles for each cluster)
- [ ] Cross-tabulation: cluster vs type, generation, legendary status

---

## Notebook 05 — Time Series & Trend Analysis

**Skills:** Temporal trends, decomposition, forecasting, statsmodels

- [ ] Aggregate stats by generation (1-9) as time proxy
- [ ] Power creep: mean/median total_stats per gen, trend regression (OLS)
- [ ] Type diversity over time: Shannon diversity index per generation
- [ ] Statsmodels: decomposition, ACF/PACF plots, simple ARIMA for "Gen 10" forecast
- [ ] Stat distribution shift: overlaid KDE curves for Gen 1 vs Gen 5 vs Gen 9
- [ ] Legendary introduction rate trend

---

## Notebook 06 — NLP & Text Analysis

**Skills:** Text preprocessing, sentiment analysis, TF-IDF, text-based prediction

- [ ] Load Pokedex flavor text from `data/raw/flavor_text.csv`
- [ ] Preprocessing: tokenize, remove stopwords, lemmatize (nltk)
- [ ] Word frequency analysis + word cloud
- [ ] Most common words per type (do Fire descriptions mention "flame" more?)
- [ ] VADER sentiment: legendary vs regular, Ghost vs Fairy type
- [ ] TF-IDF vectorization, predict type from description text
- [ ] Test if NLP features improve classification from notebook 02

---

## Notebook 07 — Hypothesis Testing & Statistical Inference

**Skills:** t-tests, ANOVA, chi-squared, statistical rigor

- [ ] t-test: are legendary Pokemon stats significantly higher than non-legendary?
- [ ] ANOVA: do base stat means differ significantly across types?
- [ ] Chi-squared: is the distribution of dual-types independent of generation?
- [ ] Mann-Whitney U: non-parametric comparison of stat distributions
- [ ] Effect size (Cohen's d) alongside p-values
- [ ] Multiple testing correction (Bonferroni) when running many comparisons
- [ ] Summarize which hypotheses from notebook 01 are statistically supported

---

## Notebook 08 — Model Comparison & Evaluation

**Skills:** Rigorous model selection, hyperparameter tuning, justification

- [ ] Re-run all classification models with consistent 5-fold stratified CV
- [ ] Re-run all regression models with consistent 5-fold CV
- [ ] Comparison tables: model x metric (accuracy, F1, AUC, R-squared, RMSE)
- [ ] Feature importance consensus across models
- [ ] Hyperparameter sensitivity plots for best model
- [ ] Final model selection narrative: interpretability vs performance tradeoffs

---

## Notebook 09 — External Data Integration

**Skills:** Joining external datasets, enrichment, thinking beyond one source

- [ ] Pull external data: Smogon competitive usage tiers OR community popularity rankings
- [ ] Join with base Pokemon dataset on name/id
- [ ] Analyze: do competitive viability and base stats correlate?
- [ ] Feature enrichment: add external features and re-run a model from notebook 02 or 03
- [ ] Compare model performance with vs without external features
- [ ] Document data sourcing methodology and limitations

---

## Notebook 10 — Storytelling & Presentation Dashboard

**Skills:** Data visualization, narrative, business recommendations

- [ ] Executive summary: 3-5 key findings in plain language
- [ ] Publication-quality charts (consistent TYPE_COLORS, annotations, titles)
- [ ] Business recommendation framework:
  - Legendaries = high-value customers (5% of population, disproportionate stats)
  - Clusters = customer segments with actionable profiles
  - Power creep = inflationary market trend
- [ ] Plotly interactive charts for type distribution, clusters, time series
- [ ] Save all figures at 300 DPI to `outputs/figures/`
- [ ] Methodology appendix suitable for a competition submission

---

## Stretch Goals

- [ ] **Streamlit dashboard** — deploy an interactive web app for the findings
- [ ] **Deep learning** — simple neural net for classification (PyTorch/TensorFlow)
- [ ] **SHAP values** — explain individual predictions with SHAP library
- [ ] **Ensemble methods** — stacking/voting classifier combining best models
- [ ] **Anomaly detection** — Isolation Forest or DBSCAN on stat data
- [ ] **Mock datathon simulation** — time-boxed end-to-end problem with a "prompt"
