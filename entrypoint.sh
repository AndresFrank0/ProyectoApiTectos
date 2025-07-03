#!/bin/bash

# Aplicar migraciones de la base de datos
echo "Applying database migrations..."
alembic upgrade head

# Iniciar la aplicación FastAPI
echo "Starting FastAPI server..."
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload