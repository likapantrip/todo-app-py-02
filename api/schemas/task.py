from typing import Optional

from pydantic import BaseModel, Field

# タスクのスキーマで共通のフィールドを定義するベースクラス
class TaskBase(BaseModel):
    title: Optional[str] = Field(None, example="クリーニングを取りに行く")

# タスクのスキーマ定義(APIの入出力に使用)
class Task(TaskBase):
    id: int
    done: bool = Field(False, description="完了フラグ")

    class Config:
        orm_mode = True

# タスク作成のためのスキーマ定義(APIの入力に使用)
class TaskCreate(TaskBase):
    pass

# タスク作成のレスポンス用スキーマ定義(APIの出力に使用)
class TaskCreateResponse(TaskCreate):
    id: int

    class Config:
        orm_mode = True # TaskCreateResponse が暗黙的にORMを受け取り、レスポンススキーマに変換する意味