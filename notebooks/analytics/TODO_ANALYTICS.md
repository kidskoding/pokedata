# TODO — Data Analytics (notebooks/analytics/)

> **Run `notebooks/setup.ipynb` once per cluster** (shared by engineering, analytics, science)
> All notebooks run on **Databricks**
> All data reads from Gold or Silver Delta tables — never raw files
> Start each notebook with:
> ```python
> import sys
> sys.path.insert(0, '/dbfs/FileStore/pokedata/src')
> from constants import TYPE_COLORS, GOLD_PATH
> gold = spark.read.format("delta").load(GOLD_PATH + "pokemon_full")
> ```

---

## Core — Intern / Co-op / New Grad

| # | Notebook | Skills |
|---|----------|--------|
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

---

## Beyond entry-level (mid / senior)

| # | Notebook | Focus |
|---|----------|-------|
| 12 | cohort_analysis | Cohort definition, funnel, lifecycle |
| 13 | business_analogies | Executive communication, storytelling |
| 14 | plotly_dashboard | Interactive dashboards, HTML export |
| 15 | executive_report | Data storytelling, methodology appendix |
| 16 | power_creep | OLS trends, stratified analysis |
| 17 | type_diversity | Shannon entropy, before/after analysis |
| 18 | distribution_shifts | Hypothesis testing (15 tests), corrections |
| 19 | forecasting | ARIMA, Holt-Winters, prediction intervals |
| 20 | external_integration | Multi-source, fuzzy matching, enrichment |

---

## 01_group_by.ipynb — GROUP BY Patterns

**Skills:** Spark SQL aggregations, ROLLUP, CUBE, GROUPING SETS, HAVING, GROUPING()

- [ ] Basic aggregations: mean/median/stddev per stat by type_1, generation, is_legendary
- [ ] `GROUP BY type_1 HAVING COUNT(*) > 10` — exclude rare types from analysis
- [ ] Multi-level GROUP BY: BST summary by (generation, legendary_status, is_dual_type)
- [ ] `ROLLUP(generation, type_1)`: subtotals at each level + grand total in one query
- [ ] `CUBE(generation, type_1, is_legendary)`: full combinatorial aggregation
- [ ] `GROUPING SETS`: custom grouping — (type_1), (generation, is_legendary), () combined
- [ ] `GROUPING()` function: identify subtotal rows vs detail rows in ROLLUP output
- [ ] Interpret every result in plain English with a business analogy

---

## 02_window_functions.ipynb — Window Functions

**Skills:** ROW_NUMBER, RANK, DENSE_RANK, NTILE, LAG, LEAD, FIRST_VALUE, LAST_VALUE,
running totals, rolling averages, PERCENT_RANK, CUME_DIST, PERCENTILE_CONT

- [ ] `ROW_NUMBER() OVER (PARTITION BY type_1 ORDER BY total_stats DESC)` — rank within type
- [ ] `RANK()` vs `DENSE_RANK()` — demonstrate difference with tied total_stats values
- [ ] `NTILE(4) OVER (PARTITION BY generation ORDER BY total_stats)` — BST quartile within gen
- [ ] `LAG(total_stats,1) / LEAD()` — BST delta from base form to evolution over chain
- [ ] `FIRST_VALUE() / LAST_VALUE()` — base form vs final form BST per evolution chain
- [ ] `SUM() OVER (PARTITION BY generation ORDER BY national_dex_number ROWS UNBOUNDED PRECEDING)` —
      cumulative legendary count as you move through the dex
- [ ] `AVG() OVER (PARTITION BY type_1 ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING)` —
      rolling 5-pokemon moving average of BST within a type
- [ ] `PERCENT_RANK() / CUME_DIST()` — percentile position of each pokemon by BST
- [ ] `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_stats)` — exact median per type
- [ ] For each function: show syntax, explain semantics, interpret output

---

## 03_advanced_queries.ipynb — CTEs, Joins & Pivots

**Skills:** Multi-level CTEs, recursive CTEs, self-joins, anti-joins, correlated subqueries,
EXISTS/NOT EXISTS, PIVOT, UNPIVOT, LATERAL VIEW EXPLODE

