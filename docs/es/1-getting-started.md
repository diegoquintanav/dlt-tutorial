# Primeros Pasos con este Tutorial

!!! warning "Asumo que usas Linux"

    Este tutorial asume que estás usando un sistema operativo basado en Linux. Aunque puede ser posible seguir adelante en otros sistemas operativos, algunos comandos e instrucciones pueden diferir.

## Usando Docker y Docker Compose

Necesitarás docker, docker-compose, python y `uv` instalados en tu sistema para seguir este tutorial.

1. Instala docker desde <https://docs.docker.com/get-docker/>
2. Instala docker-compose desde <https://docs.docker.com/compose/install/>

## ¿Qué pasa si no quiero usar Docker?

Necesitarás configurar tu entorno local para ejecutar este tutorial. Las siguientes secciones te guiarán a través de los pasos necesarios.

1. Instala python usando tu método preferido. Aquí hay algunas opciones:
     - Desde el sitio web oficial: <https://www.python.org/downloads/>
     - Usando un gestor de paquetes como `apt`, como `apt install python3` en Debian/Ubuntu
     - Usando un gestor de versiones como `pyenv`: <https://github.com/pyenv/pyenv>
     - Usando un gestor de versiones como `uv`: <https://uv.io/docs/getting-started/installation/>
2. Instala `uv` siguiendo las instrucciones en <https://uv.io/docs/getting-started/installation/>

### Usando Python puro

Este tutorial fue escrito usando `Python 3.12.3`. Puedes crear un entorno virtual usando `venv` o `virtualenv` para aislar las dependencias de este tutorial.

Si estás usando `uv`, puedes crear un entorno virtual usando `uv venv`:

```bash
uv venv --seed
uv sync
source .venv/bin/activate
```

Si estás usando Python puro, puedes crear un entorno virtual usando `venv` de la librería estándar:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

!!! info "requirements.txt"
    El archivo `requirements.txt` fue generado usando `uv export --format requirements.txt -o requirements.txt` para asegurar compatibilidad con `uv`.

### Instalando duckdb

Sigue las instrucciones en <https://duckdb.org/install/?platform=linux&environment=cli> para instalar el cliente `duckdb` en tu sistema.

### Configurando una base de datos Postgres

Se requiere una base de datos Postgres para ejecutar este tutorial. Si tienes docker compose instalado, puedes configurar una base de datos Postgres local usando Docker y Docker Compose.

```bash
docker compose -f docker-compose.yml up db -d
```

Esto iniciará una base de datos Postgres en `localhost:5555` con las siguientes credenciales (todos los valores por defecto de la documentación oficial, pero la contraseña ha sido cambiada a `test`):

- Usuario: `postgres`
- Contraseña: `test`
- Base de datos: `postgres`
- Host: `localhost`
- Puerto: `5555`

Puedes conectarte a esta base de datos usando cualquier cliente de Postgres, como `psql` o una herramienta GUI como DBeaver o pgAdmin. Se proporciona una conexión de acceso rápido a través del `Makefile`

```bash
make postgres.psql
```

### Configurando una base de datos Postgres remota usando Neon

Puedes configurar una base de datos Postgres externa si lo prefieres.

Una instancia postgres gratuita puede ser creada usando servicios como <https://neon.com/> (no estoy afiliado con ellos, solo parece menos complicado).

Crea una cuenta y obtén tu cadena de conexión, y debería verse algo así:

```bash
psql 'postgresql://neondb_owner:npg_some_long_url.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
```

Asegúrate de que cuando generes la cadena de conexión, **desactives el pooling de conexiones** si esa opción está habilitada.

![disable connection pooling](./assets/img/neon_db_disable_connection_pooling.png)

Necesitarás esta cadena de conexión, y veremos cómo usarla en las siguientes secciones.

## Usando devcontainers

Se proporciona un devcontainer para este tutorial. Si estás usando VSCode _y_ tienes docker instalado, puedes abrir esta carpeta en un _devcontainer_ y tener todo configurado para ti.
Ver <https://code.visualstudio.com/docs/devcontainers/containers> para más información sobre devcontainers.

### Configuración de conexión a base de datos Postgres desde dentro del devcontainer

Si estás usando el devcontainer, la base de datos Postgres puede ser accedida en `postgres:5432` con las mismas credenciales mencionadas anteriormente.
