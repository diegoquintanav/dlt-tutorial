# Introduction

This is the documentation for the `dlt` (data loading toolkit) tutorial, being. Do not confuse `dlt` from `Delta Live Tables` by Databricks. This has nothing to do with it.

!!! tip "Use `"dlthub"` as a keyword to search for related content in search engines"
    Otherwise you may find unrelated content about Delta Live Tables. When we say `dlt` in this documentation, we always refer to `data loading toolkit`.

In data pipelines, a common acronym used is [ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load) (Extract, Transform, Load).

Extracting has to do with getting data from a source system (e.g., an API, a database, files, etc). Transforming has to do with cleaning, normalizing, and shaping the data to fit the target system. Loading has to do with writing the data into the target system (e.g., a data warehouse, a data lake, etc).

Alternatively, a more recent paradigm is ELT (Extract, Load, Transform). This reverses the order of the last two steps, loading the raw data into the target system first, and then transforming it there. This allows for more flexibility and scalability, loading data first and transforming it later as needed. This can be especially useful when dealing with large volumes of data or when the transformation logic is complex and may change over time.

`dlt` focuses on the loading part (`L`) of these paradigms. Our main requirement is to move data from a source system to a target system, while granting some flexibility on when and how to transform the data. The code for the loading part is mostly repetitive, for some common scenarios.

Most of the time, data loading is not a one-time task. Data is continuously generated in source systems, and we need to keep our target systems up-to-date with the latest data. This is where `dlt` shines, providing features for incremental loading, change data capture, and scheduling.

## Alternatives to `dlt`

There are many alternatives to `dlt` that address the data loading tasks. The list is huge and I'm not listing everything,, but here are the ones that I have used and/or consider relevant:

- **Apache NiFi**: An open-source data integration tool that supports data routing, transformation, and system mediation logic. It provides a web-based interface for designing data flows and supports a wide range of data sources and destinations. See <https://nifi.apache.org/>
- **Airbyte**: An open-source data integration platform that focuses on ELT. It provides a wide range of connectors for various data sources and destinations, and allows users to define transformation logic using SQL. See <https://airbyte.com/>
- **Meltano**: An open-source data integration platform that focuses on ELT. It provides a wide range of connectors for various data sources and destinations, and allows users to define transformation logic using yaml configuration files. See <https://meltano.com/>
- **Dagster**: An open-source data orchestrator for machine learning, analytics, and ETL. It provides a framework for building, scheduling, and monitoring data pipelines. See <https://dagster.io/>.

If you want to explore more alternatives, you can check out the [ETL Tools Comparison](https://www.oreilly.com/radar/etl-tools-comparison/).

## Why `dlt`?

!!! warning "This is all my opinion and you should form your own."

### Less is more

Or as per in the *Zen of python*: "Simple is better than complex.".

Most of the alternatives mentioned above are powerful and flexible tools for data loading tasks. However, they can also be complex and require significant setup and configuration.

For example, Meltano is very flexible through its YAML configuration files, but this also means that you need to learn its configuration syntax and structure. For Dagster you need to learn its framework and API, and host the service somewhere. For DLT, you need Python for the most part.

### One-off tasks

A `dlt` pipeline can be as simple as a single Python script that you can run from your local machine or a server. This makes it easy to set up and use for one-off data loading tasks, without the need for complex infrastructure or configuration.

Once you get past the initial learning curve, it is easy to use.

### Environmentally friendly

Depending on the size of your data and the frequency of your loads, using a lightweight tool like `dlt` can be more environmentally friendly than using a heavy-duty data integration platform that requires significant computational resources.

!!! tip "Measure your carbon footprint"

    See <https://codecarbon.io/> if you wish to start measuring the carbon emissions of your code.
  
### Open source

[Code has an Apache 2.0 license](https://github.com/dlt-hub/dlt/blob/devel/LICENSE.txt), so you can use it freely in your projects, even commercial ones. You can also contribute to the project if you wish to improve it or add new features.

It has a `dlt+` version I have not explored nor needed yet, which seems to add more features and support.

## Cons of `dlt`

I feel it could use more love in terms of

- CLI features: the CLI is clunky and at times feels useless or clunky
- Dashboards: `dlt` has some internals it use to maintain and track state. It also provides dashboards that offer an insight on these data. I haven't used or needed these dashboards but I can understand some people want them and use them.

### Style in documentation is not consistent

Writing documentation is difficult. I struggle with it myself. One of the verses of the Zen of Python claims:

> There should be one-- and preferably only one --obvious way to do it.

The docs show multiple ways to achieve the same, which can be confusing for users. Sometimes imports are missing, some explanations on usage are unclear, and there are inconsistencies in the examples provided.
