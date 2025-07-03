import uuid
from datetime import datetime, time
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

# --- Entidad Customer (Cliente) ---
# Modelo para almacenar la información de contacto de quien hace la reserva
class Customer(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    email: str = Field(index=True)
    phone: str

    reservations: List["Reservation"] = Relationship(back_populates="customer")

# --- Entidad Restaurant (Restaurante) ---
class Restaurant(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    address: str
    phone: str
    cuisine_type: str
    opening_time: time
    closing_time: time

    tables: List["Table"] = Relationship(back_populates="restaurant")
    reservations: List["Reservation"] = Relationship(back_populates="restaurant")

# --- Entidad Table (Mesa) ---
class Table(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    table_number: int
    capacity: int

    restaurant_id: uuid.UUID = Field(foreign_key="restaurant.id")
    restaurant: Restaurant = Relationship(back_populates="tables")

    reservations: List["Reservation"] = Relationship(back_populates="table")

# --- Entidad Reservation (Reserva) ---
class Reservation(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    reservation_time: datetime
    party_size: int
    status: str = Field(default="confirmed") # Cambiado de 'pending' a 'confirmed' para simplificar

    # Relaciones con otras tablas
    restaurant_id: uuid.UUID = Field(foreign_key="restaurant.id")
    restaurant: Restaurant = Relationship(back_populates="reservations")

    table_id: uuid.UUID = Field(foreign_key="table.id")
    table: Table = Relationship(back_populates="reservations")

    customer_id: uuid.UUID = Field(foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="reservations")