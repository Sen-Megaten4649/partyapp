from __future__ import annotations
from typing import Optional

from sqlalchemy import CHAR, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from partyapp.db.base import Base


class Category(Base):
    __tablename__ = "M_CATEGORY"

    id: Mapped[str] = mapped_column(CHAR(18), primary_key=True, comment="内部ID（Snowflake型 or category_cd）")
    category_cd: Mapped[str] = mapped_column(String(3), nullable=False, unique=True, comment="e-Gov分類コード（例: 030）")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="分類名（厚生など）")
    description: Mapped[Optional[str]] = mapped_column(Text, comment="分類の説明")
