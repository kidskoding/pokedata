# TODO — Data Engineering (notebooks/engineering/)

> All notebooks run on **Databricks**
> Each notebook starts with:
> ```python
> import sys
> sys.path.insert(0, '/dbfs/FileStore/pokedata/src')
> ```
> Delta tables live at `dbfs:/FileStore/pokedata/delta/{bronze,silver,gold}/`

---

## 00_ingestion.ipynb — Async API Fetching & DBFS Caching

**Skills:** aiohttp, asyncio, semaphore, exponential backoff, DBFS caching, ingestion manifest

- [ ] Import `src/ingestion.py` — `AsyncPokeAPIFetcher` class
- [ ] Define all 18 endpoint configs: URL pattern + expected record count
- [ ] Check DBFS cache before fetching: `dbutils.fs.ls('dbfs:/FileStore/pokedata/cache/{endpoint}/')`
- [ ] Async fetch with `asyncio.Semaphore(20)` — cap concurrent requests
- [ ] Retry logic: exponential backoff 1s → 2s → 4s on 429/5xx, max 3 retries
- [ ] Write each response to `dbfs:/FileStore/pokedata/cache/{endpoint}/{id}.json`
- [ ] Update ingestion manifest per (endpoint, id): timestamp, status, bytes, retries
- [ ] `tqdm` progress bar per endpoint
- [ ] Post-fetch validation: assert file count per endpoint matches expected record count
- [ ] Display manifest summary: total fetched, total cached hits, total failures

---

## 01_bronze.ipynb — Raw Ingestion to Bronze Delta Tables

**Skills:** PySpark, Delta Lake, StructType schema enforcement, append-only writes,
Change Data Feed, audit columns, DBFS JSON reads

- [ ] Initialize SparkSession (already configured on Databricks cluster)
- [ ] Import `src/schemas.py` — all Bronze StructType definitions
- [ ] For each of the 18 endpoints:
      - Read from DBFS cache: `spark.read.json(cache_path, schema=bronze_schema)`
      - Add audit columns: `_ingested_at`, `_source_url`, `_response_bytes`, `_pipeline_run_id`
      - Write to Delta: `df.write.format("delta").mode("append").save(bronze_path)`
- [ ] Enable Change Data Feed on all 18 Bronze tables:
      `ALTER TABLE bronze.X SET TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true')`
- [ ] Validate row counts: assert each table matches expected API totals
- [ ] `DESCRIBE DETAIL bronze.pokemon` — show file count, size, partition info
- [ ] Log Bronze table stats to `dbfs:/FileStore/pokedata/pipeline_log.json`

---

## 02_silver.ipynb — Bronze → Silver Cleaning & Conforming

**Skills:** PySpark transformations, explode, pivot, null handling, unit conversion,
schema enforcement, junction tables, recursive Python for evolution chains, audit columns

### silver.pokemon

- [ ] Explode `stats` array → `hp, attack, defense, sp_attack, sp_defense, speed` (IntegerType)
- [ ] Explode `types` → `type_1, type_2 STRING` (null if mono); add `is_dual_type BOOLEAN`
- [ ] `height_m = height / 10.0`, `weight_kg = weight / 10.0`
- [ ] Extract `sprites.front_default` as `sprite_url STRING`
- [ ] Enforce schema; quarantine malformed rows to `silver._quarantine_pokemon`

### silver.pokemon_species

- [ ] Extract English `flavor_text`; strip `\f`, `\n`, special chars
- [ ] Parse `gender_rate`: −1=genderless, 0=100%M, 8=100%F, else compute float ratio
- [ ] Flatten `egg_groups` → `egg_group_1, egg_group_2 STRING`
- [ ] Flatten `pokedex_numbers` → `national_dex_number INT`
- [ ] Flatten `pal_park_encounters` → `pal_park_area, pal_park_base_score, pal_park_rate`

### silver.pokemon_abilities (junction)

- [ ] Columns: `pokemon_id, ability_id, ability_name, is_hidden BOOLEAN, slot INT`
- [ ] Up to 3 rows per pokemon

### silver.pokemon_moves (junction)

- [ ] Columns: `pokemon_id, move_id, move_name, learn_method, level_learned, version_group`
- [ ] Deduplicate: latest version_group per (pokemon, move, learn_method)
- [ ] Add `is_stab BOOLEAN`: join to silver.pokemon, check move type vs pokemon types

### silver.moves

- [ ] Parse all meta fields; null power/accuracy valid for status moves
- [ ] Add `is_physical, is_special, is_status BOOLEAN` from damage_class
- [ ] Add `has_secondary_effect, is_priority, is_multi_hit BOOLEAN`

### silver.abilities

- [ ] English effect entries only (short + long)
- [ ] Add `is_hidden_ability_only BOOLEAN`

### silver.type_matchups (18×18 matrix)

- [ ] Expand damage_relations → `attacker_type, defender_type, multiplier DECIMAL(4,2)`
- [ ] Validate: multipliers only in {0, 0.25, 0.5, 1.0, 2.0, 4.0}

