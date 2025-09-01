from datetime import datetime
from sqlalchemy.orm import Session, HTTPException
from models import User, Transaction, WalletTransfer
from schema import UserCreate, UserUpdate, TransactionCreate, WalletTransferCreate
from .db import get_db, db


def get_user(user_id: int):
    if user_id in db.users:
        return {"user_id": user_id,
                "username": "john_doe",
                "email": "john@example.com",
                "phone_number": "+1234567890",
                "balance": 150.50,
                "created_at": datetime.now()
                }
    else:
        raise HTTPException(status_code=404, detail="User not found")

def update_user(user_id: int, user: UserUpdate):
    if user_id in db.users:
        db.users[user_id] = user
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")
    

def create_transaction(user_id: int, transaction: TransactionCreate):
    if user_id in db.users:
        db.transactions.append(transaction)
        return transaction
    else:
        raise HTTPException(status_code=404, detail="User not found")

def get_transaction_history(user_id: int):
    if user_id in db.users:
        return db.transactions
    else:
        raise HTTPException(status_code=404, detail="User not found")

def get_transaction_details(transaction_id: int):
    if transaction_id in db.transactions:
        return db.transactions[transaction_id]
    else:
        raise HTTPException(status_code=404, detail="Transaction not found")


def create_wallet_transfer(wallet_transfer: WalletTransferCreate):
    if wallet_transfer.sender_user_id in db.users and wallet_transfer.recipient_user_id in db.users:
        db.wallet_transfers.append(wallet_transfer)
        return wallet_transfer
    else:
        raise HTTPException(status_code=404, detail="User not found")

def get_wallet_transfer_history(user_id: int):
    if user_id in db.users:
        return db.wallet_transfers
    else:
        raise HTTPException(status_code=404, detail="User not found")   

def get_wallet_balance(user_id: int):
    if user_id in db.users:
        return {"user_id": user_id,
                "balance": 150.50,
                "last_updated": datetime.now()
                }
    else:
        raise HTTPException(status_code=404, detail="User not found")

def update_wallet_balance(user_id: int, balance: float):
    if user_id in db.users:
        db.users[user_id]["balance"] = balance
        return {"user_id": user_id,
                "balance": balance,
                "last_updated": datetime.now()      
                }
    else:
        raise HTTPException(status_code=404, detail="User not found")

