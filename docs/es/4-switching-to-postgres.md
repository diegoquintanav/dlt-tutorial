# Parte 2: Implementando carga incremental de datos

## Introducción a la carga incremental

Considera el siguiente estado de tu tabla en un momento dado:

| id |   name    |       created_at       |       updated_at       |
|---:|-----------|------------------------|------------------------|
| 1  | Mr. Mario | 2025-10-09 14:40:00    | 2025-10-09 14:50:00    |
| 2  | Mr. Luigi | 2025-10-08 16:15:00    | 2025-10-08 16:50:00    |

En esta tabla, podemos identificar dos registros, que pueden ser identificados únicamente por sus campos `id` o `uuid`. Cada registro también tiene marcas de tiempo `created_at` y `updated_at`.

Ahora, imagina que ha pasado algo de tiempo, y tenemos nuevos datos para cargar en nuestra tabla. Obtenemos nuestros datos de una API remota que sirve actualizaciones incrementales sobre información de Mario y Luigi.

Los nuevos datos **entrantes** se ven así:

| id |   name    |       created_at       |       updated_at       |
|---:|-----------|------------------------|------------------------|
| 1  | Jumpman   | 2025-10-09 14:40:00    | 2025-10-10 11:50:00    |
| 3  | Ms. Peach | 2025-10-12 13:15:00    | 2025-10-13 13:50:00    |

