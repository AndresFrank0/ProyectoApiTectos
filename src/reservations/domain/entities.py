# src/reservations/domain/entities.py
import uuid
from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel, Field

class ReservationStatus(str, Enum):
    PENDING = "pendiente"
    CONFIRMED = "confirmada"
    CANCELLED = "cancelada"
    COMPLETED = "completada"

class Reservation(BaseModel):
    id: uuid.UUID
    client_id: uuid.UUID
    table_id: uuid.UUID
    restaurant_id: uuid.UUID
    reservation_time: datetime
    duration_minutes: int = Field(gt=0, le=240) # Max 4 horas
    number_of_guests: int
    status: ReservationStatus = ReservationStatus.PENDING
    preordered_dishes: list =

    @property
    def end_time(self) -> datetime:
        return self.reservation_time + timedelta(minutes=self.duration_minutes)

    class Config:
        from_attributes = True

class ReservationDishLink(BaseModel):
    dish_id: uuid.UUID
    quantity: int = Field(gt=0)
    
    class Config:
        from_attributes = True