### silver.dual_type_matchups (combined defense)

- [ ] All ~153 unique dual-type combos: multiply single-type multipliers
- [ ] Add `is_immune, is_4x_weak, is_4x_resist, is_2x_weak, is_2x_resist BOOLEAN` flags

### silver.evolution_chains (recursive tree → flat rows)

- [ ] Python recursive function to flatten chain tree
- [ ] Output: `chain_id, pokemon_name, evolves_from_name, evolution_stage, chain_length,
      is_branched, trigger, min_level, min_happiness, held_item, time_of_day, location,
      trade_partner, known_move, gender_required, needs_rain, turn_upside_down,
      min_affection, min_beauty, relative_physical_stats`

### silver.location_encounters (fully denormalized)

- [ ] One row per (pokemon, location, version, method):
      `pokemon_id, location_name, region, version, encounter_method,
       min_level, max_level, encounter_chance, condition_values`

### silver.items + junctions

- [ ] `silver.item_held_by`: `item_id, pokemon_id, rarity, version`
- [ ] `silver.item_machines`: `item_id, machine_number, move_id, version_group`

### silver.berries

- [ ] Pivot flavor potencies: `spicy, dry, sweet, bitter, sour INT` columns
- [ ] Join to silver.items for cost and category

### silver.natures

- [ ] Add `is_neutral BOOLEAN` (5 natures where increased == decreased stat)

### All Silver tables

- [ ] Add `_silver_updated_at TIMESTAMP` and `_row_hash STRING` (MD5 non-audit cols)
- [ ] Enforce NOT NULL on all primary key columns
- [ ] Run `src/quality.py` DQ checks on every Silver table; fail pipeline if critical rules fail

---

## 03_gold.ipynb — Silver → Gold Aggregations & Serving

**Skills:** PySpark joins, window functions for percentiles, complex aggregations,
partitioning, ZORDER, wide table construction, feature engineering at scale

### gold.pokemon_full (master wide table, ~1025 rows, ~80 cols)

- [ ] Join: silver.pokemon + silver.pokemon_species + silver.evolution_chains +
      silver.egg_groups + silver.growth_rates + gold.pokemon_movepool (built first) +
      silver.pokemon_abilities (pivoted: ability_1, ability_2, hidden_ability)
- [ ] Computed stat columns:
      `total_stats, offensive_power (atk+sp_atk), defensive_bulk (def+sp_def+hp),
       speed_tier (slow<50/mid 50-79/fast 80-109/ultra 110+),
       physical_ratio (atk/(atk+sp_atk)), stat_variance, stat_cv, min_stat, max_stat, stat_range`
- [ ] Percentiles via Spark window functions (no leakage):
      `bst_percentile, hp_percentile, atk_percentile, def_percentile,
       sp_atk_percentile, sp_def_percentile, speed_percentile`
- [ ] Evolution: `evolution_stage, chain_length, is_fully_evolved, is_branched_evolution,
       evolves_from_name, evolution_trigger`
- [ ] Availability: `total_locations_wild, total_versions_available,
       rarest_encounter_chance, most_common_encounter_method`
- [ ] `PARTITIONED BY (generation)`, `ZORDER BY (generation, total_stats)`

### gold.type_effectiveness_matrix

- [ ] Full 18×18 single-type table + `coverage_score` per attacker
- [ ] Full dual-type combined defense table (~153 combos) with resistance/weakness counts
- [ ] `best_offensive_types`: rank attacker types by avg multiplier across all defenders

### gold.pokemon_movepool (built before gold.pokemon_full)

- [ ] Per-pokemon: `movepool_size_total, movepool_size_by_levelup, movepool_size_by_tm,
      avg_move_power, max_move_power, coverage_type_count, stab_move_count,
      has_priority_move, has_recovery_move, has_setup_move, has_status_move,
      has_multi_hit_move, physical_move_count, special_move_count, status_move_count,
      avg_pp, total_pp`

### gold.generational_stats (one row per generation)

- [ ] Per-stat mean/median/stddev for all 6 stats + total_stats
- [ ] `legendary_count, mythical_count, baby_count, regular_count, dual_type_rate`
- [ ] `new_abilities_count, new_moves_count, avg_movepool_size, avg_capture_rate`
- [ ] `type_distribution` as JSON map column

### gold.ability_summary

- [ ] `pokemon_count, legendary_count, avg_bst, max_bst, min_bst,
      most_common_type, hidden_only_count`

### gold.encounter_map

- [ ] Per pokemon per region: `region, location_count, version_count,
      min_encounter_level, max_encounter_level, avg_encounter_chance, primary_method`

### gold.move_coverage

- [ ] Per move type: `avg_multiplier_vs_all_types, coverage_score, best_targets, worst_targets`

### gold.berry_analysis

- [ ] All berry attributes + `dominant_flavor, total_flavor_potency, flavor_balance_score`

### gold.nature_stat_impact

- [ ] Nature → stat boosted/reduced + which pokemon benefit most

