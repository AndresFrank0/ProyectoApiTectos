# src/dashboard/api/routers.py

from typing import Any, Dict, List
from fastapi import APIRouter, Depends, Security
from sqlmodel import Session

# Importa las dependencias desde la ubicación correcta en 'core'
from src.core.dependencies import get_current_user, get_db_session
from src.dashboard.application.services import DashboardService
from src.auth.domain.entities import User

# Define el router del dashboard
router = APIRouter()


def get_dashboard_service(
    session: Session = Depends(get_db_session),
) -> DashboardService:
    """Dependencia para obtener el servicio del dashboard."""
    return DashboardService(db_session=session)


@router.get("/dashboard/metrics", response_model=Dict[str, Any])
def get_metrics(
    # Protege el endpoint y asegura que el usuario sea un admin
    current_user: User = Security(get_current_user, scopes=["admin:read"]),
    dashboard_service: DashboardService = Depends(get_dashboard_service),
):
    """
    Endpoint para obtener métricas generales.
    Requiere rol de 'admin'.
    """
    return dashboard_service.get_general_metrics()


@router.get("/dashboard/reservations-by-day", response_model=List[Dict[str, Any]])
def get_reservations_by_day(
    current_user: User = Security(get_current_user, scopes=["admin:read"]),
    dashboard_service: DashboardService = Depends(get_dashboard_service),
):
    """
    Endpoint para obtener el número de reservas por día.
    Requiere rol de 'admin'.
    """
    return dashboard_service.get_reservations_per_day()


@router.get("/dashboard/top-restaurants", response_model=List[Dict[str, Any]])
def get_top_restaurants(
    current_user: User = Security(get_current_user, scopes=["admin:read"]),
    dashboard_service: DashboardService = Depends(get_dashboard_service),
):
    """
    Endpoint para obtener los restaurantes más populares.
    Requiere rol de 'admin'.
    """
    return dashboard_service.get_top_restaurants()