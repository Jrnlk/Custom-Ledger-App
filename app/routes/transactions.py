from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime, timezone
from decimal import Decimal

from app.db.database import get_db
from app.db import models, schemas
from app.utils.services import _calculate_balance
from app.utils.auth import get_current_user

router = APIRouter()

#  Helper: Ensure account belongs to current user
def verify_account_ownership(account_id: UUID, user: models.User, db: Session):
    account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if account.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this account")
    return account

# Deposit
@router.post("/deposit", response_model=schemas.LedgerEntryOut)
def deposit(
    entry: schemas.LedgerEntryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    verify_account_ownership(entry.account_id, current_user, db)

    if entry.type.lower() != "credit":
        raise HTTPException(status_code=400, detail="Please use 'credit' for deposits")

    new_entry = models.LedgerEntry(
        id=uuid4(),
        account_id=entry.account_id,
        type="credit",
        amount=entry.amount,
        reference_id=uuid4(),
        description=entry.description,
        timestamp=datetime.now(timezone.utc)
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

# Withdraw
@router.post("/withdraw", response_model=schemas.LedgerEntryOut)
def withdraw(
    entry: schemas.LedgerEntryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    verify_account_ownership(entry.account_id, current_user, db)

    if entry.type.lower() != "debit":
        raise HTTPException(status_code=400, detail="Please use 'debit' for withdrawals")

    balance = _calculate_balance(entry.account_id, db)
    if entry.amount > balance:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    new_entry = models.LedgerEntry(
        id=uuid4(),
        account_id=entry.account_id,
        type="debit",
        amount=entry.amount,
        reference_id=uuid4(),
        description=entry.description,
        timestamp=datetime.now(timezone.utc)
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

# Transfer
@router.post("/transfer")
def transfer(
    from_account_id: UUID,
    to_account_id: UUID,
    amount: Decimal,
    description: str = "",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    verify_account_ownership(from_account_id, current_user, db)

    if from_account_id == to_account_id:
        raise HTTPException(status_code=400, detail="Cannot transfer to the same account")

    balance = _calculate_balance(from_account_id, db)
    if amount > balance:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    reference_id = uuid4()
    timestamp = datetime.now(timezone.utc)

    debit_entry = models.LedgerEntry(
        id=uuid4(),
        account_id=from_account_id,
        type="debit",
        amount=amount,
        description=f"Transfer to {to_account_id}: {description}",
        reference_id=reference_id,
        timestamp=timestamp
    )

    credit_entry = models.LedgerEntry(
        id=uuid4(),
        account_id=to_account_id,
        type="credit",
        amount=amount,
        description=f"Transfer from {from_account_id}: {description}",
        reference_id=reference_id,
        timestamp=timestamp
    )

    db.add_all([debit_entry, credit_entry])
    db.commit()

    return {"message": "Transfer complete", "reference_id": str(reference_id)}

# Get Balance
@router.get("/balance/{account_id}")
def get_balance(
    account_id: UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    verify_account_ownership(account_id, current_user, db)
    balance = _calculate_balance(account_id, db)
    return {"account_id": str(account_id), "balance": float(balance)}

# Get Transaction History
@router.get("/transactions/{account_id}", response_model=list[schemas.LedgerEntryOut])
def get_transactions(
    account_id: UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    verify_account_ownership(account_id, current_user, db)
    entries = (
        db.query(models.LedgerEntry)
        .filter(models.LedgerEntry.account_id == account_id)
        .order_by(models.LedgerEntry.timestamp.desc())
        .all()
    )
    return entries
