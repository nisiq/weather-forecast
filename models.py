from pydantic import BaseModel
from typing import Optional
from uuid import uuid4 #códigosMaioresAleatórios

class Animal(BaseModel):
    id: Optional[str] = None
    nome: str
    idade: int
    sexo: str
    cor: str


#Model Felipe
class Conta(BaseModel):
    name: str
    BRL: float
    CPF: str
