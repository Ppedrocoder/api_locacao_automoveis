from pydantic import BaseModel

class LocacaoSchema(BaseModel):
    veiculo_id: int
    cliente: str
    dia_inicial: str
    dia_final: str
    status: str

    class Config:
        orm_mode = True