# Inspeccionar el estado de `dlt`

El [`state`](https://dlthub.com/docs/general-usage/state) es un diccionario creado por dlt en cada ejecución del pipeline. Puede suceder que durante una ejecución del pipeline ocurra un error que detenga la ejecución. Podemos simular un error como

```diff
 def sample_data() -> Generator[dict, None, None]:
+    raise Exception("Debugging state: intentional error raised")
```

## Elementos internos de `dlt`

cada vez que se ejecuta un pipeline, `dlt` creará o actualizará

1. Archivos en `~/.dlt/pipelines/<pipeline_name>/`
2. En la tabla objetivo: cada fila tiene un `_dlt_load_id` y un `_dlt_id`
3. `dlt` crea tres tablas adicionales que mantienen el estado del pipeline ([documentación](https://dlthub.com/docs/general-usage/destination-tables#dlts-internal-tables))
    1. `_dlt_loads`
    2. `_dlt_pipeline_state`
    3. `_dlt_version`

## `_dlt_loads` y `_dlt_load_id`

En cada tabla, `_dlt_load_id` es una referencia a la carga relacionada en la tabla `_dlt_loads`

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

Puedes ver de qué ejecución provienen tus datos

```sql
select loads.* 
from sample_data.samples as target 
left join sample_data._dlt_loads as loads
on target._dlt_load_id = loads.load_id;
```

---

## `_dlt_id`

- Al serializar registros de origen, cada registro produce su propio `_dlt_id`, que es un identificador único para ese registro.
- La columna `_dlt_id` se genera usando la función UUID del destino (utiliza `sqlglot`, ver [código fuente](https://github.com/dlt-hub/dlt/blob/90819a96182e8d146adfd3985a2032376440c79e/dlt/normalize/items_normalizers.py#L128)), como `generateUUIDv4()` en ClickHouse. Para dialectos sin soporte nativo de UUID:
  - En **Redshift**, `_dlt_id` se genera usando un hash `MD5` del load ID y el número de fila.
  - En **SQLite**, `_dlt_id` se simula usando `lower(hex(randomblob(16)))`.

---

## `_dlt_pipeline_state`

Creada por DLT. Rastrea los estados del pipeline, permitiendo que dlt reanude durante cargas incrementales.

---

## `_dlt_version`

Creada por DLT. Rastrea las actualizaciones del esquema en su columna `schema` y `version_hash`

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

Si consultas desde `_dlt_version.schema` obtendrás un JSON que contiene la descripción de cada tabla manejada por `dlt`.

---

## `_dlt_load_id`

Cada fila insertada en la tabla objetivo tiene una columna `_dlt_load_id` y una `_dlt_id`. La primera identifica la ejecución del pipeline, mientras que la segunda identifica la fila en sí.

---

## Inspeccionar los archivos de estado del pipeline

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

## Explorar el estado visualmente

Puedes usar `dlt pipeline <PIPELINE_NAME>` para explorar el estado del pipeline visualmente en tu navegador con una interfaz de `marimo` o `streamlit`.

```bash
dlt pipeline --list # lista los pipelines disponibles
dlt pipeline <YOUR_PIPELINE_NAME> show [--streamlit]
```
