from datetime import datetime

from pydantic import BaseModel


class HoldingOut(BaseModel):
    id: int
    symbol: str
    name: str
    current_price: int
    quantity: int
    value: int


class TransactionOut(BaseModel):
    id: int
    symbol: str
    name: str
    type: str
    quantity: int
    price: int
    timestamp: datetime


class DashboardOut(BaseModel):
    username: str
    balance: int
    stocks: list
    holdings: list[HoldingOut]
    transactions: list[TransactionOut]