- [ ] **5-level CTE chain:** 1. filter fully evolved → 2. per-type avg BST →
      3. label above/below average → 4. count by label per type → 5. pivot to wide report
- [ ] **Recursive CTE:** Walk evolution chain tree in pure SQL — find longest chain
- [ ] **Self-join:** Find all pokemon pairs sharing exact same dual-type combo.
      Count pairs per combo. Which combo has the most members?
- [ ] **Anti-join:** Gen 1 pokemon NOT in any competitive tier (after Notebook 20)
- [ ] **Correlated subquery:** For each pokemon, find the strongest same-type pokemon
      in the same generation
- [ ] **EXISTS / NOT EXISTS:** Types with zero legendary representatives
- [ ] **PIVOT:** 9×18 generation × type count matrix in one SQL statement
- [ ] **UNPIVOT:** Convert 6 stat columns → `(stat_name, stat_value)` long format
- [ ] **LATERAL VIEW EXPLODE:** Explode move arrays, aggregate move count per type per pokemon
- [ ] For every query: explain what it does, what the output means, why the pattern matters

---

## 04_query_optimization.ipynb — Explain Plans & Benchmarks

**Skills:** EXPLAIN EXTENDED, predicate pushdown, partition pruning, broadcast joins,
AQE, DataFrame caching, query benchmarking

- [ ] `EXPLAIN EXTENDED` on 3 different query types — read and interpret each plan section
- [ ] Predicate pushdown: show filter pushed into Delta scan, count files skipped
- [ ] Partition pruning: `WHERE generation = 1` on partitioned Gold — show file skip count
- [ ] Broadcast join vs sort-merge join: force with `/*+ BROADCAST(t) */` hint. Compare plans.
- [ ] AQE (Adaptive Query Execution): show skew join optimization, shuffle partition coalescing
- [ ] Benchmark: same query on Bronze JSON vs Gold Delta ZORDERed.
      Use `%timeit` or Spark UI to measure and compare.
- [ ] `df.cache()` vs `CACHE TABLE` — query time before/after with explicit timing
- [ ] For each optimization: state the principle, show the evidence, quantify the improvement

---

## 05_business_sql.ipynb — 10 Business Questions

**Skills:** Translating business questions to SQL, complex multi-step queries, result interpretation

Answer each as a standalone, well-commented SQL query with plain-English interpretation:

- [ ] Which type has the highest statistical floor (max of min BST among all its members)?
- [ ] Which egg group produces the strongest pokemon on average?
- [ ] Which pokemon is the true "all-rounder" — minimum sum of deviations from median on all 6 stats?
- [ ] Which generation introduced the most type diversity (Shannon entropy of type distribution)?
- [ ] What is the rarest dual-type combination by pokemon count?
- [ ] Which ability appears on the highest percentage of legendary pokemon?
- [ ] Which location area spans the widest encounter level range (max_level − min_level)?
- [ ] Which pokemon is available in the most game versions across all time?
- [ ] Which berry has the most balanced flavor profile (lowest variance across 5 flavor potencies)?
- [ ] Which move has the best power-to-PP ratio among physical moves with > 10 learners?

---

## 06_profiling.ipynb — Dataset Profiling

**Skills:** Pandas profiling, missingno, cardinality analysis, schema validation, row count auditing

- [ ] Schema summary: column names, dtypes, nullable counts, unique counts for every column
      in `gold.pokemon_full` — built as a summary DataFrame and displayed
- [ ] Row count waterfall: Bronze → Silver → Gold — document every transformation that
      changes row count and explain why
- [ ] Missing value heatmap (missingno) for `gold.pokemon_full`
- [ ] Cardinality report: every categorical column → unique count + top 10 values + bar chart
- [ ] Duplicate detection: (pokemon_id, generation) combos, name collisions, form duplicates
- [ ] Null rate per column: flag any unexpected nulls in columns that should be complete

---

## 07_univariate.ipynb — Univariate Distributions

