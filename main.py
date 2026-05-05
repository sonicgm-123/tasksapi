import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Inicia a Aplicação FastAPI
app = FastAPI()

class Task(BaseModel):
    title: str = Field(..., example = "Fazer compras")
    description: str = Field (..., example = "Comprar leite, pão e ovos")
    owner: str = Field(..., example = "João")
    status: str = Field(..., example = "Pendente")
    comments: list[str] = Field(default_factory=list, example=["Comentário1", "Comentário2"])

# Define um simples GET da rota padrão URL ("/")
@app.get("/") # Parametro que indica qual verbo será executado
async def get_root_message(): #Define nome da função
    # Retorna um Objeto JSON com mensagem Olá Mundo
    return {"message": "Hello World"}

@app.get("/tasks")
async def tasks(owner: str | None = None,
                status: str | None = None,
                skip: int = 0, limit: int | None = None):
    dados = await ler_arquivo_json()
    tasks_list = dados["tasks"]

    filtered_tasks = [
        task for task in tasks_list
        if(owner is None or owner.lower() in task["owner"].lower())
        and(status is None or status.lower()in task["status"].lower())
    ]

    if limit is None:
        return filtered_tasks[skip:]
    return filtered_tasks[skip:skip + limit]

@app.get("/tasks_id(id: int)")
async def tasks_id(id: int):
    responseTasks = await ler_arquivo_json()
    tasks_list = responseTasks["tasks"]
    task = next((item for item in tasks_list if item["id"] == id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks")
async def create_task(task: Task):
    tasks = await ler_arquivo_json()
    last_id = tasks["tasks"][-1]["id"] if tasks["tasks"] else 0
    new_task = task.model_dump()
    new_task["id"] = last_id + 1
    tasks["tasks"].append(new_task)
    with open("tasks.json", "w", encoding = "utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)
    return new_task



async def ler_arquivo_json():
    with open("tasks.json", encoding="utf-8") as f:
        dados = json.load(f)
    return dados 
@app.put("/tasks/{id}")
async def update_task(id: int, task: Task):
    tasks_data = await ler_arquivo_json()
    tasks_list = tasks_data["tasks"]
    index = next((i for i, item in enumerate(tasks_list) if item["id"] == id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = task.model_dump()
    updated["id"] = id
    tasks_list[index] = updated
    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump(tasks_data, f, ensure_ascii=False, indent=4)
    return updated

