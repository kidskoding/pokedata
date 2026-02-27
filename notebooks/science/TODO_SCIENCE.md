# TODO — Data Science (notebooks/science/)

> All notebooks run on Databricks Community Edition.
> All data reads from Gold or Silver Delta tables — never raw files.
> Start each notebook with:
> ```python
> import sys
> sys.path.insert(0, '/dbfs/FileStore/pokedata/src')
> from constants import TYPE_COLORS, GOLD_PATH
> import pandas as pd
> gold = spark.read.format("delta").load(GOLD_PATH + "pokemon_full").toPandas()
> ```

---

## 00_feature_engineering.ipynb — Feature Engineering for ML

**Skills:** sklearn ColumnTransformer, Pipeline, OrdinalEncoder, OneHotEncoder,
StandardScaler, train/val/test split, feature versioning, feature documentation

- [ ] Load `gold.pokemon_full` + `gold.pokemon_movepool` → merge into one ML DataFrame
- [ ] **Numeric features:** all 6 stats, total_stats, offensive_power, defensive_bulk,
      physical_ratio, stat_variance, stat_cv, height_m, weight_kg, capture_rate,
      base_experience, base_happiness, chain_length, evolution_stage (as int),
      movepool_size_total, avg_move_power, coverage_type_count, stab_move_count,
      has_priority_move (bool as int), has_recovery_move, has_setup_move
- [ ] **Ordinal features:** generation (1–9), speed_tier (slow=0/mid=1/fast=2/ultra=3)
- [ ] **Nominal features:** type_1, type_2 (with "None" for mono-type), egg_group_1,
      egg_group_2, color, shape, habitat, growth_rate, evolution_trigger
- [ ] **Type matchup features:** best_offensive_multiplier, count_4x_weaknesses,
      count_immunities, count_resistances — join from gold.type_effectiveness_matrix
- [ ] Build sklearn `Pipeline` with `ColumnTransformer`:
      numeric branch (StandardScaler) + ordinal branch (OrdinalEncoder) +
      nominal branch (OneHotEncoder with handle_unknown='ignore')
- [ ] **Train/val/test split:** 60/20/20, stratified on is_legendary, `random_state=42`
- [ ] **Feature set versions (document all 3 for ablation in 21_feature_selection_rigor):**
      - v1: stats only (6 columns)
      - v2: stats + categorical encodings
      - v3: v2 + movepool features + type matchup features
- [ ] Save fitted Pipeline transformer to `dbfs:/FileStore/pokedata/outputs/feature_pipeline.pkl`
- [ ] Feature documentation table: feature name, type, source table, description, null rate

---

## 01_binary_classification.ipynb — Legendary Status Prediction

**Skills:** Binary classification, DummyClassifier baseline, class imbalance (SMOTE, ADASYN,
class_weight), precision/recall tradeoff, threshold analysis, calibration, 5-fold CV

- [ ] **Baseline:** `DummyClassifier(strategy='stratified')` and `most_frequent` — establish floor
- [ ] **Models:** Logistic Regression, Random Forest, Gradient Boosting, XGBoost,
      LightGBM, SVM (RBF kernel), KNN (k=5, k=15)
- [ ] **Class imbalance (~5% positive) — compare 4 strategies:**
      `class_weight='balanced'`, SMOTE, ADASYN, no resampling.
      For each: precision, recall, F1, ROC-AUC, PR-AUC.
      Takeaway: which strategy best preserves precision vs recall tradeoff?
- [ ] **Metrics for all models:** confusion matrix, accuracy, precision, recall, F1,
      ROC-AUC, PR-AUC — displayed in one comparison table
- [ ] **Threshold analysis:**
      - F1 vs threshold curve for best model
      - Precision-Recall tradeoff curve
      - Choose optimal threshold; show how it shifts confusion matrix
- [ ] **Calibration curves:**
      - Reliability diagram (predicted probability vs actual fraction positive)
      - Apply Platt scaling + isotonic regression
      - Compare Brier scores before/after calibration
- [ ] **5-fold stratified CV** for all models. Report mean ± std per metric.
- [ ] **Learning curves:** train size vs CV score (train + val). Diagnose overfitting.

---

## 02_multiclass_classification.ipynb — Primary Type Prediction

