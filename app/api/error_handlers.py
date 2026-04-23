from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.domain_exceptions import (
    InvalidCredentialsException,
    InvalidTaskStatusTransitionException,
    TaskListNotFoundException,
    TaskNotFoundException,
    UnauthorizedAccessException,
    UserAlreadyExistsException,
    UserNotFoundException,
)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(TaskListNotFoundException)
    async def task_list_not_found(request: Request, exc: TaskListNotFoundException):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(TaskNotFoundException)
    async def task_not_found(request: Request, exc: TaskNotFoundException):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(UserNotFoundException)
    async def user_not_found(request: Request, exc: UserNotFoundException):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(UserAlreadyExistsException)
    async def user_already_exists(request: Request, exc: UserAlreadyExistsException):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials(request: Request, exc: InvalidCredentialsException):
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @app.exception_handler(UnauthorizedAccessException)
    async def unauthorized(request: Request, exc: UnauthorizedAccessException):
        return JSONResponse(status_code=403, content={"detail": str(exc)})

    @app.exception_handler(InvalidTaskStatusTransitionException)
    async def invalid_transition(
        request: Request, exc: InvalidTaskStatusTransitionException
    ):
        return JSONResponse(status_code=422, content={"detail": str(exc)})
