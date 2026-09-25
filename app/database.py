"""Configuración de SQLAlchemy y sesiones de base de datos."""

from __future__ import annotations

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./donaciones.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Base(DeclarativeBase):
    """Clase base declarativa para los modelos."""


def get_db() -> Generator[Session, None, None]:
    """Entrega una sesión y garantiza su cierre al terminar la solicitud."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

