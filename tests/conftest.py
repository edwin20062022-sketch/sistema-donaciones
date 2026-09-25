from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def user_token(client: TestClient) -> str:
    response = client.post("/auth/register", json={"nombre": "Usuario", "correo": "user@example.com", "password": "Password1!"})
    assert response.status_code == 201
    return client.post("/auth/login", json={"correo": "user@example.com", "password": "Password1!"}).json()["access_token"]


@pytest.fixture()
def admin_token(client: TestClient) -> str:
    from app.database import get_db
    from app.models import User
    from app.security import hash_password

    db = next(app.dependency_overrides[get_db]())
    db.add(User(nombre="Admin", correo="admin@example.com", password_hash=hash_password("AdminPass1!"), role="admin"))
    db.commit()
    db.close()
    return client.post("/auth/login", json={"correo": "admin@example.com", "password": "AdminPass1!"}).json()["access_token"]


@pytest.fixture()
def donor_payload():
    return {
        "nombre": "Banco de Alimentos",
        "correo": "donante@example.com",
        "telefono": "6141234567",
        "tipo": "organizacion",
        "recurso": "alimentos",
    }