**Skills:** 18-class classification, per-class metrics, confusion matrix analysis,
class imbalance in multiclass, interpretable results

- [ ] **Task:** predict type_1 from physical + species features only
      (no type_2, no moves — can physical features alone reveal type?)
- [ ] **Features:** stats, height_m, weight_kg, color, shape, habitat, egg_groups, generation
- [ ] **Baseline:** `DummyClassifier(strategy='stratified')` — note Water/Normal dominance
- [ ] **Models:** Logistic Regression (OvR), Random Forest, XGBoost, LightGBM
- [ ] **Metrics:** macro F1, weighted F1, per-class precision/recall table (18 rows),
      confusion matrix heatmap (18×18, annotated)
- [ ] `class_weight='balanced'` to handle 18-class imbalance
- [ ] **Which types are most predictable?** Which are most confused with each other?
      Is the confusion thematically sensible? (e.g., Poison/Bug confusion makes sense)
- [ ] **5-fold CV** for all models. Report macro F1 mean ± std.

---

## 03_additional_classification.ipynb — More Classification Tasks

**Skills:** Multiple binary and multiclass tasks, varying class balance, task framing

- [ ] **Binary: Predict is_fully_evolved** (~55/45 — balanced, minimal SMOTE needed)
      Features: all stats + generation + type encodings
- [ ] **Multiclass: Predict evolution trigger**
      Classes: level_up / trade / item / happiness / no_evolution (5 classes)
      Features: stats + species features
- [ ] **Binary: Predict is_dual_type** from stats only
      Question: does stat profile alone predict type complexity?
- [ ] **Binary: Predict has_priority_move** from stats + type
      Question: does stat profile predict movepool utility?
- [ ] For each task: state baseline, best model, key metric, key finding
- [ ] Cross-task comparison: which task is easiest/hardest to predict? Why?

---

## 04_interpretability.ipynb — Model Interpretability

**Skills:** SHAP, PDP, ICE, permutation importance, feature consensus

Use best legendary classifier from 01_binary_classification.ipynb throughout.

- [ ] **SHAP values:**
      - Beeswarm summary plot: feature importance + direction of effect for all features
      - Waterfall plot for 3 specific cases:
        one true legendary (e.g., Mewtwo), one false positive (e.g., Slaking), one true negative
      - Dependence plot: capture_rate vs legendary probability with interaction color
      - Force plots for 5 specific pokemon — individual prediction breakdowns
- [ ] **Partial Dependence Plots (PDP):**
      Top 3 features vs predicted legendary probability
- [ ] **Individual Conditional Expectation (ICE):**
      Show variation around PDP line — how much does the effect vary across pokemon?
- [ ] **Permutation importance:**
      Model-agnostic; compare ranking to built-in XGBoost feature_importances_
- [ ] **Feature importance consensus table:**
      Average rank across SHAP, permutation importance, and built-in importance
      for top 10 features. Which features are consistently important?
- [ ] **Key insight:** What does the model actually "think" makes a legendary?
      Write a plain-English explanation of the top 3 drivers.

---

## 05_bst_regression.ipynb — Predict Total BST

**Skills:** Linear/tree regression, regularization paths, residual diagnostics,
Cook's distance, Breusch-Pagan test, business coefficient interpretation

- [ ] **Features:** type encodings, generation, is_legendary, capture_rate, growth_rate,
      weight_kg, height_m, color, shape, egg_groups, evolution_stage, is_dual_type,
      movepool_size_total, ability_count (from silver.pokemon_abilities)
- [ ] **Models:** Linear Regression, Ridge, Lasso, ElasticNet, Random Forest,
      XGBoost, LightGBM, SVR (RBF), Polynomial (degree=2)
- [ ] **Metrics:** R², RMSE, MAE, MAPE — all models in one comparison table
- [ ] **Regularization paths:**
      - Ridge: plot coefficient values vs log(alpha) for all features
      - Lasso: plot coefficient values vs log(alpha) — which features shrink to zero first?
      - ElasticNet: compare to Lasso path
- [ ] **5-fold CV:** R² and RMSE mean ± std for all models
- [ ] **Residual diagnostics for best model:**
      - Residuals vs fitted values (homoscedasticity check)
      - QQ-plot of residuals (normality assumption)
      - Scale-location plot (sqrt|residuals| vs fitted)
      - Breusch-Pagan test for heteroscedasticity
      - Cook's distance: identify high-leverage / high-influence pokemon