Mario ahora es [conocido](https://www.reddit.com/r/Marioverse/comments/1ef7f4f/jan_misalis_breakdown_of_the_jumpman_is_not_mario/) como ["Jumpman"](https://www.mariowiki.com/List_of_Mario_names_in_other_languages#Jumpman), fue actualizado después de su última actualización, y un nuevo registro para "Ms. Peach" ha sido agregado.

¿Cuál debería ser el estado final de nuestra tabla después de cargar estos nuevos datos? _Depende de la lógica que queramos implementar para manejar actualizaciones e inserciones._

Aunque hay muchas estrategias, aquí hay algunas comunes:

### Reemplazar todo

Ignorar el estado existente y reemplazar todo: En este caso, simplemente reemplazaríamos toda la tabla con los datos entrantes.

| id |   name    |       created_at       |       updated_at       |
|---:|-----------|------------------------|------------------------|
| 1  | Jumpman   | 2025-10-09 11:40:00-03 | 2025-10-10 11:50:00-03 |
| 3  | Ms. Peach | 2025-10-10 13:25:00-03 | 2025-10-10 13:50:00-03 |

### Agregar nuevos datos

Simplemente agregar los datos entrantes a la tabla existente:

| id |   name    |       created_at       |       updated_at       |
|---:|-----------|------------------------|------------------------|
| 1  | Mr. Mario | 2025-10-09 11:40:00-03 | 2025-10-09 11:50:00-03 |
| 2  | Mr. Luigi | 2025-10-08 13:15:00-03 | 2025-10-08 13:50:00-03 |
| 1  | Jumpman   | 2025-10-09 11:40:00-03 | 2025-10-10 11:50:00-03 |
| 3  | Ms. Peach | 2025-10-10 13:25:00-03 | 2025-10-10 13:50:00-03 |

### Fusionar nuevos registros en los existentes

Podemos actualizar registros existentes o agregar nuevos. Para esto, necesitamos depender de algún identificador como el `id`, que _identifique únicamente_ un registro:

Si consideramos el `id` como tal registro, actualizaríamos el registro de Mario con el nuevo nombre y marca de tiempo actualizada, e insertaríamos el nuevo registro para "Ms. Peach".

| id |   name    |       created_at       |       updated_at       |
|---:|-----------|------------------------|------------------------|
| 1  | Jumpman   | 2025-10-09 11:40:00-03 | 2025-10-10 11:50:00-03 |
| 2  | Mr. Luigi | 2025-10-08 13:15:00-03 | 2025-10-08 13:50:00-03 |
| 3  | Ms. Peach | 2025-10-10 13:25:00-03 | 2025-10-10 13:50:00-03 |

La estrategia de fusión es la más común cuando se trata de carga incremental de datos. Nos permite mantener nuestros datos actualizados mientras minimizamos la cantidad de datos que necesitamos procesar.

## Un ejemplo con Postgres

Un buen ejemplo de una base de datos que soporta carga incremental es Postgres. Postgres proporciona varios mecanismos para manejar actualizaciones e inserciones, como `UPSERT` (usando `ON CONFLICT`), o `MERGE` en versiones más recientes, que nos permite insertar nuevos registros o actualizar los existentes basados en una restricción única.

Según su documentación, [`MERGE`](https://www.postgresql.org/docs/current/sql-merge.html#notes) implementa una operación de unión usando una `join_condition`.

```sql
[ WITH with_query [, ...] ]
MERGE INTO [ ONLY ] target_table_name [ * ] [ [ AS ] target_alias ]
    USING data_source ON join_condition
    when_clause [...]
    [ RETURNING [ WITH ( { OLD | NEW } AS output_alias [, ...] ) ]
                { * | output_expression [ [ AS ] output_name ] } [, ...] ]
```

En el siguiente ejemplo, `MERGE` requiere una tabla `target` (la tabla que queremos actualizar) y una tabla `source` (los nuevos datos que queremos insertar o usar para actualizar el objetivo).

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

En este ejemplo, estamos fusionando datos de `source_table` en `target_table` basándose en la columna `id`. Si se encuentra un registro coincidente, actualizamos la columna `name`; si no, insertamos un nuevo registro.

## Implementando carga incremental con `dlt`

¿Cómo sabemos qué escenario necesitamos implementar? Depende. `dlt` resume cada caso de uso con el siguiente diagrama:

![alt text](assets/img/incremental-decision-tree.png)

Podemos cargar datos de diferentes maneras, dependiendo de los requisitos. Ver la [documentación para una introducción completa](https://dlthub.com/docs/general-usage/incremental-loading)

Podemos definir la **disposición de escritura** y la **estrategia de escritura** cuando **ejecutamos un pipeline**. Podemos elegir entre `"replace"`, `"append"`, `"merge"`

1. `"replace"`: Reemplaza la tabla completamente
2. `"append"`: Carga filas incrementalmente, independientemente de sus valores
3. `"merge"`: Inserta solo filas que son relevantes para la actualización, ej. que _coinciden_ con datos en el objetivo según alguna **estrategia** y alguna **clave** que permite identificar filas coincidentes. Para la disposición "merge"

    1. `"delete-insert"`: dado una **coincidencia** entre filas entrantes y existentes en alguna **clave**, **DELETE** la fila objetivo e **INSERT** desde las entrantes. Esta operación es **bloqueante** o puede no ser soportada, dependiendo de la base de datos objetivo.
    2. `"upsert"`: dado una **coincidencia** entre filas entrantes y existentes en alguna **clave**, **UPDATE** la fila objetivo e "**INSERT**" lo que ha cambiado de los datos entrantes. Esta operación no es **bloqueante** pero puede no ser soportada, dependiendo de la base de datos objetivo.
    3. `"scd2"`: dado una **coincidencia** entre filas entrantes y existentes en alguna **clave**, dejar la fila objetivo existente e "**INSERT**" una nueva de los datos entrantes. Usando algunas columnas adicionales, esto permite rastrear la validez del último valor, pero toma más espacio en disco.

## Configurando una base de datos Postgres

Refiere a la sección [Primeros Pasos](1-getting-started.md) para aprender cómo configurar una base de datos postgres. Una vez que tengas una instancia postgres válida, necesitas configurar sus credenciales postgres.

!!! info "Algunos patrones de carga incremental no son soportados por `duckdb`"

    Duckdb es una base de datos analítica, en memoria. Brilla para algunos tipos de tareas, y ofrece su propia implementación de `MERGE`. Sin embargo, los patrones de carga incremental no son completamente soportados por `dlt` en este momento.

## Configurar `dlt` para usar Postgres

Necesitarás decirle a `dlt` cómo conectarse a tu base de datos Postgres. La forma recomendada es crear un archivo `secrets.toml` en la raíz de este proyecto con el siguiente contenido:

```toml
[sample_pipeline_postgres.destination.postgres.credentials]
host = "localhost"
port = 5555
user = "postgres"
password = "test"
dbname = "postgres"
```

Si deseas usar el método de cadena de conexión, por ejemplo cuando uses una base de datos neon, también puedes hacerlo así:

```toml
sample_pipeline_postgres.destination.postgres.credentials = 'postgresql://neondb_owner:<password>@<host>/neondb?sslmode=require&channel_binding=require'
```

!!! warning "No hagas commit de tu archivo secrets.toml"

    Asegúrate de agregar `secrets.toml` a tu archivo `.gitignore` para evitar hacer commit de información sensible al control de versiones.

!!! warning "Ajusta los parámetros de conexión según sea necesario"

    Ajusta los parámetros de conexión (`host`, `port`, `user`, `password`, `dbname`) según tu configuración de Postgres. Si estás usando el devcontainer, el host debería ser `postgres` y el puerto `5432`.

!!! tip "Configura parámetros de conexión usando variables de entorno"

    También puedes configurar los parámetros de conexión usando variables de entorno. Ver la [documentación](https://dlthub.com/docs/general-usage/credentials/setup#postgresql) para más información.

## Reemplazar todo usando postgres

Ahora puedes ejecutar el script `3_sample_pipeline_postgres_config.py` para probar la conexión y configuración de Postgres.

Las únicas cosas que han cambiado de los ejemplos anteriores son los parámetros `write_disposition` y `write_strategy` cuando se ejecuta el pipeline:

```python linenums="1" hl_lines="3-5"
--8<-- "dlt_tutorial/3_sample_pipeline_postgres_config.py:resource"
```

Si ejecutamos este ejemplo, deberíamos ver salida similar a esta:

```bash
$ python dlt_tutorial/3_sample_pipeline_postgres_config.py
Starting pipeline...
Pipeline run completed.
Pipeline sample_pipeline_postgres load step completed in 0.11 seconds
1 load package(s) were loaded to destination postgres and into dataset sample_data
The postgres destination used postgresql://postgres:***@localhost:5555/postgres location to store data
Load package 1762003276.163356 is LOADED and contains no failed jobs
```

Ahora podemos conectarnos a nuestra base de datos Postgres y verificar el contenido de la tabla `sample_data.samples`:

```bash
$PGPASSWORD=test psql -h 0.0.0.0 -p 5555 -U postgres --pset expanded=auto -c "select * from sample_data.samples;"
 id |   name    |                 uuid                 |       created_at       |       updated_at       |     metadata__ingested_at     |        metadata__script_name         |   _dlt_load_id    |    _dlt_id     
----+-----------+--------------------------------------+------------------------+------------------------+-------------------------------+--------------------------------------+-------------------+----------------
  1 | Mr. Mario | a6d7b6dd-bcdb-422e-83eb-f53b2eb4f2cc | 2025-10-09 14:40:00+00 | 2025-10-09 14:50:00+00 | 2025-11-01 10:21:16.172598+00 | 3_sample_pipeline_postgres_config.py | 1762003276.163356 | MJaJ6AzyVleWlQ
  2 | Mr. Luigi | 8c804ede-f8ae-409e-964d-9e355a3094e0 | 2025-10-08 16:15:00+00 | 2025-10-08 16:50:00+00 | 2025-11-01 10:21:16.172663+00 | 3_sample_pipeline_postgres_config.py | 1762003276.163356 | IrYyUJd1NAmnBQ
(2 rows)
```

??? question "¿Qué pasa si ejecutamos el script otra vez?"

    Si ejecutas el script otra vez, dado que el `write_disposition` está configurado como `"replace"` y el parámetro `refresh` está configurado como `"drop_sources"`, los datos existentes en la tabla `sample_data.samples` serán reemplazados con los nuevos datos obtenidos de la fuente, cada vez. Deberías ver diferentes marcas de tiempo `metadata__ingested_at`, y diferentes valores `_dlt_load_id` y `_dlt_id` con cada ejecución.
