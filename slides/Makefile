.DEFAULT_GOAL := help
.PHONY: help


# taken from https://container-solutions.com/tagging-docker-images-the-right-way/

help: ## Print this help
	@grep -E '^[0-9a-zA-Z_\-\.]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build_slides: ## Build slides PDF from markdown using Marp
	@marp --pdf --allow-local-files slides.md -o slides.pdf
