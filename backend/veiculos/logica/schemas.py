from pydantic import BaseModel

class VeiculoSchema(BaseModel):
    modelo: str
    marca: str
    status: str
    tipo: str

    class Config:
        orm_mode = True