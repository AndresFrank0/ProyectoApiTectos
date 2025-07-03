# src/auth/infrastructure/repositories.py

from typing import Optional
from sqlmodel import Session, select

# Importa la entidad desde el DOMINIO, no desde un archivo local
from src.auth.domain.entities import User
from src.auth.domain.ports import UserRepository

class PostgresUserRepository(UserRepository):
    """
    Implementación del repositorio de usuarios para PostgreSQL.
    """

    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por su correo electrónico."""
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def save(self, user: User) -> User:
        """Guarda un nuevo usuario en la base de datos."""
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user