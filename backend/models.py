from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import declarative_base
from datetime import datetime

db = create_engine('sqlite:///banco.db') # link do banco de dados

# criar a base do banco de dados
Base = declarative_base()   

# criar as classes/tabelas do banco
class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False, unique=True)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean )
    admin = Column("admin", Boolean)
    criado_em = Column("criadoem", DateTime, default=datetime.now())
    
    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin
    
class Jogo(Base):
    __tablename__ = 'jogos'
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    usuario = Column("usuario", ForeignKey('usuarios.id'))
    adversario =  Column("adversario", String) 
    local = Column("local", String) # local do jogo: casa, fora, neutro
    gols_pro = Column("golspro", Integer) # gols feitos pelo time
    gols_contra = Column("golscontra", Integer) # gols levados pelo time
    torneio = Column("torneio", String) # torneio do jogo 
    data_jogo = Column("datajogo", DateTime, default=datetime.now())
    nota = Column("nota", Float, nullable=True) # nota do jogo
    tecnico = Column("tecnico", String) # nome do técnico
    criado_em = Column("criadoem", DateTime, default=datetime.now())
    pontos = Column("pontos", Integer) # pontos ganhos no jogo
    resultado = Column("resultado", String) # resultado do jogo: vitória, derrota, empate
    # itens
    # itens = relationship("ItemPedido", cascade="all, delete")
    
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.get('usuario', None)
        self.adversario = kwargs.get('adversario', '')
        self.local = kwargs.get('local', '')
        self.gols_pro = kwargs.get('gols_pro', 0)
        self.gols_contra = kwargs.get('gols_contra', 0)
        self.torneio = kwargs.get('torneio', '')
        self.data_jogo = kwargs.get('data_jogo', datetime.now())
        self.nota = kwargs.get('nota', 0.0)
        self.tecnico = kwargs.get('tecnico', '')
        self.calcular_resultado()
        self.calcular_pontos()
        
    def calcular_resultado(self):
        if self.gols_pro > self.gols_contra:
            self.resultado = 'Vitória'
        elif self.gols_pro < self.gols_contra:
            self.resultado = 'Derrota'
        else:
            self.resultado = 'Empate'
        
    def calcular_pontos(self):
        if self.resultado == "Vitória":
            self.pontos = 3
        elif self.resultado == "Empate":
            self.pontos = 1
        else:
            self.pontos = 0
       
