# Trying out incremental loading

## A slight detour: enabling full refresh

We will explore incremental loading strategies in the next sections, but first, we are going to need an easy way to tell dlt how to handle full refreshes so we can rapidly start from scratch, if something goes wrong.

[Refresh](https://dlthub.com/docs/api_reference/dlt/pipeline/configuration#refresh) strategy tells dlt if it should drop existing data in the destination before loading new data. Available strategies are, [as per the documentation](https://dlthub.com/docs/api_reference/dlt/pipeline#run):

- `drop_sources` - Drop tables and source and resource state for all sources currently being processed in run or extract methods of the pipeline. (Note: schema history is erased)
- `drop_resources`- Drop tables and resource state for all resources being processed. Source level state is not modified. (Note: schema history is erased)
- `drop_data` - Wipe all data and resource state for all resources being processed. Schema is not modified.

```python linenums="1" hl_lines="11"
--8<-- "dlt_tutorial/3_sample_pipeline_postgres_config.py:pipeline"
```

To enable this option we can modify our pipeline script to include the `refresh` parameter when creating the pipeline.

```python linenums="1" hl_lines="1-14 32"
--8<-- "dlt_tutorial/4_sample_pipeline_append.py:parse_args"
```

This way, when we run our pipeline with the `--refresh` flag, it will drop existing data in the destination before loading new data.

We also implement the parameter to simulate loading new data in the next sections. We modify our `resource` based on this flag.

```python linenums="1" hl_lines="2 28"
--8<-- "dlt_tutorial/4_sample_pipeline_append.py:resource"
```

Our new command-line interface looks like this:

```bash
$ python dlt_tutorial/4_sample_pipeline_append.py --help
usage: 4_sample_pipeline_append.py [-h] [--refresh]

Sample DLT Pipeline with Append

options:
  -h, --help  show this help message and exit
  --refresh   Refresh the data in the destination (if applicable)
```

and it accepts a parameter through which we can simulate loading new data:

```bash
USE_NEW_DATA=1 python dlt_tutorial/4_sample_pipeline_append.py
```

## Append only

You can now run the pipeline with the `--refresh` flag to start from scratch:

```bash
$ python dlt_tutorial/4_sample_pipeline_append.py --refresh
Running pipeline...
Custom parameter value: foo
Pipeline sample_pipeline_postgres load step completed in 0.09 seconds
1 load package(s) were loaded to destination postgres and into dataset sample_data
The postgres destination used postgresql://postgres:***@localhost:5555/postgres location to store data
Load package 1762043727.4561055 is LOADED and contains no failed jobs
Done
```

and run it again without the `--refresh` flag to append new data:

```bash
$ python dlt_tutorial/4_sample_pipeline_append.py --new-data
Running pipeline...
Custom parameter value: foo
Pipeline sample_pipeline_postgres load step completed in 0.08 seconds
1 load package(s) were loaded to destination postgres and into dataset sample_data
The postgres destination used postgresql://postgres:***@localhost:5555/postgres location to store data
Load package 1762044000.123456 is LOADED and contains no failed jobs
Done
```

You can check the contents of the `sample_data` table in Postgres to see the results:

```sql
SELECT * FROM sample_data.samples;
```

??? question "What happens if we run the pipeline multiple times without the `--refresh` flag?"

    Each time we run the pipeline, new data will be appended to the existing data in the destination. This is because we are using the default `append` loading strategy, which adds new records to the existing table without modifying or deleting any existing records.

### Append with incremental primary key

In our previous example, we were able to append new data to the destination, but we did not have a way to uniquely identify each record. This can lead to duplicate records if the same data is loaded multiple times. An alternative is to use an incremental primary key to uniquely identify each record.

This can be done in two steps:

1. Modify the resource decorator to specify the `id` column as a primary key.

    ```python linenums="1" hl_lines="1"
    --8<-- "dlt_tutorial/4b_sample_pipeline_append_pk.py:resource_decorator"
    ```

2. Apply hints to the resource to specify that the `id` column should be treated as an incremental primary key. `dlt` allows this by using the `apply_hints` method on the resource.

    ```python linenums="1" hl_lines="2-5 7"
    --8<-- "dlt_tutorial/4b_sample_pipeline_append_pk.py:apply_hints"
    ```

!!! tip "See more about [schema hints in the documentation](https://dlthub.com/docs/general-usage/resource#define-schema)."

!!! warning "incremental hint only filters from incoming data"

    `dlt.sources.incremental` is recommended when you want to reduce the amount of data extracted from your source by only selecting new or updated data since your last data extraction.

You can now run the modified pipeline with the `--refresh` flag to start from scratch:

```bash
$ python dlt_tutorial/4b_sample_pipeline_append_pk.py --refresh
# output omitted for brevity
```

and run it again without the `--refresh` flag to append new data:

```bash
$ python dlt_tutorial/4b_sample_pipeline_append_pk.py
# output omitted for brevity
```

You can check the contents of the `sample_data` table in Postgres to see the results:

```sql
SELECT * FROM sample_data.samples;
```

??? question "What happens if we run the pipeline multiple times without the `--refresh` flag?"

    Each time we run the pipeline, new data will be appended to the existing data in the destination. However, since we have specified the `id` column as a primary key, `dlt` will ensure that there are no duplicate records based on this key. If a record with the same `id` already exists in the destination, incoming data with the same `id` will be discarded.

Try running the pipeline now passing the `USE_NEW_DATA=1` environment variable to simulate loading new data:

```bash
$ USE_NEW_DATA=1 python dlt_tutorial/4b_sample_pipeline_append_pk.py
# output omitted for brevity
```

??? question "What is the result of running the pipeline with `USE_NEW_DATA=1`?"

    When running the pipeline with `USE_NEW_DATA=1`, the resource function generates a new set of data that includes records with `id` values that already exist in the destination. However, since we have specified the `id` column as a primary key and applied the incremental hint, `dlt` will discard any incoming records that have an `id` that already exists in the destination. As a result, only new records with unique `id` values will be appended to the destination.

    ```txt
     id |   name    |                 uuid                 |       created_at       |       updated_at       |     metadata__ingested_at     |      metadata__script_name      |    _dlt_load_id    |    _dlt_id     
    ----+-----------+--------------------------------------+------------------------+------------------------+-------------------------------+---------------------------------+--------------------+----------------
      1 | Mr. Mario | a6d7b6dd-bcdb-422e-83eb-f53b2eb4f2cc | 2025-10-09 14:40:00+00 | 2025-10-09 14:50:00+00 | 2025-11-02 15:23:52.179837+00 | 4b_sample_pipeline_append_pk.py | 1762107832.1758425 | 5kO1pi9oN0z/vQ
      2 | Mr. Luigi | 8c804ede-f8ae-409e-964d-9e355a3094e0 | 2025-10-08 16:15:00+00 | 2025-10-08 16:50:00+00 | 2025-11-02 15:23:52.179866+00 | 4b_sample_pipeline_append_pk.py | 1762107832.1758425 | BpMmoBJH+6WA/A
      3 | Ms. Peach | 1a73f32f-9144-4318-9a00-4437bde41627 | 2025-10-12 13:15:00+00 | 2025-10-13 13:50:00+00 | 2025-11-02 15:24:00.04396+00  | 4b_sample_pipeline_append_pk.py | 1762107840.0396352 | 4ZUmjQ7Pt9N/uQ
    (3 rows)
    ```

## Merge strategies

`dlt` also supports `merge` strategies, which allow you to update existing records in the destination based on a specified key.

The merge write disposition can be used with three different strategies:

  1. `delete-insert`: The delete-insert strategy loads data to a staging dataset, deduplicates the staging data if a primary_key is provided, deletes the data from the destination using merge_key and primary_key, and then inserts the new records.
  1. `upsert`: update record if key exists in target table, or insert record if key does not exist in target table
  1. `scd2`: Slowly Changing Dimensions type 2 strategy, which tracks historical changes in data by creating new records for each change while preserving previous records. It will add a new column to track the validity period of each record.

To implement these strategies, we need to modify the `write_disposition` parameter when creating the pipeline.

```python linenums="1" hl_lines="5-8"
--8<-- "dlt_tutorial/5_sample_pipeline_merge_upsert.py:pipeline_run"
```

We can remove the `apply_hints` method since we are not using an incremental primary key in this example.

### Upsert

```python linenums="1" hl_lines="2-3"
--8<-- "dlt_tutorial/5_sample_pipeline_merge_upsert.py"
```

### Slowly Changing Dimensions (SCD2)

```python linenums="1" hl_lines="2-3"
--8<-- "dlt_tutorial/6_sample_pipeline_merge_scd2.py"
```
