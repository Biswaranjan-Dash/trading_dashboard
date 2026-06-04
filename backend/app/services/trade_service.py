from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.holding import Holding
from app.models.stock import Stock
from app.models.transaction import Transaction


def serialize_stock(stock: Stock):
    return {
        "id": stock.id,
        "symbol": stock.symbol,
        "name": stock.name,
        "current_price": stock.current_price,
    }


def serialize_holding(holding: Holding):
    return {
        "id": holding.id,
        "symbol": holding.stock.symbol,
        "name": holding.stock.name,
        "current_price": holding.stock.current_price,
        "quantity": holding.quantity,
        "value": holding.quantity * holding.stock.current_price,
    }


def serialize_transaction(transaction: Transaction):
    return {
        "id": transaction.id,
        "symbol": transaction.stock.symbol,
        "name": transaction.stock.name,
        "type": transaction.type,
        "quantity": transaction.quantity,
        "price": transaction.price,
        "timestamp": transaction.timestamp,
    }


def get_holdings(db: Session, username: str):
    holdings = (
        db.query(Holding)
        .filter(Holding.user_id == username)
        .order_by(Holding.id.desc())
        .all()
    )
    return [serialize_holding(holding) for holding in holdings]


def get_transactions(db: Session, username: str):
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == username)
        .order_by(Transaction.timestamp.desc(), Transaction.id.desc())
        .all()
    )
    return [serialize_transaction(transaction) for transaction in transactions]


def get_dashboard(db: Session, user):
    return {
        "username": user.user_name,
        "balance": user.balance,
        "stocks": [serialize_stock(stock) for stock in db.query(Stock).order_by(Stock.symbol.asc()).all()],
        "holdings": get_holdings(db, user.user_name),
        "transactions": get_transactions(db, user.user_name),
    }


def buy_stock(db: Session, user, symbol: str, quantity: int):
    stock = db.query(Stock).filter(Stock.symbol == symbol.upper()).first()
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")

    cost = quantity * stock.current_price
    if user.balance < cost:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance")

    holding = (
        db.query(Holding)
        .filter(Holding.user_id == user.user_name, Holding.stock_id == stock.id)
        .first()
    )
    if holding:
        holding.quantity += quantity
    else:
        holding = Holding(user_id=user.user_name, stock_id=stock.id, quantity=quantity)
        db.add(holding)

    user.balance -= cost
    transaction = Transaction(
        user_id=user.user_name,
        stock_id=stock.id,
        type="BUY",
        quantity=quantity,
        price=stock.current_price,
    )
    db.add(transaction)
    db.commit()
    return get_dashboard(db, user)


def sell_stock(db: Session, user, symbol: str, quantity: int):
    stock = db.query(Stock).filter(Stock.symbol == symbol.upper()).first()
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")

    holding = (
        db.query(Holding)
        .filter(Holding.user_id == user.user_name, Holding.stock_id == stock.id)
        .first()
    )
    if not holding or holding.quantity < quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough shares to sell")

    proceeds = quantity * stock.current_price
    holding.quantity -= quantity
    if holding.quantity == 0:
        db.delete(holding)

    user.balance += proceeds
    transaction = Transaction(
        user_id=user.user_name,
        stock_id=stock.id,
        type="SELL",
        quantity=quantity,
        price=stock.current_price,
    )
    db.add(transaction)
    db.commit()
    return get_dashboard(db, user)