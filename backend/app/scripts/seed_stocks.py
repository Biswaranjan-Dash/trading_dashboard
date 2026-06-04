from app.core.database import Base, ensure_database_exists, engine, sessionLocal
from app.services.stock_service import seed_default_stocks


def main():
    ensure_database_exists()
    Base.metadata.create_all(engine)
    db = sessionLocal()
    try:
        seed_default_stocks(db)
        print("Seeded stocks")
    finally:
        db.close()


if __name__ == "__main__":
    main()