---

## 04_delta_patterns.ipynb — Delta Lake Engineering Patterns

**Skills:** MERGE, time travel, Change Data Feed, OPTIMIZE, ZORDER, VACUUM,
schema evolution, partitioning benchmarks, small file problem

- [ ] **MERGE (upsert):** Simulate "Gen 10 data arrives":
      - 5 new pokemon → INSERT
      - 3 existing pokemon with stat corrections → UPDATE
      - Rest → no-op
      - Show full `MERGE INTO ... WHEN MATCHED ... WHEN NOT MATCHED` syntax
- [ ] **Time Travel:**
      - `DESCRIBE HISTORY gold.pokemon_full` — show all write versions
      - Query `VERSION AS OF 0` vs current. Show changed rows.
      - Query `TIMESTAMP AS OF '...'` — point-in-time read
- [ ] **Change Data Feed:**
      - After simulated re-ingestion, read: `spark.read.format("delta")
        .option("readChangeFeed","true").option("startingVersion",1)
        .table("bronze.pokemon")`
      - Show `_change_type`: insert / update_preimage / update_postimage / delete
      - Use CDF to do incremental Silver processing — only reprocess changed rows
- [ ] **OPTIMIZE + ZORDER:**
      - Before: `DESCRIBE DETAIL gold.pokemon_full` — show file count
      - Run: `OPTIMIZE gold.pokemon_full ZORDER BY (generation, total_stats)`
      - After: show reduced file count
      - Run same analytical query before/after; compare file skipping in `EXPLAIN`
- [ ] **VACUUM:**
      - `VACUUM gold.pokemon_full RETAIN 168 HOURS`
      - Explain what gets deleted, why, and how it limits time travel
- [ ] **Schema Evolution:**
      - Add `is_paradox_form BOOLEAN` to silver.pokemon using `mergeSchema=true`
      - Show downstream Gold reads still work without rewriting Gold
- [ ] **Partitioning benchmark:**
      - `WHERE generation = 1` on unpartitioned vs partitioned Gold
      - Show file skipping count in explain plan; measure query time difference
- [ ] **Small file problem:**
      - After 10 small incremental appends to a Silver table, show file proliferation
      - Apply `OPTIMIZE` + `coalesce`; show before/after file counts

---

## 05_data_quality.ipynb — DQ Framework & Validation

**Skills:** Great Expectations (or custom), rule-based DQ, HTML reporting, pytest patterns

- [ ] Import `src/quality.py` — `DataQualityChecker` class
- [ ] Demonstrate all rule types with Pokemon data examples:
      - `NotNullRule`: pokemon_id across all tables
      - `UniqueRule`: pokemon_id in silver.pokemon
      - `RangeRule`: all 6 stats range 1–255; capture_rate 3–255
      - `InSetRule`: type_1 + type_2 in set of 18 valid types; evolution_stage in {1,2,3};
        gender_rate in {-1,0,1,2,4,6,7,8}; multipliers in {0,0.25,0.5,1,2,4}
      - `RegexRule`: sprite_url matches `https://raw.githubusercontent.com/...`
      - `CustomFnRule`: all 18 types present in silver.type_matchups
- [ ] Run DQ suite on every Silver table; display pass/fail per rule
- [ ] Generate HTML quality report; save to `dbfs:/FileStore/pokedata/outputs/dq_report.html`
- [ ] Intentionally inject 10 bad rows into a Silver table; show DQ catches them
- [ ] Quarantine pattern: failed rows → `silver._quarantine_{table_name}` with failure reason column
- [ ] Demonstrate: pipeline halts if any CRITICAL rule fails (vs WARNING rules that log only)

---

## 06_orchestration.ipynb — Pipeline Orchestration Patterns

**Skills:** DAG design, DLT concepts, incremental CDF pipeline, Databricks Workflows concepts

- [ ] **DAG simulation:** `pipeline_dag.py` chains all 6 engineering notebooks as tasks.
      Each task: check upstream table health (row count, schema) before running.
      Task failure stops downstream execution. Show dependency graph as ASCII diagram.
- [ ] **Delta Live Tables (DLT) concepts:**
      - Define one Bronze table as `@dlt.table` with `@dlt.expect` quality constraints
      - Define one Silver table reading from Bronze via `dlt.read()`
      - Show quarantine pattern: failed rows → `_quarantine` table
      - Explain how DLT handles re-runs differently from imperative notebooks
- [ ] **Incremental CDF pipeline:**
      - Read CDF from bronze.pokemon for only changed records since last run
      - Reprocess only those records through Silver → Gold (skip unchanged)
      - Compare cost: full re-run (1025 rows) vs incremental (50 changed rows)
      - Store last processed version in `dbfs:/FileStore/pokedata/pipeline_state.json`
- [ ] **Databricks Workflows walk-through:**
      - Describe how these notebooks would be scheduled as a Workflow DAG
      - Show what the job config JSON would look like
      - Explain cluster policies, job clusters vs all-purpose clusters, cost tradeoffs
