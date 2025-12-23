setup:
	pip install uv

requirements-dev.txt: setup
	uv pip compile requirements-dev.in -o requirements-dev.txt

requirements.txt: setup
	uv pip compile requirements.in -o requirements.txt

virtual-environment: requirements.txt
	python -m venv venv
	uv pip sync requirements.txt

dev:
	uv pip sync requirements-dev.txt

quick-sync: requirements.txt requirements-dev.txt dev
	@echo "Sync finished"
