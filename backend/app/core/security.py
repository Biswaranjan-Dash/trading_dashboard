from datetime import datetime, timedelta
import jwt
import bcrypt

from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


salt = bcrypt.gensalt()

def hash_password(password:str):
    return bcrypt.hashpw(password.encode(), salt)

def check_password(password:str, hashed_pw:str):
    return bcrypt.checkpw(password.encode(), hashed_pw.encode())

def create_access_token(data:dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_access_token(data:str):
    payload = jwt.decode(data, SECRET_KEY, algorithms=[ALGORITHM])
    return payload