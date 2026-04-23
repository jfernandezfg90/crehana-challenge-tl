"""
Router de Autenticación.
Maneja el registro de usuarios y el inicio de sesión para obtener tokens JWT.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.api.v1.schemas.auth_schemas import (
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)
from app.application.use_cases.auth.login_user import LoginUserUseCase
from app.application.use_cases.auth.register_user import RegisterUserUseCase
from app.domain.entities.user import User
from app.infrastructure.database.repositories.sql_user_repository import (
    SQLUserRepository,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(body: UserRegister, db: Session = Depends(get_db)):
    repo = SQLUserRepository(db)
    use_case = RegisterUserUseCase(repo)
    user = use_case.execute(email=body.email, password=body.password, name=body.name)
    return UserResponse(
        id=user.id, email=user.email, name=user.name, created_at=user.created_at
    )


@router.post("/login", response_model=TokenResponse)
def login(body: UserLogin, db: Session = Depends(get_db)):
    repo = SQLUserRepository(db)
    use_case = LoginUserUseCase(repo)
    return use_case.execute(email=body.email, password=body.password)


@router.get("/users", response_model=list[UserResponse], tags=["Users"])
def list_users(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    repo = SQLUserRepository(db)
    users = repo.list_all()
    return [
        UserResponse(id=u.id, email=u.email, name=u.name, created_at=u.created_at)
        for u in users
    ]
