from fastapi import APIRouter, Depends
from connection.session_connection import get_session
from sqlalchemy.orm import Session
from schemas import PedidoSchema
from models.models import Pedido



order_router = APIRouter(prefix="/orders" , tags=["orders"])

@order_router.get("/")
async def pedidos():
    return {"Mensagem" : "Sucesso"}

@order_router.post("/pedido")
async def criar_pedido(pedido: PedidoSchema, session: Session=Depends(get_session)):
    novo_pedido = Pedido(id_usuario=pedido.id_usuario)

    session.add(novo_pedido)
    session.commit()

    return {"Mensagem" : f"Pedido criado com sucesso, ID do pedido: {novo_pedido.id}"}
