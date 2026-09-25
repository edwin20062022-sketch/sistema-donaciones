"""Esquemas de entrada y salida de la API."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    correo: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    correo: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    correo: EmailStr
    role: Literal["admin", "user"]
    created_at: datetime


class DonanteBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=150)
    correo: EmailStr
    telefono: str = Field(min_length=7, max_length=30)
    tipo: Literal["persona", "empresa", "organizacion"]
    recurso: str = Field(min_length=2, max_length=100)


class DonanteCreate(DonanteBase):
    pass


class DonanteUpdate(DonanteBase):
    pass


class DonanteResponse(DonanteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime | None

