from collections import Counter
from typing import Dict, Any, List
from uuid import UUID

from sqlmodel import Session, select, func

from src.restaurants.domain.entities import Reservation, Restaurant


class DashboardService:
    """
    Servicio para obtener datos agregados para el panel de control.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_general_metrics(self) -> Dict[str, Any]:
        """
        Obtiene métricas generales como el número total de reservas y restaurantes.
        """
        total_reservations = self.db_session.exec(
            select(func.count(Reservation.id))
        ).one()
        total_restaurants = self.db_session.exec(
            select(func.count(Restaurant.id))
        ).one()

        return {
            "total_reservations": total_reservations,
            "total_restaurants": total_restaurants,
        }

    def get_reservations_per_day(self) -> List[Dict[str, Any]]:
        """
        Obtiene el número de reservas agrupadas por día.
        """
        statement = select(
            func.date(Reservation.reservation_time).label("day"),
            func.count(Reservation.id).label("count"),
        ).group_by("day").order_by("day")

        result = self.db_session.exec(statement).all()
        return [{"day": row.day.isoformat(), "count": row.count} for row in result]

    def get_top_restaurants(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Obtiene los restaurantes con más reservas.
        """
        statement = (
            select(
                Restaurant.name,
                func.count(Reservation.id).label("reservation_count"),
            )
            .join(Reservation)
            .group_by(Restaurant.name)
            .order_by(func.count(Reservation.id).desc())
            .limit(limit)
        )
        result = self.db_session.exec(statement).all()
        return [{"restaurant_name": row.name, "count": row.reservation_count} for row in result]