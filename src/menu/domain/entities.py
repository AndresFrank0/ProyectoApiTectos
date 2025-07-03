# src/menu/domain/entities.py
import uuid
from enum import Enum
from pydantic import BaseModel, Field

class DishCategory(str, Enum):
    ENTRADA = "Entrada"
    PRINCIPAL = "Principal"
    POSTRE = "Postre"
    BEBIDA = "Bebida"

class Dish(BaseModel):
    id: uuid.UUID
    restaurant_id: uuid.UUID
    name: str
    description: str
    category: DishCategory
    image_url: str | None = None
    is_available: bool = True

    class Config:
        from_attributes = True