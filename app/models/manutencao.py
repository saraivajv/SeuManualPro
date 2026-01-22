from __future__ import annotations
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.core import BaseColumns


class Manutencao(BaseColumns):
    __tablename__ = "manutencoes"

    resumo: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(50), default="aberta")
    # In the challenge, candidate adds relationships here
