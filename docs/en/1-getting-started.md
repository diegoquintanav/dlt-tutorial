# Getting Started with this Tutorial

!!! warning "I'm assuming you use Linux"

    This tutorial assumes you are using a Linux-based operating system. While it may be possible to follow along on other operating systems, some commands and instructions may differ.

## Using Docker and Docker Compose

You'll need docker, docker-compose, python, and `uv` installed on your system to follow along with this tutorial.

1. Install docker from <https://docs.docker.com/get-docker/>
2. Install docker-compose from <https://docs.docker.com/compose/install/>

## What if I don't want to use Docker?

You'll need to set up your local environment to run this tutorial. The following sections will guide you through the necessary steps.

1. Install python using your preferred method. Here are some options:
     - From the official website: <https://www.python.org/downloads/>
     - Using a package manager like `apt`, like `apt install python3` on Debian/Ubuntu
     - Using a version manager like `pyenv`: <https://github.com/pyenv/pyenv>
     - Using a version manager like `uv`: <https://uv.io/docs/getting-started/installation/>
2. Install `uv` by following the instructions at <https://uv.io/docs/getting-started/installation/>

### Using plain Python

This tutorial was written using `Python 3.12.3`. You can create a virtual environment using `venv` or `virtualenv` to isolate the dependencies for this tutorial.

If you are using `uv`, you can create a virtual environment using `uv venv`:

```bash
uv venv --seed
uv sync
source .venv/bin/activate
```

If you are using plain Python, you can create a virtual environment using `venv` from the standard library:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

!!! info "requirements.txt"
    The `requirements.txt` file was generated using `uv export --format requirements.txt -o requirements.txt` to ensure compatibility with `uv`.

### Installing duckdb

Follow the instructions at <https://duckdb.org/install/?platform=linux&environment=cli> to install the `duckdb` client on your system.

### Setting up a Postgres database

A Postgres database is required to run this tutorial. If you have docker compose installed, you can set up a local Postgres database using Docker and Docker Compose.

```bash
docker compose -f docker-compose.yml up db -d
```

This will start a Postgres database on `localhost:5555` with the following credentials (all defaults from the official documentation, but the password has been changed to `test`):

- User: `postgres`
- Password: `test`
- Database: `postgres`
- Host: `localhost`
- Port: `5555`

You can connect to this database using any Postgres client, such as `psql` or a GUI tool like DBeaver or pgAdmin. A shortcut connection is provided through `Makefile`

```bash
make postgres.psql
```

### Setting a remote Postgres database using Neon

You can set up an external Postgres database if you prefer.

A free postgres instance can be created using services like <https://neon.com/> (I'm not affiliated with them, it just seems less complicated).

Create an account and get your connection string, and it should look something like this:

```bash
psql 'postgresql://neondb_owner:npg_some_long_url.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
```

Make sure that when generating the connection string, **you deactivate connection pooling** if that option is enabled.

![disable connection pooling](./assets/img/neon_db_disable_connection_pooling.png)

You'll need this connection string, and we will see how to use it in the next sections.

## Using devcontainers

A devcontainer is provided for this tutorial. If you are using VSCode _and_ have docker installed, you can open this folder in a _devcontainer_and have everything set up for you.
See <https://code.visualstudio.com/docs/devcontainers/containers> for more information on devcontainers.

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

### Postgres database connection settings from inside the devcontainer

If you are using the devcontainer, the Postgres database can be accessed at `postgres:5432` with the same credentials as above.
