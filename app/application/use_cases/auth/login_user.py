from passlib.context import CryptContext

"""
Caso de uso para el inicio de sesión de usuarios.
Valida las credenciales y genera un token JWT.
"""

from app.domain.exceptions.domain_exceptions import InvalidCredentialsException
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.auth.jwt_handler import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, email: str, password: str) -> dict:
        user = self.user_repository.get_by_email(email)
        if not user or not pwd_context.verify(password, user.hashed_password):
            raise InvalidCredentialsException()

        token = create_access_token(data={"sub": str(user.id), "email": user.email})
        return {"access_token": token, "token_type": "bearer"}
