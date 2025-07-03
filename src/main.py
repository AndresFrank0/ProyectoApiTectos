from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar los routers de los diferentes módulos de la aplicación
from src.auth.api.routers import router as auth_router
from src.core.config import settings
from src.dashboard.api.routers import router as dashboard_router
from src.restaurants.api.routers import router as restaurants_router

# Crear la instancia principal de la aplicación FastAPI
app = FastAPI(title=settings.PROJECT_NAME)

# --- Configuración de CORS ---
# Permite que un frontend se comunique con tu API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, deberías restringir esto a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Inclusión de Routers ---
# Aquí se añaden todos los endpoints a la aplicación principal
app.include_router(auth_router, prefix="/api/v1", tags=["Authentication"])
app.include_router(restaurants_router, prefix="/api/v1", tags=["Restaurants & Reservations"])
app.include_router(dashboard_router, prefix="/api/v1", tags=["Dashboard"])


# --- Endpoint Raíz ---
# Un endpoint simple para verificar que la API está funcionando
@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raíz para verificar el estado de la API.
    """
    return {"message": "Bienvenido a la API de El Buen Sabor"}