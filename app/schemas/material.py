from app.schemas.core import CamelSchema

class MaterialBase(CamelSchema):
    nome: str
    preco_unitario: float

class MaterialCreate(MaterialBase):
    pass

class MaterialSchema(MaterialBase):
    id: int

class AdicionarMaterialSchema(CamelSchema):
    material_id: int
    quantidade: int