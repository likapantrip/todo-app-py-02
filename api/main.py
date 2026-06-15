from fastapi import FastAPI

# FastAPIのインスタンスを作成。uvicornからこのappが読み込まれ、リクエストを処理する。
app = FastAPI()

# GET /hello にアクセスされたときに実行される処理を定義
@app.get("/hello")
async def hello():
    return {"message": "hello world!"}