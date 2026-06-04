from pydantic import BaseModel, Field


class TradeRequest(BaseModel):
    symbol: str
    quantity: int = Field(gt=0)
