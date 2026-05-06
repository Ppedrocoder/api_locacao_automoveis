from ninja import Schema

class VeiculoSchema(Schema):
    modelo: str
    marca: str
    tipo: str
    
    class Config:
        orm_mode = True

class LinkSchema(Schema):
    rel: str
    href: str
    method: str

class VeiculoOutSchema(Schema): 
    id: int
    modelo: str
    marca: str
    status: str
    tipo: str
    links: list[LinkSchema] = []
