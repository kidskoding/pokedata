# TODO — Datathon Skill Preparation

All work lives in Jupyter notebooks. Shared constants (TYPE_COLORS, paths, etc.)
and helper functions are defined inline in the notebooks that need them.

---

## Notebook 00 — Data Pipeline

**Datathon skill:** Data acquisition, cleaning, feature engineering

- [ ] Define constants: TYPE_COLORS dict, STATS list, data paths
- [ ] Fetch all ~1025 Pokemon via pokebase with tqdm progress bar (id, name, height, weight, base_experience, types, 6 base stats, generation, is_legendary, is_mythical, capture_rate, growth_rate, color, shape)
- [ ] Fetch Pokedex flavor text (English) via pokemon-species endpoint
- [ ] Cache raw API responses to `data/cache/` so re-runs don't re-fetch
- [ ] Save raw data to `data/raw/pokemon_raw.csv` and `data/raw/flavor_text.csv`
- [ ] Clean: handle missing values, convert units (decimeters to meters, hectograms to kg)
- [ ] Feature engineering: total_stats, offensive_power, defensive_bulk, physical_ratio, speed_tier, stat_variance, is_dual_type, stat_percentile
- [ ] Save processed data to `data/processed/pokemon_clean.csv`
- [ ] Validate: no nulls in critical columns, stat ranges 1-255, all 18 types present

---

## Notebook 01 — EDA & Data Profiling

**Datathon skill:** Exploratory data analysis

- [ ] Dataset shape, dtypes, missing value heatmap, duplicates check
- [ ] Univariate: histograms + KDE for each stat, box plots, value counts for categoricals
- [ ] Bivariate: correlation heatmap, scatter matrix of 6 base stats, violin plots by type and generation
- [ ] Statistical summaries: mean, median, skew, kurtosis for each stat
- [ ] Outlier detection using IQR and z-scores
- [ ] Hypothesis generation for later notebooks (e.g., "Do later gens have higher stats?")

---

## Notebook 02 — Classification

**Datathon skill:** Binary + multiclass classification (like credit risk 2025)

- [ ] Binary: predict legendary status (~5% positive class, like fraud/default)
- [ ] Handle class imbalance: SMOTE or class_weight
- [ ] Models: Logistic Regression, Random Forest, XGBoost, SVM
- [ ] Metrics: confusion matrix, accuracy, precision, recall, F1, ROC-AUC curve
- [ ] Multiclass: predict primary type (18 classes, like customer segment classification)
- [ ] Feature importance analysis (permutation importance, built-in importances)
- [ ] 5-fold stratified cross-validation for all models

---

## Notebook 03 — Regression

**Datathon skill:** Regression modeling (like spending forecasting 2025)

- [ ] Target: predict total_stats from non-stat features (type, generation, legendary, capture_rate, weight, height)
- [ ] Models: Linear Regression, Ridge, Lasso, Random Forest, XGBoost
- [ ] Metrics: R-squared, RMSE, MAE, residual plots
- [ ] Regularization analysis: Ridge/Lasso coefficient paths as a function of alpha
- [ ] Residual diagnostics: Q-Q plot, residuals vs fitted, heteroscedasticity check
- [ ] Interpret coefficients in business language

---

## Notebook 04 — Clustering & Segmentation

**Datathon skill:** Customer segmentation (like risk tiers 2025)

- [ ] Standardize 6 base stats (StandardScaler)
- [ ] K-Means: elbow method + silhouette analysis, optimal k
- [ ] Profile clusters as archetypes (Sweeper, Tank, Wall, Generalist)
- [ ] Hierarchical clustering + dendrogram
- [ ] PCA: reduce to 2 components, plot clusters, explain variance ratios
- [ ] t-SNE visualization (optional but impressive)
- [ ] Business-style segment recommendations
- [ ] Cross-tabulation: cluster vs type, generation, legendary status

---

## Notebook 05 — Time Series & Trends

**Datathon skill:** Temporal analysis (like stock prediction 2019, economic impact 2018)

- [ ] Aggregate stats by generation (1-9) as time proxy
- [ ] Power creep: mean/median total_stats per gen, trend regression (OLS)
- [ ] Type diversity over time: Shannon diversity index per generation
- [ ] Statsmodels: decomposition, ACF/PACF plots, simple ARIMA for "Gen 10" forecast
- [ ] Stat distribution shift: overlaid KDE curves for Gen 1 vs Gen 5 vs Gen 9
- [ ] Legendary introduction rate trend

---

## Notebook 06 — NLP & Text Analysis

**Datathon skill:** Text analytics (like chatbot satisfaction 2023, call transcripts 2024)

- [ ] Load Pokedex flavor text from `data/raw/flavor_text.csv`
- [ ] Preprocessing: tokenize, remove stopwords, lemmatize (nltk)
- [ ] Word frequency analysis + word cloud
- [ ] Most common words per type (do Fire descriptions mention "flame" more?)
- [ ] VADER sentiment: legendary vs regular, Ghost vs Fairy type
- [ ] TF-IDF vectorization, predict type from description text
- [ ] Test if NLP features improve classification from notebook 02

---

## Notebook 07 — Model Comparison & Evaluation

**Datathon skill:** Rigorous model selection (judges want this)

- [ ] Re-run all classification models with consistent 5-fold stratified CV
- [ ] Re-run all regression models with consistent 5-fold CV
- [ ] Comparison tables: model x metric (accuracy, F1, AUC, R-squared, RMSE)
- [ ] Feature importance consensus across models
- [ ] Hyperparameter sensitivity plots for best model
- [ ] Final model selection narrative: interpretability vs performance tradeoffs

---

## Notebook 08 — Storytelling Dashboard

**Datathon skill:** Presentation + business recommendations (wins the competition)

- [ ] Executive summary: 3-5 key findings in plain language
- [ ] Publication-quality charts (consistent TYPE_COLORS, annotations, titles)
- [ ] Business recommendation framework:
  - Legendaries = high-value customers (5% of population, disproportionate stats)
  - Clusters = customer segments with actionable profiles
  - Power creep = inflationary market trend
- [ ] Plotly interactive charts for type distribution, clusters, time series
- [ ] Save all figures at 300 DPI to `outputs/figures/`
- [ ] Methodology appendix for datathon submission

---

## Stretch Goals

- [ ] **Streamlit dashboard** — deploy an interactive web app for the findings
- [ ] **Deep learning** — simple neural net for classification (PyTorch/TensorFlow)
- [ ] **External data integration** — pull Smogon competitive usage tiers, join with base stats
- [ ] **SHAP values** — explain individual predictions with SHAP library
- [ ] **Ensemble methods** — stacking/voting classifier combining best models
- [ ] **Anomaly detection** — Isolation Forest or DBSCAN on stat data
- [ ] **Mock datathon simulation** — time-boxed end-to-end problem with a "prompt"
