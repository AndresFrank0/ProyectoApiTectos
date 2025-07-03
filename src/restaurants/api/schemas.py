from datetime import datetime, date, time
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


# Schemas base para entidades
class TableBase(BaseModel):
    capacity: int


class RestaurantBase(BaseModel):
    name: str
    address: str
    phone: str
    cuisine_type: str


class ReservationBase(BaseModel):
    reservation_time: datetime
    party_size: int = Field(..., gt=0, description="El tamaño del grupo debe ser mayor a 0")


class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str


# Schemas para creación de entidades
class CreateReservationRequest(BaseModel):
    restaurant_id: UUID
    customer: CustomerBase
    reservation_time: datetime
    party_size: int


# Schemas para respuestas de la API
class TableResponse(TableBase):
    id: UUID

    class Config:
        orm_mode = True


class TimeSlotResponse(BaseModel):
    time: time
    is_available: bool


class RestaurantResponse(RestaurantBase):
    id: UUID
    opening_time: time
    closing_time: time

    class Config:
        orm_mode = True


class RestaurantDetailsResponse(RestaurantResponse):
    tables: List[TableResponse] = []


class AvailabilityResponse(BaseModel):
    table: TableResponse
    available_slots: List[TimeSlotResponse]


class ReservationResponse(ReservationBase):
    id: UUID
    restaurant_id: UUID
    customer_id: UUID
    table_id: UUID
    status: str

    class Config:
        orm_mode = True