from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.trade import TradeRequest
from app.services.trade_service import buy_stock, sell_stock


router = APIRouter(prefix="/trades", tags=["trades"])


@router.post("/buy")
def buy(request: TradeRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return buy_stock(db, current_user, request.symbol, request.quantity)


@router.post("/sell")
def sell(request: TradeRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return sell_stock(db, current_user, request.symbol, request.quantity)