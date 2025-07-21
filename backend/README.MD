# Configurações e Pacotes Necessários

- FastAPI
- Uvicorn
- SQLAlchemy
- Python-Jose[cryptography]
- python-dotenv 
- pyhton-multipart
- passlib[bcrypt]
- sqlalchemy_utils
- alembic

### Rodar a API

```bash
uvicorn main:app --reload
```
This command runs the FastAPI application defined in main.py with live reloading enabled.
The `--reload` flag allows the server to automatically restart when code changes are detected,
which is particularly useful during development for testing changes without manually restarting the server.

Link para acesso a documentação da API http://127.0.0.1:8000/docs

### Rest APIs

Get -> leitura/pegar
Post -> enviar/criar
Put/Patch -> edição
Delete -> Deletar

# Criação e Migração dos Dados com Alembic
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

outro exemplo: alembic revision --autogenerate -m "Adicionar itens no pedido"
