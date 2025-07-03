# src/auth/domain/ports.py

from abc import ABC, abstractmethod
from typing import Optional

from .entities import User


class PasswordManager(ABC):
    """
    Interfaz para la gestión de contraseñas.
    """

    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Convierte una contraseña de texto plano a un hash."""
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica si una contraseña coincide con su hash."""
        pass


class TokenService(ABC):
    """
    Interfaz para la creación y validación de tokens JWT.
    """

    @abstractmethod
    def create_access_token(self, data: dict) -> str:
        """Crea un nuevo token de acceso."""
        pass

    @abstractmethod
    def decode_token(self, token: str) -> Optional[dict]:
        """
        Decodifica un token, retornando su payload (contenido) si es válido.
        """
        pass


class UserRepository(ABC):
    """
    Interfaz para el repositorio de usuarios.
    ESTA ES LA CLASE QUE FALTA O ESTÁ INCORRECTA.
    """

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por su correo electrónico."""
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        """Guarda un nuevo usuario en la base de datos."""
        pass