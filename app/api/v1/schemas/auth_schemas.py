"""
Esquemas de validación (Pydantic) para la autenticación.
Define la estructura de datos para el registro, inicio de sesión y respuestas de token.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    name: str
    created_at: datetime
