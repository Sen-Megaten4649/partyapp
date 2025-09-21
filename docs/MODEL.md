# モデル定義（SQLAlchemy 2.x）

- DB: MariaDB/MySQL（utf8mb4）
- 文字列長・型は仕様どおり（char(18), varchar(…), enum, date, text, datetime）
- ENUM は `src/partyapp/db/models/enums.py` に一元管理し、モデルから参照する。

---

## 目次

- [モデル定義（SQLAlchemy 2.x）](#モデル定義sqlalchemy-2x)
  - [目次](#目次)
  - [T_LAW](#t_law)
  - [M_CATEGORY](#m_category)
  - [T_LAW_CATEGORY_MAP](#t_law_category_map)
  - [M_PARTY](#m_party)
  - [T_PARTY_LAW_ROLE](#t_party_law_role)
  - [モデル一括 import](#モデル一括-import)
  - [今後の拡張予定](#今後の拡張予定)

---

## T_LAW

**ファイル**: `src/partyapp/db/models/law.py`

```python
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
```

---

## M_CATEGORY

**ファイル**: `src/partyapp/db/models/category.py`

```python
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
```

---

## T_LAW_CATEGORY_MAP

> 中間テーブルは **複合主キー**（`(law_id, category_id)`）にする。

**ファイル**: `src/partyapp/db/models/associations.py`（前半）

```python
from __future__ import annotations

from sqlalchemy import CHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from partyapp.db.base import Base


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
```

---

## M_PARTY

**ファイル**: `src/partyapp/db/models/party.py`

```python
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
```

---

## T_PARTY_LAW_ROLE

**ファイル**: `src/partyapp/db/models/associations.py`（後半）

```python
from __future__ import annotations
from typing import Optional

from sqlalchemy import CHAR, ForeignKey, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column
from partyapp.db.base import Base
from .enums import SUBMISSION_ROLE_VALUES, PROMOTION_ROLE_VALUES, VOTE_ROLE_VALUES


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
```

---

## モデル一括 import

**ファイル**: `src/partyapp/db/models/__init__.py`

```python
from .law import Law
from .category import Category
from .party import Party
from .associations import LawCategoryMap, PartyLawRole
from .enums import (
    LAW_TYPE_VALUES, JURISDICTION_VALUES,
    SUBMISSION_ROLE_VALUES, PROMOTION_ROLE_VALUES, VOTE_ROLE_VALUES,
)

__all__ = [
    "Law", "Category", "Party", "LawCategoryMap", "PartyLawRole",
    "LAW_TYPE_VALUES", "JURISDICTION_VALUES",
    "SUBMISSION_ROLE_VALUES", "PROMOTION_ROLE_VALUES", "VOTE_ROLE_VALUES",
]
```

---

## 今後の拡張予定

- ENUM 日本語説明は UI でラベル表示に活用予定
- created_at, updated_at に Mixin を導入して自動更新対応
- Alembic によるマイグレーション管理
