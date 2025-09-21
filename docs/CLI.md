# partyapp CLI コマンド集

Typer により自動生成される CLI。  
`pa --help` でコマンド一覧、`pa <command> --help` で詳細が読める。

---

## 基本の使い方

```bash
# コマンド一覧を表示
# docstringが –help に反映されるから、説明はコードと一元管理できる
pa --help

# 各コマンドの詳細を表示
pa connect-db --help
pa init-db --help
pa reset-db --help
pa list-models --help
pa show-sql --help
```

---

## コマンド一覧

### `pa connect-db`

DB 接続確認: MariaDB のバージョンを表示する。

### `pa init-db`

DB 初期化: モデル定義に基づきテーブルを作成（既存は維持）。

### `pa reset-db`

DB リセット: すべてのテーブルを削除 → 再作成。  
誤操作防止のため確認あり。  
`--yes` を付けると確認をスキップ。

### `pa list-models`

モデル一覧を表示（テーブル名とカラム構造）。

### `pa show-sql`

テーブル作成時の CREATE TABLE 文をプレビュー。
