from __future__ import annotations
from typing import Optional
from datetime import date

from sqlalchemy import CHAR, String, Date
from sqlalchemy.orm import Mapped, mapped_column
from partyapp.db.base import Base


class Party(Base):
    __tablename__ = "M_PARTY"

    id: Mapped[str] = mapped_column(CHAR(18), primary_key=True, comment="内部ID（Snowflake型）")
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, comment="政党名")
    short_name: Mapped[Optional[str]] = mapped_column(String(50), comment="略称")
    founded_on: Mapped[Optional[date]] = mapped_column(Date, comment="成立日")
    dissolved_on: Mapped[Optional[date]] = mapped_column(Date, comment="解散日")
