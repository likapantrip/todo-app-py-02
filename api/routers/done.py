from fastapi import APIRouter

# FastAPIでAPIのルーティング（URLと処理の対応付け）をまとめるためのオブジェクトを作成する。
router = APIRouter()

# PUT /tasks/{task_id}/done にリクエストが送信されたときに実行される処理を定義
@router.put("/tasks/{task_id}/done")
async def mark_task_as_done():
    pass # 何もしない文

# DELETE /tasks/{task_id}/done にリクエストが送信されたときに実行される処理を定義
@router.delete("/tasks/{task_id}/done")
async def unmark_task_as_done():
    pass # 何もしない文