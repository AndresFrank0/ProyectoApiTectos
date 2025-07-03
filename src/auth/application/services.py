from typing import Optional

# Importa los puertos (interfaces) con los nombres correctos
from src.auth.domain.ports import (
    PasswordManager,
    TokenService,
    UserRepository,
)
from src.auth.domain.entities import User
from src.core.errors import AlreadyExistsError, InvalidCredentialsError


class AuthService:
    """
    Servicio de aplicación que orquesta la lógica de autenticación.
    """
    def __init__(
        self,
        user_repository: UserRepository,
        password_manager: PasswordManager,
        token_service: TokenService,
    ):
        self.user_repository = user_repository
        self.password_manager = password_manager
        self.token_service = token_service

    def register_user(self, email: str, password: str, full_name: str) -> User:
        """Registra un nuevo usuario."""
        if self.user_repository.get_by_email(email):
            raise AlreadyExistsError("El correo electrónico ya está registrado.")

        hashed_password = self.password_manager.hash_password(password)
        new_user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
        )
        return self.user_repository.save(new_user)

    def login(self, email: str, password: str) -> str:
        """Inicia sesión y devuelve un token de acceso."""
        user = self.user_repository.get_by_email(email)
        if not user:
            raise InvalidCredentialsError("Credenciales incorrectas.")

        if not self.password_manager.verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Credenciales incorrectas.")
            
        # Define los scopes según el rol del usuario
        scopes = ["client:read", "client:write"]
        if user.role == "admin":
            scopes.extend(["admin:read", "admin:write", "dashboard:read"])

        token = self.token_service.create_access_token(
            data={"sub": user.email, "scopes": scopes}
        )
        return token