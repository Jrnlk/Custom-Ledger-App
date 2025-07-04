from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Account
from app.utils.auth import get_current_user

router = APIRouter()

@router.get("/user/accounts")
def get_user_accounts(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
    return accounts