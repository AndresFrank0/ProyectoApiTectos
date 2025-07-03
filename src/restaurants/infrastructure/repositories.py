# src/restaurants/infrastructure/repositories.py

from datetime import date, time, datetime
from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select, func, and_

# Importa solo las entidades que son tablas de la base de datos
from src.restaurants.domain.entities import (
    Restaurant,
    Table,
    Reservation,
    Customer,
)
from src.restaurants.domain.repositories import (
    RestaurantRepository,
    ReservationRepository,
)


class SQLModelRestaurantRepository(RestaurantRepository):
    """
    Repositorio de restaurantes implementado con SQLModel.
    """

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, restaurant_id: UUID) -> Optional[Restaurant]:
        """Obtiene un restaurante por su ID."""
        return self.session.get(Restaurant, restaurant_id)

    def list_all(self) -> List[Restaurant]:
        """Lista todos los restaurantes."""
        return self.session.exec(select(Restaurant)).all()

    def find_available_tables(
        self, restaurant_id: UUID, reservation_date: date, party_size: int
    ) -> List[Table]:
        """
        Encuentra mesas disponibles para un restaurante, fecha y tamaño de grupo.
        """
        restaurant = self.get_by_id(restaurant_id)
        if not restaurant:
            return []

        # Subconsulta para encontrar mesas que ya tienen una reserva en esa fecha
        booked_tables_subquery = (
            select(Reservation.table_id)
            .where(Reservation.restaurant_id == restaurant_id)
            .where(func.date(Reservation.reservation_time) == reservation_date)
            .where(Reservation.status != "cancelled")
        )

        # Consulta para mesas que cumplen la capacidad y no están en la lista de reservadas
        statement = (
            select(Table)
            .where(Table.restaurant_id == restaurant_id)
            .where(Table.capacity >= party_size)
            .where(Table.id.notin_(booked_tables_subquery))
        )
        return self.session.exec(statement).all()


class SQLModelReservationRepository(ReservationRepository):
    """
    Repositorio de reservas implementado con SQLModel.
    """

    def __init__(self, session: Session):
        self.session = session

    def create(self, reservation: Reservation) -> Reservation:
        """Crea una nueva reserva."""
        self.session.add(reservation)
        self.session.commit()
        self.session.refresh(reservation)