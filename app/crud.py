from http.client import HTTPException
from sqlalchemy.orm import Session
from app.schemas import ClienteCreate, ProdutoCreate
from app.models import AporteExtra, Cliente, Plano, Produto, Resgate

from datetime import datetime

def create_cliente_db(db: Session, cliente: ClienteCreate):
    db_cliente = Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def create_produto_db(db: Session, produto: ProdutoCreate):
    db_produto = Produto(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def get_produto_by_id(db: Session, produto_id: str):
    return db.query(Produto).filter(Produto.id == produto_id).first()

def get_cliente_by_id(db: Session, cliente_id: str):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()

def contratar_plano(db: Session, contratacao):
    db_plano = Plano(
        idCliente=contratacao.idCliente,
        idProduto=contratacao.idProduto,
        aporte=contratacao.aporte,
        dataDaContratacao=contratacao.dataDaContratacao,
        idadeDeAposentadoria=contratacao.idadeDeAposentadoria,
        saldo=contratacao.aporte
    )
    db.add(db_plano)
    db.commit()
    db.refresh(db_plano)
    return db_plano

def get_plano_by_id(db: Session, cliente_id: str):
    return db.query(Plano).filter(Plano.id == cliente_id).first()

def aplicar_aporte_extra(db: Session, aporte):
    plano = db.query(Plano).filter(Plano.id == aporte.idPlano).first()
    plano.saldo += aporte.valorAporte
    
    db_aporte = AporteExtra(idPlano=aporte.idPlano, valorAporte=aporte.valorAporte)
    db.add(db_aporte)
    db.commit()
    db.refresh(db_aporte)
    return db_aporte

def verificar_carencia_resgate(plano, produto):
    if not plano.dataPrimeiroResgate:
        return (datetime.now() - plano.dataDaContratacao).days >= produto.carenciaInicialDeResgate
    else:
        return (datetime.now() - plano.dataUltimoResgate).days >= produto.carenciaEntreResgates

def realizar_resgate(db: Session, resgate):
    plano = db.query(Plano).filter(Plano.id == resgate.idPlano).first()

    if resgate.valorResgate > plano.saldo:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para resgate")
    
    plano.saldo -= resgate.valorResgate
    db_resgate = Resgate(idPlano=resgate.idPlano, valorResgate=resgate.valorResgate)
    
    plano.dataUltimoResgate = datetime.now()
    db.add(db_resgate)
    db.commit()
    db.refresh(db_resgate)
    return db_resgate

