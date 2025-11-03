# Introducción

Esta es la documentación del tutorial de `dlt` (kit de herramientas de carga de datos). No confundas `dlt` con `Delta Live Tables` de Databricks. Esto no tiene nada que ver con ello.

!!! tip "Usa `"dlthub"` como palabra clave para buscar contenido relacionado en motores de búsqueda"
    De lo contrario, puedes encontrar contenido no relacionado sobre Delta Live Tables. Cuando decimos `dlt` en esta documentación, siempre nos referimos al `kit de herramientas de carga de datos`.

En pipelines de datos, un acrónimo comúnmente usado es [ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load) (Extraer, Transformar, Cargar).

La extracción tiene que ver con obtener datos de un sistema fuente (por ejemplo, una API, una base de datos, archivos, etc.). La transformación tiene que ver con limpiar, normalizar y dar forma a los datos para que se ajusten al sistema de destino. La carga tiene que ver con escribir los datos en el sistema de destino (por ejemplo, un almacén de datos, un lago de datos, etc.).

Alternativamente, un paradigma más reciente es ELT (Extraer, Cargar, Transformar). Esto invierte el orden de los dos últimos pasos, cargando primero los datos sin procesar en el sistema de destino, y luego transformándolos allí. Esto permite más flexibilidad y escalabilidad, cargando los datos primero y transformándolos más tarde según sea necesario. Esto puede ser especialmente útil cuando se trata de grandes volúmenes de datos o cuando la lógica de transformación es compleja y puede cambiar con el tiempo.

`dlt` se enfoca en la parte de carga (`L`) de estos paradigmas. Nuestro requisito principal es mover datos de un sistema fuente a un sistema de destino, mientras otorgamos cierta flexibilidad sobre cuándo y cómo transformar los datos. El código para la parte de carga es mayormente repetitivo, para algunos escenarios comunes.

La mayoría de las veces, la carga de datos no es una tarea única. Los datos se generan continuamente en los sistemas fuente, y necesitamos mantener nuestros sistemas de destino actualizados con los datos más recientes. Aquí es donde `dlt` brilla, proporcionando características para carga incremental, captura de cambios de datos y programación.

## Alternativas a `dlt`

Hay muchas alternativas a `dlt` que abordan las tareas de carga de datos. La lista es enorme y no estoy listando todo, pero aquí están las que he usado y/o considero relevantes:

- **Apache NiFi**: Una herramienta de integración de datos de código abierto que soporta enrutamiento de datos, transformación y lógica de mediación de sistemas. Proporciona una interfaz basada en web para diseñar flujos de datos y soporta una amplia gama de fuentes y destinos de datos. Ver <https://nifi.apache.org/>
- **Airbyte**: Una plataforma de integración de datos de código abierto que se enfoca en ELT. Proporciona una amplia gama de conectores para varias fuentes y destinos de datos, y permite a los usuarios definir lógica de transformación usando SQL. Ver <https://airbyte.com/>
- **Meltano**: Una plataforma de integración de datos de código abierto que se enfoca en ELT. Proporciona una amplia gama de conectores para varias fuentes y destinos de datos, y permite a los usuarios definir lógica de transformación usando archivos de configuración yaml. Ver <https://meltano.com/>
- **Dagster**: Un orquestador de datos de código abierto para aprendizaje automático, analítica y ETL. Proporciona un marco para construir, programar y monitorear pipelines de datos. Ver <https://dagster.io/>.

## ¿Por qué `dlt`?

![youropinion](https://c.tenor.com/dlLdNF3Z-CUAAAAd/the-big-lebowski-thats-like-your-opinion-man.gif)

### Menos es más

O como dice en el *Zen de python*: "Simple es mejor que complejo."

La mayoría de las alternativas mencionadas anteriormente son herramientas poderosas y flexibles para tareas de carga de datos. Sin embargo, también pueden ser complejas y requerir configuración significativa.

Por ejemplo, Meltano es muy flexible a través de sus archivos de configuración YAML, pero esto también significa que necesitas aprender su sintaxis y estructura de configuración. Para Dagster necesitas aprender su marco y API, y hospedar el servicio en algún lugar. Para DLT, necesitas Python en su mayor parte.

### Tareas puntuales

Un pipeline de `dlt` puede ser tan simple como un script de Python que puedes ejecutar desde tu máquina local o un servidor. Esto hace que sea fácil de configurar y usar para tareas de carga de datos puntuales, sin la necesidad de infraestructura compleja o configuración.

Una vez que superas la curva de aprendizaje inicial, es fácil de usar.

### Ambientalmente amigable

Dependiendo del tamaño de tus datos y la frecuencia de tus cargas, usar una herramienta ligera como `dlt` puede ser más amigable con el medio ambiente que usar una plataforma de integración de datos pesada que requiere recursos computacionales significativos.

!!! tip "Mide tu huella de carbono"

    Ver <https://codecarbon.io/> si deseas comenzar a medir las emisiones de carbono de tu código.
  
### Código abierto

[El código tiene una licencia Apache 2.0](https://github.com/dlt-hub/dlt/blob/devel/LICENSE.txt), por lo que puedes usarlo libremente en tus proyectos, incluso comerciales. También puedes contribuir al proyecto si deseas mejorarlo o agregar nuevas características.

Tiene una versión `dlt+` que no he explorado ni necesitado aún, que parece agregar más características y soporte.

## Contras de `dlt`

Siento que podría usar más amor en términos de

- Características de CLI: la CLI es torpe y a veces se siente inútil o tosca
- Dashboards: `dlt` tiene algunos elementos internos que usa para mantener y rastrear el estado. También proporciona dashboards que ofrecen una perspectiva sobre estos datos. No he usado ni necesitado estos dashboards pero puedo entender que algunas personas los quieren y los usan.

### El estilo en la documentación no es consistente

Escribir documentación es difícil. Yo mismo lucho con ello. Uno de los versos del Zen de Python afirma:

> Debería haber una-- y preferiblemente solo una --manera obvia de hacerlo.

Los documentos muestran múltiples formas de lograr lo mismo, lo que puede ser confuso para los usuarios. A veces faltan importaciones, algunas explicaciones sobre el uso no están claras, y hay inconsistencias en los ejemplos proporcionados. Se siente caótico a veces.
