from fastapi import APIRouter, Depends, HTTPException
from models.models import Usuario
from connection.session_connection import get_session
from main import bcrypt_context
from sqlalchemy.orm import Session
from schemas import UsuarioSchema, LoginSchema


auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def auth():
    return {"Mensagem" : "Rota de auth0", "IsAuth" : True}


@auth_router.post("/criar_conta")
async def criar_conta(user: UsuarioSchema, session: Session=Depends(get_session)):
    user_exists = session.query(Usuario).filter(Usuario.email == user.email).first()

    if user_exists:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    else:
        password_crypt = bcrypt_context.hash(user.password)
        new_user = Usuario(nome=user.nome,email=user.email, senha=password_crypt)
        session.add(new_user)
        session.commit()
        
        return {"message" : "Usuário cadastrado com sucesso"}

def criar_token(id_usuario: int):
    token = 'jwt.encode'
    return token

def autenticar_usuario(email: str, senha: str, session : Session):
    user = session.query(Usuario).filter(Usuario.email == email).first()
    
    if not user:
        return False
    elif not bcrypt_context.verify(senha, user.senha):
        return False
    return user




@auth_router.post("/login")
async def login(login: LoginSchema, session: Session=Depends(get_session)):
    # user = session.query(Usuario).filter(Usuario.email == login.email).first()
    user = autenticar_usuario(login.email, login.senha, session)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(user.id) 
        return {"access_token" : access_token, "token_type" : "Bearer"}