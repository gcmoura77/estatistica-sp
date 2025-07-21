from fastapi import APIRouter, Depends, HTTPException
from models import Jogo, Usuario
from dependencies import pegar_sessao, verificar_token
from schemas import JogoSchema, ResponseJogoSchema
from sqlalchemy.orm import Session
from typing import List

jogos_router = APIRouter(prefix="/jogos", tags=["jogos"], dependencies=[Depends(verificar_token)])

@jogos_router.get("/")
async def jogos():
    """
    Essa é a rota padrão de jogos do nosso sistema. Todas as rotas dos jogos precisam de autenticação
    """    
    return {"messagem": "acessando a rota de jogos"}

@jogos_router.post("/resultado")
async def criar_resultado(jogo_schema: JogoSchema, 
                          session: Session = Depends(pegar_sessao), 
                          usuario: Usuario = Depends(verificar_token)):
    """
    Essa rota é responsável por criar um novo resultado de jogo
    """
    novo_resultado = Jogo(usuario=usuario.id,
                          adversario=jogo_schema.adversario,
                          local=jogo_schema.local,
                          gols_pro=jogo_schema.gols_pro,
                          gols_contra=jogo_schema.gols_contra,
                          torneio=jogo_schema.torneio,
                          data_jogo=jogo_schema.data_jogo,
                          nota=jogo_schema.nota,
                          tecnico=jogo_schema.tecnico)
    session.add(novo_resultado)
    session.commit()
    return {"mensagem": f"Resultado criado com sucesso. ID do resultado: {novo_resultado.id}",
            "resultado": novo_resultado}


@jogos_router.post("/resultado/remover/{id_resultado}")
async def remover_resultado(id_resultado: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Essa rota é responsável por remover um resultado de jogo
    """
    resultado = session.query(Jogo).filter(Jogo.id == id_resultado).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Resultado não encontrado")
    # usuario é admin
    # usuario.id = resultado.usuario
    if not usuario.admin and resultado.usuario != usuario.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para remover este resultado")
    
    session.delete(resultado)
    session.commit()
    return {"mensagem": "Resultado removido com sucesso",
            "resultado": resultado
    }
    
@jogos_router.get("/listar")
async def listar_resultados(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Essa rota é responsável por listar todos os resultados cadastrados no sistema.
    """
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Você não tem permissão para listar resultados")
    else:
        resultados = session.query(Jogo).all()
        return {"quantidade_resultados": len(resultados),
                "resultados": resultados,
                
        }
    
#visualizar resultado
@jogos_router.get("/resultado/{id_resultado}")
async def visualizar_resultado(id_resultado: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Essa rota é responsável por visualizar um resultado específico
    """
    resultado = session.query(Jogo).filter(Jogo.id == id_resultado).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Resultado não encontrado")
    
    if resultado.usuario != usuario.id and not usuario.admin:
        raise HTTPException(status_code=403, detail="Você não tem permissão para visualizar este resultado")
    
    return {
        "id": resultado.id,
        "resultado": resultado
    }

@jogos_router.get("/zerar")
async def visualizar_resultado(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Somente administradores podem zerar resultados")
    else:
        session.query(Jogo).delete()
        session.commit()
    
    return {
        "mensagem": "Base de dados zerada com sucesso"
    }
    