**Skills:** Histograms, KDE, QQ-plots, box plots, value counts, distributional statistics

- [ ] Histogram + KDE for every numeric column: all 6 stats, total_stats, height_m,
      weight_kg, capture_rate, base_experience, base_happiness, movepool_size_total, chain_length
- [ ] For each: state skewness, kurtosis, min, max, mean, median, IQR in a summary table
- [ ] QQ-plots for each stat: assess normality assumption visually
- [ ] Box plots for each stat grouped by: type_1, generation, is_legendary, speed_tier, evolution_stage
- [ ] Value counts + bar charts: type_1, type_2, egg_group_1, color, shape,
      habitat, growth_rate, evolution_trigger, most_common_encounter_method
- [ ] Identify and name the distributional shape of each numeric column

---

## 08_bivariate.ipynb — Bivariate & Multivariate Analysis

**Skills:** Correlation matrices, scatter plots, violin plots, pair plots, type co-occurrence,
radar charts, heatmaps

- [ ] Full Pearson correlation heatmap: all numeric pairs, annotated, upper triangle masked
- [ ] Spearman rank correlation heatmap: compare to Pearson — which pairs differ meaningfully?
- [ ] Scatter matrix of all 6 stats, colored by is_legendary
- [ ] Scatter: total_stats vs capture_rate — label top 10 named outliers
- [ ] Scatter: height_m vs weight_kg, colored by type_1 — identify physically extreme pokemon
- [ ] Violin plots: each stat by type_1, panels sorted by type median BST (18 panels)
- [ ] Heatmap: type co-occurrence matrix (how often do each pair of types appear together?)
- [ ] Pair plot: stats for legendary vs non-legendary separately — compare structures
- [ ] Radar chart: average stat profile per type (18-panel small multiples)
- [ ] Stat signature heatmap: mean stat value per type × stat (18×6 annotated heatmap)

---

## 09_outlier_detection.ipynb — Outlier Detection & Annotation

**Skills:** IQR method, Z-score, Mahalanobis distance, outlier interpretation

- [ ] IQR method per stat: flag outliers, identify and name each flagged pokemon
- [ ] Z-score method: flag |z| > 3 across all stats — which pokemon appear repeatedly?
- [ ] Multivariate outliers: Mahalanobis distance on 6-stat feature space
      — rank all 1025 pokemon by anomaly score; name the top 20
- [ ] Manual annotation: explain each major outlier (Shuckle, Blissey, Deoxys,
      Slaking, Chansey, Magikarp, Wishiwashi) in terms of game mechanics
- [ ] For each outlier: which specific stat(s) drive the anomaly?
- [ ] IQR vs Z-score vs Mahalanobis comparison: do they agree on the same pokemon?

---

## 10_hypothesis_inventory.ipynb — Hypothesis Generation & Documentation

**Skills:** EDA-driven hypothesis formulation, statistical test selection, pre-registration

Document 15 hypotheses to be formally tested in 17_distribution_shifts.ipynb.
For each hypothesis: state H0, H1, planned test, expected direction, rationale.

- [ ] H1: Legendary pokemon have significantly higher BST than non-legendary
- [ ] H2: Dual-type pokemon have higher BST than mono-type on average
- [ ] H3: capture_rate is negatively correlated with total_stats
- [ ] H4: Later generations have higher average BST (power creep)
- [ ] H5: Dragon type has highest average BST of all 18 types
- [ ] H6: Bug type has lowest average BST of all 18 types
- [ ] H7: Pokemon with larger movepools have higher BST
- [ ] H8: Speed and Defense are negatively correlated
- [ ] H9: Normal type is closest to the all-pokemon average across all stats
- [ ] H10: Gen 1 and Gen 9 stat distributions are significantly different
- [ ] H11: Pokemon that evolve via happiness have higher base_happiness than average
- [ ] H12: Water is the most common primary type
- [ ] H13: Pokemon with hidden abilities have higher BST than those without
- [ ] H14: Egg group "Undiscovered" is exclusive to legendaries/mythicals/babies
- [ ] H15: base_experience correlates more strongly with total_stats than any single stat
- [ ] For each: assign planned test (t-test, ANOVA, chi-squared, Pearson, Spearman, KS)

