#!/bin/bash

# Rodar as migrations
alembic upgrade head

# Subir o servidor Uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000
