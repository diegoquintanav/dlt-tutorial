# Parte 1: Usando `resources` y `sources` para estructurar la extracción de datos

En la parte anterior, vimos un ejemplo simple de usar `dlt` para cargar datos en una base de datos `duckdb`. Aunque ese ejemplo fue directo, podemos hacerlo mejor.

## Una introducción a iteradores y generadores

Un concepto importante en Python que `dlt` aprovecha es la idea de iteradores y generadores. Estas construcciones permiten un bucle eficiente sobre datos sin la necesidad de cargar todo en memoria de una vez.

- Un **iterador** es un objeto que implementa el protocolo iterador, que consiste en los métodos `__iter__()` y `__next__()`. Un iterador te permite recorrer todos los elementos de una colección, como una lista o un conjunto, uno a la vez.
- Un **generador** es un tipo especial de iterador que se define usando una función y la palabra clave `yield`. Los generadores te permiten producir una secuencia de valores a lo largo del tiempo, en lugar de calcularlos todos a la vez y almacenarlos en memoria.

Aquí hay un ejemplo simple de una función generadora que produce números del 0 al n-1:

```python
def count_up_to(n):
    count = 0
    while count < n:
        yield count
        count += 1
```

Puedes usar este generador así:

```python
for number in count_up_to(5):
    print(number)
```

Esto producirá:

```text
0
1
2
3
4
```

Los generadores son particularmente útiles cuando se trata de grandes conjuntos de datos o flujos de datos, ya que te permiten procesar un elemento a la vez sin cargar todo en memoria.

Sin embargo, los generadores solo pueden ser iterados una vez. Después de que se agotan, no pueden ser reutilizados. Si necesitas iterar sobre los datos múltiples veces, necesitarás crear una nueva instancia del generador cada vez.

```ipython
>>> my_gen_5 = count_up_to(5)

>>> my_gen_5
<generator object count_up_to at 0x71aa29e4bb80>

>>> [num for num in my_gen_5]
[0, 1, 2, 3, 4]

>>> [num for num in my_gen_5]
[]
```

## Reescribiendo nuestro ejemplo anterior usando un generador

Reescribamos nuestro ejemplo anterior usando una función generadora para producir los datos. Esto nos permitirá manejar conjuntos de datos más grandes de manera más eficiente.

```python linenums="1"
--8<-- "dlt_tutorial/1_sample_pipeline_basic.py:sample_data"
```

Ahora podemos pasar esta función generadora a nuestro pipeline de `dlt`:

```python linenums="1" hl_lines="10"
--8<-- "dlt_tutorial/1_sample_pipeline_basic.py:pipeline"
```

Esta vez, sin embargo, estamos imprimiendo el resultado del método `pipeline.run()`, que devuelve un objeto `LoadInfo` que contiene detalles sobre el proceso de carga.

```python linenums="1" hl_lines="10"
--8<-- "dlt_tutorial/1_sample_pipeline_basic.py:load_info"
```

Puedes ejecutar este script de la misma manera que antes

```bash
$ python dlt_tutorial/1_sample_pipeline_basic.py
Running pipeline...
Done
Load info:
Pipeline sample_pipeline load step completed in 0.28 seconds
1 load package(s) were loaded to destination duckdb and into dataset sample_data
The duckdb destination used duckdb:////home/diego/Code/playground/dlt-tutorial/sample_pipeline.duckdb location to store data
Load package 1762003350.048731 is LOADED and contains no failed jobs
```

!!! tip "¿Qué es la información de carga?"

    La información de carga proporciona detalles sobre el proceso de carga, incluyendo el tiempo tomado, el número de paquetes de carga y el destino donde se almacenaron los datos. También indica si hubo trabajos fallidos durante el proceso de carga.

!!! tip "Usando generadores con dlt"

    `dlt` funciona mejor si el generador produce diccionarios en lotes, ver <https://dlthub.com/docs/reference/performance#yield-pages-instead-of-rows>

## Usando `resources` y `sources`

- Un [resource](https://dlthub.com/docs/general-usage/glossary#resource) es una función ([opcionalmente async](https://dlthub.com/docs/reference/performance#parallelism-within-a-pipeline)) que **produce datos**. Para crear un resource, agregamos el decorador `@dlt.resource` a esa función.
- Un [source](https://dlthub.com/docs/general-usage/source) es una función decorada con `@dlt.source` que devuelve uno o más resources.

En su implementación más básica, un `resource` se implementa decorando nuestra función generadora de datos con `@dlt.resource`:

```python linenums="1" hl_lines="1"
--8<-- "dlt_tutorial/2_sample_pipeline_sources_resources.py:sample_data"
```

Un `source` se crea definiendo una función que devuelve el resource:

```python linenums="1" hl_lines="1 3"
--8<-- "dlt_tutorial/2_sample_pipeline_sources_resources.py:sample_source"
```

Luego podemos usar este source en nuestro pipeline:

```python linenums="1" hl_lines="8"
--8<-- "dlt_tutorial/2_sample_pipeline_sources_resources.py:pipeline"
```

## ¿Qué cambió?

`dlt` genera automáticamente **especificaciones** de configuración para funciones decoradas con `@dlt.source`, `@dlt.resource` y `@dlt.destination`

Por ejemplo, ahora permite **[inyectar valores de configuración](https://dlthub.com/docs/general-usage/credentials/setup)**

## Inyectando valores de configuración

Podemos modificar nuestra función source para aceptar un parámetro de configuración:

```python linenums="1" hl_lines="2"
--8<-- "dlt_tutorial/2b_sample_pipeline_sources_resources_with_config.py:sample_source"
```

Este parámetro ahora puede ser configurado usando variables de entorno, archivos de configuración o argumentos de línea de comandos cuando se ejecuta el pipeline.

```bash
$ MY_CUSTOM_PARAMETER="pythonchile" python dlt_tutorial/2b_sample_pipeline_sources_resources_with_config.py
Custom parameter value: pythonchile
Running pipeline...
Done
...
```

Alternativamente, podemos configurar el parámetro en un archivo de configuración ubicado en `.dlt/config.toml`:

```toml
[sample_pipeline]
my_custom_parameter = "baz"
```

Ejecutar el pipeline ahora usará el valor del archivo de configuración:

```bash
$ python dlt_tutorial/2b_sample_pipeline_sources_resources_with_config.py
Custom parameter value: baz
Running pipeline...
Done
...
```

!!! tip "dlt busca valores en múltiples lugares en un orden específico"

    Ver <https://dlthub.com/docs/general-usage/credentials/setup#how-dlt-looks-for-values> para más información sobre cómo `dlt` busca valores de configuración.

!!! warning "Usaremos `resource` directamente de ahora en adelante"

    De ahora en adelante, usaremos `resource` directamente en lugar de envolverlos en _sources_, a menos que necesitemos agrupar múltiples resources juntos.

    Dado que solo estamos usando un solo resource, podemos pasarlo directamente al método `pipeline.run()`.

## Resumiendo

En esta parte, aprendimos sobre iteradores y generadores en Python, y cómo pueden ser usados para manejar datos eficientemente en pipelines de `dlt`. También introdujimos los conceptos de `resources` y `sources`, que ayudan a estructurar la extracción de datos de una manera más modular.

En la siguiente parte, cambiaremos a un destino postgres y veremos cómo manejar patrones de carga más complejos.
