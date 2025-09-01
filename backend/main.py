from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db import get_db, engine
from models import Base
from services import (
    get_user, update_user, get_wallet_balance, add_money_to_wallet,
    withdraw_from_wallet, create_transaction, get_transaction_history,
    get_transaction_details, transfer_money, get_transfer_details
)
from schema import (
    UserUpdate, WalletAddMoney, WalletWithdraw, TransactionCreate,
    TransferCreate
)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Digital Wallet API", version="1.0.0")

# User Profile Endpoints
@app.get("/users/{user_id}")
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)

@app.put("/users/{user_id}")
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user)

# Wallet Endpoints
@app.get("/wallet/{user_id}/balance")
def get_wallet_balance_endpoint(user_id: int, db: Session = Depends(get_db)):
    return get_wallet_balance(db, user_id)

@app.post("/wallet/{user_id}/add-money")
def add_money_endpoint(user_id: int, wallet_data: WalletAddMoney, db: Session = Depends(get_db)):
    return add_money_to_wallet(db, user_id, wallet_data.amount, wallet_data.description)

@app.post("/wallet/{user_id}/withdraw")
def withdraw_money_endpoint(user_id: int, wallet_data: WalletWithdraw, db: Session = Depends(get_db)):
    return withdraw_from_wallet(db, user_id, wallet_data.amount, wallet_data.description)

# Transaction Endpoints
@app.post("/transactions")
def create_transaction_endpoint(transaction: TransactionCreate, db: Session = Depends(get_db)):
    return create_transaction(db, transaction)

@app.get("/transactions/{user_id}")
def get_transaction_history_endpoint(
    user_id: int, 
    page: int = Query(1, ge=1), 
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return get_transaction_history(db, user_id, page, limit)

@app.get("/transactions/detail/{transaction_id}")
def get_transaction_details_endpoint(transaction_id: int, db: Session = Depends(get_db)):
    return get_transaction_details(db, transaction_id)

# Transfer Endpoints
@app.post("/transfer")
def create_transfer_endpoint(transfer: TransferCreate, db: Session = Depends(get_db)):
    return transfer_money(db, transfer)

@app.get("/transfer/{transfer_id}")
def get_transfer_details_endpoint(transfer_id: str, db: Session = Depends(get_db)):
    return get_transfer_details(db, transfer_id)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Digital Wallet API is running"}
