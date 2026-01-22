#!/bin/bash

uv run sh -c "alembic upgrade head; python -m src.main"
