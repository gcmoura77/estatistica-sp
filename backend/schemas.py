from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool] = True
    admin: Optional[bool] = False
    
    class Config:
        from_attributes = True 
        # Permite que o Pydantic use os atributos do modelo SQLAlchemy diretamente
        
class JogoSchema(BaseModel):
    adversario: str
    local: str
    gols_pro: int
    gols_contra: int
    torneio: str
    data_jogo: datetime
    nota: Optional[float] = None
    tecnico: str
    
    class Config:
        from_attributes = True 
        
class LoginSchema(BaseModel):
    email: str
    senha: str
    
    class Config:
        from_attributes = True
        
class ResponseJogoSchema(BaseModel):
    id: int
    adversario: str
    local: str
    gols_pro: int
    gols_contra: int
    torneio: str
    data_jogo: datetime
    nota: float
    tecnico: str
    criado_em: datetime
    pontos: int
    resultado: str

    class Config:
        from_attributes = True 
