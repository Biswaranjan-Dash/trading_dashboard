from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.services.stock_service import list_stocks
from app.services.trade_service import serialize_stock


router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("")
def read_stocks(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return [serialize_stock(stock) for stock in list_stocks(db)]