- [ ] **Largest residuals:** Which 10 pokemon are hardest to predict? Explain why.
- [ ] **Business interpretation:** Lasso coefficient table with plain-English impact statements
      ("Being legendary is associated with ~X additional BST, holding all else equal")

---

## 06_stat_regression.ipynb — Predict Individual Stats

**Skills:** Multi-output regression, single stat prediction, feature-target analysis

- [ ] **Multi-output:** `MultiOutputRegressor(XGBoost)` predicts all 6 stats simultaneously
      vs 6 separate single-output models — which approach wins per stat?
- [ ] **Per-stat analysis:** Which individual stat is easiest vs hardest to predict
      from non-stat features? Why does this make sense?
- [ ] **Predict speed** from physical features only: height_m, weight_kg, type_1, generation
      (speed is the "most physical" stat — does body type predict it?)
- [ ] **Predict hp** from weight_kg + egg_group_1 + growth_rate
      (hp is often associated with bulkiness)
- [ ] For each: R², RMSE, residual plot, key feature (SHAP or permutation importance)

---

## 07_additional_regression.ipynb — More Regression Targets

**Skills:** Regression on non-stat targets, ordinal regression, feature transfer

- [ ] **Predict capture_rate** from stats + is_legendary + type + generation
      Treat as continuous regression; discuss why ordinal regression could also apply
- [ ] **Predict base_experience** from stats + evolution_stage
- [ ] **Predict movepool_size_total** from generation + type + total_stats
- [ ] **Ordinal regression (Smogon tier):** (requires Notebook 19 to run first)
      Map OU/UU/RU/NU/PU/Ubers to numeric 1–6 scale.
      Fit `mord.LogisticAT` (ordinal logistic). Compare to naive multiclass XGBoost.
- [ ] For each: best model, R²/RMSE, top 3 features, key finding

---

## 08_feature_selection.ipynb — Feature Selection Methods

**Skills:** VIF, RFE, Lasso path, mutual information, minimal model analysis

- [ ] **VIF (Variance Inflation Factor):** detect multicollinearity among stat predictors.
      Drop features with VIF > 10; retrain BST regressor. How much does it matter?
- [ ] **RFE with Random Forest:** CV score vs number of features curve.
      Find "knee" — smallest feature set within 1% of full-model R².
- [ ] **Lasso path:** features surviving at optimal alpha (from 05_bst_regression)
- [ ] **Mutual information:** non-linear relevance scores for all features vs BST target
- [ ] **Consensus minimal model:**
      Features agreed on by VIF (keep), RFE (selected), Lasso (non-zero), MI (top quartile).
      Train on consensus features; report R² tradeoff vs full model.
- [ ] **Plain-English summary:** "A business analyst could predict BST from just these
      5 features with Y% of the full model's accuracy."

---

## 09_stat_clustering.ipynb — Stat-Based Clustering

**Skills:** K-Means, Agglomerative, DBSCAN, GMM, cluster validation indices

- [ ] Standardize all 6 stats with `StandardScaler`
- [ ] **K-Means:**
      - Inertia elbow method (k=2 to 15) — mark elbow point
      - Silhouette analysis: average score + per-sample silhouette plot at optimal k
      - Calinski-Harabasz index and Davies-Bouldin index across k
      - Final model at optimal k; add `cluster_label` column to DataFrame
- [ ] **Agglomerative Hierarchical:**
      - Ward, complete, average, single — show all 4 dendrograms
      - Cophenetic correlation coefficient per linkage (measure quality)
      - Cut at optimal k; compare assignments to K-Means via ARI score
- [ ] **DBSCAN:**
      - k-distance graph (k=4) to find eps knee point
      - Identify core / border / noise samples
      - Try 3 eps values; show sensitivity of noise count to eps
      - Noise points = truly anomalous pokemon — name each one
- [ ] **GMM:**
      - Select k by BIC criterion (plot BIC vs k)
      - Show soft assignments: max responsibility < 0.8 = ambiguous pokemon
      - Compare hard K-Means vs soft GMM for 20 most ambiguous pokemon

---

## 10_cluster_profiling.ipynb — Cluster Profiling & Segment Briefs

