from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.task as task_schema
import api.cruds.task as task_crud
from api.db import get_db

# FastAPIでAPIのルーティング（URLと処理の対応付け）をまとめるためのルーターを作成
router = APIRouter()

# GET /tasks にリクエストが送信されたときに実行される処理を定義
@router.get("/tasks", response_model=List[task_schema.Task])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    return await task_crud.get_tasks_with_done(db)

# POST /tasks にリクエストが送信されたときに実行される処理を定義
@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(
    task_body: task_schema.TaskCreate, # 保存するタスクの情報を受け取るためのスキーマオブジェクト
    db: AsyncSession = Depends(get_db) # DBセッションを取得するための依存関係注入
):
    create_task = await task_crud.create_task(db, task_body) # タスクをDBに保存し、保存したタスクの情報を返す
    return create_task

# PUT /tasks/{task_id} にリクエストが送信されたときに実行される処理を定義
@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(
    task_id: int, task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)
):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.update_task(db, task_body, original=task)

# DELETE /tasks/{task_id} にリクエストが送信されたときに実行される処理を定義
@router.delete("/tasks/{task_id}", response_model=None)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.delete_task(db, original=task)