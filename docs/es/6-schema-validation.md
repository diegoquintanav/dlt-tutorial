# Validación de esquemas y Contratos de datos

[Textualmente de los documentos](https://dlthub.com/docs/general-usage/schema)

> - El esquema describe la estructura de datos normalizados (ej., tablas, columnas, tipos de datos, etc.) y proporciona instrucciones sobre cómo los datos deben ser procesados y cargados.
> - dlt genera esquemas de los datos durante el proceso de normalización. Los usuarios pueden afectar este comportamiento estándar proporcionando **pistas** que cambian cómo las tablas, columnas y otros metadatos son generados y cómo los datos son cargados.
> - Tales pistas pueden ser pasadas en el código, ej., al decorador `dlt.resource` o método `pipeline.run`. Los esquemas también pueden ser exportados e importados como archivos, que pueden ser modificados directamente.
> - `dlt` asocia un esquema con una [fuente](https://dlthub.com/docs/general-usage/source) y un esquema de tabla con un [recurso](https://dlthub.com/docs/general-usage/resource).

En resumen, `dlt` **inferirá** el esquema pero podemos forzarlo a tipos explícitos

1. Usando una especificación `dict`
2. Usando un modelo `Pydantic`
3. Usando `hints`

## Definiciones de esquema

!!! warning "Los ejemplos usan la disposición de escritura `replace`"

    Los ejemplos en esta sección usan la disposición de escritura `replace` por simplicidad. En un escenario de producción, puedes querer usar `append` o `merge` para preservar datos existentes.

Dado nuestro ejemplo anterior, podemos definir el esquema para el recurso `sample_data` usando una especificación `dict`:

```python linenums="1"
--8<-- "dlt_tutorial/7_sample_pipeline_schema.py:my_data"
```

Usando `dlt` podemos definir el esquema de la siguiente manera:

```python linenums="1" hl_lines="11"
--8<-- "dlt_tutorial/7_sample_pipeline_schema.py:resource_decorator"
```

Por ahora, ignora el argumento `schema_contract`, ya que lo explicaremos más tarde.

Para campos anidados se vuelve un poco más complejo. Podemos usar el argumento `nested_columns` para definir el esquema para campos anidados:

```python linenums="1" hl_lines="12-25"
--8<-- "dlt_tutorial/7_sample_pipeline_schema.py:resource_decorator"
```

### Usando modelos Pydantic

Alternativamente, podemos usar modelos `Pydantic` para definir el esquema:

```python linenums="1"
--8<-- "dlt_tutorial/8_sample_pipeline_schema_with_pydantic.py:pydantic_models"
```

Y reemplazar el argumento `columns` en el decorador `dlt.resource` con el modelo `Pydantic`:

```python linenums="1" hl_lines="11"
--8<-- "dlt_tutorial/8_sample_pipeline_schema_with_pydantic.py:resource_decorator"
```

## Contratos de datos

Anteriormente mencionamos el argumento `schema_contract` en el decorador `dlt.resource`. Esto nos permite definir un **contrato de datos** que especifica cómo `dlt` debe manejar cambios de esquema durante la carga de datos.

`dlt` manejará cambios en tablas, columnas y tipos de datos por defecto. Puedes configurar su comportamiento explícitamente pasando valores al argumento `schema_contract` del decorador `dlt.resource`, como:

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

Puedes controlar las siguientes **entidades de esquema**:

- `tables` - el contrato se aplica cuando se crea una nueva tabla
- `columns` - el contrato se aplica cuando se crea una nueva columna en una tabla existente
- `data_type` - el contrato se aplica cuando los datos no pueden ser coercionados a un tipo de datos asociado con una columna existente.

Puedes usar **modos de contrato** para decirle a `dlt` cómo aplicar el contrato para una entidad particular:

- `evolve`: Sin restricciones en cambios de esquema.
- `freeze`: Esto lanzará una excepción si se encuentran datos que no se ajustan al esquema existente, por lo que no se cargarán datos al destino.
- `discard_row`: Esto descartará cualquier fila extraída si no se adhiere al esquema existente, y esta fila no será cargada al destino.
- `discard_value`: Esto descartará datos en una fila extraída que no se adhiere al esquema existente, y la fila será cargada sin estos datos.

!!! info "¿Cómo funciona "evolve"?"

    El modo por defecto (**evolve**) funciona de la siguiente manera:

    1. Nuevas tablas siempre pueden ser creadas.
    2. Nuevas columnas siempre pueden ser agregadas a la tabla existente.
    3. Datos que no se coercionan al tipo de datos existente de una columna particular serán enviados a una [columna variante](https://dlthub.com/docs/general-usage/schema#variant-columns) creada para este tipo particular.

## Probando cumplimiento de contratos

Considera la primera definición de esquema usando una especificación `dict`, donde definimos que ni las columnas ni los tipos de datos deben cambiar:

```python linenums="1" hl_lines="26-30"
--8<-- "dlt_tutorial/7_sample_pipeline_schema.py:resource_decorator"
```

```python linenums="1" hl_lines="6-10"
--8<-- "dlt_tutorial/8_sample_pipeline_schema_with_pydantic.py:resource_decorator"
```

??? question "¿Qué pasa si configuramos `id=1` a `id='oops, esto es un string ahora'` en su lugar?"

    Deberías obtener un error como este:

    ```bash
    <class 'dlt.normalize.exceptions.NormalizeJobFailed'>
    Job for `job_id=samples.e278217ef2.typed-jsonl.gz` failed terminally in load with `load_id=1762124329.823492` with message: In schema `sample_pipeline_postgres`: In Table: `samples` Column: `id__v_text` . Contract on `data_type` with `contract_mode=freeze` is violated. Can't add variant column `id__v_text` for table `samples` because `data_types` are frozen. Offending data item: id: None.
    ```

    Si intentamos lo mismo con la definición de esquema del modelo Pydantic, obtendremos un error similar:

!!! tip "Revisa la documentación para más detalles"

    Ver <https://dlthub.com/docs/general-usage/schema-contracts> para más información sobre contratos de datos y validación de esquemas.
