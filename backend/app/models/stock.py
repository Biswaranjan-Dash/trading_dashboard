from sqlalchemy import Column, DateTime, Integer, String, func

from app.core.database import Base


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(120), nullable=False)
    current_price = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())