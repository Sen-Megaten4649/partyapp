import os
import urllib.parse

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# パスワードをURLエンコードしてから埋め込む
encoded_pw = urllib.parse.quote_plus(DB_PASSWORD or "")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{encoded_pw}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)