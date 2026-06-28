from sqlalchemy.ext.asyncio import AsyncSession

import api.models.task as task_model
import api.schemas.task as task_schema

# タスクを作成する非同期関数
async def create_task(
    # DBセッションとタスク作成用のスキーマオブジェクトを受け取る
    db: AsyncSession, task_create: task_schema.TaskCreate
) -> task_model.Task:
    # スキーマのデータ(task_create)を使い、DBモデル(Task)のインスタンスを作成する
    task = task_model.Task(**task_create.dict())
    # セッションにtaskを追加する（まだDBには保存されていない）
    db.add(task)
    # トランザクションをコミットし、DBへ保存する
    await db.commit()
    # 自動採番されたidなどをオブジェクトへ反映するため、DBから最新状態を再取得する
    await db.refresh(task)
    # 作成したタスクを返す
    return task