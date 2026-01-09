setup:
	pip install uv

virtual-environment: setup
	python -m venv .venv
	uv sync

dev: setup
	uv sync --extra dev

run:
	uv run python -m src.main

quick-sync: dev
	@echo "Sync finished"
