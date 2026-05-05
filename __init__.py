from contextlib import asynccontextmanager
from fastapi import fasrAPI
@asynccontextmanager
async def lifespan(_: fastAPI):
    app = fastAPI(
        title="Todo API",
        description="API para gerenciamento de tarefas com arquitetura em comandas.",
        versiom="1.0.0",
        lifespan=lifespan,
        contact={
            "name": "Equipe da disciplina INF8",
           } ,)

    return app 