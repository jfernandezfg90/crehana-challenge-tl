"""
Repositorio SQL para Usuarios.
Implementa UserRepository utilizando SQLAlchemy.
"""

from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.models.user_model import UserModel


class SQLUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            hashed_password=model.hashed_password,
            name=model.name,
            created_at=model.created_at,
        )

    def create(self, user: User) -> User:
        model = UserModel(
            id=user.id,
            email=user.email,
            hashed_password=user.hashed_password,
            name=user.name,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def get_by_email(self, email: str) -> Optional[User]:
        model = self.session.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(model) if model else None

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        model = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(model) if model else None

    def list_all(self) -> list[User]:
        return [
            self._to_entity(m)
            for m in self.session.query(UserModel).order_by(UserModel.name).all()
        ]
