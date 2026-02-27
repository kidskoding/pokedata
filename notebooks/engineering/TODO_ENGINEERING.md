# TODO — Data Engineering (notebooks/engineering/)

> All notebooks run on **Databricks**
> Each notebook starts with:
> ```python
> import sys
> sys.path.insert(0, '/dbfs/FileStore/pokedata/src')
> ```
> Delta tables live at `dbfs:/FileStore/pokedata/delta/{bronze,silver,gold}/`

---

## Core — Intern / Co-op / New Grad

| # | Notebook | Skills |
|---|----------|--------|
| 00 | ingestion | Batch ingestion, idempotency, caching, retry, rate limiting |
| 01 | file_formats | Parquet vs JSON vs CSV, columnar vs row, compression |
| 02 | bronze | Raw landing zone, schema-on-read/write, append-only, CDF |
| 03 | data_modeling | Star schema, fact vs dimension, SCD, wide vs normalized |
| 04 | silver | Cleaning, conforming, junction tables, null handling |
| 05 | gold | Aggregations, partitioning, serving layer |
| 06 | etl_vs_elt | ETL vs ELT, push-down computation |
| 07 | warehouse_concepts | OLAP vs OLTP, lakehouse, dimensional modeling |
| 08 | delta_patterns | MERGE, time travel, CDF, OPTIMIZE, ZORDER |
| 09 | data_quality | DQ rules, quarantine, pipeline contracts |
| 10 | pipeline_testing | Unit tests, integration tests, pytest |

## Beyond entry-level (mid / senior)

| # | Notebook | Focus |
|---|----------|-------|
| 11 | distributed_systems | Shuffles, partitioning, skew, Spark internals |
| 12 | streaming | Structured Streaming, watermarks, stateful ops |
| 13 | storage_optimization | Z-ordering, bloom filters, liquid clustering |
| 14 | query_optimization | Explain plans, AQE, broadcast/skew joins |
| 15 | data_modeling_advanced | Data vault, OBT, medallion patterns |
| 16 | cdc_patterns | CDC beyond CDF, SCD Type 2, log-based |
| 17 | orchestration | DAG, DLT, incremental CDF, Workflows |
| 18 | observability | Monitoring, alerting, lineage |
| 19 | security_governance | PII, masking, Unity Catalog |

---

## 00_ingestion.ipynb — Batch Ingestion & Caching

**Skills:** Batch ingestion, idempotency, caching, retry, rate limiting, manifests, ETL vs ELT intro

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

## 01_file_formats.ipynb — File Formats & Storage

**Skills:** Parquet vs JSON vs CSV vs Avro vs Delta, columnar vs row, compression, when to use each

- [ ] Compare read/write performance: JSON vs CSV vs Parquet vs Delta on Pokemon data
- [ ] Columnar vs row storage: explain and demonstrate scan patterns
- [ ] Compression: Snappy, GZIP, Zstd — size vs speed tradeoffs
- [ ] When to use each format: landing (JSON), staging (Parquet), serving (Delta)
- [ ] Schema evolution implications per format

---

## 02_bronze.ipynb — Raw Landing Zone

**Skills:** Raw landing zone, schema-on-read vs schema-on-write, append-only, audit trails, CDF

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

## 03_data_modeling.ipynb — Data Modeling Fundamentals

**Skills:** Star schema, snowflake, SCD Type 1/2/3, fact vs dimension tables, normalization, wide tables

- [ ] Map Pokemon domain to star schema: facts (stats, encounters) vs dimensions (species, types)
- [ ] Snowflake vs star: when to normalize dimensions
- [ ] SCD Type 1/2/3: demonstrate with evolution chain changes
- [ ] Wide vs normalized: tradeoffs for analytics vs storage
- [ ] Design gold.pokemon_full as wide table; show equivalent star representation

---

## 04_silver.ipynb — Bronze → Silver Cleaning & Conforming

**Skills:** Cleaning, conforming, junction tables, CDC, deduplication, null handling

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

