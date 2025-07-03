# src/auth/domain/entities.py
import uuid
from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr

from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: Optional[str] = None
    role: str = Field(default="client") # Por defecto, todos son clientes
    is_active: bool = Field(default=True)


class UserRole(str, Enum):
    CLIENT = "client"
    ADMIN = "admin"