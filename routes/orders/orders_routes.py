from fastapi import APIRouter, Depends, HTTPException
from connection.session_connection import get_session
from dependencies import verify_token
from sqlalchemy.orm import Session
from schemas import ItemPedidoSchema, PedidoSchema
from models.models import Pedido, PedidoItens, Usuario



order_router = APIRouter(prefix="/orders" , tags=["orders"], dependencies=[Depends(verify_token)])


@order_router.get("/orders_all")
async def all_orders(user: Usuario = Depends(verify_token), session: Session=Depends(get_session)):
    if not user.admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Apenas administradores podem acessar todos os pedidos.")

    orders = session.query(Pedido).all()

    if not orders:
        raise HTTPException(status_code=404, detail="Nenhum pedido encontrado")

    return {"message" : "Sucesso", "orders": orders}

@order_router.post("/create_order")
async def create_order(order: PedidoSchema, session: Session=Depends(get_session)):
    new_order = Pedido(id_usuario=order.id_usuario)

    session.add(new_order)
    session.commit()

    return {"message" : f"Pedido criado com sucesso, ID do pedido: {new_order.id}"}

@order_router.delete("/order/cancel/{order_id}")
async def cancel_order(order_id: int, user: Usuario = Depends(verify_token), session: Session=Depends(get_session)):
    order = session.query(Pedido).filter(Pedido.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")  
    if order.id_usuario != user.id:
        raise HTTPException(status_code=403, detail="Não autorizado a cancelar este pedido")
    

    if user.admin:
        session.delete(order)
        session.commit()
        return {"message" : "Pedido deletado com sucesso pelo Admin"}
    else:    
        order.status = "CANCELADO"
    
    session.commit()
    session.refresh(order)

    return {
        "message" : "Pedido cancelado com sucesso", 
        "order": {order}
        }

@order_router.post("/order/complete/{order_id}")
async def add_item_to_order(order_id: int, item_order: ItemPedidoSchema, user: Usuario = Depends(verify_token), session: Session=Depends(get_session)):
    order = session.query(Pedido).filter(Pedido.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if order.id_usuario != user.id:
        raise HTTPException(status_code=401, detail="Não autorizado a completar este pedido")

    data_order = PedidoItens(
        quantidade = item_order.quantidade,
        sabor = item_order.sabor,
        tamanho = item_order.tamanho,
        preco_unitario = item_order.preco_unitario,
        id_pedido = order.id
    )
    
    session.add(data_order)
    order.calcular_preco()
    session.commit()
    session.refresh(order)

    return {
        "message" : "Pedido cadastrado com sucesso", 
        "order_id": order.id,
        "total_price": order.preco
        } 