# src/reservations/domain/services.py
from datetime import datetime, timedelta
from typing import List
from.entities import Reservation
from src.restaurants.domain.entities import Restaurant, Table
from src.menu.domain.entities import Dish

class ReservationValidator:
    def validate_new_reservation(
        self,
        reservation_to_create: Reservation,
        client_reservations: List,
        table_reservations: List,
        restaurant: Restaurant,
        table: Table,
        preordered_dishes: List
    ):
        # 1. Validar que la reserva esté dentro del horario del restaurante
        if not (restaurant.opening_time <= reservation_to_create.reservation_time.time() < restaurant.closing_time and
                restaurant.opening_time < reservation_to_create.end_time.time() <= restaurant.closing_time):
            raise ValueError("Reservation time is outside of restaurant operating hours.")

        # 2. Validar que la mesa tenga capacidad suficiente
        if reservation_to_create.number_of_guests > table.capacity:
            raise ValueError("Number of guests exceeds table capacity.")

        # 3. Validar solapamiento de reservas para la mesa
        for existing_res in table_reservations:
            if self._reservations_overlap(reservation_to_create, existing_res):
                raise ValueError(f"Table {table.table_number} is already booked at this time.")

        # 4. Validar que el cliente no tenga otra reserva en el mismo horario
        for client_res in client_reservations:
            if self._reservations_overlap(reservation_to_create, client_res):
                raise ValueError("Client already has a reservation at this time.")

        # 5. Validar pre-orden
        if reservation_to_create.preordered_dishes:
            if len(reservation_to_create.preordered_dishes) > 5:
                raise ValueError("Cannot pre-order more than 5 unique dishes.")
            
            preordered_dish_ids = {item.dish_id for item in reservation_to_create.preordered_dishes}
            available_dish_ids = {dish.id for dish in preordered_dishes if dish.is_available and dish.restaurant_id == restaurant.id}
            
            if not preordered_dish_ids.issubset(available_dish_ids):
                raise ValueError("One or more pre-ordered dishes are invalid or do not belong to this restaurant.")


    def can_client_cancel(self, reservation: Reservation) -> bool:
        # El cliente puede cancelar con al menos 1 hora de antelación
        return reservation.reservation_time - datetime.now(reservation.reservation_time.tzinfo) > timedelta(hours=1)

    def _reservations_overlap(self, res1: Reservation, res2: Reservation) -> bool:
        return res1.reservation_time < res2.end_time and res2.reservation_time < res1.end_time