---

## 11_kpi_framework.ipynb — KPI Definition & Computation

**Skills:** KPI design, percentile computation, Shannon entropy, business metric framing

- [ ] **Power KPIs:** BST_p25, BST_p50, BST_p75, BST_p90, BST_p99 overall + per type + per gen
- [ ] **Rarity KPIs:** legendary_rate, mythical_rate, baby_rate, pseudo_legendary_rate per gen
- [ ] **Catchability KPI:** % pokemon with capture_rate ≤ 45, ≤ 10 — ultra-rare tier
- [ ] **Coverage KPI:** avg coverage_type_count per pokemon per type
- [ ] **Availability KPI:** avg_versions_available, % exclusive to one version, % in all versions
- [ ] **Diversity KPI:** Shannon entropy of type distribution per generation
- [ ] **Completeness KPI:** % pokemon with hidden ability; % with full evolution line; 
      % with Smogon tier (after Notebook 20)
- [ ] Build a KPI dashboard DataFrame: all KPIs in one table, filterable by generation/type
- [ ] Identify which generation scores best/worst on each KPI — interpret why

---

## 12_cohort_analysis.ipynb — Cohort Analysis

**Skills:** Cohort definition, comparative profiling, funnel analysis, lifecycle framing

- [ ] **Generation cohorts:** Each gen's BST distribution vs all-time benchmark.
      Is each new generation stronger than the all-time median at its release?
- [ ] **Evolution stage cohorts:** Avg BST gain per stage (1→2, 2→3) across all chains.
      Do later generations show larger or smaller evolution gains?
- [ ] **Type cohorts:** BST trend per type across generations — has each type gotten stronger?
      Which type has grown most? Which has stayed flattest?
- [ ] **Capture difficulty cohorts:** Easy (>150) / Medium (45–150) / Hard (<45) / Ultra (<10).
      Profile each cohort: avg stats, type distribution, legendary rate, generation distribution
- [ ] **Movepool richness cohorts:** Low/Medium/High quartiles.
      Do richer movepools correlate with higher competitive tiers? (after Notebook 20)
- [ ] For each cohort analysis: visualize with box plots or violin plots; state key finding

---

## 13_business_analogies.ipynb — Business Framing & Storytelling

**Skills:** Business analogy construction, executive communication, insight framing

- [ ] **Legendaries = High-Value Customers (HVC):**
      5% of population, disproportionate stats. Build HVC funnel: Regular → Pseudo → Mythical → Legendary.
      Map to: HVC identification, segmentation, retention strategy.
- [ ] **Capture rate = Churn risk:**
      Low capture rate = high churn. Build acquisition difficulty funnel with conversion rates.
- [ ] **Evolution = Customer Lifecycle:**
      Stage 1 = acquisition, Stage 2 = activation, Stage 3 = maturity.
      Plot BST growth as "customer value growth over lifecycle."
- [ ] **Stat clusters = Market segments:**
      Each cluster = a distinct customer segment with different needs.
      Write a 3-sentence segment brief per cluster (reference Notebook 09 in science/).
- [ ] **Power creep = Market inflation:**
      BST inflation per gen = GameFreak releasing premium-tier products each cycle.
      Map to product strategy, feature bloat, competitive pressure.
- [ ] **Type matchups = Competitive landscape:**
      18×18 matrix = market positioning map. Which types dominate? Which are underserved?
- [ ] **Movepool = Product feature set:**
      Coverage moves = product versatility. Wide movers = platform products. Narrow = niche.
- [ ] For each analogy: one visualization, one paragraph explanation, one actionable implication

---

## 14_plotly_dashboard.ipynb — Interactive Plotly Dashboard

**Skills:** Plotly Express, Plotly Graph Objects, interactive charts, HTML export

Save final dashboard as `dbfs:/FileStore/pokedata/outputs/dashboard.html`

