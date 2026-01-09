from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from connection.session_connection import get_session
from main import ALGORITHM, SECRET_KEY, oauth2_scheme
from models.models import Usuario
from jose import jwt, JWTError


def verify_token(token: str=Depends(oauth2_scheme), session: Session=Depends(get_session)):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY,algorithms=ALGORITHM)
        user_id = payload.get("sub")        
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    
    user = session.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return user