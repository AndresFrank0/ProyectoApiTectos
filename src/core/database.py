# src/core/database.py

from sqlmodel import create_engine
from .config import settings

# El engine es el punto de entrada a la base de datos.
# Se crea una sola vez para toda la aplicación.
engine = create_engine(
    settings.DATABASE_URL,
    echo=True, # Poner en False en producción
    pool_pre_ping=True
)