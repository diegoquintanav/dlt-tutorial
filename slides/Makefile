.DEFAULT_GOAL := help
.PHONY: help


# taken from https://container-solutions.com/tagging-docker-images-the-right-way/

help: ## Print this help
	@grep -E '^[0-9a-zA-Z_\-\.]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build_slides_en: ## Build slides PDF from markdown using Marp, in english
	@marp --pdf --allow-local-files EN_slides.md -o slides_en.pdf

serve_slides_en: ## Build slides PDF from markdown using Marp, in english
	@marp --watch --preview --allow-local-files EN_slides.md

build_slides_es: ## Build slides PDF from markdown using Marp, in spanish
	@marp --pdf --allow-local-files ES_slides.md -o slides_es.pdf

serve_slides_es: ## Build slides PDF from markdown using Marp, in spanish
	@marp --watch --preview --allow-local-files ES_slides.md