**Skills:** Cluster characterization, business labeling, cross-tabulation, radar charts,
segment strategy writing

- [ ] Compute mean + std of all features per cluster (from 09_stat_clustering)
- [ ] Assign archetype labels based on dominant stat patterns:
      Sweeper (high Speed+Atk), Physical Wall (high Def+HP), Special Attacker (high SpAtk),
      Mixed Attacker, Bulky Supporter, All-Rounder, Glass Cannon, Pure Utility
- [ ] Cross-tabulations: each cluster vs type_1, generation, is_legendary, is_fully_evolved
- [ ] Radar charts: average stat profile per cluster (6-axis polygon, one per cluster)
- [ ] **Segment briefs:** 1 paragraph per cluster:
      who they are, what they do, key member examples, real-world business analogy
- [ ] **Competitive mapping:** which clusters map to which Smogon tiers? (after Notebook 19)
- [ ] Which cluster is most diverse (highest within-cluster stat variance)?
- [ ] Which cluster is most "pure" (lowest within-cluster variance)?

---

## 11_dimensionality_reduction.ipynb — PCA, t-SNE & UMAP

**Skills:** PCA with biplots, t-SNE sensitivity analysis, UMAP 2D/3D, comparison framework

- [ ] **PCA on 6 stats:**
      - Scree plot: variance explained per component
      - Cumulative variance: how many PCs for 80%, 90%, 95%?
      - Biplot: PC1 vs PC2 with loading vectors labeled + annotated
      - Interpretation: PC1 = overall power? PC2 = offense vs defense tradeoff?
      - Project all 1025 pokemon into PC1/PC2 — color by type (one plot) and by cluster (one plot)
- [ ] **t-SNE:**
      - Run at perplexity 15, 30, 50 — plot all 3 side by side; discuss sensitivity
      - 4 color schemes: type_1, cluster, is_legendary, generation
      - Annotate specific pokemon: Arceus, Magikarp, Shuckle, Mewtwo, Blissey, Chansey
- [ ] **UMAP:**
      - 2D static plot colored by cluster
      - 3D Plotly interactive plot colored by type_1
      - Compare to t-SNE: does UMAP preserve more global structure?
- [ ] **Comparison summary:** When would you choose PCA vs t-SNE vs UMAP?
      Which reveals most meaningful structure in this dataset?

---

## 12_full_feature_clustering.ipynb — Full Feature Space Clustering

**Skills:** High-dimensional clustering, cluster comparison, stability analysis, ARI

- [ ] Build full feature matrix: stats + type OHE + generation + movepool features +
      evolution stage + is_legendary + type matchup features
- [ ] StandardScaler on numeric; OHE on categorical
- [ ] K-Means at same optimal k as stat-only clustering
- [ ] **Compare to stat-only clusters** using Adjusted Rand Index (ARI) — do they agree?
- [ ] Which pokemon migrate to different clusters when non-stat features included?
      List top 20 movers with explanation.
- [ ] **Cluster stability analysis:**
      Run K-Means 20× with different random seeds.
      Compute pairwise ARI between all 190 run-pairs.
      Report mean ± std ARI — are these clusters stable or seed-dependent?
- [ ] t-SNE of full feature space vs stat-only: which produces cleaner cluster separation?

---

## 13_text_preprocessing.ipynb — NLP Data & Preprocessing

**Skills:** spaCy pipeline, custom stopwords, lemmatization, vocabulary statistics,
corpus construction

- [ ] Load 3 text corpora from Silver Delta tables:
      - Pokedex flavor text (~1025 descriptions from silver.pokemon_species)
      - Ability effect descriptions (~298 from silver.abilities)
      - Move effect descriptions (~920 from silver.moves)
- [ ] **spaCy preprocessing pipeline (for each corpus):**
      - Lowercase, strip punctuation and numeric tokens
      - Custom domain stoplist: standard English + {"pokémon","trainer","battle","move",
        "wild","uses","attack","user","target","holder","foe","ally","turn","pp","may"}
      - Lemmatize with `en_core_web_sm`
      - Remove tokens shorter than 3 characters
- [ ] **Vocabulary statistics per corpus:**
      - Vocab size (unique lemmas), total tokens, avg/median token count per document
      - Type-token ratio (lexical richness) overall + per type + per generation
      - Hapax legomena (lemmas appearing exactly once)
      - Top 5 most frequent lemmas per type (before and after stopword removal — compare)
