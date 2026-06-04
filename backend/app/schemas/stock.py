from pydantic import BaseModel


class StockOut(BaseModel):
    id: int
    symbol: str
    name: str
    current_price: int


class StockSeed(BaseModel):
    symbol: str
    name: str
    current_price: int