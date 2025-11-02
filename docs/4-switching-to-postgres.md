# Part 2: Implementing incremental data loading

## Introduction to incremental loading

Consider the following state of your table at a given time:

| id |   name    |       created_at       |       updated_at       |
|---:|-----------|------------------------|------------------------|
| 1  | Mr. Mario | 2025-10-09 14:40:00    | 2025-10-09 14:50:00    |
| 2  | Mr. Luigi | 2025-10-08 16:15:00    | 2025-10-08 16:50:00    |

In this table, we can identify two records, which can be uniquely identified by their `id` or `uuid` fields. Each record also has `created_at` and `updated_at` timestamps.

Now, imagine that some time has passed, and we have new data to load into our table. We fetch our data from a remote API that serves incremental updates on information about Mario and Luigi.

The new **incoming** data looks like this:

| id |   name    |       created_at       |       updated_at       |
|---:|-----------|------------------------|------------------------|
| 1  | Jumpman   | 2025-10-09 14:40:00    | 2025-10-10 11:50:00    |
| 3  | Ms. Peach | 2025-10-12 13:15:00    | 2025-10-11 13:50:00    |

Mario is [now known](https://www.reddit.com/r/Marioverse/comments/1ef7f4f/jan_misalis_breakdown_of_the_jumpman_is_not_mario/) as ["Jumpman"](https://www.mariowiki.com/List_of_Mario_names_in_other_languages#Jumpman), it was updated a day after its latest update, and a new record for "Ms. Peach" has been added.

What should be the final state of our table after loading this new data? _It depends on the logic we want to implement for handling updates and inserts._

Although there are many strategies, here are some common ones:

### Replace everything

Ignore existing state and replace everything: In this case, we would simply replace the entire table with the incoming data.

| id |   name    |       created_at       |       updated_at       |
|---:|-----------|------------------------|------------------------|
| 1  | Jumpman   | 2025-10-09 11:40:00-03 | 2025-10-10 11:50:00-03 |
| 3  | Ms. Peach | 2025-10-10 13:25:00-03 | 2025-10-10 13:50:00-03 |

### Append new data

Simply append the incoming data to the existing table:

| id |   name    |       created_at       |       updated_at       |
|---:|-----------|------------------------|------------------------|
| 1  | Mr. Mario | 2025-10-09 11:40:00-03 | 2025-10-09 11:50:00-03 |
| 2  | Mr. Luigi | 2025-10-08 13:15:00-03 | 2025-10-08 13:50:00-03 |
| 1  | Jumpman   | 2025-10-09 11:40:00-03 | 2025-10-10 11:50:00-03 |
| 3  | Ms. Peach | 2025-10-10 13:25:00-03 | 2025-10-10 13:50:00-03 |

### Merge new records into existing ones

We can update existing records or append new ones. For this, we need to rely on some identifier such as the `id`, that _uniquely identifies_ a record:

If we consider the `id` as such a record, we would update Mario's record with the new name and updated timestamp, and insert the new record for "Ms. Peach".

| id |   name    |       created_at       |       updated_at       |
|---:|-----------|------------------------|------------------------|
| 1  | Jumpman   | 2025-10-09 11:40:00-03 | 2025-10-10 11:50:00-03 |
| 2  | Mr. Luigi | 2025-10-08 13:15:00-03 | 2025-10-08 13:50:00-03 |
| 3  | Ms. Peach | 2025-10-10 13:25:00-03 | 2025-10-10 13:50:00-03 |

The merge strategy is the most common one when dealing with incremental data loading. It allows us to keep our data up-to-date while minimizing the amount of data we need to process.

## An example with Postgres

A good example of a database that supports incremental loading is Postgres. Postgres provides several mechanisms for handling updates and inserts, such as `UPSERT` (using `ON CONFLICT`), or `MERGE` in more recent versions, which allows us to insert new records or update existing ones based on a unique constraint.

As per its documentation, [`MERGE`](https://www.postgresql.org/docs/current/sql-merge.html#notes) implements a join operation using a `join_condition`.

```sql
[ WITH with_query [, ...] ]
MERGE INTO [ ONLY ] target_table_name [ * ] [ [ AS ] target_alias ]
    USING data_source ON join_condition
    when_clause [...]
    [ RETURNING [ WITH ( { OLD | NEW } AS output_alias [, ...] ) ]
                { * | output_expression [ [ AS ] output_name ] } [, ...] ]
```

In the following example, `MERGE` requires a `target` table (the table we want to update) and a `source` table (the new data we want to insert or use to update the target).

```sql
MERGE INTO target_table tt
  USING source_table st
    ON st.id = tt.id
WHEN MATCHED THEN
  UPDATE SET name = st.name
WHEN NOT MATCHED THEN
  INSERT (id, name)
  VALUES (st.id, st.name);
```

In this example, we are merging data from `source_table` into `target_table` based on the `id` column. If a matching record is found, we update the `name` column; if not, we insert a new record.

## Implementing incremental loading with `dlt`

How do we know what scenario we need to implement? It depends. `dlt` summarizes every use case with the following diagram:

![alt text](assets/img/incremental-decision-tree.png)

We can load data in different ways, depending on the requirements. See the [documentation for a full introduction](https://dlthub.com/docs/general-usage/incremental-loading)

We can define the **write disposition** and the **write strategy** when **running a pipeline**. We can choose from `"replace"`, `"append"`, `"merge"`

1. `"replace"`: Replaces the table entirely
2. `"append"`: Loads rows incrementally, regardless of their values
3. `"merge"`: Inserts only rows that are relevant to the update, e.g. that _match_ data in target according to some **strategy** and some **key** that allows for identifying matching rows. For the "merge" disposition

    1. `"delete-insert"`: given a **match** between incoming and existing rows on some **key**, **DELETE** the target row and **INSERT** it from incoming. This operation is **locking** or it may not be supported, depending on the target database.
    2. `"upsert"`: given a **match** between incoming and existing rows on some **key**, **UPDATE** the target row and "**INSERT**" what's changed from incoming data. This operation is not **locking** but it may not be supported, depending on the target database.
    3. `"scd2"`: given a **match** between incoming and existing rows on some **key**, leave the existing target row and "**INSERT**" a new one from the incoming data. Using some additional columns, this allows for tracking the validity of the latest value, but it takes more space in disk.

## Setting up a Postgres database

Refer to the [Getting Started](getting-started.md) section to learn how to set up a postgres database. Once you have a valid postgres instance, you need to setup its postgres credentials.

!!! info "Incremental loading patterns are not supported by duckdb"

    Duckdb is an analytics, in-memory database. It shines for some types of tasks, and it offers its own implementation of `MERGE`. However, incremental loading patterns are not fully supported by `dlt` at the moment.

## Configure `dlt` to use Postgres

You'll need to tell `dlt` how to connect to your Postgres database. The recommended way is to create a `secrets.toml` file in the root of this project with the following content:

```toml
[sample_pipeline_postgres.destination.postgres.credentials]
host = "localhost"
port = 5555
user = "postgres"
password = "test"
dbname = "postgres"
```

If you wish to use the connection string method, for example when using a neon database, you can also do it like this:

```toml
sample_pipeline_postgres.destination.postgres.credentials = 'postgresql://neondb_owner:<password>@<host>/neondb?sslmode=require&channel_binding=require'
```

!!! warning "Do not commit your secrets.toml file"

    Make sure to add `secrets.toml` to your `.gitignore` file to avoid committing sensitive information to version control.

!!! warning "Adjust connection parameters as needed"

    Adjust the connection parameters (`host`, `port`, `user`, `password`, `dbname`) according to your Postgres setup. If you are using the devcontainer, the host should be `postgres` and the port `5432`.

You can also set the connection parameters using environment variables. See the [documentation](https://dlthub.com/docs/general-usage/credentials/setup#postgresql) for more information.

## Replace everything using postgres

You can run now the [3_sample_pipeline_postgres_config.py](../dlt_tutorial/3_sample_pipeline_postgres_config.py) script to test the Postgres connection and configuration.

The only things that have changed from the previous examples is the `write_disposition` and `write_strategy` parameters when running the pipeline:

```python linenums="1" hl_lines="2-3"
--8<-- "dlt_tutorial/3_sample_pipeline_postgres_config.py:pipeline"
```

If we run this example, we should see output similar to this:

```bash
$ python dlt_tutorial/3_sample_pipeline_postgres_config.py
Starting pipeline...
Custom parameter value: foo
Pipeline run completed.
Pipeline sample_pipeline_postgres load step completed in 0.11 seconds
1 load package(s) were loaded to destination postgres and into dataset sample_data
The postgres destination used postgresql://postgres:***@localhost:5555/postgres location to store data
Load package 1762003276.163356 is LOADED and contains no failed jobs
```

We can now connect to our Postgres database and check the contents of the `sample_data.samples` table:

```bash
$PGPASSWORD=test psql -h 0.0.0.0 -p 5555 -U postgres --pset expanded=auto -c "select * from sample_data.samples;"
 id |   name    |                 uuid                 |       created_at       |       updated_at       |     metadata__ingested_at     |        metadata__script_name         |   _dlt_load_id    |    _dlt_id     
----+-----------+--------------------------------------+------------------------+------------------------+-------------------------------+--------------------------------------+-------------------+----------------
  1 | Mr. Mario | a6d7b6dd-bcdb-422e-83eb-f53b2eb4f2cc | 2025-10-09 14:40:00+00 | 2025-10-09 14:50:00+00 | 2025-11-01 10:21:16.172598+00 | 3_sample_pipeline_postgres_config.py | 1762003276.163356 | MJaJ6AzyVleWlQ
  2 | Mr. Luigi | 8c804ede-f8ae-409e-964d-9e355a3094e0 | 2025-10-08 16:15:00+00 | 2025-10-08 16:50:00+00 | 2025-11-01 10:21:16.172663+00 | 3_sample_pipeline_postgres_config.py | 1762003276.163356 | IrYyUJd1NAmnBQ
(2 rows)
```

??? question "What happens if we run the script again?"

    If you run the script again, since the `write_disposition` is set to `"replace"` and the `refresh` parameter is set to `"drop_sources"`, the existing data in the `sample_data.samples` table will be replaced with the new data fetched from the source, every time. You should see different `metadata__ingested_at` timestamps, and different `_dlt_load_id` and `_dlt_id` values with each run.
