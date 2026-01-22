from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from app.models.manutencao import Manutencao
from app.models.material import ManutencaoMaterial, Material
from app.schemas.manutencao import ManutencaoCreate
from app.schemas.material import AdicionarMaterialSchema

def get_by_id(db: Session, id: int) -> Manutencao | None:
    return db.scalar(select(Manutencao).where(Manutencao.id == id))

def create(db: Session, schema: ManutencaoCreate) -> Manutencao:
    db_obj = Manutencao(**schema.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def add_material(db: Session, manutencao_id: int, dados: AdicionarMaterialSchema):
    manutencao = get_by_id(db, manutencao_id)
    if not manutencao:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada")

    if manutencao.status.lower() in ["finalizada", "concluida", "finished"]:
        raise HTTPException(status_code=400, detail="Não é possível adicionar materiais a uma manutenção finalizada.")

    # Verifica se Material existe
    material = db.scalar(select(Material).where(Material.id == dados.material_id))
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    
    # Verifica se já existe esse material nessa manutenção
    assoc_existente = db.scalar(
        select(ManutencaoMaterial)
        .where(ManutencaoMaterial.manutencao_id == manutencao_id)
        .where(ManutencaoMaterial.material_id == dados.material_id)
    )

    if assoc_existente:
        assoc_existente.quantidade += dados.quantidade
    else:
        nova_assoc = ManutencaoMaterial(
            manutencao_id=manutencao_id,
            material_id=dados.material_id,
            quantidade=dados.quantidade
        )
        db.add(nova_assoc)
    
    db.commit()
    db.refresh(manutencao)
    return manutencao

def update_status(db: Session, id: int, novo_status: str) -> Manutencao | None:
    manutencao = get_by_id(db, id)
    if not manutencao:
        return None
    
    manutencao.status = novo_status
    db.commit()
    db.refresh(manutencao)
    return manutencao

def delete(db: Session, id: int) -> bool:
    obj = get_by_id(db, id)
    if not obj:
        return False

    db.delete(obj)
    db.commit()
    return True