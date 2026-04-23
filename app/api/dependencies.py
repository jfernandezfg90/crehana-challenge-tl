from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.infrastructure.auth.jwt_handler import decode_token
from app.infrastructure.database.connection import SessionLocal
from app.infrastructure.database.repositories.sql_user_repository import (
    SQLUserRepository,
)

bearer_scheme = HTTPBearer()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if not user_id:
            raise ValueError("Token sin identificador de usuario")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticacion invalido",
        )

    from uuid import UUID

    user_repo = SQLUserRepository(db)
    user = user_repo.get_by_id(UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado"
        )
    return user
