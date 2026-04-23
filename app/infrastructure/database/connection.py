"""
Configuración de la conexión a la base de datos.
Soporta SQLite y PostgreSQL con pooling automático según el entorno.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import NullPool

from app.config import settings

_db_url = settings.database_url

# Fallback para Vercel: Si se usa SQLite, usar /tmp para evitar errores de solo lectura
if _db_url.startswith("sqlite") and "VERCEL" in os.environ:
    _db_url = "sqlite:////tmp/tasks.db"

_is_sqlite = _db_url.startswith("sqlite")

if _is_sqlite:
    # SQLite: local y Docker — pool estandar con check_same_thread
    engine = create_engine(
        _db_url,
        connect_args={"check_same_thread": False},
    )
else:
    # PostgreSQL: Vercel serverless — NullPool evita agotar conexiones
    engine = create_engine(
        _db_url,
        poolclass=NullPool,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
