from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import FRONTEND_ORIGIN
from app.core.database import Base, engine, ensure_database_exists, sessionLocal
from app.models.holding import Holding
from app.models.stock import Stock
from app.models.transaction import Transaction
from app.models.user import User
from app.routes.auth import router as auth_router
from app.routes.portfolio import router as portfolio_router
from app.routes.stocks import router as stocks_router
from app.routes.trades import router as trades_router
from app.services.stock_service import seed_default_stocks


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    ensure_database_exists()
    Base.metadata.create_all(engine)
    db = sessionLocal()
    try:
        seed_default_stocks(db)
    finally:
        db.close()


app.include_router(auth_router)
app.include_router(stocks_router)
app.include_router(portfolio_router)
app.include_router(trades_router)


@app.get("/")
async def read_root():
    return {"status": "Running"}