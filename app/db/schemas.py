from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from enum import Enum


# Enums for cred/deb
class EntryType(str, Enum):
    credit = "credit"
    debit = "debit"


# User Schemas
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    full_name: str
    password: str


class UserOut(UserBase):
    id: UUID
    full_name: str
    created_at: datetime

    class Config:
        orm_mode = True


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


# Account Schemas
class AccountBase(BaseModel):
    name: str


class AccountCreate(AccountBase):
    pass


class AccountOut(AccountBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


# Balance Schemas
class BalanceOut(BaseModel):
    account_id: UUID
    current_balance: Decimal
    last_updated: datetime

    class Config:
        orm_mode = True


# Ledger Entry Schemas
class LedgerEntryCreate(BaseModel):
    account_id: UUID
    type: EntryType
    amount: Decimal
    description: str = ""


class LedgerEntryOut(BaseModel):
    id: UUID
    account_id: UUID
    type: EntryType
    amount: Decimal
    reference_id: UUID
    timestamp: datetime
    description: str

    class Config:
        orm_mode = True
