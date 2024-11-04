## Descrição

API REST para cadastro de clientes, produtos e planos de previdência privada.

## Instalação

1. Clone o repositório
2. Ative o ambiente virtual
3. Instale as dependências

Executando com Docker

```bash
docker-compose up --build
```

Rotas:

POST /clientes/
POST /produtos/
POST /planos/contratacao
POST /planos/aporte-extra
POST /planos/resgate

### 6. **Documentação**

Use o Swagger do FastAPI acessando `http://localhost:8000/docs`.
