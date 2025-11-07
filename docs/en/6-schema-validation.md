# Schema validation and Data Contracts

[Verbatim from the docs](https://dlthub.com/docs/general-usage/schema)

> - The schema describes the structure of normalized data (e.g., tables, columns, data types, etc.) and provides instructions on how the data should be processed and loaded.
> - dlt generates schemas from the data during the normalization process. Users can affect this standard behavior by providing **hints** that change how tables, columns, and other metadata are generated and how the data is loaded.
> - Such hints can be passed in the code, i.e., to the `dlt.resource` decorator or `pipeline.run` method. Schemas can also be exported and imported as files, which can be directly modified.
> - `dlt` associates a schema with a [source](https://dlthub.com/docs/general-usage/source) and a table schema with a [resource](https://dlthub.com/docs/general-usage/resource).

In short, `dlt` will **infer** the schema but we can force it to explicit types

1. Using  a `dict` specification
2. Using a `Pydantic` model
3. Using `hints`

## Schema definitions

!!! warning "Examples use the `replace` write disposition"

    The examples in this section use the `replace` write disposition for simplicity. In a production scenario, you may want to use `append` or `merge` to preserve existing data.

Given our previous example, we can define the schema for the `sample_data` resource using a `dict` specification:

```python linenums="1"
--8<-- "dlt_tutorial/7_sample_pipeline_schema.py:my_data"
```

Using `dlt` we can define the schema as follows:

```python linenums="1" hl_lines="11"
--8<-- "dlt_tutorial/7_sample_pipeline_schema.py:resource_decorator"
```

For now, ignore the `schema_contract` argument, as we will explain it later.

For nested fields it gets a bit more complex. We can use the `nested_columns` argument to define the schema for nested fields:

```python linenums="1" hl_lines="12-25"
--8<-- "dlt_tutorial/7_sample_pipeline_schema.py:resource_decorator"
```

### Using Pydantic models

Alternatively, we can use `Pydantic` models to define the schema:

```python linenums="1"
--8<-- "dlt_tutorial/8_sample_pipeline_schema_with_pydantic.py:pydantic_models"
```

And replace the `columns` argument in the `dlt.resource` decorator with the `Pydantic` model:

```python linenums="1" hl_lines="11"
--8<-- "dlt_tutorial/8_sample_pipeline_schema_with_pydantic.py:resource_decorator"
```

## Data contracts

Previously we mentioned the `schema_contract` argument in the `dlt.resource` decorator. This allows us to define a **data contract** that specifies how `dlt` should handle schema changes during data loading.

`dlt` will handle changes in tables, columns and data types by default. You can set its behaviour explicitly by passing values to the `schema_contract` argument of the `dlt.resource` decorator, such as:

```python
@dlt.resource(
 schema_contract={
        "tables": "evolve",
        "columns": "freeze",
        "data_type": "freeze",
    })
def my_resource():
  ...
```

You can control the following **schema entities**:

- `tables` - the contract is applied when a new table is created
- `columns` - the contract is applied when a new column is created on an existing table
- `data_type` - the contract is applied when data cannot be coerced into a data type associated with an existing column.

You can use **contract modes** to tell `dlt` how to apply the contract for a particular entity:

- `evolve`: No constraints on schema changes.
- `freeze`: This will raise an exception if data is encountered that does not fit the existing schema, so no data will be loaded to the destination.
- `discard_row`: This will discard any extracted row if it does not adhere to the existing schema, and this row will not be loaded to the destination.
- `discard_value`: This will discard data in an extracted row that does not adhere to the existing schema, and the row will be loaded without this data.

!!! info "How does "evolve" work?"

    The default mode (**evolve**) works as follows:

    1. New tables may always be created.
    2. New columns may always be appended to the existing table.
    3. Data that do not coerce to the existing data type of a particular column will be sent to a [variant column](https://dlthub.com/docs/general-usage/schema#variant-columns) created for this particular type.

## Testing contract enforcement

Consider the first schema definition using a `dict` specification, where we defined that neither columns nor data types should change:

```python linenums="1" hl_lines="26-30"
--8<-- "dlt_tutorial/7_sample_pipeline_schema.py:resource_decorator"
```

```python linenums="1" hl_lines="6-10"
--8<-- "dlt_tutorial/8_sample_pipeline_schema_with_pydantic.py:resource_decorator"
```

??? question "What happens if we set the `id=1` to `id='oops, this is a string now'` instead?"

    You should get an error like this:

    ```bash
    <class 'dlt.normalize.exceptions.NormalizeJobFailed'>
    Job for `job_id=samples.e278217ef2.typed-jsonl.gz` failed terminally in load with `load_id=1762124329.823492` with message: In schema `sample_pipeline_postgres`: In Table: `samples` Column: `id__v_text` . Contract on `data_type` with `contract_mode=freeze` is violated. Can't add variant column `id__v_text` for table `samples` because `data_types` are frozen. Offending data item: id: None.
    ```

    If we try the same with the Pydantic model schema definition, we will get a similar error:

!!! tip "Check the documentation for more details"

    See <https://dlthub.com/docs/general-usage/schema-contracts> for more information on data contracts and schema validation.
