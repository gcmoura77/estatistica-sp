from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv(".env")
SECRET_KEY = os.getenv("SECRET_KEY")
print(SECRET_KEY)
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
# deprecated -> pode ser passado mais de um esquema de criptografia e ele usario o modelo que não está obsoleto
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from auth_routes import auth_router
from jogos_routes import jogos_router

app.include_router(auth_router)
app.include_router(jogos_router)    