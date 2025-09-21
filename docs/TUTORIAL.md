# partyapp チュートリアル

## ０．Git 初期化と最初のコミット

まずは Git リポジトリを初期化して、初期ファイル（README.md, TUTORIAL.md など）をコミットしておく。

```bash
cd /home/<user>/partyapp/partyapp
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

`requirements.txt` に以下を追記。

```text
SQLAlchemy>=2.0
PyMySQL>=1.1
typer>=0.12
python-dotenv>=1.0
-e .
```

仮想環境を有効化してインストール。

```bash
cd /home/sen/partyapp/app
source ../.partyapp/bin/activate
pip install -r requirements.txt
```

---

## ５．データベースハンドラの作成

`app/src/partyapp/db/base.py`

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

## ６．モデル定義

### `party.py`

```python
from sqlalchemy import String, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column
from partyapp.db.base import Base

class Party(Base):
    __tablename__ = "M_PARTY"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    short_name: Mapped[str] = mapped_column(String(50))
    founded_on: Mapped[Date] = mapped_column(Date)
    dissolved_on: Mapped[Date] = mapped_column(Date)
```

### `category.py`

```python
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from partyapp.db.base import Base

class Category(Base):
    __tablename__ = "M_CATEGORY"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_cd: Mapped[str] = mapped_column(String(3), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
```

### `law.py`

```python
from sqlalchemy import String, Integer, Date, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column
from partyapp.db.base import Base

class Law(Base):
    __tablename__ = "T_LAW"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    law_id: Mapped[str] = mapped_column(String(20))
    law_num: Mapped[str] = mapped_column(String(50))
    law_type: Mapped[str] = mapped_column(Enum("constitution","law","cabinet_order","imperial_order",
                                              "ministerial_order","rule","ordinance","local_rule"))
    jurisdiction: Mapped[str] = mapped_column(Enum("national","local"))
    title: Mapped[str] = mapped_column(String(200))
    promulgation_date: Mapped[Date] = mapped_column(Date)
    enforcement_date: Mapped[Date] = mapped_column(Date)
    summary: Mapped[str] = mapped_column(Text)
    law_url: Mapped[str] = mapped_column(Text)
```

### `associations.py`

```python
from sqlalchemy import Integer, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from partyapp.db.base import Base

class LawCategoryMap(Base):
    __tablename__ = "T_LAW_CATEGORY_MAP"
    __table_args__ = (UniqueConstraint("law_id","category_id", name="uq_law_category"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    law_id: Mapped[int] = mapped_column(ForeignKey("T_LAW.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("M_CATEGORY.id"))

class PartyLawRole(Base):
    __tablename__ = "T_PARTY_LAW_ROLE"
    __table_args__ = (UniqueConstraint("law_id","party_id", name="uq_party_law"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    law_id: Mapped[int] = mapped_column(ForeignKey("T_LAW.id"))
    party_id: Mapped[int] = mapped_column(ForeignKey("M_PARTY.id"))
    submission_role: Mapped[str] = mapped_column(Enum("submitter","co_submitter","cabinet","amendment","none"))
    promotion_role: Mapped[str] = mapped_column(Enum("coalition","support","none"))
    vote_role: Mapped[str] = mapped_column(Enum("voted_for","voted_against","abstained","boycott","none"))
    note: Mapped[str]
```

### `__init__.py`

```python
from .party import Party
from .category import Category
from .law import Law
from .associations import LawCategoryMap, PartyLawRole

__all__ = ["Party", "Category", "Law", "LawCategoryMap", "PartyLawRole"]
```

---

## ７．CLI の作成

`app/src/partyapp/cli.py`

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

## ８．pyproject.toml の作成

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "partyapp"
version = "0.1.0"
requires-python = ">=3.10"

[tool.setuptools.packages.find]
where = ["src"]

[project.scripts]
pa = "partyapp.cli:cli"
```

---

## ９．テーブル作成

```bash
cd /home/sen/partyapp/app
source ../.partyapp/bin/activate

# インストール
pip install -r requirements.txt

# DB接続確認
pa connect-db

# 初回だけ実行
pa init-db
```
