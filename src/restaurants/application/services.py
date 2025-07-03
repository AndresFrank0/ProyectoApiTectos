from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from src.core.errors import NotFoundError, AlreadyExistsError, ValidationError
from src.restaurants.domain.entities import Restaurant, Table, Reservation, Customer
from src.restaurants.domain.repositories import (
    RestaurantRepository,
    ReservationRepository,
)
from src.restaurants.domain.validators import ReservationValidator


class RestaurantService:
    """
    Servicio de aplicación para la gestión de restaurantes y la búsqueda de disponibilidad.
    """

    def __init__(self, restaurant_repository: RestaurantRepository):
        self.restaurant_repository = restaurant_repository

    def get_all_restaurants(self) -> List[Restaurant]:
        """Obtiene una lista de todos los restaurantes."""
        return self.restaurant_repository.list_all()

    def get_restaurant_details(self, restaurant_id: UUID) -> Optional[Restaurant]:
        """Obtiene los detalles de un restaurante específico."""
        restaurant = self.restaurant_repository.get_by_id(restaurant_id)
        if not restaurant:
            raise NotFoundError("Restaurante no encontrado.")
        return restaurant

    def find_available_tables(
        self, restaurant_id: UUID, reservation_date: date, party_size: int
    ) -> List[Table]:
        """
        Encuentra mesas disponibles para una fecha y tamaño de grupo.
        """
        if not self.get_restaurant_details(restaurant_id): # Valida existencia
            raise NotFoundError("Restaurante no encontrado.")

        return self.restaurant_repository.find_available_tables(
            restaurant_id, reservation_date, party_size
        )


class ReservationService:
    """
    Servicio de aplicación para la creación y gestión de reservas.
    """

    def __init__(
        self,
        reservation_repository: ReservationRepository,
        restaurant_repository: RestaurantRepository,
        reservation_validator: ReservationValidator,
    ):
        self.reservation_repository = reservation_repository
        self.restaurant_repository = restaurant_repository
        self.reservation_validator = reservation_validator

    def create_reservation(
        self,
        restaurant_id: UUID,
        customer_data: dict,
        reservation_time: datetime,
        party_size: int,
    ) -> Reservation:
        """
        Crea una nueva reserva, validando la disponibilidad y las reglas de negocio.
        """
        restaurant = self.restaurant_repository.get_by_id(restaurant_id)
        if not restaurant:
            raise NotFoundError("Restaurante no encontrado.")

        # Validar la reserva
        self.reservation_validator.validate(
            restaurant, reservation_time, party_size
        )

        # Buscar si la mesa está reservada
        available_tables = self.restaurant_repository.find_available_tables(
            restaurant_id, reservation_time.date(), party_size
        )
        if not available_tables:
            raise ValidationError("No hay mesas disponibles para los criterios seleccionados.")

        # Seleccionar la primera mesa disponible (lógica simple)
        table_to_book = available_tables[0]

        # Verificar si la mesa específica ya fue tomada en ese instante
        if self.reservation_repository.is_table_booked(
            table_to_book.id, reservation_time
        ):
            raise AlreadyExistsError(
                "La mesa acaba de ser reservada por otro usuario."
            )

        # Crear o encontrar al cliente
        customer = self.reservation_repository.find_customer_by_email(
            customer_data["email"]
        )
        if not customer:
            customer = self.reservation_repository.create_customer(
                Customer(**customer_data)
            )

        # Crear la reserva
        reservation = Reservation(
            restaurant_id=restaurant_id,
            customer_id=customer.id,
            table_id=table_to_book.id,
            reservation_time=reservation_time,
            party_size=party_size,
        )

        return self.reservation_repository.create(reservation)

    def get_reservation_details(self, reservation_id: UUID) -> Optional[Reservation]:
        """Obtiene los detalles de una reserva."""
        reservation = self.reservation_repository.get_by_id(reservation_id)
        if not reservation:
            raise NotFoundError("Reserva no encontrada.")
        return reservation

    def get_user_reservations(self, user_id: UUID) -> List[Reservation]:
        """Obtiene todas las reservas de un usuario (cliente)."""
        return self.reservation_repository.get_by_customer_id(user_id)