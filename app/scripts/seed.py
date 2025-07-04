from uuid import uuid4
from app.db.database import SessionLocal
from app.db import models
from datetime import datetime, timezone
from decimal import Decimal
from app.auth.hash import hash_password

db = SessionLocal()

# Create user
user_id = uuid4()
new_user = models.User(
    id=user_id,
    email="Jarnell@example.com",
    full_name="Jarnell Kabore",
    hashed_password = hash_password("TestPass"),
    created_at=datetime.now(timezone.utc)
)

# Create account
account_id = uuid4()
new_account = models.Account(
    id=account_id,
    user_id=user_id,
    name="Investment Checking",
    created_at=datetime.now(timezone.utc)
)

# Create ledger entry (first deposit)
ledger_entry = models.LedgerEntry(
    id=uuid4(),
    account_id=account_id,
    type=models.EntryType.credit,
    amount=Decimal("10500.00"),
    reference_id=uuid4(),
    timestamp=datetime.now(timezone.utc),
    description="First deposit"
)

# Set initial balance to match ledger entry
balance = models.Balance(
    account_id=account_id,
    current_balance=Decimal("10500.00"),
    last_updated=datetime.now(timezone.utc)
)

# Add to DB
db.add_all([new_user, new_account, ledger_entry, balance])
db.commit()

# Print summary
print(f"\n✅ Seeded user: {new_user.full_name}")
print(f"   Account ID: {account_id}")
print(f"   User ID:    {user_id}")
print(f"   Initial balance: {balance.current_balance}\n")

db.close()

# Seed cmd
# 