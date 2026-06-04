from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.user_name", ondelete="CASCADE"), nullable=False, index=True)
    stock_id = Column(ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(String(10), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    stock = relationship("Stock")