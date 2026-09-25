"""Punto de entrada de la API FastAPI."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from .database import Base, engine
from .routers import auth, donantes


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Añade cabeceras defensivas a las respuestas HTTP de la API."""

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        return response


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Sistema de Gestión de Donaciones",
        description="API académica para administrar usuarios y donantes de alimentos y recursos.",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.add_middleware(SecurityHeadersMiddleware)

    @app.get("/health", tags=["Sistema"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(auth.router)
    app.include_router(donantes.router)
    return app


app = create_app()
