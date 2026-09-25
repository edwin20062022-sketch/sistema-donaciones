"""CRUD protegido de donantes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import require_role
from ..models import Donante, User
from ..schemas import DonanteCreate, DonanteResponse, DonanteUpdate


router = APIRouter(prefix="/donantes", tags=["Donantes"])


@router.post("", response_model=DonanteResponse, status_code=status.HTTP_201_CREATED)
def create_donante(
    payload: DonanteCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("user", "admin")),
) -> Donante:
    donante = Donante(**payload.model_dump())
    db.add(donante)
    db.commit()
    db.refresh(donante)
    return donante


@router.get("", response_model=list[DonanteResponse])
def list_donantes(
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin")),
) -> list[Donante]:
    return list(db.scalars(select(Donante).order_by(Donante.id)).all())


@router.get("/{donante_id}", response_model=DonanteResponse)
def get_donante(
    donante_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("user", "admin")),
) -> Donante:
    donante = db.get(Donante, donante_id)
    if donante is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donante no encontrado")
    return donante


@router.put("/{donante_id}", response_model=DonanteResponse)
def update_donante(
    donante_id: int,
    payload: DonanteUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin")),
) -> Donante:
    donante = db.get(Donante, donante_id)
    if donante is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donante no encontrado")
    for field, value in payload.model_dump().items():
        setattr(donante, field, value)
    db.commit()
    db.refresh(donante)
    return donante


@router.delete("/{donante_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_donante(
    donante_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin")),
) -> None:
    donante = db.get(Donante, donante_id)
    if donante is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donante no encontrado")
    db.delete(donante)
    db.commit()