- [ ] Save preprocessed corpora to DBFS as Parquet for reuse in downstream notebooks

---

## 14_tfidf_analysis.ipynb — TF-IDF & Frequency Analysis

**Skills:** TF-IDF vectorization, word clouds, bigrams/trigrams, co-occurrence networks,
semantic field analysis

- [ ] Word frequency bar charts: top 30 lemmas overall + top 20 per type (18 subplots)
- [ ] Word clouds: one per primary type using TYPE_COLORS palette — save to outputs/figures/
- [ ] **TF-IDF per type** (treat all type descriptions as one document per type):
      most distinctive lemmas per type (what words identify Fire vs Water vs Ghost?)
      Do Fire descriptions mention "flame" more than expected by chance?
- [ ] Bigram and trigram frequency: most common 2/3-word phrases overall and per type
- [ ] **Co-occurrence matrix** (top 50 lemmas): which lemmas most often co-occur?
      Visualize as heatmap + network graph (networkx, edge weight = co-occurrence count)
- [ ] **Semantic field analysis:**
      Group lemmas into themes: violence, nature, darkness, speed, loyalty, ancient, ocean.
      Count theme frequency per type — which types concentrate in which themes?

---

## 15_sentiment.ipynb — Sentiment & Tone Analysis

**Skills:** VADER sentiment, TextBlob, sentiment comparisons, trend analysis, t-tests on sentiment

- [ ] **VADER sentiment** (compound, pos, neg, neu) for each pokemon description
- [ ] Distribution plots: compound score for legendary vs regular, each type, each generation
- [ ] **T-test:** Is Ghost type compound sentiment significantly more negative than Fairy type?
- [ ] **T-test:** Are mythical pokemon descriptions more extreme (higher |compound|) than legendary?
- [ ] **TextBlob subjectivity:** are earlier or later generation descriptions more subjective?
      OLS: subjectivity ~ generation. Slope significance.
- [ ] Sentiment trend over generations: OLS on mean compound score ~ generation
- [ ] Annotation: 5 most positive and 5 most negative descriptions — show full text + pokemon name
- [ ] Which type has the most emotionally consistent descriptions (lowest sentiment variance)?

---

## 16_text_classification.ipynb — Text-Based Prediction

**Skills:** TF-IDF + ML classifiers, sentence transformers, embedding visualization,
NLP feature enrichment experiment

- [ ] **TF-IDF + Logistic Regression:** predict type_1 from flavor text alone.
      Macro F1 score. Per-class precision/recall. Which types does text most/least reliably predict?
- [ ] **TF-IDF + XGBoost:** predict is_legendary from flavor text. ROC-AUC score.
      Compare to stat-based legendary classifier from 01_binary_classification.
- [ ] **Sentence Transformers** (`all-MiniLM-L6-v2`):
      - Embed all 1025 Pokedex descriptions into 384-dim vectors
      - t-SNE of embeddings colored by type_1 — do semantic clusters emerge?
      - KNN classifier on embeddings: predict type_1. Compare macro F1 to TF-IDF baseline.
- [ ] **NLP enrichment experiment:**
      Add top 50 TF-IDF SVD components to legendary classifier feature set.
      Compare AUC before/after NLP features. Does language improve the model?
- [ ] **Ability NLP:** TF-IDF on ability descriptions.
      What words distinguish passive abilities from active abilities?
- [ ] **Move NLP:** Sentence-embed move effect descriptions.
      K-Means cluster on embeddings. Does text clustering align with damage_class (physical/special/status)?
      Which moves have most similar effect descriptions? (cosine similarity top-10 pairs)

---

## 17_topic_modeling.ipynb — LDA Topic Modeling

**Skills:** LDA, coherence scores, pyLDAvis, topic-type cross-tabulation, generational tone analysis

- [ ] Fit LDA on Pokedex flavor text corpus
- [ ] Select k by coherence score (c_v metric, sweep k=6 to 12). Plot coherence vs k.
- [ ] Fit final LDA at optimal k. Extract top 15 words per topic.
- [ ] Visualize with pyLDAvis — save as `dbfs:/FileStore/pokedata/outputs/lda_topics.html`
- [ ] Name each topic from top words:
      e.g., "ancient/legendary power", "ocean/sea", "darkness/evil",
      "elemental fire", "speed/agility", "friendship/bond", "battle aggression"
