#!/bin/bash

echo "Rodando alembic upgrade head..."
python -m alembic upgrade head 2>&1 | tee alembic.log

echo "Subindo uvicorn..."
uvicorn src.main:app --host 0.0.0.0 --port 8000
