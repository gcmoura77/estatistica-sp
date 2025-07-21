from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_scheme

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()
        
def verificar_token(token: str = Depends(oauth2_scheme), session: Session = Depends(pegar_sessao)):
    """
    Função para verificar o token JWT (JSON Web Token) e retornar o usuário associado.
    """
    # verificar se o token é válido
    try:
        dic_info_usuario = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info_usuario.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso negado, verifique a validade do token.")  
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return usuario
        
