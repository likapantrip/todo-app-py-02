## 概要
FastAPIの学習を目的として作成したTODOアプリ。

### 主な機能
- TODO一覧取得
- TODO登録
- TODO更新
- TODO削除

### 技術スタック
- FastAPI
- Docker
- Poetry
- SQLAlchemy（予定）
- SQLite（予定）

### 参考書籍
[FastAPI入門](https://zenn.dev/sh0nk/books/537bb028709ab9)

## ディレクトリ構成
```
todo-app-py-02
├─ /.dockervenv        # Docker コンテナ用の仮想環境
├─ /.venv              # ローカル環境の仮想環境
├─ api
│   ├─ __init__.py
│   ├─ db.py
│   ├─ main.py
│   ├─ migrate_db.py
│   ├─ cruds
│   │   ├─ __init__.py
│   │   ├─ done.py
│   │   └─ task.py
│   ├─ models
│   │   ├─ __init__.py
│   │   └─ task.py
│   ├─ routers
│   │   ├─ __init__.py
│   │   ├─ done.py
│   │   └─ task.py
│   └─ schemas
│       ├─ __init__.py
│       └─ task.py
├─ tests
│   ├─ __init__.py
│   └─ test_main.py
├─ .gitattributes
├─ .gitignore
├─ docker-compose.yaml
├─ Dockerfile
├─ poetry.lock
├─ pyproject.toml
└─ README.md
```

## テーブル設計
### tasks
|カラム名|Type|備考|
|-|-|-|
|id|INT|primary, auto increment|
|title|VARCHAR(1024)||

### dones
|カラム名|Type|備考|
|-|-|-|
|id|INT|primary, auto increment, foreign key(task.id)|

## 手順
### Docker環境を構築
1. DockerがPCにインストールされていることを確認する
    ```bash
    $ docker compose version
    # Docker Compose version v5.1.3
    ```
1. プロジェクトディレクトリの直下に `docker-compose.yaml` を作成する
    ```docker-compose.yaml
    services:                          # 起動するコンテナの一覧を定義
        demo-app:                      # サービス名(コンテナを識別する名前)
            build: .                   # カレントディレクトリのDockerfileを使ってイメージを作成 (.は、カレントディレクトリ)
            volumes:                   # ホスト(PC)とコンテナの間でファイルを共有(同期)する設定
            - .dockervenv:/src/.venv   # ホストマシンの .dockervenv を、コンテナ内の /src/.venv と同期
            - .:/src                   # ホストマシンのカレントディレクトリ全体をコンテナの /src と同期
            ports:                     # ホストマシンとコンテナの間でポートを接続するための設定
            - 8000:8000                # localhost:8000 へのアクセスを、コンテナの8000番ポートへ転送
    ```
1. プロジェクトディレクトリの直下に `Dockerfile` を作成する
    ```Dockerfile
    # Python3.11が使えるLinux環境をベースイメージとして指定
    FROM python:3.11-slim

    # Pythonのログを即座に表示する環境変数を設定
    ENV PYTHONUNBUFFERED=1 

    # 作業ディレクトリを指定
    WORKDIR /src

    # pipを使ってpoetryをインストール
    RUN pip install poetry

    # poetryの定義ファイル(pyproject.toml / poetry.lock)をコピー
    # 存在するファイルのみコピー
    COPY pyproject.toml* poetry.lock* ./

    # 仮想環境をプロジェクト内(.venv)に作成するように、poetryを設定変更
    RUN poetry config virtualenvs.in-project true

    # (pyproject.tomlが存在する場合、)poetryで依存ライブラリをインストール
    # --no-rootオプションは、プロジェクトのルートパッケージをインストールしないようにするためのもの
    RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

    # uvicornのサーバーを立ち上げ、FastAPIのアプリを起動
    ENTRYPOINT ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]
    ```
1. 下記コマンドを実行することで、Dockerイメージをビルドする
    ```bash
    $ docker compose build
    # [+] build 1/1
    #  ✔ Image todo-app-py-02-demo-app Built                                    111.4s
    ```
1. `pyproject.toml`を作成する
    1. 下記コマンドを実行することで、Dockerコンテナ（demo-app）の中で、 `poetry init` コマンドを実行する
        ```bash
        $ docker compose run \
        --entrypoint "poetry init \
            --name demo-app \
            --dependency fastapi \
            --dependency uvicorn[standard]" \
        demo-app
        ```
    1. Authorのパートのみ `n` を入力し、それ以外はすべてEnterキーを押下する
        ```bash
        Version [0.1.0]:  
        Description []:  
        Author [None, n to skip]:  n
        License []:  
        Compatible Python versions [>=3.11]:  
        ...
        ```
1. 下記コマンドを実行し、`pyproject.toml` に定義された依存パッケージ（FastAPI、uvicorn）をインストールする
    ```bash
    $ docker compose run --entrypoint "poetry install --no-root" demo-app
    ```
1. インストール完了後、`poetry.lock` がプロジェクトディレクトリ直下に作成されたことを確認する
1. プロジェクトディレクトリの直下に `.gitignore` を作成する
    ```.gitignore
    # Docker関連の仮想環境
    .dockervenv/

    # Python 仮想環境
    .venv/
    venv/
    env/
    ENV/
    env.bak/
    venv.bak/

    # Python キャッシュ
    __pycache__/
    *.py[cod]
    *$py.class
    *.so
    .Python

    # 分布パッケージ
    build/
    develop-eggs/
    dist/
    downloads/
    eggs/
    .eggs/
    lib/
    lib64/
    parts/
    sdist/
    var/
    wheels/
    pip-wheel-metadata/
    share/python-wheels/
    *.egg-info/
    .installed.cfg
    *.egg
    MANIFEST

    # PyInstaller
    *.manifest
    *.spec

    # pytest
    .pytest_cache/
    .coverage
    htmlcov/

    # IDE
    .vscode/
    .idea/
    *.swp
    *.swo
    *~
    .DS_Store

    # 環境変数ファイル
    .env
    .env.local
    .env.*.local

    # その他
    *.log
    .mypy_cache/
    .dmypy.json
    dmypy.json
    .pyre/
    *.bak
    ```

### FastAPIを実行
1. `api/__init__.py` を作成する
1. `api/main.py`を作成する
    ```py:main.py
    from fastapi import FastAPI

    # FastAPIのインスタンスを作成。uvicornからこのappが読み込まれ、リクエストを処理する。
    app = FastAPI()

    # GET /hello にアクセスされたときに実行される処理を定義
    @app.get("/hello")
    async def hello():
        return {"message": "hello world!"}
    ```
1. 下記コマンドを実行し、サーバーを立ち上げる
    ```bash
    $ docker compose up -d
    ```
1. ブラウザで[http://localhost:8000/docs](http://localhost:8000/docs)にアクセスする
1. `Execute` をクリックし、`{"message": "hello world!"}`が返ることを確認する
    [![Image from Gyazo](https://i.gyazo.com/11201b29b3a86068cd5724ddda310268.gif)](https://gyazo.com/11201b29b3a86068cd5724ddda310268)

### ルーター実装
1. `api/routers/__init__.py` を作成する
1. `api/routers/task.py` を作成する
    ```py:task.py
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
    ```
1. `api/routers/done.py` を作成する
    ```py:done.py
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
    ```
1. `api/main.py` を編集し、FastAPI本体にルーターを登録する
    ```py:main.py
    from fastapi import FastAPI
    from api.routers import task, done

    # FastAPIのインスタンスを作成。uvicornからこのappが読み込まれ、リクエストを処理する。
    app = FastAPI()

    # FastAPI本体にルーターを登録する。これにより、ルーターで定義されたエンドポイントが有効になる。
    # この登録がない場合、Swagger UIなどでエンドポイントが表示されない。
    app.include_router(task.router)
    app.include_router(done.router)
    ```
1. ブラウザで[http://localhost:8000/docs](http://localhost:8000/docs)にアクセスする
1. ６つのパスオペレーション関数に対応するエンドポイントが表示されることを確認する
    [![Image from Gyazo](https://i.gyazo.com/bf9e9aab6fd65a27e127c7783e3f574a.png)](https://gyazo.com/bf9e9aab6fd65a27e127c7783e3f574a)
1. Response bodyは `null` になることを確認する
    [![Image from Gyazo](https://i.gyazo.com/ca898b52ab9264a52c95f0d5e9325e39.png)](https://gyazo.com/ca898b52ab9264a52c95f0d5e9325e39)

### スキーマ実装
1. `api/schemas/__init__.py` を作成する
1. `api/schemas/task.py` を作成する
    ```py:task.py
    from typing import Optional

    from pydantic import BaseModel, Field

    # タスクのスキーマ定義(APIの入出力に使用)
    class Task(BaseModel):
        id: int
        title: Optional[str] = Field(None, example="クリーニングを取りに行く")
        done: bool = Field(False, description="完了フラグ")
    ```
1. `api/routers/task.py`を編集し、GET /tasks のレスポンスに使用するスキーマを指定する
    ```py:task.py
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
    ```
1. ブラウザで[http://localhost:8000/docs](http://localhost:8000/docs)にアクセスする
1. Response bodyが追加されたことを確認する
    [![Image from Gyazo](https://i.gyazo.com/46e6d7c197a91d244131e915d40df5cb.png)](https://gyazo.com/46e6d7c197a91d244131e915d40df5cb)
1. `api/schemas/task.py` を編集する
    1. 必要なスキーマを定義する
        ```py:task.py
        from typing import Optional

        from pydantic import BaseModel, Field

        # タスクのスキーマ定義(APIの入出力に使用)
        class Task(BaseModel):
            id: int
            title: Optional[str] = Field(None, example="クリーニングを取りに行く")
            done: bool = Field(False, description="完了フラグ")

        # タスク作成のためのスキーマ定義(APIの入力に使用)
        class TaskCreate(BaseModel):
            title: Optional[str] = Field(None, example="クリーニングを取りに行く")

        # タスク作成のレスポンス用スキーマ定義(APIの出力に使用)
        class TaskCreateResponse(BaseModel):
            id: int
            title: Optional[str] = Field(None, example="クリーニングを取りに行く")
        ```
    1. SQLAlchemyのORMモデルをPydanticスキーマへ変換できるように
 `orm_mode` を追加する
        ```py:task.py
        from typing import Optional

        from pydantic import BaseModel, Field

        # タスクのスキーマ定義(APIの入出力に使用)
        class Task(BaseModel):
            id: int
            title: Optional[str] = Field(None, example="クリーニングを取りに行く")
            done: bool = Field(False, description="完了フラグ")

            class Config:
                orm_mode = True

        # タスク作成のためのスキーマ定義(APIの入力に使用)
        class TaskCreate(BaseModel):
            title: Optional[str] = Field(None, example="クリーニングを取りに行く")

        # タスク作成のレスポンス用スキーマ定義(APIの出力に使用)
        class TaskCreateResponse(BaseModel):
            id: int
            title: Optional[str] = Field(None, example="クリーニングを取りに行く")

            class Config:
                orm_mode = True
        ```
    1. `TaskBase` を作成し、リファクタリングする
        ```py:task.py
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
                orm_mode = True
        ```
1. `api/routers/task.py` を編集し、POST /tasks のレスポンスに使用するスキーマを指定する
    ```py:task.py
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
    @router.put("/tasks/{task_id}")
    async def update_task():
        pass # 何もしない文

    # DELETE /tasks/{task_id} にリクエストが送信されたときに実行される処理を定義
    @router.delete("/tasks/{task_id}")
    async def delete_task():
        pass # 何もしない文
    ```
1. ブラウザで[http://localhost:8000/docs](http://localhost:8000/docs)にアクセスする
1. POSTのリクエストボディが動的に変更されることを確認する
    [![Image from Gyazo](https://i.gyazo.com/38c6eb1af4967121eacfc8e266d96566.gif)](https://gyazo.com/38c6eb1af4967121eacfc8e266d96566)
1. `api/routers/task.py` を編集し、PUT /tasks/{task_id} のリクエスト・レスポンスに使用するスキーマと、 DELETE /tasks/{task_id} のレスポンスに使用するスキーマを指定する
    ```py:task.py
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
    ```
1. `api/routers/done.py` を編集し、スキーマを指定する
    ```py:done.py
    from fastapi import APIRouter

    # FastAPIでAPIのルーティング（URLと処理の対応付け）をまとめるためのオブジェクトを作成する。
    router = APIRouter()

    # PUT /tasks/{task_id}/done にリクエストが送信されたときに実行される処理を定義
    @router.put("/tasks/{task_id}/done", response_model=None)
    async def mark_task_as_done(task_id: int):
        return

    # DELETE /tasks/{task_id}/done にリクエストが送信されたときに実行される処理を定義
    @router.delete("/tasks/{task_id}/done", response_model=None)
    async def unmark_task_as_done(task_id: int):
        return
    ```

### DB接続
1. `docker-compose.yaml` を編集し、DB接続できるように修正する
    ```docker-compose.yaml
    services:                              # 起動するコンテナの一覧を定義
        demo-app:                          # サービス名(コンテナを識別する名前)
            build: .                       # カレントディレクトリのDockerfileを使ってイメージを作成 (.は、カレントディレクトリ)
            volumes:                       # ホスト(PC)とコンテナの間でファイルを共有(同期)する設定
                - .dockervenv:/src/.venv   # ホストマシンの .dockervenv を、コンテナ内の /src/.venv と同期
                - .:/src                   # ホストマシンのカレントディレクトリ全体をコンテナの /src と同期
            ports:                         # ホストマシンとコンテナの間でポートを接続するための設定
                - 8000:8000                # localhost:8000 へのアクセスを、コンテナの8000番ポートへ転送
        db:
            image: mysql:8.0
            platform: linux/x86_64                 # M1 Macの場合必要
            environment:
                MYSQL_ALLOW_EMPTY_PASSWORD: 'yes'  # rootアカウントをパスワードなしで作成
                MYSQL_DATABASE: 'demo'             # 初期データベースとしてdemoを設定
                TZ: 'Asia/Tokyo'                   # タイムゾーンを日本時間に設定
            volumes:
                - mysql_data:/var/lib/mysql
            command: --default-authentication-plugin=mysql_native_password  # MySQL8.0ではデフォルトが"caching_sha2_password"で、ドライバが非対応のため変更
            ports:
                - 33306:3306  # ホストマシンのポート33306を、docker内のポート3306に接続する
    volumes:
        mysql_data:
    ```
1. 下記コマンドを実行し、サーバーを停止する
    ```bash
    $ docker compose down
    ```
1. 下記コマンドを実行し、サーバーとSQLを同時に立ち上げる
    ```bash
    $ docker compose up -d
    ```
1. 別のコンソールを開く
1. プロジェクトディレクトリで下記コマンドを実行し、MySQLクライアントが実行されて、DBに接続できていることを確認する
    ```bash
    % docker compose exec db mysql demo
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 8
    Server version: 8.0.46 MySQL Community Server - GPL

    Copyright (c) 2000, 2026, Oracle and/or its affiliates.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql> exit
    Bye
    ```
1. 下記コマンドを実行し、`sqlalchemy` と `aiomysql` をインストールする
    ```bash
    $ docker compose exec demo-app poetry add sqlalchemy aiomysql
    ```
1. インストールした結果、`pyproject.toml` や `poetry.lock` の中身が変更されていることを確認する
1. `api/db.py` を作成する
    ```py:db.py
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker, declarative_base

    # MySQLのdockerコンテナに対して接続するセッションを作成
    ASYNC_DB_URL = "mysql+aiomysql://root@db:3306/demo?charset=utf8"

    async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
    async_session = sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )

    Base = declarative_base()

    # データベースセッションを取得するための依存関係
    async def get_db():
        async with async_session() as session:
            yield session
    ```

### DBモデル実装
1. `api/models/__init__.py` を作成する
1. `api/models/task.py` を作成する
    ```py:task.py
    from sqlalchemy import Column, Integer, String, ForeignKey
    from sqlalchemy.orm import relationship

    from api.db import Base

    # tasksテーブルのモデルクラスを定義
    class Task(Base):
        __tablename__ = "tasks"

        id = Column(Integer, primary_key=True)
        title = Column(String(1024))

        done = relationship("Done", back_populates="task", cascade="delete")

    # donesテーブルのモデルクラスを定義
    class Done(Base):
        __tablename__ = "dones"

        id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)

        task = relationship("Task", back_populates="done")
    ```

### テーブル作成
1. DBマイグレーション用のスクリプト `api/migrate_db.py` を作成する
    ```py:migrate_db.py
    from sqlalchemy import create_engine

    from api.models.task import Base

    # どのデータベースに接続するか」を表す接続文字列（DB URL）
    DB_URL = "mysql+pymysql://root@db:3306/demo?charset=utf8"
    # 接続情報(DB_URL)を使ってDB接続用のエンジンを作成。echo=TrueはSQL文をログに出力するオプション
    engine = create_engine(DB_URL, echo=True)


    def reset_database():
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)


    if __name__ == "__main__":
        reset_database()
    ```
1. 下記コマンドでスクリプトを実行し、MySQLにテーブルを作成する
    ```bash
    $ docker compose exec demo-app poetry run python -m api.migrate_db
    ```
1. 下記コマンドを実行してMySQLクライアントを起動し、テーブル情報を確認する
    ```bash
    % docker compose exec db mysql demo
    Reading table information for completion of table and column names
    You can turn off this feature to get a quicker startup with -A

    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 11
    Server version: 8.0.46 MySQL Community Server - GPL

    Copyright (c) 2000, 2026, Oracle and/or its affiliates.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql> SHOW TABLES;
    +----------------+
    | Tables_in_demo |
    +----------------+
    | dones          |
    | tasks          |
    +----------------+
    2 rows in set (0.01 sec)

    mysql> DESCRIBE tasks;
    +-------+---------------+------+-----+---------+----------------+
    | Field | Type          | Null | Key | Default | Extra          |
    +-------+---------------+------+-----+---------+----------------+
    | id    | int           | NO   | PRI | NULL    | auto_increment |
    | title | varchar(1024) | YES  |     | NULL    |                |
    +-------+---------------+------+-----+---------+----------------+
    2 rows in set (0.02 sec)

    mysql> DESCRIBE dones;
    +-------+------+------+-----+---------+-------+
    | Field | Type | Null | Key | Default | Extra |
    +-------+------+------+-----+---------+-------+
    | id    | int  | NO   | PRI | NULL    |       |
    +-------+------+------+-----+---------+-------+
    1 row in set (0.01 sec)

    mysql> exit
    Bye
    ```

### CRUDs実装
1. `api/cruds/__init__.py` を作成する
1. `api/cruds/task.py` を作成し、Create処理を記述する
    ```py:task.py
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
    ```
1. `api/routers/task.py` を編集し、DBにデータ登録できるように修正する
    ```py:task.py
    from fastapi import APIRouter, Depends
    from typing import List
    from sqlalchemy.ext.asyncio import AsyncSession

    import api.schemas.task as task_schema
    import api.cruds.task as task_crud
    from api.db import get_db

    # FastAPIでAPIのルーティング（URLと処理の対応付け）をまとめるためのルーターを作成
    router = APIRouter()

    # GET /tasks にリクエストが送信されたときに実行される処理を定義
    @router.get("/tasks", response_model=List[task_schema.Task])
    async def list_tasks():
        return [task_schema.Task(id=1, title="1つ目のTODOタスク")]

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
    async def update_task(task_id: int, task_body: task_schema.TaskCreate):
        return task_schema.TaskCreateResponse(id=task_id, **task_body.dict())

    # DELETE /tasks/{task_id} にリクエストが送信されたときに実行される処理を定義
    @router.delete("/tasks/{task_id}", response_model=None)
    async def delete_task(task_id: int):
        return
    ```
1. ブラウザで[http://localhost:8000/docs](http://localhost:8000/docs)にアクセスする
1. POSTの「Execute」をクリックするたびに、`id` がインクリメントされて結果が返ることを確認する
    [![Image from Gyazo](https://i.gyazo.com/c871aa6b324c697372844412083076fa.gif)](https://gyazo.com/c871aa6b324c697372844412083076fa)
1. `api/cruds/task.py` を編集し、Read処理を追記する
    ```py:task.py
    from typing import List, Tuple

    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy import select
    from sqlalchemy.engine import Result

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

    # タスクの一覧を取得する非同期関数
    async def get_tasks_with_done(db: AsyncSession) -> List[Tuple[int, str, bool]]:
        result: Result = await (
            db.execute(
                select(
                    task_model.Task.id,
                    task_model.Task.title,
                    task_model.Done.id.isnot(None).label("done"),
                ).outerjoin(task_model.Done)
            )
        )
        return result.all()
    ```
1. `api/routers/task.py` を編集し、DBデータを表示できるように修正する
    ```py:task.py
    from fastapi import APIRouter, Depends
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
    async def update_task(task_id: int, task_body: task_schema.TaskCreate):
        return task_schema.TaskCreateResponse(id=task_id, **task_body.dict())

    # DELETE /tasks/{task_id} にリクエストが送信されたときに実行される処理を定義
    @router.delete("/tasks/{task_id}", response_model=None)
    async def delete_task(task_id: int):
        return
    ```
1. ブラウザで[http://localhost:8000/docs](http://localhost:8000/docs)にアクセスする
1. Createした回数のTODOタスクが作成されていることを確認する
    [![Image from Gyazo](https://i.gyazo.com/c2d1dbfdf26c032685a91211c118fbf0.png)](https://gyazo.com/c2d1dbfdf26c032685a91211c118fbf0)
1. `api/cruds/task.py` を編集し、Update処理を追記する
    ```py:task.py
    from typing import List, Tuple, Optional

    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy import select
    from sqlalchemy.engine import Result

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

    # タスクの一覧を取得する非同期関数
    async def get_tasks_with_done(db: AsyncSession) -> List[Tuple[int, str, bool]]:
        result: Result = await (
            db.execute(
                select(
                    task_model.Task.id,
                    task_model.Task.title,
                    task_model.Done.id.isnot(None).label("done"),
                ).outerjoin(task_model.Done)
            )
        )
        return result.all()

    # タスクを取得する非同期関数
    async def get_task(db: AsyncSession, task_id: int) -> Optional[task_model.Task]:
        result: Result = await db.execute(
            select(task_model.Task).filter(task_model.Task.id == task_id)
        )
        task: Optional[Tuple[task_model.Task]] = result.first()
        return task[0] if task is not None else None  # 要素が一つであってもtupleで返却されるので１つ目の要素を取り出す

    # タスクを更新する非同期関数
    async def update_task(
        db: AsyncSession, task_create: task_schema.TaskCreate, original: task_model.Task
    ) -> task_model.Task:
        original.title = task_create.title
        db.add(original)
        await db.commit()
        await db.refresh(original)
        return original
    ```
1. `api/routers/task.py` を編集し、DBデータを更新できるようにする
    ```py:task.py
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
    async def delete_task(task_id: int):
        return
    ```
1. TODOタスクのtitleが更新できることを確認する
    [![Image from Gyazo](https://i.gyazo.com/7fbe85c2cb43f770202d21145d935009.gif)](https://gyazo.com/7fbe85c2cb43f770202d21145d935009)
    [![Image from Gyazo](https://i.gyazo.com/56ed8336e60109c344985b6be52c9849.png)](https://gyazo.com/56ed8336e60109c344985b6be52c9849)
1. `api/cruds/task.py` を編集し、Delete処理を追記する
    ```py:task.py
    from typing import List, Tuple, Optional

    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy import select
    from sqlalchemy.engine import Result

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

    # タスクの一覧を取得する非同期関数
    async def get_tasks_with_done(db: AsyncSession) -> List[Tuple[int, str, bool]]:
        result: Result = await (
            db.execute(
                select(
                    task_model.Task.id,
                    task_model.Task.title,
                    task_model.Done.id.isnot(None).label("done"),
                ).outerjoin(task_model.Done)
            )
        )
        return result.all()

    # タスクを取得する非同期関数
    async def get_task(db: AsyncSession, task_id: int) -> Optional[task_model.Task]:
        result: Result = await db.execute(
            select(task_model.Task).filter(task_model.Task.id == task_id)
        )
        task: Optional[Tuple[task_model.Task]] = result.first()
        return task[0] if task is not None else None  # 要素が一つであってもtupleで返却されるので１つ目の要素を取り出す

    # タスクを更新する非同期関数
    async def update_task(
        db: AsyncSession, task_create: task_schema.TaskCreate, original: task_model.Task
    ) -> task_model.Task:
        original.title = task_create.title
        db.add(original)
        await db.commit()
        await db.refresh(original)
        return original

    # タスクを削除する非同期関数
    async def delete_task(db: AsyncSession, original: task_model.Task) -> None:
        await db.delete(original)
        await db.commit()
    ```
1. `api/routers/task.py` を編集し、DBデータを削除できるようにする
    ```py:task.py
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
    ```
1. TODOタスクが削除できることを確認する
    [![Image from Gyazo](https://i.gyazo.com/9439411464e91435a931fade5802c0a1.gif)](https://gyazo.com/9439411464e91435a931fade5802c0a1)
    [![Image from Gyazo](https://i.gyazo.com/091afe5482ca076c00748f267d83a214.png)](https://gyazo.com/091afe5482ca076c00748f267d83a214)
1. `api/cruds/done.py` を作成する
    ```py:done.py
    from typing import Tuple, Optional

    from sqlalchemy import select
    from sqlalchemy.engine import Result
    from sqlalchemy.ext.asyncio import AsyncSession

    import api.models.task as task_model


    async def get_done(db: AsyncSession, task_id: int) -> Optional[task_model.Done]:
        result: Result = await db.execute(
            select(task_model.Done).filter(task_model.Done.id == task_id)
        )
        done: Optional[Tuple[task_model.Done]] = result.first()
        return done[0] if done is not None else None  # 要素が一つであってもtupleで返却されるので１つ目の要素を取り出す


    async def create_done(db: AsyncSession, task_id: int) -> task_model.Done:
        done = task_model.Done(id=task_id)
        db.add(done)
        await db.commit()
        await db.refresh(done)
        return done


    async def delete_done(db: AsyncSession, original: task_model.Done) -> None:
        await db.delete(original)
        await db.commit()
    ```
1. `api/routers/done.py` を編集する
    ```done.py
    from fastapi import APIRouter, HTTPException, Depends
    from sqlalchemy.ext.asyncio import AsyncSession

    import api.schemas.done as done_schema
    import api.cruds.done as done_crud
    from api.db import get_db

    # FastAPIでAPIのルーティング（URLと処理の対応付け）をまとめるためのオブジェクトを作成する。
    router = APIRouter()

    # PUT /tasks/{task_id}/done にリクエストが送信されたときに実行される処理を定義
    @router.put("/tasks/{task_id}/done", response_model=done_schema.DoneResponse)
    async def mark_task_as_done(task_id: int, db: AsyncSession = Depends(get_db)):
        done = await done_crud.get_done(db, task_id=task_id)
        if done is not None:
            raise HTTPException(status_code=400, detail="Done already exists")

        return await done_crud.create_done(db, task_id)

    # DELETE /tasks/{task_id}/done にリクエストが送信されたときに実行される処理を定義
    @router.delete("/tasks/{task_id}/done", response_model=None)
    async def unmark_task_as_done(task_id: int, db: AsyncSession = Depends(get_db)):
        done = await done_crud.get_done(db, task_id=task_id)
        if done is None:
            raise HTTPException(status_code=404, detail="Done not found")

        return await done_crud.delete_done(db, original=done)
    ```
1. `api/schemas/done.py` を作成する
    ```py:done.py
    from pydantic import BaseModel

    class DoneResponse(BaseModel):
        id: int

        class Config:
            orm_mode = True
    ```
1. ブラウザで[http://localhost:8000/docs](http://localhost:8000/docs)にアクセスする
1. DoneをCreateすることで、完了フラグをtrueにできることを確認する
    [![Image from Gyazo](https://i.gyazo.com/0163575b3a1c0a4a8b1ff7a92179b631.png)](https://gyazo.com/0163575b3a1c0a4a8b1ff7a92179b631)

### ユニットテスト
1. 下記コマンドを実行し、開発用モードの場合に `pytest-asyncio` をインストールする
    ```bash
    $ docker compose exec demo-app poetry add -D pytest-asyncio aiosqlite httpx
    ```
1. インストールした結果、`pyproject.toml` や `poetry.lock` の中身が変更されていることを確認する
1. プロジェクトディレクトリの直下に `tests` ディレクトリを作成する
1. `tests/__init__.py` を作成する
1. テストファイル`tests/test_main.py` を作成する
    ```py:test_main.py
    import pytest
    import pytest_asyncio
    from httpx import AsyncClient, ASGITransport
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker

    from api.db import get_db, Base
    from api.main import app

    import starlette.status

    ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"


    @pytest_asyncio.fixture
    async def async_client() -> AsyncClient:
        # Async用のengineとsessionを作成
        async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
        async_session = sessionmaker(
            autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
        )

        # テスト用にオンメモリのSQLiteテーブルを初期化（関数ごとにリセット）
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        # DIを使ってFastAPIのDBの向き先をテスト用DBに変更
        async def get_test_db():
            async with async_session() as session:
                yield session

        app.dependency_overrides[get_db] = get_test_db

        # テスト用に非同期HTTPクライアントを返却
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            yield client

    @pytest.mark.asyncio
    async def test_create_and_read(async_client):
        response = await async_client.post("/tasks", json={"title": "テストタスク"})
        assert response.status_code == starlette.status.HTTP_200_OK
        response_obj = response.json()
        assert response_obj["title"] == "テストタスク"

        response = await async_client.get("/tasks")
        assert response.status_code == starlette.status.HTTP_200_OK
        response_obj = response.json()
        assert len(response_obj) == 1
        assert response_obj[0]["title"] == "テストタスク"
        assert response_obj[0]["done"] is False

    @pytest.mark.asyncio
    async def test_done_flag(async_client):
        response = await async_client.post("/tasks", json={"title": "テストタスク2"})
        assert response.status_code == starlette.status.HTTP_200_OK
        response_obj = response.json()
        assert response_obj["title"] == "テストタスク2"

        # 完了フラグを立てる
        response = await async_client.put("/tasks/1/done")
        assert response.status_code == starlette.status.HTTP_200_OK

        # 既に完了フラグが立っているので400を返却
        response = await async_client.put("/tasks/1/done")
        assert response.status_code == starlette.status.HTTP_400_BAD_REQUEST

        # 完了フラグを外す
        response = await async_client.delete("/tasks/1/done")
        assert response.status_code == starlette.status.HTTP_200_OK

        # 既に完了フラグが外れているので404を返却
        response = await async_client.delete("/tasks/1/done")
        assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
    ```
1. 下記コマンドを実行し、テストを行う
    ```bash
    $ docker compose run --entrypoint "poetry run pytest" demo-app
    ```
1. テストが成功したことを確認する
    ```bash
    ============================= test session starts ==============================
    platform linux -- Python 3.11.15, pytest-9.1.0, pluggy-1.6.0
    rootdir: /src
    …
    ======================== 2 passed, 8 warnings in 1.62s =========================
    ```

### サーバー停止
1. 下記コマンドを実行し、サーバーを停止する
    ```bash
    $ docker compose down
    ```

## 補足説明
### Docker関連ファイル
|ファイル名|役割|
|-|-|
|docker-compose.yaml|Docker Composeの設定ファイル。コンテナの構成（イメージ、ポート、ボリュームなど）を定義する。`build` を指定した場合は `Dockerfile` を利用してイメージを作成する。|
|Dockerfile|Dockerイメージの設計図。Python環境の作成やライブラリのインストール手順を定義する。|

### Docker構成
#### ファイル構成・volume同期
```
ホスト(Mac)
todo-app-py-02 (プロジェクトフォルダ)  <────────────────────────────────────────────────────────────────┐
│                                                                                                    │ /src と同期
├─ /.venv                                                                                            │ (設定: volumes の .:/src)
├─ docker-compose.yaml                                                                               │
├─ Dockerfile                                                                                        │
├─ poetry.lock                                                                                       │
├─ pyproject.toml                                                                                    │
│                                                                                                    │
└─ /.dockervenv                     <────────────────────┐                                           │
                                                         │ /src/.venv と同期                          │
                                                         │ (設定: volumes の .dockervenv:/src/.venv)  │
Dockerコンテナ (demo-app)                                 │                                           │
│                                                        │                                           │
├─ /src/.venv                       <────────────────────┘                                           │
│                                                                                                    │
└─ /src                             <────────────────────────────────────────────────────────────────┘
    ├─ api
    │    ├─ __init__.py
    │    └─ main.py        <- FastAPIアプリを定義
    ├─ docker-compose.yaml
    ├─ Dockerfile
    └─ pyproject.toml
```

- volumes はホストとコンテナでファイルを同期する仕組み
- コードを修正すると volumes によりコンテナ側にも即時反映される

#### ネットワーク通信
```
ブラウザ
    │
    ▼
http://localhost:8000
    │
    │ 通信
    │ (設定: ports)
    │
    ▼
Dockerコンテナ(demo-app)
    │
    ▼
uvicorn
    │
    ▼
FastAPI(api/main.py)
```

- ports はホストとコンテナで通信する仕組み
- FastAPIはコンテナ内で動作する

### `poetry init` コマンド
`pyproject.toml` を生成し、FastAPI本体とASGIサーバーである `uvicorn` を依存関係として登録する。

### ルーター構造イメージ
```
app = FastAPI()      <- アプリ本体
      │
      ├─ include_router(task.router)
      │      │
      │      ├─ GET /tasks
      │      ├─ POST /tasks
      │      ├─ PUT /tasks/{task_id}
      │      └─ DELETE /tasks/{task_id}
      │
      └─ include_router(done.router)
             │
             ├─ PUT /tasks/{task_id}/done
             └─ DELETE /tasks/{task_id}/done
```

### スキーマ構成イメージ
```
┌ task_schema.py ─────────────────┐
│                                 │
│ class Task(BaseModel)           │
│   ▲   「APIで返すデータの形」を定義  │
│   │                             │
└── │ ────────────────────────────┘
    └──────────────┐
                   │
┌ router.py ────── │ ──────────────────────────┐
│ @router.get(     │                           │
│     "/tasks",    │                           │
│     response_model=List[task_schema.Task]    │
│ )                │                           │
└──────────────────│ ──────────────────────────┘
                   ▼
          FastAPIが返却値を検証
                   │
                   ▼
          Taskスキーマ形式のJSONとして返却
```

### DB接続
```
FastAPI
   │
   ▼
SQLAlchemy
   │
   ▼
engine <- create_engine()で作成
 ↑データベースに接続して通信するための窓口
   │
   ▼
MySQL
```

### DBモデル構成イメージ
```
DBモデル <- テーブル構造を表現する（設計図）
  class Task(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    │
    │ DBモデル定義に合わせてDBにテーブルを作成
    ▼
tasksテーブル
  ┌────┬────────┐
  │ id │ title  │
  ├────┼────────┤
  │ 1  │ 買い物  │
  └────┴────────┘
    │
    │ CRUDsで select(Task) などを実行
    ▼
Taskオブジェクト <- テーブルの1レコードを表現する
  Task(
    id=1,
    title="買い物"
  )
```

### DBモデルによるオブジェクト化
```
基本的にはSQLを書かなくてもDB操作でき、PythonオブジェクトとしてDBを扱える。

DBモデル + SQLAlchemy(ORM)
    │
    ▼
SQLAlchemyがSQLを自動生成
    │
    ▼
MySQL
```