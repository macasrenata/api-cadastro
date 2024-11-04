from app import database
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import (
    AporteExtraRequest, AporteExtraResponse,
    ClienteCreate, ClienteResponse,
    ContratacaoPlanoRequest, ContratacaoPlanoResponse,
    ProdutoCreate, ProdutoResponse,
    ResgateRequest, ResgateResponse
)
from app.crud import (
    aplicar_aporte_extra,
    create_cliente_db,
    create_produto_db,
    get_cliente_by_id,
    get_plano_by_id,
    get_produto_by_id,
    realizar_resgate,
    verificar_carencia_resgate
)


router = APIRouter()

@router.post("/clientes/", response_model=ClienteResponse)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(database.Base)):
    return create_cliente_db(db=db, cliente=cliente)

@router.post("/produtos/", response_model=ProdutoResponse)
def create_produto(produto: ProdutoCreate, db: Session = Depends(database.get_db)):
    return create_produto_db(db=db, produto=produto)

@router.post("/planos/contratacao", response_model=ContratacaoPlanoResponse)
def contratar_plano(contratacao: ContratacaoPlanoRequest, db: Session = Depends(database.get_db)):
    produto = get_produto_by_id(db, contratacao.idProduto)
    cliente = get_cliente_by_id(db, contratacao.idCliente)
    
    if produto.expiracaoDeVenda < contratacao.dataDaContratacao:
        raise HTTPException(status_code=400, detail="Produto com prazo de venda expirado")
    if cliente.idade < produto.idadeDeEntrada or cliente.idade > produto.idadeDeSaida:
        raise HTTPException(status_code=400, detail="Idade fora do intervalo permitido para contratação")
    if contratacao.aporte < produto.valorMinimoAporteInicial:
        raise HTTPException(status_code=400, detail="Aporte inicial abaixo do mínimo exigido")

    return contratar_plano(db, contratacao)

@router.post("/planos/aporte-extra", response_model=AporteExtraResponse)
def aporte_extra(aporte: AporteExtraRequest, db: Session = Depends(database.get_db)):
    plano = get_plano_by_id(db, aporte.idPlano)
    produto = get_produto_by_id(db, plano.idProduto)
    
    if aporte.valorAporte < produto.valorMinimoAporteExtra:
        raise HTTPException(status_code=400, detail="Aporte abaixo do valor mínimo permitido")

    return aplicar_aporte_extra(db, aporte)

@router.post("/planos/resgate", response_model=ResgateResponse)
def resgate(resgate: ResgateRequest, db: Session = Depends(database.get_db)):
    plano = get_plano_by_id(db, resgate.idPlano)
    produto = get_produto_by_id(db, plano.idProduto)
    
    if not verificar_carencia_resgate(plano, produto):
        raise HTTPException(status_code=400, detail="Carência de resgate não cumprida")
    if resgate.valorResgate > plano.saldo:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para resgate")

    return realizar_resgate(db, resgate)