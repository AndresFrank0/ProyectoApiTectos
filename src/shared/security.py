# src/shared/security.py
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from typing import Annotated
from sqlmodel import Session
from src.shared.database import get_session
from src.auth.domain.entities import User
from src.auth.infrastructure.repositories import PostgresUserRepository
from src.auth.infrastructure.security import JwtTokenManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated,
    session: Session = Depends(get_session)
) -> User:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    token_manager = JwtTokenManager()
    payload = token_manager.decode_token(token)
    
    if payload is None or "sub" not in payload:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    user_repo = PostgresUserRepository(session)
    user = user_repo.get_by_email(email)
    if user is None:
        raise credentials_exception

    token_scopes = payload.get("scopes",)
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
            
    return user

# Helper dependencies for role checks
def require_admin(current_user: Annotated)]):
    return current_user

def require_client(current_user: Annotated)]):
    return current_user