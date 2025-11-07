# DLT Tutorial

This repository contains materials for a tutorial on Data Load Tool (DLT). It includes slides in both English and Spanish, as well as example code and configurations.

## Getting Started

Follow along the documentation in <https://diegoquintanav.github.io/dlt-tutorial/> to set up your environment and access the tutorial materials.

## Prerequisites

You can review the prerequisites in the [docs](https://diegoquintanav.github.io/dlt-tutorial/en/1-getting-started/).

## Using a Codespaces environment

Fork this repository to your own GitHub account. Then, you can create a Codespace directly from the GitHub web interface by clicking on the green "Code" button and selecting "Open with Codespaces" > "New codespace".

Wait for the Codespace to be created and initialized. This may take a few minutes.

Once the Codespace is ready, you can open a terminal and run the following commands to make sure all dependencies are installed:

### Checking postgres connection

```bash
bash # start a bash shell
ping postgres # test connectivity to the Postgres service
^C # stop the ping command
```

Open a `psql` session to the Postgres database with `make postgres.<devcontainer|host>.psql` and run a simple query to check the version:

```psql
postgres=# select version();
                                                       version                                                        
----------------------------------------------------------------------------------------------------------------------
 PostgreSQL 15.14 (Debian 15.14-1.pgdg13+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
(1 row)
```

### Checking duckdb and dlt installation

```bash
duckdb --version # check duckdb installation
dlt --version # check dlt installation
```

## Building and accessing the docs locally

To build and preview the documentation locally, you can use docker-compose. Run the following command in the root directory of the repository:

```bash
docker-compose -f docker-compose.mkdocs.yml up
```

## Slides

The slides for the tutorial are available in both English and Spanish. You can build and preview the slides using the provided Makefile in the `slides` directory. Use `make help` from the `slides` directory to see available commands.

```bash
cd slides
make help
make all
```
