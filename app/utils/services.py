from decimal import Decimal
from sqlalchemy.orm import Session
from app.db.models import LedgerEntry, EntryType

def _calculate_balance(account_id, db: Session) -> Decimal:
    entries = db.query(LedgerEntry).filter(LedgerEntry.account_id == account_id).all()

    balance = Decimal("0.00")
    for entry in entries:
        if entry.type == EntryType.credit:
            balance += entry.amount
        elif entry.type == EntryType.debit:
            balance -=entry.amount
    
    return balance