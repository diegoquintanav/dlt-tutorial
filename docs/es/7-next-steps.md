# Conclusiones y Próximos Pasos

Esperamos que a estas alturas tengas una buena comprensión de cómo funciona DLT y cómo usarlo para construir pipelines de datos. Aunque la documentación de dlt es bastante extensa, aún está un poco áspera en los bordes y puede ser difícil de navegar a veces. Tratamos de cubrir lo que siento son los aspectos más importantes de dlt para empezar, pero hay mucho más por explorar.

Aquí hay algunas sugerencias para qué hacer a continuación:

## Pregunta a la comunidad y el `dlthub bot` en Slack

Si tienes preguntas o necesitas ayuda, puedes unirte a la [comunidad DLT Slack](https://dlthub.com/community) y hacer tus preguntas allí. La comunidad es muy activa y útil.

## Explora la CLI de `dlt`

La interfaz de línea de comandos (CLI) de `dlt` proporciona algunos comandos para gestionar y ejecutar tus pipelines. Puedes explorar los comandos disponibles ejecutando:

```bash
dlt --help
```

Puede ser de particular interés explorar los comandos de [dashboard](https://dlthub.com/docs/reference/command-line-interface#dlt-pipeline-show):

```bash
dlt pipeline sample_pipeline show
```

Refiere a la [documentación oficial](https://dlthub.com/docs/reference/command-line-interface) para más detalles sobre los comandos disponibles y su uso.

## Usa el comando `dlt init` y benefíciate de plantillas de proyecto

Aunque en la documentación oficial esto se introduce muy temprano, lo encuentro más útil una vez que tienes una mejor comprensión de cómo funciona dlt. El comando `dlt init` te permite crear un nuevo proyecto dlt desde una plantilla. Puedes explorar las plantillas disponibles ejecutando:

```bash
dlt init <SOURCE> <DESTINATION>
```

Por ejemplo, prueba:

```bash
mkdir my_dlt_project
cd my_dlt_project
dlt init postgres duckdb
```

Esto iniciará un nuevo proyecto dlt que extrae datos de una base de datos Postgres y los carga en una base de datos DuckDB (Y algunas otras cosas también).

!!! warning "Las plantillas pueden ser abrumadoras al principio"

    El código generado puede ser abrumador al principio, pero esperamos que ahora entiendas cómo las diferentes partes funcionan juntas.

Puedes verificar las plantillas disponibles usando:

```bash
dlt init --list-sources
```

y

```bash
dlt init --list-destinations
```

## Explora tutoriales y cursos más avanzados

Si sientes que `dlt` es una buena opción para tus necesidades de carga de datos, puedes explorar tutoriales y cursos más avanzados disponibles en el sitio de documentación oficial en <https://dlthub.com/docs/tutorial/education>:

- <https://dlthub.com/docs/tutorial/fundamentals-course>
- <https://dlthub.com/docs/tutorial/advanced-course>

¡Hasta la próxima, feliz carga de datos!
