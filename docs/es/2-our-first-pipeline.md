# Un ejemplo simple usando `duckdb`

En su forma más básica, `dlt` toma un iterable que produce diccionarios. Tratará cada diccionario como una unidad de datos y lo moverá a un `destino`.

Toma por ejemplo el siguiente diccionario:

```python linenums="1"
--8<-- "dlt_tutorial/0_sample_pipeline_basic.py:my_data"
```

Aquí hay un ejemplo simple que usa `dlt` para cargar datos en una base de datos `duckdb`.

```python linenums="1"
--8<-- "dlt_tutorial/0_sample_pipeline_basic.py:pipeline"
```

!!! tip "dlt no se preocupa por cómo produces los datos"

    La fuente de datos puede ser cualquier cosa que produzca diccionarios. Por ejemplo, puedes usar `pandas`, ej. `[row.to_dict() for _, row in df.iterrows()]`.

## ¿Qué está pasando aquí?

1. Definimos una lista de diccionarios llamada `my_data`. Cada diccionario representa un registro con campos como `id`, `name`, `age` y `address`.
2. Creamos un pipeline de `dlt` usando `dlt.pipeline()`, especificando el nombre del pipeline y el destino como `duckdb`.
3. Usamos `pipeline.run(my_data)` para cargar los datos de `my_data` en la base de datos `duckdb`. El parámetro `write_disposition` está configurado como `replace`, lo que significa que si la tabla de destino ya existe, será reemplazada con los nuevos datos. Esto es útil en este ejemplo para asegurar que comenzamos con una pizarra limpia cada vez que ejecutamos el script.

## Ejecutando el ejemplo

Ejecuta el script directamente usando Python:

```bash
$ python dlt_tutorial/0_sample_pipeline_basic.py
Running pipeline...
Done
```

!!! warning "Limitaciones de DuckDB en concurrencia"

    Ten en cuenta que duckdb no permite acceso concurrente. **Si intentas ejecutar el pipeline mientras tienes un cliente ya conectado a la base de datos, el pipeline fallará.**

Esto creará un archivo de base de datos `duckdb` en el directorio actual (por defecto llamado `sample_pipeline.duckdb`) y cargará los datos en él. Luego puedes consultar la base de datos usando cualquier cliente o librería de `duckdb`.

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

## ¿Qué está haciendo `dlt` internamente?

¡Felicitaciones! Has cargado exitosamente datos en una base de datos `duckdb` usando `dlt`. Hay algunas cosas que están sucediendo internamente que vale la pena mencionar:

1. Creó una `tabla` llamada `sample_data.samples`. En esta tabla, cada fila tiene un `_dlt_load_id` y un `_dlt_id`. Estas son referencias a mecanismos internos de `dlt` para rastrear cargas e identificar registros.

2. `dlt` también crea tres tablas más que persisten el estado del pipeline
    1. `_dlt_loads`
    2. `_dlt_pipeline_state`
    3. `_dlt_version`

3. Sin que lo sepas, `dlt` también creó un directorio en `~/.dlt/pipelines/sample_pipeline`

## Resumiendo

Vimos un ejemplo simple de usar `dlt` para cargar datos en una base de datos `duckdb`.

Subiremos el nivel en la siguiente parte usando `resources` y `sources` para estructurar mejor nuestra extracción de datos.

## Ejemplo completo

```python linenums="1"
--8<-- "dlt_tutorial/0_sample_pipeline_basic.py"
```
