from __future__ import annotations
from typing import List, Any
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.core import BaseColumns
from app.models.material import ManutencaoMaterial

class Manutencao(BaseColumns):
    __tablename__ = "manutencoes"

    resumo: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(50), default="aberta")

    # Relacionamento no banco
    materiais_assoc: Mapped[List[ManutencaoMaterial]] = relationship(
        "ManutencaoMaterial", 
        backref="manutencao",
        lazy="selectin"
    )

    # --- PROPRIEDADES PARA A API ---
    
    @property
    def custo_total_materiais(self) -> float:
        """Calcula o custo total."""
        total = 0.0
        for item in self.materiais_assoc:
            if item.material:
                total += item.quantidade * item.material.preco_unitario
        return total

    @property
    def materiais(self) -> List[dict[str, Any]]:
        """Formata a lista para o JSON de resposta."""
        output = []
        for assoc in self.materiais_assoc:
            if assoc.material:
                custo_item = assoc.quantidade * assoc.material.preco_unitario
                output.append({
                    "id": assoc.material.id,
                    "nome": assoc.material.nome,
                    "quantidade": assoc.quantidade,
                    "preco_unitario": assoc.material.preco_unitario,
                    "custo": custo_item
                })
        return output