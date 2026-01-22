from app.schemas.core import CamelSchema
from datetime import datetime


class ManutencaoBase(CamelSchema):
    resumo: str
    status: str = "aberta"


class ManutencaoCreate(ManutencaoBase):
    pass


class ManutencaoSchema(ManutencaoBase):
    id: int
    created_at: datetime | None = None

    # Candidate will add 'materials' and 'total_cost' here
