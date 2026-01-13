# FastAPI Ordering System

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>

<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/badge/python-3.10.11-%2334D058" alt="Package version">
</a>
</p>

Uma API robusta para gerenciamento de pedidos, construída com FastAPI, SQLAlchemy e Alembic. Este projeto oferece suporte a autenticação JWT, controle de usuários e um fluxo completo de pedidos com múltiplos itens.

## 🚀 Funcionalidades

- **Autenticação:** Sistema de login seguro usando OAuth2 com tokens JWT.
- **Gerenciamento de Usuários:** Cadastro, ativação e controle de privilégios administrativos.
- **Sistema de Pedidos:** 
  - Criação de pedidos vinculados a usuários.
  - Adição de múltiplos itens a um único pedido (sabor, tamanho, quantidade).
  - Cálculo automático de preço total.
  - Gestão de status do pedido (PENDENTE, FINALIZADO, etc.).
- **Banco de Dados:** Integração com SQLite via SQLAlchemy.
- **Migrações:** Controle de versão do banco de dados com Alembic.

## 🛠️ Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [SQLite](https://www.sqlite.org/)
- [Uvicorn](https://www.uvicorn.org/)

## 📁 Estrutura do Projeto

```text
fast_api/
├── alembic/              # Scripts de migração do banco de dados
├── connection/           # Gerenciamento de conexão com o DB
├── database/             # Arquivo do banco de dados SQLite
├── models/               # Modelos SQLAlchemy
│   └── models.py         # Definição de Usuário, Pedido e ItemPedido
├── routes/               # Rotas da API divididas por contexto
│   ├── auth/             # Rotas de autenticação
│   └── orders/           # Rotas de gerenciamento de pedidos
├── schemas.py            # Esquemas de validação Pydantic
├── main.py               # Ponto de entrada da aplicação
├── dependencies.py       # Dependências injetáveis (DB, Auth)
├── requirements.txt      # Dependências do projeto
└── alembic.ini           # Configuração do Alembic
```

## ⚙️ Configuração e Instalação

### Pré-requisitos
- Python 3.8+
- venv (recomendado)

### Instalação

1. Clone o repositório ou baixe os arquivos.
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   # No Windows:
   .\venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure o arquivo `.env` na raiz do projeto:
   ```env
   SECRET_KEY=sua_chave_secreta_aqui
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

## 🗄️ Migrações de Banco de Dados

Caso precise atualizar o banco de dados:

1. Gere uma nova migração:
   ```bash
   alembic revision --autogenerate -m "descrição das mudanças"
   ```
2. Aplique a migração:
   ```bash
   alembic upgrade head
   ```

## 🏁 Como Executar

Para iniciar o servidor de desenvolvimento com recarregamento automático:

```bash
uvicorn main:app --reload
```

Acesse a documentação interativa da API em:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 📡 Endpoints Principais

### Autenticação
- `POST /auth/create_account`: Cadastro de conta
- `POST /auth/login`: Login do usuário 
- `GET /auth/refresh_token`: Gera novo access token
- `POST /auth/login_oauth`: Login para obtenção de token JWT.

### Pedidos
- `GET /orders/all`: Pegar todos os pedidos cadastrados
- `GET /orders/order/view_order_user`: Listagem de pedidos do usuário autenticado.
- `GET /orders/order/{order_id}`: Lista o pedido conforme o id dele
- `POST /orders/create_order`: Criar pedido
- `POST /orders/order/cancel/{order_id}`: Mudar o status do pedido para CANCELADO
- `POST /orders/finalize/{order_id}`: Mudar o status do pedido para FINALIZADO
- `POST /orders/order/add_item_to_order/{order_id}`: Adiciona itens ao pedido
- `DELETE /orders/order/remove_item/{item_order_id}`: Deleta itens do pedido

