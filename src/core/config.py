# src/core/config.py

from pydantic import Extra
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "El Buen Sabor API"
    
    # Base de Datos
    DATABASE_URL: str

    # Seguridad y JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- INICIO DE LA SOLUCIÓN ---
    # Le decimos a Pydantic que ignore los campos extra del .env
    class Config:
        env_file = ".env"
        extra = "ignore" 
    # --- FIN DE LA SOLUCIÓN ---

# Se crea una única instancia que será usada en toda la app
settings = Settings()