from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType


# cria a conexao do seu banco
db = create_engine("sqlite:///database/banco.db")

# cria a base do banco de dados
Base = declarative_base()

# cria as classes

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(100))
    email = Column("email", String(100), nullable=False,)
    senha = Column("senha", String(100))
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin
    
class PedidoItens(Base):
    __tablename__ = "pedido_itens"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String(100))
    tamanho = Column("tamanho", String(100))
    preco_unitario = Column("preco_unitario", Float)
    id_pedido = Column("id_pedido", Integer, ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, id_pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.id_pedido = id_pedido

        

class Pedido(Base):
    __tablename__ = "pedidos"

    # STATUS_PEDIDOS = (
    #     ("PENDENTE","PENDENTE"),
    #     ("CANCELADO", "CANCELADO"),
    #     ("FINALIZADO", "FINALIZADO")
    # )
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    # status = Column("status", ChoiceType(STATUS_PEDIDOS))
    status = Column("status", String)
    id_usuario = Column("id_usuario", Integer, ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    # id_itens

    def __init__(self, id_usuario, status="PENDENTE", preco=0.00):
        self.id_usuario = id_usuario
        self.status = status
        self.preco = preco