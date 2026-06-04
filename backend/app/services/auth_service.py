from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, check_password
from app.models.user import User


def register_user(db: Session, username: str, password: str) -> User:
    existing_user = db.query(User).filter(User.user_name == username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    user = User(user_name=username, hashed_password=hash_password(password).decode(), balance=1000)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, username: str, password: str) -> str:
    user = db.query(User).filter(User.user_name == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exist")

    if not check_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    return create_access_token({"sub": user.user_name})