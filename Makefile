-include .env
export

setup:
	pip install uv

virtual-environment: setup
	python -m venv .venv
	uv sync

dev: setup
	uv sync --extra dev

db:
	docker run --name $(POSTGRES_DB) \
	-p 5432:5432 \
	-e POSTGRES_USER=$(POSTGRES_USER) \
	-e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
	-d postgres

run:
	uv run python -m src.main

quick-sync: dev
	@echo "Sync finished"