- [ ] Scatter: BST vs capture_rate, color=is_legendary, size=generation,
      hover shows name + sprite_url + type_1 + type_2
- [ ] Radar charts: average stat profile per cluster archetype (6-axis polygon)
- [ ] Animated bar: type distribution per generation, Gen 1→9 with play/pause button
- [ ] Treemap: all pokemon by region → type → name, sized by total_stats
- [ ] Sunburst: generation → legendary_status → type — hierarchical composition
- [ ] 18×18 heatmap: type matchup matrix, hover shows attacker/defender/multiplier
- [ ] Multi-KPI line chart: KPI trends over generations with toggle per KPI
- [ ] Box plot: stat distributions by type, sorted by median, interactive type filter
- [ ] Each chart: proper title, axis labels, color scale, legend

---

## 15_executive_report.ipynb — Executive Summary & Report

**Skills:** Data storytelling, plain-English writing, structured reporting, methodology appendix

- [ ] 5-finding executive summary: each finding =
      observation → interpretation → business implication → recommended action
- [ ] All findings written for a non-technical executive audience — zero jargon
- [ ] Finding 1: Power creep — BST has inflated X% from Gen 1 to Gen 9
- [ ] Finding 2: Legendary concentration — 5% of pokemon account for Y% of top-tier slots
- [ ] Finding 3: Type imbalance — Water/Normal dominate; some types remain niche
- [ ] Finding 4: Capture difficulty distribution — Z% of pokemon are ultra-rare catches
- [ ] Finding 5: Movepool diversity — later generations get richer movepools on average
- [ ] Methodology appendix: data source, pipeline summary, freshness date, known limitations
- [ ] Competition submission format: abstract + methods + results + figures + appendix

---

## 16_power_creep.ipynb — Power Creep Analysis

**Skills:** OLS trend regression, confidence intervals, quadratic vs linear model comparison,
AIC, log transformation, stratified trend lines

- [ ] Mean + median + stddev of total_stats per generation with 95% CI bands
- [ ] Per-stat trend lines (6 subplots): which stat inflated most?
- [ ] Stratified: legendary, pseudo-legendary (BST ≥ 600), starter, regular — separate lines
- [ ] OLS: `total_stats ~ generation`. Report slope, p-value, R², 95% CI on slope.
- [ ] Quadratic term: `total_stats ~ generation + generation²` — is creep accelerating?
      Compare AIC of linear vs quadratic.
- [ ] Log-transform BST: is growth multiplicative or additive?
- [ ] Game mechanics trends: avg movepool size, ability count, capture_rate per generation
- [ ] Legendary introduction rate per generation

---

## 17_type_diversity.ipynb — Type Diversity Over Generations

**Skills:** Shannon entropy, before/after analysis, diversity indices, type balance

- [ ] Shannon entropy of type_1 distribution per generation — trend over time
- [ ] New unique dual-type combinations introduced per generation
- [ ] Steel (Gen 2) introduction: how did defensive meta shift? Before/after comparison.
- [ ] Fairy (Gen 6) introduction: how did Dragon/Dark/Fighting defensive dynamics change?
- [ ] Dual-type rate over generations: is GameFreak using more dual types over time?
- [ ] Average capture_rate per generation
- [ ] Average base_happiness per generation
- [ ] For each finding: statistical test + interpretation

---

## 18_distribution_shifts.ipynb — Hypothesis Testing & Statistical Inference

**Skills:** t-tests, ANOVA, chi-squared, Mann-Whitney U, KS test, effect sizes,
Bonferroni correction, Benjamini-Hochberg FDR

Test all 15 hypotheses documented in 09_hypothesis_inventory.ipynb:

