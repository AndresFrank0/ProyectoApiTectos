from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from .entities import Customer, Reservation, Restaurant, Table


class RestaurantRepository(ABC):
    """
    Interfaz para el repositorio de restaurantes.
    """
    @abstractmethod
    def get_by_id(self, restaurant_id: UUID) -> Optional[Restaurant]:
        pass

    @abstractmethod
    def list_all(self) -> List[Restaurant]:
        pass

    @abstractmethod
    def find_available_tables(
        self, restaurant_id: UUID, reservation_date: date, party_size: int
    ) -> List[Table]:
        pass


class ReservationRepository(ABC):
    """
    Interfaz para el repositorio de reservas.
    """
    @abstractmethod
    def create(self, reservation: Reservation) -> Reservation:
        pass

    @abstractmethod
    def get_by_id(self, reservation_id: UUID) -> Optional[Reservation]:
        pass

    @abstractmethod
    def get_by_customer_id(self, customer_id: UUID) -> List[Reservation]:
        pass

    @abstractmethod
    def is_table_booked(self, table_id: UUID, reservation_time: datetime) -> bool:
        pass

    @abstractmethod
    def find_customer_by_email(self, email: str) -> Optional[Customer]:
        pass
    
    @abstractmethod
    def create_customer(self, customer: Customer) -> Customer:
        pass