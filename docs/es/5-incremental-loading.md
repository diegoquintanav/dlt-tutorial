# Probando carga incremental

## Una pequeña desviación: habilitando refrescado completo a través de argumentos de línea de comandos

Exploraremos estrategias de carga incremental en las siguientes secciones, pero primero, vamos a necesitar una manera fácil de decirle a dlt cómo manejar refrescados completos para que podamos comenzar rápidamente desde cero, si algo sale mal.

La estrategia de [Refresh](https://dlthub.com/docs/api_reference/dlt/pipeline/configuration#refresh) le dice a dlt si debe eliminar datos existentes en el destino antes de cargar nuevos datos. Las estrategias disponibles son, [según la documentación](https://dlthub.com/docs/api_reference/dlt/pipeline#run):

- `drop_sources` - Eliminar tablas y estado de fuente y recurso para todas las fuentes actualmente siendo procesadas en métodos run o extract del pipeline. (Nota: la historia del esquema es borrada)
- `drop_resources`- Eliminar tablas y estado de recurso para todos los recursos siendo procesados. El estado a nivel de fuente no es modificado. (Nota: la historia del esquema es borrada)
- `drop_data` - Limpiar todos los datos y estado de recurso para todos los recursos siendo procesados. El esquema no es modificado.

```python linenums="1" hl_lines="11"
--8<-- "dlt_tutorial/3_sample_pipeline_postgres_config.py:pipeline"
```

Para habilitar esta opción podemos modificar nuestro script de pipeline para incluir el parámetro `refresh` cuando creamos el pipeline.

```python linenums="1" hl_lines="1-8 12-13 28"
--8<-- "dlt_tutorial/4_sample_pipeline_append.py:parse_args"
```

De esta manera, cuando ejecutemos nuestro pipeline con la bandera `--refresh`, eliminará datos existentes en el destino antes de cargar nuevos datos.

También implementamos el parámetro para simular cargar nuevos datos en las siguientes secciones. Modificamos nuestro `resource` basado en esta bandera.

```python linenums="1" hl_lines="2 27"
--8<-- "dlt_tutorial/4_sample_pipeline_append.py:new_data"
```

Nuestra nueva interfaz de línea de comandos se ve así:

```bash
$ python dlt_tutorial/4_sample_pipeline_append.py --help
usage: 4_sample_pipeline_append.py [-h] [--refresh]

Sample DLT Pipeline with Append

options:
  -h, --help  show this help message and exit
  --refresh   Refresh the data in the destination (if applicable)
```

y acepta un parámetro a través del cual podemos simular cargar nuevos datos:

```bash
USE_NEW_DATA=1 python dlt_tutorial/4_sample_pipeline_append.py
```

## Solo agregar

Ahora puedes ejecutar el pipeline con la bandera `--refresh` para comenzar desde cero:

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

y ejecutarlo otra vez sin la bandera `--refresh` para agregar nuevos datos:

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

Puedes verificar el contenido de la tabla `sample_data` en Postgres para ver los resultados:

```sql
SELECT * FROM sample_data.samples;
```

??? question "¿Qué pasa si ejecutamos el pipeline múltiples veces sin la bandera `--refresh`?"

    Cada vez que ejecutemos el pipeline, nuevos datos serán agregados a los datos existentes en el destino. Esto es porque estamos usando la estrategia de carga por defecto `append`, que agrega nuevos registros a la tabla existente sin modificar o eliminar registros existentes.

    ```
     id |   name    |                 uuid                 |       created_at       |       updated_at       |     metadata__ingested_at     |    metadata__script_name    |    _dlt_load_id    |    _dlt_id     
    ----+-----------+--------------------------------------+------------------------+------------------------+-------------------------------+-----------------------------+--------------------+----------------
      1 | Mr. Mario | a6d7b6dd-bcdb-422e-83eb-f53b2eb4f2cc | 2025-10-09 14:40:00+00 | 2025-10-09 14:50:00+00 | 2025-11-02 18:30:16.036039+00 | 4_sample_pipeline_append.py | 1762119016.0306315 | pJA1hF4HneOUbw
      2 | Mr. Luigi | 8c804ede-f8ae-409e-964d-9e355a3094e0 | 2025-10-08 16:15:00+00 | 2025-10-08 16:50:00+00 | 2025-11-02 18:30:16.036077+00 | 4_sample_pipeline_append.py | 1762119016.0306315 | UxcgfhkMgMleKg
      1 | Mr. Mario | a6d7b6dd-bcdb-422e-83eb-f53b2eb4f2cc | 2025-10-09 14:40:00+00 | 2025-10-09 14:50:00+00 | 2025-11-02 18:30:20.517005+00 | 4_sample_pipeline_append.py | 1762119020.5093243 | HMDNsEtH+RBPXQ
      2 | Mr. Luigi | 8c804ede-f8ae-409e-964d-9e355a3094e0 | 2025-10-08 16:15:00+00 | 2025-10-08 16:50:00+00 | 2025-11-02 18:30:20.517057+00 | 4_sample_pipeline_append.py | 1762119020.5093243 | SbekuWD7fosP1Q
    (4 rows)

    ```

### Agregar con clave primaria incremental

En nuestro ejemplo anterior, pudimos agregar nuevos datos al destino, pero no teníamos una manera de identificar únicamente cada registro. Esto puede llevar a registros duplicados si los mismos datos son cargados múltiples veces. Una alternativa es usar una clave primaria incremental para identificar únicamente cada registro.

Esto puede hacerse en dos pasos:

1. Modificar el decorador del recurso para especificar la columna `id` como clave primaria.

    ```python linenums="1" hl_lines="1"
    --8<-- "dlt_tutorial/4b_sample_pipeline_append_pk.py:resource_decorator"
    ```

2. Aplicar pistas al recurso para especificar que la columna `id` debe ser tratada como una clave primaria incremental. `dlt` permite esto usando el método `apply_hints` en el recurso.

    ```python linenums="1" hl_lines="2-5 7"
    --8<-- "dlt_tutorial/4b_sample_pipeline_append_pk.py:apply_hints"
    ```

!!! tip "Ver más sobre [pistas de esquema en la documentación](https://dlthub.com/docs/general-usage/resource#define-schema)."

!!! warning "la pista incremental solo filtra de datos entrantes"

    `dlt.sources.incremental` es recomendado cuando quieres reducir la cantidad de datos extraídos de tu fuente seleccionando solo datos nuevos o actualizados desde tu última extracción de datos.

Ahora puedes ejecutar el pipeline modificado con la bandera `--refresh` para comenzar desde cero:

```bash
$ python dlt_tutorial/4b_sample_pipeline_append_pk.py --refresh
# salida omitida por brevedad
```

y ejecutarlo otra vez **sin** la bandera `--refresh` para agregar nuevos datos:

```bash linenums="1" hl_lines="3"
$ python dlt_tutorial/4b_sample_pipeline_append_pk.py
# salida omitida por brevedad
0 load package(s) were loaded to destination postgres and into dataset None
The postgres destination used postgresql://postgres:***@localhost:5555/postgres location to store data
Done
```

Verás que no se agregaron nuevos registros a la tabla `sample_data`. Puedes verificar el contenido de la tabla `sample_data` en Postgres para ver los resultados:

```sql
SELECT * FROM sample_data.samples;
```

??? question "¿Qué pasa si ejecutamos el pipeline múltiples veces sin la bandera `--refresh`?"

    Cada vez que ejecutemos el pipeline, nuevos datos serán agregados a los datos existentes en el destino. Sin embargo, dado que hemos especificado la columna `id` como clave primaria, `dlt` asegurará que no haya registros duplicados basados en esta clave. Si un registro con el mismo `id` ya existe en el destino, los datos entrantes con el mismo `id` serán descartados.

Intenta ejecutar el pipeline ahora pasando la variable de entorno `USE_NEW_DATA=1` para simular cargar nuevos datos:

```bash
$ USE_NEW_DATA=1 python dlt_tutorial/4b_sample_pipeline_append_pk.py
# salida omitida por brevedad
```

??? question "¿Cuál es el resultado de ejecutar el pipeline con `USE_NEW_DATA=1`?"

    Cuando ejecutas el pipeline con `USE_NEW_DATA=1`, la función del recurso genera un nuevo conjunto de datos que incluye registros con valores `id` que ya existen en el destino. Sin embargo, dado que hemos especificado la columna `id` como clave primaria y aplicado la pista incremental, `dlt` descartará cualquier registro entrante que tenga un `id` que ya existe en el destino. Como resultado, solo nuevos registros con valores `id` únicos serán agregados al destino.

    ```txt
     id |   name    |                 uuid                 |       created_at       |       updated_at       |     metadata__ingested_at     |      metadata__script_name      |    _dlt_load_id    |    _dlt_id     
    ----+-----------+--------------------------------------+------------------------+------------------------+-------------------------------+---------------------------------+--------------------+----------------
      1 | Mr. Mario | a6d7b6dd-bcdb-422e-83eb-f53b2eb4f2cc | 2025-10-09 14:40:00+00 | 2025-10-09 14:50:00+00 | 2025-11-02 15:23:52.179837+00 | 4b_sample_pipeline_append_pk.py | 1762107832.1758425 | 5kO1pi9oN0z/vQ
      2 | Mr. Luigi | 8c804ede-f8ae-409e-964d-9e355a3094e0 | 2025-10-08 16:15:00+00 | 2025-10-08 16:50:00+00 | 2025-11-02 15:23:52.179866+00 | 4b_sample_pipeline_append_pk.py | 1762107832.1758425 | BpMmoBJH+6WA/A
      3 | Ms. Peach | 1a73f32f-9144-4318-9a00-4437bde41627 | 2025-10-12 13:15:00+00 | 2025-10-13 13:50:00+00 | 2025-11-02 15:24:00.04396+00  | 4b_sample_pipeline_append_pk.py | 1762107840.0396352 | 4ZUmjQ7Pt9N/uQ
    (3 rows)
    ```

## Estrategias de fusión

`dlt` también soporta estrategias de `merge`, que te permiten actualizar registros existentes en el destino basándose en una clave especificada.

La disposición de escritura merge puede ser usada con tres estrategias diferentes:

  1. `delete-insert`: La estrategia delete-insert carga datos a un conjunto de datos de staging, deduplica los datos de staging si se proporciona una primary_key, elimina los datos del destino usando merge_key y primary_key, y luego inserta los nuevos registros.
  1. `upsert`: actualizar registro si la clave existe en la tabla objetivo, o insertar registro si la clave no existe en la tabla objetivo
  1. `scd2`: Estrategia Slowly Changing Dimensions tipo 2, que rastrea cambios históricos en datos creando nuevos registros para cada cambio mientras preserva registros anteriores. Agregará una nueva columna para rastrear el período de validez de cada registro.

Para implementar estas estrategias, necesitamos modificar el parámetro `write_disposition` cuando creamos el pipeline.

### Upsert

Podemos eliminar el método `apply_hints` ya que no estamos usando una clave primaria incremental en este ejemplo.

Si queremos usar la estrategia `upsert`, podemos ejecutar el pipeline modificado con la bandera `--refresh` para comenzar desde cero:

```linenums="1" hl_lines="4"
--8<-- "dlt_tutorial/5_sample_pipeline_merge_upsert.py:resource_decorator"
```

```bash
$ python dlt_tutorial/5_sample_pipeline_merge_upsert.py --refresh
# salida omitida por brevedad
```

y ejecutarlo otra vez sin la bandera `--refresh` para hacer upsert de nuevos datos:

```bash
$ python dlt_tutorial/5_sample_pipeline_merge_upsert.py
# salida omitida por brevedad
```

Deberías ver que no se agregaron registros a la tabla `sample_data`. Puedes verificar el contenido de la tabla `sample_data` en Postgres para ver los resultados:

```sql
SELECT * FROM sample_data;

```

Intenta ahora ejecutar el pipeline pasando la variable de entorno `USE_NEW_DATA=1` para simular cargar nuevos datos:

```bash
$ USE_NEW_DATA=1 python dlt_tutorial/5_sample_pipeline_merge_upsert.py
# salida omitida por brevedad
```

??? question "¿Cuál es el resultado de ejecutar el pipeline con `USE_NEW_DATA=1`?"

    Cuando ejecutas el pipeline con `USE_NEW_DATA=1`, la función del recurso genera un nuevo conjunto de datos que incluye registros con valores `id` que ya existen en el destino. Dado que estamos usando la estrategia `upsert`, `dlt` actualizará registros existentes en el destino si un registro con el mismo `id` ya existe, o insertará nuevos registros si el `id` no existe.

    ```txt
    postgres=# select * from sample_data.samples;
     id |   name    |                 uuid                 |       created_at       |       updated_at       |     metadata__ingested_at     |       metadata__script_name       |    _dlt_load_id    |_dlt_id
    ----+-----------+--------------------------------------+------------------------+------------------------+-------------------------------+-----------------------------------+--------------------+----------------
      2 | Mr. Luigi | 8c804ede-f8ae-409e-964d-9e355a3094e0 | 2025-10-08 16:15:00+00 | 2025-10-08 16:50:00+00 | 2025-11-02 18:37:17.901958+00 | 5_sample_pipeline_merge_upsert.py | 1762119437.8970616 | M6/KlLzJ2FeV/w
      1 | Jumpman   | a6d7b6dd-bcdb-422e-83eb-f53b2eb4f2cc | 2025-10-09 14:40:00+00 | 2025-10-10 11:50:00+00 | 2025-11-02 18:37:23.170644+00 | 5_sample_pipeline_merge_upsert.py | 1762119443.1653655 | z5jIxXIbUnmbKw
      3 | Ms. Peach | 1a73f32f-9144-4318-9a00-4437bde41627 | 2025-10-12 13:15:00+00 | 2025-10-13 13:50:00+00 | 2025-11-02 18:37:23.170657+00 | 5_sample_pipeline_merge_upsert.py | 1762119443.1653655 | hKdQ/VhGat+Pgw
    (3 rows)
    ```

### Slowly Changing Dimensions (SCD2)

De la misma manera, podemos implementar la estrategia `scd2` modificando el parámetro `write_disposition` cuando creamos el pipeline.

Dado una **coincidencia** entre filas entrantes y existentes en alguna **clave**, dejar la fila objetivo existente e "**INSERT**" un nuevo registro de los datos entrantes, usando algunas columnas auxiliares.

Esto permite rastrear la validez del último valor, pero toma más espacio en disco.

```python linenums="1" hl_lines="4"
--8<-- "dlt_tutorial/6_sample_pipeline_merge_scd2.py:resource_decorator"
```

En la práctica, `dlt` calculará una clave sustituta para cada registro basada en la clave primaria y el hash del contenido del registro.

Cuando se encuentra un registro con la misma clave primaria pero contenido diferente, se inserta un nuevo registro con una nueva clave sustituta, mientras que el registro existente se marca como expirado.

Puedes ejecutar el pipeline modificado con la bandera `--refresh` para comenzar desde cero:

```bash
$ python dlt_tutorial/6_sample_pipeline_merge_scd2.py --refresh
# salida omitida por brevedad
```

y ejecutarlo otra vez sin la bandera `--refresh` para hacer upsert de nuevos datos:

```bash
$ python dlt_tutorial/6_sample_pipeline_merge_scd2.py
# salida omitida por brevedad  
```

Dado que nuestros datos tienen una columna de metadatos llamada `metadata__ingested_at` que está basada en la marca de tiempo de ejecución, `dlt` calculará una clave sustituta diferente cada vez que se inserte un registro.

Esto efectivamente insertará nuevas filas cada vez que ejecutemos el pipeline, y marcará las filas anteriores como expiradas.

```psql
postgres=# select * from sample_data.samples;
        _dlt_valid_from        |        _dlt_valid_to         | id |   name    |                 uuid                 |       created_at       |       updated_at       |     metadata__ingested_at     |      metadata__script_name      |    _dlt_load_id    |    _dlt_id     
-------------------------------+------------------------------+----+-----------+--------------------------------------+------------------------+------------------------+-------------------------------+---------------------------------+--------------------+----------------
 2025-11-02 21:43:43.942528+00 | 2025-11-02 21:46:07.88226+00 |  1 | Mr. Mario | a6d7b6dd-bcdb-422e-83eb-f53b2eb4f2cc | 2025-10-09 14:40:00+00 | 2025-10-09 14:50:00+00 | 2025-11-02 18:43:43.948416+00 | 6_sample_pipeline_merge_scd2.py | 1762119823.9425282 | 2PDbMZWckGbEzQ
 2025-11-02 21:43:43.942528+00 | 2025-11-02 21:46:07.88226+00 |  2 | Mr. Luigi | 8c804ede-f8ae-409e-964d-9e355a3094e0 | 2025-10-08 16:15:00+00 | 2025-10-08 16:50:00+00 | 2025-11-02 18:43:43.94847+00  | 6_sample_pipeline_merge_scd2.py | 1762119823.9425282 | zFQAhPCh1tzs2A
 2025-11-02 21:46:07.88226+00  |                              |  1 | Mr. Mario | a6d7b6dd-bcdb-422e-83eb-f53b2eb4f2cc | 2025-10-09 14:40:00+00 | 2025-10-09 14:50:00+00 | 2025-11-02 18:46:07.887446+00 | 6_sample_pipeline_merge_scd2.py | 1762119967.8822596 | I6WPZYVDBhg9zQ
 2025-11-02 21:46:07.88226+00  |                              |  2 | Mr. Luigi | 8c804ede-f8ae-409e-964d-9e355a3094e0 | 2025-10-08 16:15:00+00 | 2025-10-08 16:50:00+00 | 2025-11-02 18:46:07.887478+00 | 6_sample_pipeline_merge_scd2.py | 1762119967.8822596 | CrpVG8J0ezqiQg
(4 rows)
```

??? question "¿Cómo sabemos cuál es el valor más reciente cuando usamos SCD2?"

    Cuando usas la estrategia SCD2, cada registro tiene dos columnas adicionales: `_dlt_valid_from` y `_dlt_valid_to`. La columna `_dlt_valid_from` indica la marca de tiempo cuando el registro se volvió válido, mientras que la columna `_dlt_valid_to` indica la marca de tiempo cuando el registro fue reemplazado por una versión más nueva.

    Para encontrar el valor más reciente para una clave primaria dada, puedes consultar registros donde la columna `_dlt_valid_to` es `NULL`, ya que esto indica que el registro es actualmente válido.

    Por ejemplo, para encontrar los registros más recientes en la tabla `sample_data.samples`, puedes ejecutar la siguiente consulta SQL:

    ```sql
    SELECT * FROM sample_data.samples WHERE _dlt_valid_to IS NULL;
    ```

    Esto devolverá solo los registros que son actualmente válidos, permitiéndote ver los valores más recientes para cada clave primaria.

??? question "¿Qué pasa si ejecutas el pipeline usando la variable de entorno `USE_NEW_DATA=1`?"

    En los nuevos datos verás que `Mr. Luigi` no está presente. Esto significa que cuando ejecutes el pipeline con `USE_NEW_DATA=1`, este registro será marcado como expirado en la tabla de destino (Un _hard delete_), y un nuevo registro para `Jumpman` será insertado.

## Resumiendo

Hemos explorado diferentes estrategias de carga incremental usando `dlt`, incluyendo `append`, `upsert` y `SCD2`. Cada estrategia tiene sus propios casos de uso y beneficios, dependiendo de los requisitos de tu pipeline de datos.

`dlt` ofrece más estrategias y opciones para carga incremental. Refiere a la [documentación de dlt](https://dlthub.com/docs/general-usage/incremental-loading) para más información sobre cómo implementar estas estrategias en tus pipelines de datos.
