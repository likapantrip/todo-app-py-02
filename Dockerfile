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