"""
Punto de entrada principal para la aplicación FastAPI.
Maneja middlewares, routers, errores y sirve el frontend.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.api.error_handlers import register_error_handlers
from app.api.v1.routers.auth_router import router as auth_router
from app.api.v1.routers.task_list_router import router as task_list_router
from app.api.v1.routers.task_router import router as task_router
from app.infrastructure.database import models as _models  # noqa: F401
from app.infrastructure.database.connection import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Crehana Task Manager API",
    description="API REST para gestionar listas de tareas — Crehana Backend Challenge",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_error_handlers(app)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(task_list_router, prefix="/api/v1")
app.include_router(task_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


# ─── Frontend ────────────────────────────────────────────────────────────────


@app.get("/", include_in_schema=False)
def serve_login():
    return FileResponse("frontend/index.html")


@app.get("/dashboard", include_in_schema=False)
def serve_dashboard():
    return FileResponse("frontend/dashboard.html")


@app.get("/static/style.css", include_in_schema=False)
def serve_css():
    return FileResponse("frontend/style.css", media_type="text/css")


@app.get("/static/logo.png", include_in_schema=False)
def serve_logo():
    return FileResponse("assets/logo.png", media_type="image/png")


@app.get("/static/isotipo.png", include_in_schema=False)
def serve_isotipo():
    return FileResponse("assets/isotipo.png", media_type="image/png")
