import typer
from sqlalchemy import text
from sqlalchemy.schema import CreateTable

from partyapp.db.base import engine, Base
from partyapp.db.models import (
    Law, Category, Party, LawCategoryMap, PartyLawRole
)

cli = typer.Typer(help="partyapp 開発用 CLI ツール")


@cli.command("connect-db")
def connect_db() -> None:
    """
    DB接続確認: MariaDB のバージョンを表示する
    """
    with engine.connect() as conn:
        version = conn.execute(text("SELECT VERSION()")).scalar_one()
        typer.echo(f"✅ DB接続成功: MariaDB バージョン {version}")


@cli.command("init-db")
def init_db() -> None:
    """
    DB初期化: モデル定義に基づきテーブルを作成（既存は維持）
    """
    Base.metadata.create_all(bind=engine)
    typer.echo("✅ テーブルを作成しました（既存は維持されます）")


@cli.command("reset-db")
def reset_db(
    yes: bool = typer.Option(False, "--yes", help="確認なしで実行")
) -> None:
    """
    DBリセット: すべてのテーブルを削除 → 再作成
    """
    if not yes:
        typer.confirm("⚠️ 本当に DB をリセットしますか？", abort=True)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    typer.echo("✅ DB をリセットしました（全テーブル再作成）")


@cli.command("list-models")
def list_models() -> None:
    """
    モデル一覧を表示（テーブル名とカラム定義）
    """
    for table in Base.metadata.sorted_tables:
        typer.echo(f"📖 {table.name}")
        for column in table.columns:
            typer.echo(f"   - {column.name} ({column.type})")


@cli.command("show-sql")
def show_sql() -> None:
    """
    CREATE TABLE 文をプレビュー（dry-run）
    """
    for table in Base.metadata.sorted_tables:
        sql = str(CreateTable(table).compile(engine))
        typer.echo(f"--- {table.name} ---")
        typer.echo(sql)