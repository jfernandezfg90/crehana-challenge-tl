from unittest.mock import MagicMock

import pytest

from app.application.use_cases.auth.login_user import LoginUserUseCase
from app.application.use_cases.auth.register_user import RegisterUserUseCase
from app.domain.entities.user import User
from app.domain.exceptions.domain_exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
)


def make_user(email="test@example.com"):
    return User(email=email, hashed_password="hashed", name="Test")


class TestRegisterUser:
    def test_registers_new_user(self):
        repo = MagicMock()
        repo.get_by_email.return_value = None
        user = make_user()
        repo.create.return_value = user

        result = RegisterUserUseCase(repo).execute(
            "test@example.com", "pass123", "Test"
        )

        repo.create.assert_called_once()
        assert result.email == "test@example.com"

    def test_raises_if_email_exists(self):
        repo = MagicMock()
        repo.get_by_email.return_value = make_user()

        with pytest.raises(UserAlreadyExistsException):
            RegisterUserUseCase(repo).execute("test@example.com", "pass", "T")

    def test_password_is_hashed(self):
        repo = MagicMock()
        repo.get_by_email.return_value = None
        repo.create.side_effect = lambda u: u

        result = RegisterUserUseCase(repo).execute("a@b.com", "plaintext", "T")
        assert result.hashed_password != "plaintext"


class TestLoginUser:
    def test_returns_token_on_valid_credentials(self):
        repo = MagicMock()
        from passlib.context import CryptContext

        ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
        user = User(
            email="t@t.com",
            hashed_password=ctx.hash("secret"),
            name="T",
        )
        repo.get_by_email.return_value = user

        result = LoginUserUseCase(repo).execute("t@t.com", "secret")

        assert "access_token" in result
        assert result["token_type"] == "bearer"

    def test_raises_on_wrong_password(self):
        repo = MagicMock()
        from passlib.context import CryptContext

        ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
        user = User(email="t@t.com", hashed_password=ctx.hash("correct"), name="T")
        repo.get_by_email.return_value = user

        with pytest.raises(InvalidCredentialsException):
            LoginUserUseCase(repo).execute("t@t.com", "wrong")

    def test_raises_when_user_not_found(self):
        repo = MagicMock()
        repo.get_by_email.return_value = None

        with pytest.raises(InvalidCredentialsException):
            LoginUserUseCase(repo).execute("no@one.com", "pass")
