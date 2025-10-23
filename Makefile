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

postgres.query_sample: ## Run sample query against postgres database
	@docker compose -f $(main_compose_file) exec db psql -U postgres --pset expanded=auto -c "select * from sample_data.samples;"

postgres.psql: ## Run sample query against postgres database
	@docker compose -f $(main_compose_file) exec db psql -U postgres --pset expanded=auto

mkdocs.serve.docker: ## serve the mkdocs documentation
	@docker compose -f $(mkdocs_compose_file) up

mkdocs.logs.docker: ## show the logs of the mkdocs container
	@docker compose -f $(mkdocs_compose_file) logs -ft mkdocs

mkdocs.requirements.txt: ## update requirements.txt file from pyproject.toml
	@poetry export -f requirements.txt --only mkdocs --without-hashes > poetry-mkdocs-requirements.txt
	@echo "poetry-mkdocs-requirements.txt file updated"
