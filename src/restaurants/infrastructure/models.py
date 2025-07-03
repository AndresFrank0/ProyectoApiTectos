# src/restaurants/infrastructure/models.py
import uuid
from datetime import time
from typing import List
from sqlmodel import Field, SQLModel, Relationship

class Restaurant(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    location: str
    opening_time: time
    closing_time: time
    tables: List = Relationship(back_populates="restaurant", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class Table(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    restaurant_id: uuid.UUID = Field(foreign_key="restaurant.id", index=True)
    table_number: int
    capacity: int
    location_in_restaurant: str
    restaurant: Restaurant = Relationship(back_populates="tables")