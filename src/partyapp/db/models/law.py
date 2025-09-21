from __future__ import annotations
from typing import Optional
from datetime import date, datetime

from sqlalchemy import CHAR, String, Text, Date, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from partyapp.db.base import Base
from .enums import LAW_TYPE_VALUES, JURISDICTION_VALUES


class Law(Base):
    __tablename__ = "T_LAW"

    id: Mapped[str] = mapped_column(CHAR(18), primary_key=True, comment="内部ID（Snowflake型）")
    law_id: Mapped[Optional[str]] = mapped_column(String(20), comment="e-GovのlawId")
    law_num: Mapped[Optional[str]] = mapped_column(String(50), comment="e-GovのlawNum（例: 令和4年法律第75号）")
    law_type: Mapped[Optional[str]] = mapped_column(
        Enum(*(val for val, _ in LAW_TYPE_VALUES), name="law_type"),
        comment="法令種別"
    )
    jurisdiction: Mapped[Optional[str]] = mapped_column(
        Enum(*(val for val, _ in JURISDICTION_VALUES), name="jurisdiction"),
        comment="管轄レベル"
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="法令名")
    promulgation_date: Mapped[Optional[date]] = mapped_column(Date, comment="公布日")
    enforcement_date: Mapped[Optional[date]] = mapped_column(Date, comment="施行日")
    summary: Mapped[Optional[str]] = mapped_column(Text, comment="概要")
    law_url: Mapped[Optional[str]] = mapped_column(Text, comment="e-GovのURL")
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="作成日時")
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="更新日時")