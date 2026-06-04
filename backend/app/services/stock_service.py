from sqlalchemy.orm import Session

from app.models.stock import Stock


DEFAULT_STOCKS = [
    {"symbol": "AAPL", "name": "Apple", "current_price": 200},
    {"symbol": "TSLA", "name": "Tesla", "current_price": 300},
    {"symbol": "MSFT", "name": "Microsoft", "current_price": 400},
    {"symbol": "NVDA", "name": "Nvidia", "current_price": 500},
    {"symbol": "AMZN", "name": "Amazon", "current_price": 250},
]


def seed_default_stocks(db: Session):
    for stock_data in DEFAULT_STOCKS:
        existing_stock = db.query(Stock).filter(Stock.symbol == stock_data["symbol"]).first()
        if not existing_stock:
            db.add(Stock(**stock_data))
    db.commit()


def list_stocks(db: Session):
    return db.query(Stock).order_by(Stock.symbol.asc()).all()