## 05_gold.ipynb — Silver → Gold Aggregations & Serving

**Skills:** Aggregation design, partitioning strategy, serving layer, wide vs normalized

### gold.pokemon_movepool (build first, before gold.pokemon_full)

- [ ] Per-pokemon: `movepool_size_total, movepool_size_by_levelup, movepool_size_by_tm,
      avg_move_power, max_move_power, coverage_type_count, stab_move_count,
      has_priority_move, has_recovery_move, has_setup_move, has_status_move,
      has_multi_hit_move, physical_move_count, special_move_count, status_move_count,
      avg_pp, total_pp`

### gold.pokemon_full (master wide table, ~1025 rows, ~80 cols)

- [ ] Join: silver.pokemon + silver.pokemon_species + silver.evolution_chains +
      silver.egg_groups + silver.growth_rates + gold.pokemon_movepool +
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

## 06_etl_vs_elt.ipynb — ETL vs ELT Architecture

**Skills:** ETL vs ELT architecture, push-down computation, when each pattern applies

- [ ] Define ETL: transform in pipeline before load
- [ ] Define ELT: load raw, transform in warehouse/lakehouse
- [ ] Push-down computation: when to filter/aggregate at source vs in Spark
- [ ] When each pattern applies: batch vs streaming, latency vs flexibility
- [ ] Map Pokemon pipeline: ingestion (E) → Bronze (L) → Silver/Gold (T) — hybrid pattern

---

## 07_warehouse_concepts.ipynb — Warehouse & Lakehouse Concepts

**Skills:** OLAP vs OLTP, normalization levels, why lakehouses exist, dimensional modeling

- [ ] OLAP vs OLTP: read patterns, consistency, use cases
- [ ] Normalization levels: 1NF–3NF vs denormalized for analytics
- [ ] Why lakehouses exist: data lakes + ACID + schema
- [ ] Dimensional modeling: Kimball vs Inmon, applied to Pokemon

---

## 08_delta_patterns.ipynb — Delta Lake Engineering Patterns

**Skills:** MERGE, time travel, CDF, OPTIMIZE, ZORDER, VACUUM, schema evolution, small files

- [ ] **MERGE (upsert):** Simulate "Gen 10 data arrives" — INSERT, UPDATE, no-op
- [ ] **Time Travel:** `DESCRIBE HISTORY`, `VERSION AS OF`, `TIMESTAMP AS OF`
- [ ] **Change Data Feed:** read CDF, show `_change_type`, incremental Silver
- [ ] **OPTIMIZE + ZORDER:** before/after file count, explain plan comparison
- [ ] **VACUUM:** `RETAIN 168 HOURS`, explain tradeoffs
- [ ] **Schema Evolution:** `mergeSchema=true`, add `is_paradox_form`
- [ ] **Partitioning benchmark:** unpartitioned vs partitioned query
- [ ] **Small file problem:** proliferation, OPTIMIZE + coalesce

---

## 09_data_quality.ipynb — DQ Framework & Validation

**Skills:** DQ dimensions, rule engines, quarantine, Great Expectations, pipeline contracts

- [ ] Import `src/quality.py` — `DataQualityChecker` class
- [ ] Demonstrate all rule types: NotNull, Unique, Range, InSet, Regex, CustomFn
- [ ] Run DQ suite on every Silver table; display pass/fail per rule
- [ ] Generate HTML quality report
- [ ] Quarantine pattern: failed rows → `silver._quarantine_{table_name}`
- [ ] Pipeline halts if CRITICAL rule fails

---

## 10_pipeline_testing.ipynb — Pipeline Testing

**Skills:** Unit testing transforms, integration testing, test data generation, pytest

- [ ] Unit test transform functions: mock inputs, assert outputs
- [ ] Integration test: run Bronze → Silver on fixture data
- [ ] Test data generation: minimal valid datasets
- [ ] pytest fixtures for SparkSession, sample DataFrames
- [ ] CI: run tests before merge

---

## 11_distributed_systems.ipynb — Spark Internals & Distributed Systems

