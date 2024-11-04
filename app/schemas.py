from pydantic import BaseModel
from datetime import datetime

class ClienteCreate(BaseModel):
    cpf: str
    nome: str
    email: str
    dataDeNascimento: datetime
    genero: str
    rendaMensal: float

class ClienteResponse(BaseModel):
    id: str

class ProdutoCreate(BaseModel):
    nome: str
    susep: str
    expiracaoDeVenda: datetime
    valorMinimoAporteInicial: float
    valorMinimoAporteExtra: float
    idadeDeEntrada: int
    idadeDeSaida: int
    carenciaInicialDeResgate: int
    carenciaEntreResgates: int

class ProdutoResponse(BaseModel):
    id: str

class ContratacaoPlanoRequest(BaseModel):
    idCliente: str
    idProduto: str
    aporte: float
    dataDaContratacao: datetime
    idadeDeAposentadoria: int

class ContratacaoPlanoResponse(BaseModel):
    id: str

class AporteExtraRequest(BaseModel):
    idCliente: str
    idPlano: str
    valorAporte: float

class AporteExtraResponse(BaseModel):
    id: str

class ResgateRequest(BaseModel):
    idPlano: str
    valorResgate: float

class ResgateResponse(BaseModel):
    id: str