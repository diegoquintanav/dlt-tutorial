# A simple example using `duckdb`

At its most basic form, `dlt` takes in an iterable that produces dictionaries. it will treat every dictionary as a unit of data and it will move it into a `target`.

Take for example the following dictionary:

```python linenums="1"
--8<-- "dlt_tutorial/0_sample_pipeline_basic.py:my_data"
```

Here is a simple example that uses `dlt` to load data into a `duckdb` database.

```python linenums="1"
--8<-- "dlt_tutorial/0_sample_pipeline_basic.py:pipeline"
```

!!! tip "dlt does not care how you produce the data"

    The data source can be anything that produces dictionaries. For example, you can use `pandas`, e.g. `[row.to_dict() for _, row in df.iterrows()]`.

## What is happening here?

1. We define a list of dictionaries called `my_data`. Each dictionary represents a record with fields like `id`, `name`, `age`, and `address`.
2. We create a `dlt` pipeline using `dlt.pipeline()`, specifying the pipeline name and the destination as `duckdb`.
3. We use `pipeline.run(my_data)` to load the data from `my_data` into the `duckdb` database. The `write_disposition` parameter is set to `replace`, which means that if the target table already exists, it will be replaced with the new data. This is useful in this example to ensure that we start with a clean slate each time we run the script.

## Running the example

Run the script directly using Python:

```bash
$ python dlt_tutorial/0_sample_pipeline_basic.py
Running pipeline...
Done
```

!!! warning "DuckDB limitations on concurrency"

    Beware that duckdb does not allow for concurrent access. **If you try to run the pipeline while having a client already connected to the database, the pipeline will fail.**

This will create a `duckdb` database file in the current directory (by default named `sample_pipeline.duckdb`) and load the data into it. You can then query the database using any `duckdb` client or library.

```bash
$ duckdb sample_pipeline.duckdb -c "select * from sample_data.samples;"
┌───────┬───────────┬──────────────────────────────────────┬──────────────────────────┬──────────────────────────┬───────────────────────────────┬────────────────────────────┬────────────────────┬────────────────┐
│  id   │   name    │                 uuid                 │        created_at        │        updated_at        │     metadata__ingested_at     │   metadata__script_name    │    _dlt_load_id    │    _dlt_id     │
│ int64 │  varchar  │               varchar                │ timestamp with time zone │ timestamp with time zone │   timestamp with time zone    │          varchar           │      varchar       │    varchar     │
├───────┼───────────┼──────────────────────────────────────┼──────────────────────────┼──────────────────────────┼───────────────────────────────┼────────────────────────────┼────────────────────┼────────────────┤
│     1 │ Mr. Mario │ a6d7b6dd-bcdb-422e-83eb-f53b2eb4f2cc │ 2025-10-09 11:40:00-03   │ 2025-10-09 11:50:00-03   │ 2025-10-29 14:32:44.702763-03 │ 0_sample_pipeline_basic.py │ 1761769965.1842644 │ sVJ0ooLEPZsP1Q │
│     2 │ Mr. Luigi │ 8c804ede-f8ae-409e-964d-9e355a3094e0 │ 2025-10-08 13:15:00-03   │ 2025-10-08 13:50:00-03   │ 2025-10-29 14:32:44.702794-03 │ 0_sample_pipeline_basic.py │ 1761769965.1842644 │ P7QNYrq+IMHy1A │
└───────┴───────────┴──────────────────────────────────────┴──────────────────────────┴──────────────────────────┴───────────────────────────────┴────────────────────────────┴────────────────────┴────────────────┘
```

## What is `dlt` doing under the hood?

Congratulations! You have successfully loaded data into a `duckdb` database using `dlt`. There are a few things happening under the hood that are worth mentioning:

1. It created a `table` called `sample_data.samples`. In this table, every row has a `_dlt_load_id` and a `_dlt_id`. These are references to internal `dlt` mechanisms for tracking loads and identifying records.

2. `dlt` creates also three more tables that persist the state of the pipeline
    1. `_dlt_loads`
    2. `_dlt_pipeline_state`
    3. `_dlt_version`

3. Unknown to you, `dlt` also created a directory in `~/.dlt/pipelines/sample_pipeline`

## Wrapping up

We saw a simple example of using `dlt` to load data into a `duckdb` database.

We'll step it up a notch in the next part by using `resources` and `sources` to structure our data extraction better.

## Full example

```python linenums="1"
--8<-- "dlt_tutorial/0_sample_pipeline_basic.py"
```
