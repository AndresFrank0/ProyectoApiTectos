# src/auth/infrastructure/models.py
import uuid
from sqlmodel import Field, SQLModel
from src.auth.domain.entities import UserRole

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    hashed_password: str
    role: UserRole = Field(default=UserRole.CLIENT)