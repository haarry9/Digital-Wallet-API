from fastapi import FastAPI
from db import engine
from models import Base
from services import get_user, update_user, get_wallet_balance, update_wallet_balance

app = FastAPI("Digital Wallet API")


@app.get("users/{user_id}")
def get_user(user_id: int):
    return get_user(user_id)

@app.put("users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    return update_user(user_id, user)

@app.get("wallet/{user_id}/balance")
def get_wallet_balance(user_id: int):
    return get_wallet_balance(user_id)

@app.put("wallet/{user_id}/balance")
def update_wallet_balance(user_id: int, balance: float):
    return update_wallet_balance(user_id, balance)


