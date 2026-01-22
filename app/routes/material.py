from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database.core import get_db
from app.models.material import Material
from app.schemas.material import MaterialSchema, MaterialCreate

router = APIRouter(prefix="/materiais", tags=["Materiais"])

@router.post("/", response_model=MaterialSchema, status_code=201)
def create_material(data: MaterialCreate, db: Session = Depends(get_db)):
    """
    Cria um novo material no catálogo (Ex: Cimento, Areia).
    """
    try:
        db_obj = Material(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Já existe um material com este nome.")

@router.get("/", response_model=List[MaterialSchema])
def list_materiais(db: Session = Depends(get_db)):
    """
    Lista todos os materiais disponíveis.
    """
    return db.scalars(select(Material)).all()