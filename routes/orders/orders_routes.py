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

@order_router.get("/order/{order_id}")
async def view_order(order_id: int, user: Usuario = Depends(verify_token), session: Session=Depends(get_session)):  
    order = session.query(Pedido).filter(Pedido.id == order_id).first()

    if not user.admin and order.id_usuario != user.id:
        raise HTTPException(status_code=401, detail="Não autorizado a completar este pedido")

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
    return {
        "count_itens_order" : len(order.itens),
        "order" : {order}
    }


@order_router.post("/create_order")
async def create_order(order: PedidoSchema, session: Session=Depends(get_session)):
    new_order = Pedido(id_usuario=order.id_usuario)

    session.add(new_order)
    session.commit()

    return {"message" : f"Pedido criado com sucesso, ID do pedido: {new_order.id}"}

@order_router.delete("/order/cancel/{order_id}")
async def cancel_order(order_id: int, user: Usuario = Depends(verify_token), session: Session=Depends(get_session)):
    order = session.query(Pedido).filter(Pedido.id == order_id).first()

    if not user.admin and order.id_usuario != user.id:
        raise HTTPException(status_code=403, detail="Não autorizado a cancelar este pedido")
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")  
    

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

@order_router.post("/order/finalize/{order_id}")
async def finalize_order(order_id: int, user: Usuario = Depends(verify_token), session: Session=Depends(get_session)):
    order = session.query(Pedido).filter(Pedido.id == order_id).first()

    if not user.admin and order.id_usuario != user.id:
        raise HTTPException(status_code=403, detail="Não autorizado a finalizar o pedido")
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    order.status = "FINALIZADO"

    session.commit()
    session.refresh(order)
    
    return {
        "message" : "Pedido finalizado com sucesso",
        "order" : {order}
        }

@order_router.post("/order/add_item_to_order/{order_id}")
async def add_item_to_order(order_id: int, item_order: ItemPedidoSchema, user: Usuario = Depends(verify_token), session: Session=Depends(get_session)):
    order = session.query(Pedido).filter(Pedido.id == order_id).first()
    
    if not user.admin and order.id_usuario != user.id:
        raise HTTPException(status_code=401, detail="Não autorizado a completar este pedido")
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

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

@order_router.delete("/order/remove_item/{item_order_id}")
async def remove_item_from_order(item_order_id: int, user: Usuario = Depends(verify_token), session: Session=Depends(get_session)):
    item_order = session.query(PedidoItens).filter(PedidoItens.id == item_order_id).first()
    
    if not user.admin and item_order.pedido.id_usuario != user.id:
        raise HTTPException(status_code=401, detail="Não autorizado a remover este item do pedido")
    if not item_order:
        raise HTTPException(status_code=404, detail="Item do pedido não encontrado")
    
    
    session.delete(item_order)
    item_order.pedido.calcular_preco()
    session.commit()
    session.refresh(item_order.pedido)

    return {
        "message" : "Item do pedido removido com sucesso",         
        "count_itens_order": len(item_order.pedido.itens),
        "order": item_order.pedido
    }
