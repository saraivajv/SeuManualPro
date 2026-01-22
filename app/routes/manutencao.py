from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.core import get_db
from app.schemas.manutencao import ManutencaoSchema, ManutencaoCreate
from app.services import manutencao as service

router = APIRouter(prefix="/manutencao", tags=["Manutencao"])


@router.post("/", response_model=ManutencaoSchema)
def create_manutencao(data: ManutencaoCreate, db: Session = Depends(get_db)):
    return service.create(db, data)


@router.get("/{id}", response_model=ManutencaoSchema)
def get_manutencao(id: int, db: Session = Depends(get_db)):
    obj = service.get_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Manutencao not found")
    return obj
