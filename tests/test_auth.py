from datetime import timedelta

import jwt

from app.security import JWT_ALGORITHM, JWT_SECRET_KEY, create_access_token, hash_password, verify_password


def test_register_and_me(client):
    registered = client.post("/auth/register", json={"nombre": "Ana Pérez", "correo": "ANA@EXAMPLE.COM", "password": "Password1!"})
    assert registered.status_code == 201
    assert registered.json()["role"] == "user"
    assert "password_hash" not in registered.json()
    token = client.post("/auth/login", json={"correo": "ana@example.com", "password": "Password1!"}).json()["access_token"]
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["correo"] == "ana@example.com"


def test_public_registration_cannot_choose_admin(client):
    response = client.post("/auth/register", json={"nombre": "No Admin", "correo": "noadmin@example.com", "password": "Password1!", "role": "admin"})
    assert response.status_code == 201
    assert response.json()["role"] == "user"


def test_duplicate_and_invalid_registration(client):
    payload = {"nombre": "Persona", "correo": "same@example.com", "password": "Password1!"}
    assert client.post("/auth/register", json=payload).status_code == 201
    assert client.post("/auth/register", json=payload).status_code == 409
    invalid = client.post("/auth/register", json={"nombre": "A", "correo": "not-email", "password": "short"})
    assert invalid.status_code == 422


def test_login_errors_and_missing_auth(client):
    assert client.post("/auth/login", json={"correo": "missing@example.com", "password": "Password1!"}).status_code == 401
    client.post("/auth/register", json={"nombre": "User", "correo": "user2@example.com", "password": "Password1!"})
    assert client.post("/auth/login", json={"correo": "user2@example.com", "password": "wrong"}).status_code == 401
    assert client.get("/auth/me").status_code == 401
    assert client.get("/auth/me", headers={"Authorization": "Bearer invalid"}).status_code == 401


def test_password_hashing_and_token_claims():
    hashed = hash_password("Password1!")
    assert hashed != "Password1!"
    assert verify_password("Password1!", hashed)
    assert not verify_password("wrong", hashed)
    token = create_access_token(user_id=7, role="user", expires_delta=timedelta(minutes=5))
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    assert payload["sub"] == "7"
    assert payload["role"] == "user"
    assert "exp" in payload


def test_expired_token_is_rejected(client):
    expired = create_access_token(user_id=1, role="user", expires_delta=timedelta(seconds=-1))
    assert client.get("/auth/me", headers={"Authorization": f"Bearer {expired}"}).status_code == 401

