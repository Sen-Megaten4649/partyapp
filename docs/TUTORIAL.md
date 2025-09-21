# partyapp チュートリアル

## ０．Git 初期化と最初のコミット

まずは Git リポジトリを初期化して、初期ファイル（README.md, TUTORIAL.md など）をコミットしておく。

```bash
cd /home/sen/partyapp/partyapp
git init
git add .
git commit -m "chore: initial commit (README + TUTORIAL.md + requirements.txt + skeleton)"
```

GitHub に push する場合は、リモートを追加して push。

```bash
git branch -M main
git remote add origin https://github.com/<yourname>/partyapp.git
git push -u origin main
```

---

## １．前提

- Proxmox 上に Ubuntu サーバーを構築済み
- `/home/sen/partyapp/` ワークスペースを作成済み
- Python 仮想環境 `.partyapp` が有効化できる状態
- 連携先の MariaDB (partyappdb) が起動済で、ユーザー・DB が作成済み

---

## ２．環境変数の設定

DB 接続情報を環境変数に設定する。  
`~/.bashrc` の末尾に追記すると便利。

```bash
export DB_USER="username"
export DB_PASSWORD="password"
export DB_HOST="192.168.0.xxx"
export DB_PORT="3306"
export DB_NAME="partyapp"

# 即時反映
source ~/.bashrc
```

---

## ３．ディレクトリ構成（この時点）

```
/home/sen/partyapp/
├── credentials/
│   └── .env
├── .partyapp/              # venv
└── partyapp/               # Gitリポジトリ
    ├── docs/
    │   └── TUTORIAL.md
    ├── README.md
    ├── requirements.txt
    ├── src/
    │   └── partyapp/
    └── tests/
```

---

## ４．依存パッケージのインストール

`requirements.txt` に以下を記載。

```text
SQLAlchemy>=2.0
PyMySQL>=1.1
typer>=0.12
python-dotenv>=1.0
-e .
```

- `-e .` は **「このプロジェクト自身を editable install する」** という指定。
- つまり `src/partyapp/` を **pip でパッケージとして認識させる**ために必要。

---

## ５．pyproject.toml の作成

### なぜ必要？

Python の世界では、`setup.py` が昔から使われていましたが、  
現在は **PEP 518/PEP 621** に基づく `pyproject.toml` が主流です。

役割は：

- **パッケージの名前やバージョンを定義する**
- **どのディレクトリを import 対象にするか指定する**
- **コマンドラインツールのエントリポイントを定義する**

このプロジェクトでは、`requirements.txt` に `-e .` があるので、  
`pyproject.toml` が無いと「ここが Python プロジェクトだ」と認識されません。

### 作成方法

リポジトリ直下 `/home/sen/partyapp/partyapp/pyproject.toml` に以下を追加。

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "partyapp"
version = "0.1.0"
description = "Political party data collection system (MVP)"
requires-python = ">=3.10"

[tool.setuptools.packages.find]
where = ["src"]

[project.scripts]
pa = "partyapp.cli:cli"
```

---

### 解説ポイント（忘れないように）

- `[build-system]`

  - 「このプロジェクトをどうビルドするか」を書く。
  - 今は setuptools と wheel が標準。

- `[project]`

  - `name` → パッケージ名（import で使う名前ではなく、配布名）
  - `version` → バージョン番号
  - `description` → 簡単な説明
  - `requires-python` → サポートする Python バージョン

- `[tool.setuptools.packages.find]`

  - `where = ["src"]` により、**src 下のディレクトリをパッケージ探索対象にする**
  - これで `src/partyapp` が Python パッケージとして認識される

- `[project.scripts]`
  - コマンドラインツールを登録するセクション
  - 今回は `pa` → `partyapp.cli:cli` と指定し、  
    `pa init-db` などの CLI コマンドが使えるようになる

---

### インストール

`pyproject.toml` を作成したら再度実行。

```bash
cd /home/sen/partyapp/partyapp
source ../.partyapp/bin/activate
pip install -r requirements.txt
```

これで editable インストールが成功し、  
`pa` コマンドが有効になる。

---

## ６．データベースハンドラの作成

`partyapp/src/partyapp/db/base.py`

```python
from __future__ import annotations
import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

class Base(DeclarativeBase):
    pass

def _db_url() -> str:
    return (
        f"mysql+pymysql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
        f"@{os.environ.get('DB_HOST','127.0.0.1')}:{os.environ.get('DB_PORT','3306')}"
        f"/{os.environ.get('DB_NAME','partyapp')}?charset=utf8mb4"
    )

engine = create_engine(_db_url(), pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def get_session() -> Generator[Session, None, None]:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
```

---

## ７．モデル定義

（Party, Category, Law, Associations を定義する章。省略）

---

## ８．CLI の作成

`partyapp/src/partyapp/cli.py`

```python
import typer
from sqlalchemy import text
from partyapp.db.base import engine, Base

cli = typer.Typer(help="partyapp CLI")

@cli.command("connect-db")
def connect_db() -> None:
    with engine.connect() as conn:
        version = conn.execute(text("SELECT VERSION()")).scalar_one()
        typer.echo(f"Connected. MariaDB version: {version}")

@cli.command("init-db")
def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    typer.echo("Tables created (if not exists).")
```

---

## ９．テーブル作成

```bash
cd /home/sen/partyapp/partyapp
source ../.partyapp/bin/activate

# インストール
pip install -r requirements.txt

# DB接続確認
pa connect-db

# 初回だけ実行
pa init-db
```
