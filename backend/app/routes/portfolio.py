from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.services.trade_service import get_dashboard, get_holdings, get_transactions


router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_dashboard(db, current_user)


@router.get("/holdings")
def holdings(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_holdings(db, current_user.user_name)


@router.get("/transactions")
def transactions(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_transactions(db, current_user.user_name)