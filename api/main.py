from fastapi import FastAPI
from api.routers import task, done

# FastAPIのインスタンスを作成。uvicornからこのappが読み込まれ、リクエストを処理する。
app = FastAPI()

# FastAPI本体にルーターを登録する。これにより、ルーターで定義されたエンドポイントが有効になる。
# この登録がない場合、Swagger UIなどでエンドポイントが表示されない。
app.include_router(task.router)
app.include_router(done.router)