- [ ] Assign dominant topic (argmax of doc-topic distribution) to each pokemon
- [ ] Cross-tabulation: dominant topic vs type_1 (which types concentrate in which topics?)
- [ ] Cross-tabulation: dominant topic vs generation (has tone shifted over generations?)
- [ ] Key question: do earlier generations concentrate more "dark" topics?
- [ ] Ability descriptions: fit separate LDA (k=5). Do ability topics correspond to
      battle mechanics categories (stat changes, status, immunity, damage boost, weather)?

---

## 18_unified_evaluation.ipynb — Unified Model Comparison

**Skills:** Cross-model comparison, McNemar's test, Wilcoxon signed-rank, learning curves,
validation curves

- [ ] Re-run ALL classifiers from 01–03 with identical 5-fold stratified CV on feature set v3
- [ ] Re-run ALL regressors from 05–07 with identical 5-fold CV
- [ ] **Master results table:** model × task × metric (precision, recall, F1, AUC, R², RMSE)
      — one row per model, sortable by any metric
- [ ] **McNemar's test:** Are differences between top 2 legendary classifiers statistically significant?
      (requires matched test set predictions from same splits)
- [ ] **Wilcoxon signed-rank test:** Are per-fold CV score differences significant across model pairs?
- [ ] **Learning curves:** performance vs training set size for top 3 models.
      Diagnose: high bias (both curves low) vs high variance (large train-val gap)?
- [ ] **Validation curves:** CV score vs key hyperparameter for best classifier and best regressor.
      Show underfitting and overfitting regions explicitly.
- [ ] Summary: which model wins for each task, by how much, and is the difference significant?

---

## 19_hyperparameter_tuning.ipynb — Hyperparameter Optimization

**Skills:** RandomizedSearchCV, Optuna TPE sampler, early stopping, convergence plots,
hyperparameter importance

- [ ] **RandomizedSearchCV:** Random Forest + XGBoost on legendary classification.
      100 configurations, 5-fold CV. Report best params + improvement over default XGBoost.
- [ ] **Optuna (TPE sampler) for XGBoost legendary classifier:**
      - Define objective: 5-fold CV ROC-AUC
      - Search space: n_estimators, max_depth, learning_rate, subsample,
        colsample_bytree, min_child_weight, reg_alpha, reg_lambda
      - 200 trials with MedianPruner (prune unpromising trials early)
      - Convergence plot: best objective value vs trial number
      - Parallel coordinate plot: hyperparameter combinations explored across trials
      - `optuna.visualization.plot_param_importances`: which hyperparams matter most?
      - Final tuned vs default model: F1, AUC, Brier score — how much did tuning help?
- [ ] **XGBoost early stopping:**
      `early_stopping_rounds=50` on val set.
      Plot train vs val metric per boosting round.
      Show overfitting curve; identify optimal n_estimators from early stopping.
- [ ] Takeaway: what was the biggest gain — algorithm choice, imbalance handling, or tuning?

---

## 20_ensembles.ipynb — Ensemble Methods

**Skills:** Soft voting, stacking, calibrated ensembles, ablation study

- [ ] **Soft Voting Classifier:** Logistic Regression + Random Forest + XGBoost (tuned).
      Does ensemble beat best single model? Report AUC difference + McNemar's test.
- [ ] **Stacking:**
      Base models: LR + RF + XGB → Logistic Regression meta-learner.
      Implement with sklearn `StackingClassifier`.
      Out-of-fold predictions used as meta-features (no leakage).
      Compare to voting ensemble: which approach wins?
- [ ] **Calibrated ensemble:**
      Calibrate each base model (isotonic regression) before voting.
      Compare Brier scores before/after calibration.
- [ ] **Ablation study:**
      Remove one model at a time from the best ensemble.
      Measure AUC drop per removal — which base model contributes most?
      Quantify marginal contribution of each component.
- [ ] **Regression ensemble:** Apply same voting + stacking approach to BST regressor.
      Does ensemble help for regression too?

---

## 21_feature_selection_rigor.ipynb — Feature Selection Deep Dive

**Skills:** RFE, Boruta, permutation importance stability, minimal model analysis,
feature selection consensus

