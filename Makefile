.DEFAULT_GOAL := help
.PHONY: help


# taken from https://container-solutions.com/tagging-docker-images-the-right-way/

help: ## Print this help
	@grep -E '^[0-9a-zA-Z_\-\.]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build_slides_en: ## Build slides PDF from markdown using Marp, in english
	@marp --pdf --allow-local-files EN_slides.md -o slides_en.pdf

duckdb.query_sample: ## Run sample query against duckdb database
	@duckdb sample_pipeline.duckdb -c "select * from sample_data.samples;"

postgres.query_sample: ## Run sample query against postgres database
	@docker compose exec db psql -U postgres --pset expanded=auto -c "select * from sample_data.samples;"