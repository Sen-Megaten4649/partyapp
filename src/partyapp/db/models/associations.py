from __future__ import annotations
from typing import Optional

from sqlalchemy import CHAR, ForeignKey, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column
from partyapp.db.base import Base
from .enums import SUBMISSION_ROLE_VALUES, PROMOTION_ROLE_VALUES, VOTE_ROLE_VALUES


# 法令とカテゴリの紐づけ
class LawCategoryMap(Base):
    __tablename__ = "T_LAW_CATEGORY_MAP"

    law_id: Mapped[str] = mapped_column(
        CHAR(18),
        ForeignKey("T_LAW.id"),
        primary_key=True,
        comment="T_LAW.id"
    )
    category_id: Mapped[str] = mapped_column(
        CHAR(18),
        ForeignKey("M_CATEGORY.id"),
        primary_key=True,
        comment="M_CATEGORY.id"
    )


# 政党と法令の紐づけ
class PartyLawRole(Base):
    __tablename__ = "T_PARTY_LAW_ROLE"

    law_id: Mapped[str] = mapped_column(
        CHAR(18),
        ForeignKey("T_LAW.id"),
        primary_key=True,
        comment="T_LAW.id"
    )
    party_id: Mapped[str] = mapped_column(
        CHAR(18),
        ForeignKey("M_PARTY.id"),
        primary_key=True,
        comment="M_PARTY.id"
    )

    submission_role: Mapped[Optional[str]] = mapped_column(
        Enum(*(val for val, _ in SUBMISSION_ROLE_VALUES), name="submission_role"),
        comment="提出系"
    )
    promotion_role: Mapped[Optional[str]] = mapped_column(
        Enum(*(val for val, _ in PROMOTION_ROLE_VALUES), name="promotion_role"),
        comment="推進系"
    )
    vote_role: Mapped[Optional[str]] = mapped_column(
        Enum(*(val for val, _ in VOTE_ROLE_VALUES), name="vote_role"),
        comment="投票系"
    )
    note: Mapped[Optional[str]] = mapped_column(Text, comment="補足メモ（会派、造反など）")