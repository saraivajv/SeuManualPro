from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.manutencao import Manutencao
from app.schemas.manutencao import ManutencaoCreate


def get_by_id(db: Session, id: int) -> Manutencao | None:
    return db.scalar(select(Manutencao).where(Manutencao.id == id))


def create(db: Session, schema: ManutencaoCreate) -> Manutencao:
    db_obj = Manutencao(**schema.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
