from fastapi import APIRouter, Depends, HTTPException
from dependencies import verify_token
from models.models import Usuario
from connection.session_connection import get_session
from main import ALGORITHM, SECRET_KEY, bcrypt_context, ACCESS_TOKEN_EXPIRE_MINUTES
from sqlalchemy.orm import Session
from schemas import UsuarioSchema, LoginSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta,timezone
from fastapi.security import OAuth2PasswordRequestForm


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/create_account")
async def create_account(user: UsuarioSchema, session: Session=Depends(get_session)):
    user_exists = session.query(Usuario).filter(Usuario.email == user.email).first()

    if user_exists:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    else:
        password_crypt = bcrypt_context.hash(user.senha)
        new_user = Usuario(nome=user.nome,email=user.email, senha=password_crypt, ativo=user.ativo, admin=user.admin)
        session.add(new_user)
        session.commit()
        
        return {"message" : "Usuário cadastrado com sucesso"}


def authenticate_user(email: str, senha: str, session : Session):
    user = session.query(Usuario).filter(Usuario.email == email).first()
    
    if not user:
        return False
    elif not bcrypt_context.verify(senha, user.senha):
        return False
    return user


def create_token(id_usuario: int, duration_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    date_expire = datetime.now(timezone.utc) + duration_token
    dic_info  = { "sub" : str(id_usuario),"exp" : date_expire }

    return jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)


@auth_router.post("/login")
async def login(login: LoginSchema, session: Session=Depends(get_session)):
    user = authenticate_user(login.email, login.senha, session)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = create_token(user.id) 
        refresh_token = create_token(user.id, duration_token=timedelta(days=7))
        return {
                "access_token" : access_token, 
                "refresh_token" : refresh_token,
                "token_type" : "Bearer"
                }

@auth_router.post("/login_oauth")
async def login_oauth(payload: OAuth2PasswordRequestForm = Depends(), session: Session=Depends(get_session)):
    user = authenticate_user(payload.username, payload.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = create_token(user.id) 
        return {
                "access_token" : access_token, 
                "token_type" : "Bearer"
                }


@auth_router.get("/refresh_token")
async def use_refresh_token(user: Usuario = Depends(verify_token)):  
    access_token = create_token(user.id)
    return {
            "access_token" : access_token, 
            "token_type" : "Bearer"
            }