**Skills:** Shuffles, partitioning, skew, broadcasting, memory management, Spark internals

- [ ] Explain shuffle: when it happens, why it's expensive
- [ ] Partitioning: coalesce, repartition, partitionBy
- [ ] Skew: detect, salting, skew joins
- [ ] Broadcasting: when to broadcast small tables
- [ ] Memory management: executor/driver, OOM prevention
- [ ] Spark execution model: DAG, stages, tasks

---

## 12_streaming.ipynb — Structured Streaming

**Skills:** Structured Streaming, micro-batch vs continuous, watermarks, late data, stateful ops

- [ ] Micro-batch vs continuous processing
- [ ] Watermarks and late data handling
- [ ] Stateful operations: aggregations, deduplication
- [ ] Simulate streaming: read Bronze as stream, append to Silver
- [ ] Checkpointing and exactly-once semantics

---

## 13_storage_optimization.ipynb — Storage Optimization

**Skills:** Z-ordering, bloom filters, liquid clustering, compaction, statistics, predicate pushdown

- [ ] Z-ordering: when and how, measure query improvement
- [ ] Bloom filters: when they help, `delta.autoOptimize.optimizeWrite`
- [ ] Liquid clustering (Databricks): vs Z-order
- [ ] Compaction: small file coalescing
- [ ] Statistics and predicate pushdown: EXPLAIN to verify

---

## 14_query_optimization.ipynb — Query Optimization

**Skills:** Explain plans, AQE, broadcast joins, skew joins, caching, partitioning benchmarks

- [ ] EXPLAIN / EXPLAIN EXTENDED: read plans, identify bottlenecks
- [ ] Adaptive Query Execution (AQE): what it does
- [ ] Broadcast joins: `broadcast()` hint, auto-broadcast threshold
- [ ] Skew joins: `skewJoin`
- [ ] Caching: when to cache, cache eviction
- [ ] Partitioning benchmarks: measure before/after

---

## 15_data_modeling_advanced.ipynb — Advanced Data Modeling

**Skills:** Data vault, one big table, lakehouse modeling, medallion design patterns

- [ ] Data vault: hubs, links, satellites
- [ ] One Big Table (OBT): when to denormalize heavily
- [ ] Lakehouse modeling: medallion (bronze/silver/gold) patterns
- [ ] Compare approaches for Pokemon: which fits?

---

## 16_cdc_patterns.ipynb — CDC Patterns

**Skills:** CDC beyond CDF, SCD implementation, upsert patterns, log-based CDC concepts

- [ ] CDC beyond Delta CDF: Debezium, Kafka, log-based
- [ ] SCD Type 2 implementation in Delta
- [ ] Upsert patterns: MERGE, deduplication
- [ ] Log-based CDC concepts: change capture, replay

---

## 17_orchestration.ipynb — Pipeline Orchestration

**Skills:** DAG design, dependency management, idempotent pipelines, failure handling, backfill

- [ ] DAG simulation: chain notebooks as tasks, dependency graph
- [ ] Delta Live Tables (DLT) concepts: `@dlt.table`, `@dlt.expect`
- [ ] Incremental CDF pipeline: reprocess only changed rows
- [ ] Databricks Workflows: job config, cluster policies
- [ ] Failure handling, backfill strategies

---

## 18_observability.ipynb — Pipeline Observability

**Skills:** Pipeline monitoring, alerting, data freshness, SLAs, lineage, logging patterns

- [ ] Pipeline monitoring: what to track
- [ ] Alerting: freshness, row counts, DQ failures
- [ ] Data freshness and SLAs
- [ ] Lineage: table-to-table, column-level
- [ ] Logging patterns: structured logs, correlation IDs

---

## 19_security_governance.ipynb — Security & Governance

**Skills:** PII handling, data masking, row/column security, Unity Catalog, data contracts

- [ ] PII handling: identification, masking strategies
- [ ] Row/column-level security
- [ ] Unity Catalog: metastore, access control
- [ ] Data contracts: schema enforcement, versioning
