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