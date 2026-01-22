#!/bin/bash

# uv run sh -c "alembic upgrade head; python -m src.main"
# DB migration
alembic upgrade head

# Run main script
python -m src.main