- [ ] H1: t-test legendary vs non-legendary BST (per stat + total). Cohen's d effect size.
- [ ] H2: t-test dual-type vs mono-type BST. Cohen's d.
- [ ] H3: Pearson + Spearman correlation: capture_rate vs total_stats. P-value + r.
- [ ] H4: OLS regression: total_stats ~ generation. Slope significance.
- [ ] H5: ANOVA: mean BST differs across all 18 types? Eta-squared effect size.
- [ ] H6: Same ANOVA — post-hoc Tukey HSD: which type pairs differ significantly?
- [ ] H7: Pearson: movepool_size vs total_stats.
- [ ] H8: Pearson: speed vs defense correlation.
- [ ] H9: Which type's mean stat vector has smallest Euclidean distance to all-pokemon mean?
- [ ] H10: KS test: Gen 1 vs Gen 9 BST distributions. Are they significantly different?
- [ ] H11: t-test: happiness-evolution pokemon vs others on base_happiness.
- [ ] H12: Chi-squared / proportion test: is Water significantly over-represented?
- [ ] H13: t-test: pokemon with hidden abilities vs without on BST.
- [ ] H14: Chi-squared: Undiscovered egg group vs legendary/mythical/baby status.
- [ ] H15: Compare Pearson r of base_experience vs each individual stat and vs total_stats.
- [ ] Multiple testing correction: Bonferroni + Benjamini-Hochberg FDR across all tests
- [ ] Levene's test and Shapiro-Wilk where normality assumption is being made
- [ ] Summary table: hypothesis → test → statistic → p-value → corrected p → effect size → supported?

---

## 19_forecasting.ipynb — Time Series Forecasting

**Skills:** ARIMA, Holt-Winters, ACF/PACF, Ljung-Box test, prediction intervals, statsmodels

- [ ] Overlaid KDE curves: Gen 1 vs Gen 3 vs Gen 6 vs Gen 9 total_stats
- [ ] KS test: Gen 1 vs Gen 9 — significantly different distributions?
- [ ] Levene's test: equal variance across all 9 generations
- [ ] Cohen's d for all 36 generation-pair BST comparisons; Bonferroni correction
- [ ] ARIMA on per-generation mean total_stats. Select order by AIC. Fit and diagnose.
- [ ] ACF and PACF plots. Interpret autocorrelation structure.
- [ ] Ljung-Box test on ARIMA residuals — white noise check.
- [ ] Holt-Winters exponential smoothing as alternative. Compare AIC and forecast intervals.
- [ ] Forecast Gen 10 mean stats with 80% and 95% prediction intervals per stat
- [ ] Forecast legendary introduction rate for Gen 10
- [ ] Sanity check: do forecasts align with known Scarlet/Violet design trends?

---

## 20_external_integration.ipynb — External Data Enrichment

**Skills:** Multi-source pipeline extension, fuzzy name matching, Delta MERGE with schema
evolution, data lineage, enrichment analysis

- [ ] Load `data/external/smogon_tiers.csv` → ingest to `bronze.external_smogon`
- [ ] Load `data/external/vgc_usage.csv` → `bronze.external_vgc`
- [ ] Load `data/external/popularity.csv` → `bronze.external_popularity`
- [ ] Load `data/external/anime_appearances.csv` → `bronze.external_anime`
- [ ] Build fuzzy name matcher (difflib + `data/external/name_mapping.json`) for edge cases:
      Farfetch'd, Mr. Mime, Nidoran♀/♂, Type: Null, Flabébé, Sirfetch'd, Mr. Rime, Ho-Oh
- [ ] Clean → `silver.external_*` tables with standardized pokemon_id join key
- [ ] Delta MERGE enriched columns into `gold.pokemon_full` via `mergeSchema=true`:
      add `smogon_tier, vgc_usage_rate, popularity_rank, anime_appearances`
- [ ] Analysis: does total_stats predict Smogon tier? (Blissey counterexample)
- [ ] Overperformers: high tier + average stats — what distinguishes them?
- [ ] Underperformers: high stats + low tier — what limits them? (Slaking case study)
- [ ] Popularity vs power: Pearson + Spearman. Do fans prefer strong or iconic?
- [ ] Anime appearances vs competitive usage: correlated?
- [ ] Data lineage diagram: ASCII art showing all sources → Bronze → Silver → Gold
- [ ] `DESCRIBE HISTORY gold.pokemon_full` — show the MERGE operation in history