from fastapi import APIRouter

# FastAPIでAPIのルーティング（URLと処理の対応付け）をまとめるためのルーターを作成
router = APIRouter()

# GET /tasks にリクエストが送信されたときに実行される処理を定義
@router.get("/tasks")
async def list_tasks():
    pass # 何もしない文

# POST /tasks にリクエストが送信されたときに実行される処理を定義
@router.post("/tasks")
async def create_task():
    pass # 何もしない文

# PUT /tasks/{task_id} にリクエストが送信されたときに実行される処理を定義
@router.put("/tasks/{task_id}")
async def update_task():
    pass # 何もしない文

# DELETE /tasks/{task_id} にリクエストが送信されたときに実行される処理を定義
@router.delete("/tasks/{task_id}")
async def delete_task():
    pass # 何もしない文