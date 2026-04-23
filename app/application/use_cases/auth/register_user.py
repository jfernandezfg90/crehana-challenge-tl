"""
Caso de uso para el registro de nuevos usuarios.
Valida que el email no exista y persiste al nuevo usuario con su contraseña hasheada.
"""

from passlib.context import CryptContext

from app.domain.entities.user import User
from app.domain.exceptions.domain_exceptions import UserAlreadyExistsException
from app.domain.repositories.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, email: str, password: str, name: str) -> User:
        existing = self.user_repository.get_by_email(email)
        if existing:
            raise UserAlreadyExistsException(email)

        hashed_password = pwd_context.hash(password)
        user = User(email=email, hashed_password=hashed_password, name=name)
        return self.user_repository.create(user)
