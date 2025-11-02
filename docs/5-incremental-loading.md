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

We also implement the `--new-data` flag to simulate loading new data in the next sections. We modify our source based on this flag.

```python linenums="1"
--8<-- "dlt_tutorial/4_sample_pipeline_append.py:source"
```

Our new command-line interface looks like this:

```bash
$ python dlt_tutorial/4_sample_pipeline_append.py --help
usage: 4_sample_pipeline_append.py [-h] [--refresh] [--new-data]

Sample DLT Pipeline with Append

options:
  -h, --help  show this help message and exit
  --refresh   Refresh the data in the destination (if applicable)
  --new-data  Assume new data is loaded this time
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

## Append with primary key

```python linenums="1" hl_lines="2-3"
--8<-- "dlt_tutorial/4b_sample_pipeline_append_pk.py"
```

## Upsert strategy

```python linenums="1" hl_lines="2-3"
--8<-- "dlt_tutorial/5_sample_pipeline_merge_upsert.py"
```

## Slowly Changing Dimensions (SCD2)

```python linenums="1" hl_lines="2-3"
--8<-- "dlt_tutorial/6_sample_pipeline_merge_scd2.py"
```
