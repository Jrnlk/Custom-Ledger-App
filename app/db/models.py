from sqlalchemy import Column, String, Numeric, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
import uuid
from datetime import datetime, timezone

from app.db.database import Base

class EntryType(enum.Enum):
    credit = "credit"
    debit = "debit"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    accounts = relationship("Account", back_populates="user")

class Account(Base):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="accounts")
    ledger_entries = relationship("LedgerEntry", back_populates="account")
    balance = relationship("Balance", uselist=False, back_populates="account")

class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    type = Column(Enum(EntryType), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    reference_id = Column(UUID(as_uuid=True), nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    description = Column(String)

    account = relationship("Account", back_populates="ledger_entries")

class Balance(Base):
    __tablename__ = "balances"

    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), primary_key=True)
    current_balance = Column(Numeric(12, 2), nullable=False)
    last_updated = Column(DateTime, default=datetime.now(timezone.utc))

    account = relationship("Account", back_populates="balance")
