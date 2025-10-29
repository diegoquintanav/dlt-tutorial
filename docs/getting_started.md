# Getting Started with this Tutorial

!!! warning "I'm assuming you use Linux"

    This tutorial assumes you are using a Linux-based operating system. While it may be possible to follow along on other operating systems, some commands and instructions may differ.

You'll need docker, docker-compose, python, and `uv` installed on your system to follow along with this tutorial.

1. Install docker from <https://docs.docker.com/get-docker/>
2. Install docker-compose from <https://docs.docker.com/compose/install/>
3. Install python using your preferred method. Here are some options:
   - From the official website: <https://www.python.org/downloads/>
   - Using a package manager like `apt`, like `apt install python3` on Debian/Ubuntu
   - Using a version manager like `pyenv`: <https://github.com/pyenv/pyenv>
   - Using a version manager like `uv`: <https://uv.io/docs/getting-started/installation/>
4. Install `uv` by following the instructions at <https://uv.io/docs/getting-started/installation/>

## Using plain Python

This tutorial was written using `Python 3.12.3`. You can create a virtual environment using `venv` or `virtualenv` to isolate the dependencies for this tutorial.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Using devcontainers

A devcontainer is provided for this tutorial. If you are using VSCode, you can open this folder in a devcontainer and have everything set up for you.
See <https://code.visualstudio.com/docs/devcontainers/containers> for more information on devcontainers.

## Setting up a local Postgres database

A Postgres database is required to run this tutorial. You can set up a local Postgres database using Docker and Docker Compose.

```bash
docker compose -f docker-compose.yml up db -d
```

This will start a Postgres database on `localhost:5555` with the following credentials (all defaults from the official documentation, but the password has been changed to `test`):

- User: `postgres`
- Password: `test`
- Database: `postgres`

You can connect to this database using any Postgres client, such as `psql` or a GUI tool like DBeaver or pgAdmin. A shortcut connection is provided through `Makefile`

```bash
make postgres.psql
```

You can set up an external Postgres database if you prefer. Just make sure to update the connection details in the code accordingly.

A free postgres instance can be created using services like <https://neon.com/> (I'm not affiliated with them, it just seems less complicated).

Create an account and get your connection string, then update the connection details in the code accordingly. We will see how to do this in the next sections.
