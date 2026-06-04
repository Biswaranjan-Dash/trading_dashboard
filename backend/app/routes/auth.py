from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import TokenResponse, UserRegister
from app.services.auth_service import login_user, register_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(request: UserRegister, db: Session = Depends(get_db)):
    user = register_user(db, request.username, request.password)
    token = login_user(db, user.user_name, request.password)
    return TokenResponse(token=token, username=user.user_name)


@router.post("/login", response_model=TokenResponse)
def login(request: UserRegister, db: Session = Depends(get_db)):
    token = login_user(db, request.username, request.password)
    return TokenResponse(token=token, username=request.username)