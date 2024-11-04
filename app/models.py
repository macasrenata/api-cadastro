from datetime import datetime
import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from app.database import Base

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(String, primary_key=True, index=True)
    cpf = Column(String, unique=True, index=True)
    nome = Column(String)
    email = Column(String)
    dataDeNascimento = Column(DateTime)
    genero = Column(String)
    rendaMensal = Column(Float)

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String)
    susep = Column(String, unique=True)
    expiracaoDeVenda = Column(DateTime)
    valorMinimoAporteInicial = Column(Float)
    valorMinimoAporteExtra = Column(Float)
    idadeDeEntrada = Column(Integer)
    idadeDeSaida = Column(Integer)
    carenciaInicialDeResgate = Column(Integer)
    carenciaEntreResgates = Column(Integer)

class Plano(Base):
    __tablename__ = "planos"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    idCliente = Column(String, ForeignKey("clientes.id"))
    idProduto = Column(String, ForeignKey("produtos.id"))
    aporte = Column(Float)
    dataDaContratacao = Column(DateTime, default=datetime)
    idadeDeAposentadoria = Column(Integer)
    saldo = Column(Float, default=0.0)
    dataPrimeiroResgate = Column(DateTime, nullable=True)
    dataUltimoResgate = Column(DateTime, nullable=True)

class AporteExtra(Base):
    __tablename__ = "aportes_extras"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    idPlano = Column(String, ForeignKey("planos.id"))
    valorAporte = Column(Float)

class Resgate(Base):
    __tablename__ = "resgates"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    idPlano = Column(String, ForeignKey("planos.id"))
    valorResgate = Column(Float)