from typing import Optional
from pydantic import BaseModel, EmailStr
import uuid

# Esquema para la creación de un nuevo usuario
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


# Esquema para leer los datos de un usuario (sin la contraseña)
class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: Optional[str] = None
    role: str

    class Config:
        orm_mode = True


# Esquema para el token JWT
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    scopes: list[str] = []