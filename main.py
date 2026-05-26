from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_db_and_tables
from routes.task_routes import router
from models.task_models import Task

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Todo API",
    description="API para gerenciamento de tarefas com arquitetura em camadas.",
    version="1.0.0",
    contact={
        "name": "Equipe da disciplina INF8B",
    },
    lifespan=lifespan,
)

app.include_router(router)
from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_db_and_tables
from routes.task_routes import router as task_router
from routes.auth_routes import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Todo API",
    description="API para gerenciamento de tarefas com autenticação JWT.",
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(task_router)
