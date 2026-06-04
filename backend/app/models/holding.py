from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.user_name", ondelete="CASCADE"), nullable=False, index=True)
    stock_id = Column(ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=0)

    user = relationship("User")
    stock = relationship("Stock")

    __table_args__ = (UniqueConstraint("user_id", "stock_id", name="uq_user_stock"),)