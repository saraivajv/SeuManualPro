from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from app.models.material import Material, ManutencaoMaterial
from app.schemas.material import MaterialCreate, MaterialUpdate

def create(db: Session, schema: MaterialCreate) -> Material:
    # Verifica duplicidade de nome
    existente = db.scalar(select(Material).where(Material.nome == schema.nome))
    if existente:
        raise HTTPException(status_code=400, detail="Já existe um material com este nome.")
    
    db_obj = Material(**schema.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_all(db: Session):
    return db.scalars(select(Material)).all()

def update(db: Session, id: int, schema: MaterialUpdate) -> Material | None:
    db_obj = db.get(Material, id)
    if not db_obj:
        return None
    
    # Atualiza apenas os campos enviados
    dados = schema.model_dump(exclude_unset=True)
    for key, value in dados.items():
        setattr(db_obj, key, value)
    
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, id: int):
    db_obj = db.get(Material, id)
    if not db_obj:
        return False

    # Verifica se está em uso
    em_uso = db.scalar(select(ManutencaoMaterial).where(ManutencaoMaterial.material_id == id))
    if em_uso:
        raise HTTPException(
            status_code=400, 
            detail="Não é possível excluir este material pois ele está vinculado a uma ou mais manutenções."
        )

    db.delete(db_obj)
    db.commit()
    return True