# src/auth/api/routers.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.application.services import AuthService
from src.core.dependencies import get_auth_service, get_current_user
from src.core.errors import AlreadyExistsError, InvalidCredentialsError
from .schemas import UserCreate, UserRead, Token
from ..domain.entities import User

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(
    user_in: UserCreate, auth_service: AuthService = Depends(get_auth_service)
):
    """
    Endpoint para registrar un nuevo usuario.
    """
    try:
        user = auth_service.register_user(
            email=user_in.email,
            password=user_in.password,
            full_name=user_in.full_name,
        )
        return user
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Endpoint para iniciar sesión y obtener un token de acceso.
    """
    try:
        token = auth_service.login(
            email=form_data.username, # OAuth2PasswordRequestForm usa 'username' para el email
            password=form_data.password
        )
        return {"access_token": token, "token_type": "bearer"}
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Endpoint de prueba para obtener los datos del usuario autenticado.
    """
    return current_user