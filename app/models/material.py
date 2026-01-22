from sqlalchemy import String, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.core import BaseColumns, Base

# Tabela Associativa (Association Object)
class ManutencaoMaterial(Base):
    __tablename__ = "manutencoes_materiais"

    manutencao_id: Mapped[int] = mapped_column(ForeignKey("manutencoes.id"), primary_key=True)
    material_id: Mapped[int] = mapped_column(ForeignKey("materiais.id"), primary_key=True)
    
    quantidade: Mapped[int] = mapped_column(Integer, default=1)

    material: Mapped["Material"] = relationship()

class Material(BaseColumns):
    __tablename__ = "materiais"

    nome: Mapped[str] = mapped_column(String(200), unique=True)
    preco_unitario: Mapped[float] = mapped_column(Float)