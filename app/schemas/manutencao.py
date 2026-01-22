from typing import List
from app.schemas.core import CamelSchema
from datetime import datetime

# Schema interno para cada item da lista
class MaterialConsumido(CamelSchema):
    id: int
    nome: str
    quantidade: int
    preco_unitario: float
    custo: float

class ManutencaoBase(CamelSchema):
    resumo: str
    status: str = "aberta"

class ManutencaoCreate(ManutencaoBase):
    pass

class ManutencaoSchema(ManutencaoBase):
    id: int
    criado_em: datetime | None = None
    materiais: List[MaterialConsumido] = []
    custo_total_materiais: float = 0.0