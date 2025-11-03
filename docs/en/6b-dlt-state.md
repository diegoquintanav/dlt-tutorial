
# Inspecting `dlt` state

The [`state`](https://dlthub.com/docs/general-usage/state) is a dictionary created by dlt every pipeline run. It can happen that during a pipeline run an error may occur that will halt the execution. We can simulate an error like

```diff
 def sample_data() -> Generator[dict, None, None]:
+    raise Exception("Debugging state: intentional error raised")
```

## `dlt` internals

every time a pipeline is run, `dlt`  will create or update

1. Files in `~/.dlt/pipelines/<pipeline_name>/`
2. In the target table: every row has a `_dlt_load_id`and a `_dlt_id`
3. `dlt` creates three more tables that persist the state of the pipeline ([docs](https://dlthub.com/docs/general-usage/destination-tables#dlts-internal-tables))
    1. `_dlt_loads`
    2. `_dlt_pipeline_state`
    3. `_dlt_version`

## `_dlt_loads` and `_dlt_load_id`

In every table, `_dlt_load_id` is a reference to related load in `_dlt_loads` table

```bash
postgres=# select * from sample_data._dlt_loads order by inserted_at desc limit 5;
      load_id       | schema_name | status |          inserted_at          |             schema_version_hash              
-------------+-------------+--------+-------------------------------+----------------------------------------------
 1757440438.5399692 | sample      |      0 | 2025-09-09 17:53:58.733743+00 | cZ8OQrQKft5FGQB62cV3gmpFng1wBUK4sW/q0skFEtQ=
 1757440119.8848214 | sample      |      0 | 2025-09-09 17:48:41.095752+00 | NyiayaWGe3diqa2Za1rNh9FJ6yomB7l5qZ2Q4ElyBHo=
 1757439294.8177757 | sample      |      0 | 2025-09-09 17:34:54.943091+00 | YXohSbRKFxnKQhpoJtyYbZptbh3jj2A4HLmMtBR9J+k=
 1757439272.1402698 | sample      |      0 | 2025-09-09 17:34:32.274734+00 | YXohSbRKFxnKQhpoJtyYbZptbh3jj2A4HLmMtBR9J+k=
 1757439224.961723  | sample      |      0 | 2025-09-09 17:33:45.097805+00 | YXohSbRKFxnKQhpoJtyYbZptbh3jj2A4HLmMtBR9J+k=
```

You can see what execution your data is from

```sql
select loads.* 
from sample_data.samples as target 
left join sample_data._dlt_loads as loads
on target._dlt_load_id = loads.load_id;
```

---

## `_dlt_id`

- When serializing source records, each record produces its own `_dlt_id`, which is a unique identifier for that record.
- The `_dlt_id` column is generated using the destination's UUID function (it uses `sqlglot`, see [source](https://github.com/dlt-hub/dlt/blob/90819a96182e8d146adfd3985a2032376440c79e/dlt/normalize/items_normalizers.py#L128)), such as `generateUUIDv4()` in ClickHouse. For dialects without native UUID support:
  - In **Redshift**, `_dlt_id` is generated using an `MD5` hash of the load ID and row number.
  - In **SQLite**, `_dlt_id` is simulated using `lower(hex(randomblob(16)))`.

---

## `_dlt_pipeline_state`

Created by DLT. Tracks pipeline states, allowing dlt to resume during incremental loads.

---

## `_dlt_version`

Created by DLT. Tracks schema updates on its column `schema` and `version_hash`

```sql
select column_name from information_schema.columns
where table_name = '_dlt_version' and table_schema = 'sample_data';
```

```bash
  column_name   
----------------
 version
 engine_version
 inserted_at
 schema_name
 version_hash
 schema
```

If you fetch from `_dlt_version.schema` you'll get a JSON that contains description for every table handled by `dlt`.

---

## `_dlt_load_id`

Every row inserted in the target table has a `_dlt_load_id` and a `_dlt_id` column. The former identifies the pipeline run, whereas the latter identifies the row itself.

---

## Inspecting the pipeline state files

```bash
tree  ~/.dlt/pipelines/sample_pipeline/
/home/diego/.dlt/pipelines/sample_pipeline/
├── load
│   ├── loaded
│   │   └── 1757350132.6024446
│   │       ├── applied_schema_updates.json
│   │       ├── completed_jobs
│   │       │   ├── _dlt_pipeline_state.8ef7eda44e.0.insert_values.gz
│   │       │   └── samples.b4c250888f.0.insert_values.gz
│   │       ├── failed_jobs
│   │       ├── load_package_state.json
│   │       ├── new_jobs
│   │       ├── package_completed.json
│   │       ├── schema.json
│   │       └── started_jobs
│   ├── new
│   └── normalized
├── normalize
│   └── extracted
├── schemas
│   └── sample_source.schema.json
├── state.json
└── trace.pickle

12 directories, 9 files
```
