from fastapi import APIRouter
from typing import List
import api.schemas.task as task_schema

# FastAPIでAPIのルーティング（URLと処理の対応付け）をまとめるためのルーターを作成
router = APIRouter()

# GET /tasks にリクエストが送信されたときに実行される処理を定義
@router.get("/tasks", response_model=List[task_schema.Task])
async def list_tasks():
    return [task_schema.Task(id=1, title="1つ目のTODOタスク")]

# POST /tasks にリクエストが送信されたときに実行される処理を定義
@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=1, **task_body.dict())

# PUT /tasks/{task_id} にリクエストが送信されたときに実行される処理を定義
@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(task_id: int, task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=task_id, **task_body.dict())

# DELETE /tasks/{task_id} にリクエストが送信されたときに実行される処理を定義
@router.delete("/tasks/{task_id}", response_model=None)
async def delete_task(task_id: int):
    return