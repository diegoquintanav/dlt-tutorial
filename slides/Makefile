.DEFAULT_GOAL := help
.PHONY: help


# taken from https://container-solutions.com/tagging-docker-images-the-right-way/

help: ## Print this help
	@grep -E '^[0-9a-zA-Z_\-\.]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

duckdb.query_sample: ## Run sample query against duckdb database
	@duckdb sample_pipeline.duckdb -c "select * from sample_data.samples;"

postgres.query_sample: ## Run sample query against postgres database
	@docker compose exec db psql -c "select * from sample_data.samples;"