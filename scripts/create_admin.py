"""Crea o actualiza un administrador sin permitir altas públicas con ese rol."""

from __future__ import annotations

import os

from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.models import User
from app.security import hash_password


def main() -> None:
    nombre = os.getenv("ADMIN_NAME")
    correo = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")
    if not all((nombre, correo, password)):
        raise SystemExit("Define ADMIN_NAME, ADMIN_EMAIL y ADMIN_PASSWORD antes de ejecutar el script.")
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.correo == correo.lower()))
        if user is None:
            user = User(nombre=nombre, correo=correo.lower(), password_hash=hash_password(password), role="admin")
            db.add(user)
        else:
            user.nombre = nombre
            user.password_hash = hash_password(password)
            user.role = "admin"
        db.commit()
    print(f"Administrador listo: {correo.lower()}")


if __name__ == "__main__":
    main()

