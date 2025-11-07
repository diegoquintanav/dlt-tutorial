.DEFAULT_GOAL := help
.PHONY: help

mkdocs_compose_file := docker-compose.mkdocs.yml
main_compose_file := docker-compose.yml

# taken from https://container-solutions.com/tagging-docker-images-the-right-way/

help: ## Print this help
	@grep -E '^[0-9a-zA-Z_\-\.]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build_slides_en: ## Build slides PDF from markdown using Marp, in english
	@marp --pdf --allow-local-files EN_slides.md -o slides_en.pdf

duckdb.query_sample: ## Run sample query against duckdb database
	@duckdb sample_pipeline.duckdb -c "select * from sample_data.samples;"

postgres.host.query_sample: ## Run sample query against postgres database (from host)
	@PGPASSWORD=test psql -h 0.0.0.0 -p 5555 -U postgres --pset expanded=auto -c "select * from sample_data.samples;"

postgres.devcontainer.query_sample: ## Run sample query against postgres database (from devcontainer)
	@PGPASSWORD=test psql -h postgres -p 5432 -U postgres --pset expanded=auto -c "select * from sample_data.samples;"

postgres.host.psql: ## Run psql against postgres database (from host)
	@PGPASSWORD=test psql -h 0.0.0.0 -p 5555 -U postgres

postgres.devcontainer.psql: ## Run psql against postgres database (from devcontainer)
	@PGPASSWORD=test psql -h postgres -p 5432 -U postgres

compose.postgres.query_sample: ## Run sample query against postgres database in docker compose
	@docker compose -f $(main_compose_file) exec db psql -U postgres --pset expanded=auto -c "select * from sample_data.samples;"

compose.postgres.psql: ## Run sample query against postgres database
	@docker compose -f $(main_compose_file) exec db psql -U postgres --pset expanded=auto

mkdocs.serve.docker: ## serve the mkdocs documentation
	@docker compose -f $(mkdocs_compose_file) up

mkdocs.logs.docker: ## show the logs of the mkdocs container
	@docker compose -f $(mkdocs_compose_file) logs -ft mkdocs

mkdocs.requirements.txt: ## update requirements.txt file from pyproject.toml (only mkdocs)
	@uv export --format requirements.txt --only-group mkdocs --no-hashes -o mkdocs-requirements.txt
	@echo "mkdocs-requirements.txt file updated"

tutorial.requirements.txt: ## update requirements.txt file from pyproject.toml (only tutorial)
	@uv export --format requirements.txt --only-group tutorial --no-hashes -o requirements.txt
	@echo "tutorial-requirements.txt file updated"
