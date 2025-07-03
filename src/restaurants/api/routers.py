from datetime import date
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dependencies import get_restaurant_service, get_reservation_service
from src.core.errors import NotFoundError, ValidationError, AlreadyExistsError
from src.restaurants.api.schemas import (
    RestaurantResponse,
    RestaurantDetailsResponse,
    AvailabilityResponse,
    CreateReservationRequest,
    ReservationResponse,
)
from src.restaurants.application.services import RestaurantService, ReservationService

router = APIRouter(tags=["Restaurants"])


@router.get("/restaurants", response_model=List[RestaurantResponse])
def list_restaurants(
    restaurant_service: RestaurantService = Depends(get_restaurant_service),
):
    """Obtiene una lista de todos los restaurantes."""
    return restaurant_service.get_all_restaurants()


@router.get("/restaurants/{restaurant_id}", response_model=RestaurantDetailsResponse)
def get_restaurant_details(
    restaurant_id: UUID,
    restaurant_service: RestaurantService = Depends(get_restaurant_service),
):
    """Obtiene los detalles de un restaurante, incluyendo sus mesas."""
    try:
        return restaurant_service.get_restaurant_details(restaurant_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/restaurants/{restaurant_id}/availability",
    response_model=List[AvailabilityResponse],
)
def get_availability(
    restaurant_id: UUID,
    reservation_date: date,
    party_size: int,
    restaurant_service: RestaurantService = Depends(get_restaurant_service),
):
    """
    Obtiene la disponibilidad de mesas para un restaurante, fecha y número de comensales.
    """
    try:
        # Aquí se debería implementar una lógica más compleja para generar los slots
        # Por simplicidad, se devuelve una lista de mesas disponibles
        available_tables = restaurant_service.find_available_tables(
            restaurant_id, reservation_date, party_size
        )
        # Esto es una simulación. En un caso real, se generarían los TimeSlots.
        response = [
            AvailabilityResponse(table=table, available_slots=[])
            for table in available_tables
        ]
        return response
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
    "/reservations",
    response_model=ReservationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_reservation(
    request: CreateReservationRequest,
    reservation_service: ReservationService = Depends(get_reservation_service),
):
    """Crea una nueva reserva."""
    try:
        reservation = reservation_service.create_reservation(
            restaurant_id=request.restaurant_id,
            customer_data=request.customer.dict(),
            reservation_time=request.reservation_time,
            party_size=request.party_size,
        )
        return reservation
    except (NotFoundError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error inesperado al crear la reserva.",
        )