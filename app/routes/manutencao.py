from app.schemas.material import AdicionarMaterialSchema
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.core import get_db
from app.schemas.manutencao import ManutencaoSchema, ManutencaoCreate, ManutencaoUpdateStatus
from app.services import manutencao as service

router = APIRouter(prefix="/manutencao", tags=["Manutencao"])


@router.post("/", response_model=ManutencaoSchema, status_code=201)
def create_manutencao(data: ManutencaoCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova ordem de manutenção.
    
    - **status default**: "aberta"
    """
    return service.create(db, data)


@router.get("/{id}", response_model=ManutencaoSchema)
def get_manutencao(id: int, db: Session = Depends(get_db)):
    """
    Busca uma manutenção pelo ID.
    
    A resposta inclui automaticamente:
    - Lista de **materiais** consumidos.
    - **Custo total** calculado (Quantidade * Preço Unitário).
    """
    obj = service.get_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Manutencao not found")
    return obj


@router.post("/{id}/materiais", response_model=ManutencaoSchema)
def add_material_to_manutencao(
    id: int, 
    data: AdicionarMaterialSchema, 
    db: Session = Depends(get_db)
):
    """
    Adiciona um material consumido a uma manutenção existente.
    
    - **Regra de Negócio**: Não é possível adicionar materiais se a manutenção estiver com status **'finalizada'**.
    """
    return service.add_material(db, id, data)


@router.patch("/{id}/status", response_model=ManutencaoSchema)
def update_manutencao_status(
    id: int, 
    data: ManutencaoUpdateStatus, 
    db: Session = Depends(get_db)
):
    """
    Atualiza apenas o status da manutenção.
    
    Exemplo: Alterar de 'aberta' para 'finalizada' para bloquear novas adições de materiais.
    """
    obj = service.update_status(db, id, data.status)
    if not obj:
        raise HTTPException(status_code=404, detail="Manutencao not found")
    return obj

@router.delete("/{id}", status_code=204)
def delete_manutencao(id: int, db: Session = Depends(get_db)):
    """
    Exclui uma manutenção existente.
    """
    sucesso = service.delete(db, id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Manutencao not found")
    return None