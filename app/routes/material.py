from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.core import get_db
from app.schemas.material import MaterialSchema, MaterialCreate, MaterialUpdate
from app.services import material as service # Usando o novo service

router = APIRouter(prefix="/materiais", tags=["Materiais"])

@router.post("/", response_model=MaterialSchema, status_code=201)
def create_material(data: MaterialCreate, db: Session = Depends(get_db)):
    """Cria um novo material."""
    return service.create(db, data)

@router.get("/", response_model=List[MaterialSchema])
def list_materiais(db: Session = Depends(get_db)):
    """Lista todos os materiais."""
    return service.get_all(db)

@router.patch("/{id}", response_model=MaterialSchema)
def update_material_price(id: int, data: MaterialUpdate, db: Session = Depends(get_db)):
    """
    Atualiza preço ou nome do material.
    """
    obj = service.update(db, id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    return obj

@router.delete("/{id}", status_code=204)
def delete_material(id: int, db: Session = Depends(get_db)):
    """
    Exclui um material.
    
    - **Erro 400**: Se o material estiver sendo usado em alguma manutenção.
    """
    sucesso = service.delete(db, id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    return None # 204 No Content