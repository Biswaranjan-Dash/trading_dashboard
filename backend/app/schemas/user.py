from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    token: str
    token_type: str = "Bearer"
    username: str


class UserOut(BaseModel):
    username: str
    balance: int