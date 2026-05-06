from datetime import date

from ninja import Schema

class LocacaoSchema(Schema):
    veiculo_id: int
    cliente: str
    dia_inicial: date
    dia_final: date

    class Config:
        orm_mode = True
    
class LinkSchema(Schema):
    rel: str
    href: str
    method: str

class LocacaoOutSchema(Schema):
    id: int
    veiculo_id: int
    cliente: str
    dia_inicial: date
    dia_final: date
    status: str
    links: list[LinkSchema] = []