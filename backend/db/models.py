import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    LargeBinary,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class RuleAction(str, enum.Enum):
    reinvest_all = "reinvest_all"
    threshold = "threshold"
    target_symbol = "target_symbol"


class ReinvestmentStatus(str, enum.Enum):
    pending = "pending"
    filled = "filled"
    failed = "failed"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    credential: Mapped["AlpacaCredential | None"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    rules: Mapped[list["Rule"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    reinvestment_logs: Mapped[list["ReinvestmentLog"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class AlpacaCredential(Base):
    __tablename__ = "alpaca_credentials"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    # API key and secret are stored as Fernet-encrypted bytes
    encrypted_api_key: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    encrypted_secret_key: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    base_url: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user: Mapped["User"] = relationship(back_populates="credential")


class Rule(Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    action: Mapped[RuleAction] = mapped_column(Enum(RuleAction), nullable=False)
    # Used when action == threshold: only reinvest if dividend >= this amount
    threshold_amount: Mapped[float | None] = mapped_column(Numeric(12, 4), nullable=True)
    # Used when action == target_symbol: buy this symbol regardless of which stock paid
    target_symbol: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped["User"] = relationship(back_populates="rules")


class ReinvestmentLog(Base):
    __tablename__ = "reinvestment_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # Symbol that paid the dividend
    source_symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    # Symbol that was purchased (may differ if rule uses target_symbol)
    target_symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    dividend_amount: Mapped[float] = mapped_column(Numeric(12, 4), nullable=False)
    shares_purchased: Mapped[float | None] = mapped_column(Numeric(16, 8), nullable=True)
    alpaca_order_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[ReinvestmentStatus] = mapped_column(Enum(ReinvestmentStatus), nullable=False, default=ReinvestmentStatus.pending)
    rule_id: Mapped[int | None] = mapped_column(ForeignKey("rules.id", ondelete="SET NULL"), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped["User"] = relationship(back_populates="reinvestment_logs")
