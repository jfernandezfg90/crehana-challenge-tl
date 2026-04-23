"""
Interfaz para el repositorio de usuarios.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    def list_all(self) -> List[User]:
        pass
