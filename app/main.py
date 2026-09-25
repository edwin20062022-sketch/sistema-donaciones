"""Punto de entrada de la API FastAPI."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import Base, engine
from .routers import auth, donantes


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

    @app.get("/health", tags=["Sistema"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(auth.router)
    app.include_router(donantes.router)
    return app


app = create_app()
