from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(idusuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    """
    Função para criar um token JWT (JSON Web Token) para o usuário autenticado.
    """
    # Aqui você implementaria a lógica para gerar o token JWT
    # idusuario
    data_expiracao = datetime.now(timezone.utc) + duracao_token  # Token válido por um tempo determinado
    dic_info = {
        "sub": str(idusuario),  # 'sub' é o campo padrão para o ID do usuário
        "exp": data_expiracao,  # Data de expiração do token
    }
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado

def autenticar_usuario(email, senha, session):
    """
    Função para autenticar o usuário com email e senha.
    """
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    
    return usuario

@auth_router.get("/")
async def home():
    """
    Essa é a rota padrão de autenticação do nosso sistema
    """
    return {"mensagem": "Você acessou a rota padrão de autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    """
    Essa rota é responsável por criar uma nova conta de usuário
    """
    
    # TODO: não permitir que o usuario que está criando a conta não seja admin para criar uma conta de admin
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        # já existe um usuário com esse email
        # montrar uma mensagem de erro
        raise HTTPException(status_code=400, detail="Já existe um usuário com esse email.")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(nome=usuario_schema.nome, 
                               email=usuario_schema.email, 
                               senha=senha_criptografada, 
                               ativo=usuario_schema.ativo, 
                               admin=usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Conta criada com sucesso {usuario_schema.email}"}
        
# login -> email e senha -> token JWT (JSON Web Token) 
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    """
    Essa rota é responsável por fazer o login do usuário
    """
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou credencias não estão corretas.")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))  # Exemplo de refresh token com duração maior
        return {"access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer"}

@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    """
    Essa rota é responsável por fazer o login do usuário
    """
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou credencias não estão corretas.")
    else:
        access_token = criar_token(usuario.id)
        return {"access_token": access_token,
                "token_type": "Bearer"}

@auth_router.get("/refresh_token")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    # verificar o token
    access_token = criar_token(usuario.id)
    return {"access_token": access_token, "token_type": "Bearer"}

@auth_router.get("/remover_usuario/{id_usuario}")
async def remover_usario(id_usuario: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    # verificar o token
    access_token = criar_token(usuario.id)
    
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Apenas administradores podem remover usuários.")
    if id_usuario == usuario.id:
        raise HTTPException(status_code=400, detail="Você não pode remover a si mesmo.")
    
    # lógica para remover o usuário
    sucess = session.query(Usuario).filter(Usuario.id == id_usuario).delete()
    if not sucess:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    session.commit()
    return {"mensagem": f"Usuário {id_usuario} removido com sucesso"}
