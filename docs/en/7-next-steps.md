# Conclusions and Next Steps

Hopefully by now you have a good understanding of how DLT works and how to use it to build data pipelines. Although the dlt documentation is quite extensive, is still a bit rough around the edges and can be hard to navigate at times. We tried to cover what I feel are the most important aspects of dlt to get you started, but there is much more to explore.

Here are some suggestions for what to do next:

## Ask the community and the `dlthub bot` on Slack

If you have questions or need help, you can join the [DLT Slack community](https://dlthub.com/community) and ask your questions there. The community is very active and helpful.

## Explore the `dlt` CLI

The `dlt` command-line interface (CLI) provides some commands to manage and run your pipelines. You can explore the available commands by running:

```bash
dlt --help
```

It may be of particular interest to explore the [dashboard](https://dlthub.com/docs/reference/command-line-interface#dlt-pipeline-show) commands:

```bash
dlt pipeline --list # shows existing pipelines
dlt pipeline <pipeline_name> show # shows pipeline details using streamlit
dlt pipeline <pipeline_name> show --dashboard # shows pipeline dashboard using marimo
```

Refer to the [official documentation](https://dlthub.com/docs/reference/command-line-interface) for more details on the available commands and their usage.

## Use the `dlt init` command and benefit from project templates

Although in the official documentation this is introduced very early, I find it more useful once you have a better understanding of how dlt works. The `dlt init` command allows you to create a new dlt project from a template. You can explore the available templates by running:

```bash
dlt init <SOURCE> <DESTINATION>
```

For example, try:

```bash
mkdir my_dlt_project
cd my_dlt_project
dlt init postgres duckdb
```

This will bootstrap a new dlt project that extracts data from a Postgres database and loads it into a DuckDB database (And some other things too).

!!! warning "Templates may be overwhelming at first"

    The generated code may be overwhelming at first, but hopefully you understand now how the different parts work together.

You can check the available templates using:

```bash
dlt init --list-sources
```

and

```bash
dlt init --list-destinations
```

## Explore more advanced tutorials and courses

If you feel that `dlt` is a good fit for your data loading needs, you can explore more advanced tutorials and courses available on the official documentation site at <https://dlthub.com/docs/tutorial/education>:

- <https://dlthub.com/docs/tutorial/fundamentals-course>
- <https://dlthub.com/docs/tutorial/advanced-course>

## Tips and tricks and recommendations

- Pass `PROGRESS=log|tqdm|enlighten python script.py` to change the progress bar style ([source](https://dlthub.com/docs/general-usage/pipeline#monitor-the-loading-progress))
- Stick to one `pipeline.run` per script.
- Use `dlt` for ELT, not for ETL. Transform data as close to the source as possible.
- Send the output of `pipeline.run` to another call to `pipeline.run` to persist execution logs to the same target
- Pass `dev_mode=True` to `dlt.pipeline` to experiment ([source](https://dlthub.com/docs/general-usage/pipeline#do-experiments-with-dev-mode))
- Separate dev/prod environments using `pipelines_dir` ([source](https://dlthub.com/docs/general-usage/pipeline#separate-working-environments-with-pipelines_dir))
- `dlt` supports parallel execution through `concurrent.futures` ([source](https://dlthub.com/docs/reference/performance#running-multiple-pipelines-in-parallel))
- Send errors to sentry by setting `runtime.sentry_dsn="https:///<...>"` in `config.toml` ([source](https://dlthub.com/docs/running-in-production/tracing))

Until next time, happy data loading!
