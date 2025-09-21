from __future__ import annotations
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

from config import DATABASE_URL


class Base(DeclarativeBase):
    """全ての ORM モデルが継承するベースクラス"""
    pass


# DB エンジン
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # 切断検知＆自動再接続
    future=True,          # SQLAlchemy 2.0 スタイル
    echo=False            # True にすると SQL ログ出力
)

# セッションファクトリ
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


def get_session() -> Generator[Session, None, None]:
    """セッションを生成して呼び出し元に返す。"""
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()