- [ ] **RFE with Random Forest:** CV score vs number of features (1 to all).
      Plot the curve; find knee point = minimal useful feature count.
- [ ] **Boruta algorithm:**
      Run Boruta on legendary classifier features.
      Classify features as: definitely important / tentative / rejected.
      Compare to Lasso path (from 05_bst_regression) and SHAP rankings (from 04_interpretability) —
      how much do the 3 methods agree?
- [ ] **Permutation importance stability:**
      Run permutation importance 10× with different random seeds.
      Report mean ± std per feature.
      Which features have stable importance vs noisy importance?
- [ ] **Feature set ablation:**
      Compare feature set v1 (stats only) vs v2 (+ categorical) vs v3 (+ movepool + matchups)
      on all classification + regression tasks. Quantify gain per feature set addition.
- [ ] **Minimal model:**
      Top-5 consensus features only (agreed on by RFE + Boruta + SHAP).
      Report: AUC tradeoff vs full model, inference time speedup, interpretability gain.
      Question: "Could a business analyst deploy this as a simple rule-based system?"

---

## 22_experiment_tracking.ipynb — Experiment Tracking & Reproducibility

**Skills:** Lightweight experiment logging, JSONL format, run reproducibility,
MLflow conceptual comparison

- [ ] Import `src/tracking.py` — `ExperimentTracker` class
- [ ] Log every model run from 01–21 that wasn't already tracked:
      model_name, task, feature_set_version, hyperparams dict, all metrics, timestamp, run_id
- [ ] Append to `dbfs:/FileStore/pokedata/outputs/experiments.jsonl`
- [ ] `summarize_experiments()`: load JSONL → DataFrame sortable by any metric, filterable by task
- [ ] **Reproducibility test:**
      Pick the best legendary classifier run. Load its logged hyperparams.
      Retrain from scratch with those exact params + same random_state.
      Confirm AUC matches logged value exactly.
- [ ] **Best run leaderboard:** Top 3 models per task with full metric breakdown
- [ ] **MLflow comparison:**
      Discuss how Databricks MLflow replaces this at production scale.
      What does MLflow add? (artifact storage, model registry, UI, compare runs visually,
      serve models as REST endpoints, A/B experiment tracking)
- [ ] Show what this experiment log would look like imported into MLflow

---

## 23_model_cards.ipynb — Model Cards & Production Readiness

**Skills:** Model card writing, fairness analysis, failure mode analysis,
production monitoring design, data drift concepts

### Model Card: Legendary Classifier (best model from 19/20)
- [ ] **Intended use:** Identify potentially legendary-tier pokemon from stats and species features
- [ ] **Out-of-scope uses:** Do not use to predict legendary status of fan-made pokemon;
      do not use as ground truth — game design intent supersedes model output
- [ ] **Training data:** 1025 pokemon, Gen 1–9, PokeAPI as of [fetch date], ~5% positive rate
- [ ] **Known biases:** over-representation of Water/Normal types; small sample (1025 rows);
      no Gen 10 pokemon; alternate forms may inflate features for some species
- [ ] **Performance metrics:** precision, recall, F1, AUC with 95% bootstrap confidence intervals
- [ ] **Fairness analysis:** does performance differ by generation? by primary type?
      Any type systematically misclassified?
- [ ] **Failure modes:** 5 specific misclassified pokemon with explanation:
      e.g., Slaking (legendary-tier stats but not legendary), Cosmog (legendary but weak stats)
- [ ] **Monitoring plan:** what constitutes "data drift" when Gen 10 releases?
      Which features would shift? How would you detect it?

### Model Card: BST Regressor (best model from 05)
- [ ] Same structure, adapted for regression:
      RMSE and R² with bootstrap CIs instead of classification metrics;
      residual analysis instead of confusion matrix;
      discuss which types of pokemon the model over/under-predicts

### Production Readiness Checklist
- [ ] Model serialized and saveable to DBFS (`joblib.dump`)
- [ ] Inference function: takes raw pokemon dict → returns prediction + confidence
- [ ] Input validation: raise clear errors on malformed inputs
- [ ] Unit test for inference function with known pokemon as test cases
- [ ] Discussion: how would you serve this model in production on Databricks?
      (MLflow model serving, REST API endpoint, batch inference job)