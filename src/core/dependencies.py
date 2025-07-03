# src/core/dependencies.py

from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlmodel import Session

from src.auth.application.services import AuthService
from src.auth.domain.entities import User
from src.auth.domain.ports import PasswordManager, TokenService, UserRepository
from src.auth.infrastructure.repositories import PostgresUserRepository
from src.auth.infrastructure.security import JoseTokenService, PasslibPasswordManager
from src.core.database import engine
from src.core.errors import InvalidCredentialsError
from src.restaurants.application.services import RestaurantService, ReservationService
from src.restaurants.domain.repositories import ReservationRepository, RestaurantRepository
from src.restaurants.domain.validators import ReservationValidator
from src.restaurants.infrastructure.repositories import SQLModelReservationRepository, SQLModelRestaurantRepository

# --- Dependencia de Sesión de Base de Datos ---
def get_db_session() -> Generator[Session, None, None]:
    """
    Crea y proporciona una sesión de base de datos por petición.
    """
    with Session(engine) as session:
        yield session

# --- Dependencias de Autenticación (Auth) ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_password_manager() -> PasswordManager:
    return PasslibPasswordManager()

def get_token_service() -> TokenService:
    return JoseTokenService()

def get_user_repository(session: Session = Depends(get_db_session)) -> UserRepository:
    return PostgresUserRepository(session)

def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    password_manager: PasswordManager = Depends(get_password_manager),
    token_service: TokenService = Depends(get_token_service),
) -> AuthService:
    return AuthService(user_repo, password_manager, token_service)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    token_service: TokenService = Depends(get_token_service),
    user_repo: UserRepository = Depends(get_user_repository),
) -> User:
    """
    Decodifica el token, obtiene el usuario y lo devuelve.
    Esta es la dependencia principal para proteger endpoints.
    """
    try:
        payload = token_service.decode_token(token)
        if payload is None or "sub" not in payload:
            raise InvalidCredentialsError("Token inválido.")
        
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise InvalidCredentialsError("Token inválido.")

        user = user_repo.get_by_email(email)
        if user is None:
            raise InvalidCredentialsError("Usuario no encontrado.")
        return user
    except JWTError:
        raise InvalidCredentialsError("No se pudo validar el token.")

# --- Dependencias de Restaurantes y Reservas ---
def get_restaurant_repository(session: Session = Depends(get_db_session)) -> RestaurantRepository:
    return SQLModelRestaurantRepository(session)

def get_reservation_repository(session: Session = Depends(get_db_session)) -> ReservationRepository:
    return SQLModelReservationRepository(session)

def get_restaurant_service(repo: RestaurantRepository = Depends(get_restaurant_repository)) -> RestaurantService:
    return RestaurantService(restaurant_repository=repo)
    
def get_reservation_validator() -> ReservationValidator:
    return ReservationValidator()

def get_reservation_service(
    res_repo: ReservationRepository = Depends(get_reservation_repository),
    rest_repo: RestaurantRepository = Depends(get_restaurant_repository),
    validator: ReservationValidator = Depends(get_reservation_validator),
) -> ReservationService:
    return ReservationService(
        reservation_repository=res_repo,
        restaurant_repository=rest_repo,
        reservation_validator=validator,
    )