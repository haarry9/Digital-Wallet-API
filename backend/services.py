from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import User, Transaction
from schema import UserUpdate, TransactionCreate, TransferCreate
import uuid
from decimal import Decimal

def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "phone_number": user.phone_number,
        "balance": float(user.balance),
        "created_at": user.created_at
    }

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.username is not None:
        user.username = user_update.username
    if user_update.phone_number is not None:
        user.phone_number = user_update.phone_number
    
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    return {"message": "User updated successfully"}

def get_wallet_balance(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user.id,
        "balance": float(user.balance),
        "last_updated": user.updated_at
    }

def add_money_to_wallet(db: Session, user_id: int, amount: float, description: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    # Create transaction
    transaction = Transaction(
        user_id=user_id,
        transaction_type="CREDIT",
        amount=Decimal(str(amount)),
        description=description
    )
    
    # Update balance
    user.balance += Decimal(str(amount))
    user.updated_at = datetime.utcnow()
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    db.refresh(user)
    
    return {
        "transaction_id": transaction.id,
        "user_id": user.id,
        "amount": amount,
        "new_balance": float(user.balance),
        "transaction_type": "CREDIT"
    }

def withdraw_from_wallet(db: Session, user_id: int, amount: float, description: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    if user.balance < Decimal(str(amount)):
        raise HTTPException(
            status_code=400, 
            detail="Insufficient balance",
            headers={"current_balance": float(user.balance), "required_amount": amount}
        )
    
    # Create transaction
    transaction = Transaction(
        user_id=user_id,
        transaction_type="DEBIT",
        amount=Decimal(str(amount)),
        description=description
    )
    
    # Update balance
    user.balance -= Decimal(str(amount))
    user.updated_at = datetime.utcnow()
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    db.refresh(user)
    
    return {
        "transaction_id": transaction.id,
        "user_id": user.id,
        "amount": amount,
        "new_balance": float(user.balance),
        "transaction_type": "DEBIT"
    }

def create_transaction(db: Session, transaction_data: TransactionCreate):
    user = db.query(User).filter(User.id == transaction_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    transaction = Transaction(
        user_id=transaction_data.user_id,
        transaction_type=transaction_data.transaction_type,
        amount=Decimal(str(transaction_data.amount)),
        description=transaction_data.description
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    return {"message": "Transaction created successfully", "transaction_id": transaction.id}

def get_transaction_history(db: Session, user_id: int, page: int = 1, limit: int = 10):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    offset = (page - 1) * limit
    
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).offset(offset).limit(limit).all()
    
    total = db.query(Transaction).filter(Transaction.user_id == user_id).count()
    
    return {
        "transactions": [
            {
                "transaction_id": t.id,
                "transaction_type": t.transaction_type,
                "amount": float(t.amount),
                "description": t.description,
                "created_at": t.created_at
            } for t in transactions
        ],
        "total": total,
        "page": page,
        "limit": limit
    }

def get_transaction_details(db: Session, transaction_id: int):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return {
        "transaction_id": transaction.id,
        "user_id": transaction.user_id,
        "transaction_type": transaction.transaction_type,
        "amount": float(transaction.amount),
        "description": transaction.description,
        "recipient_user_id": transaction.recipient_user_id,
        "reference_transaction_id": transaction.reference_transaction_id,
        "created_at": transaction.created_at
    }

def transfer_money(db: Session, transfer_data: TransferCreate):
    sender = db.query(User).filter(User.id == transfer_data.sender_user_id).first()
    recipient = db.query(User).filter(User.id == transfer_data.recipient_user_id).first()
    
    if not sender:
        raise HTTPException(status_code=404, detail="Sender user not found")
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient user not found")
    
    if sender.id == recipient.id:
        raise HTTPException(status_code=400, detail="Cannot transfer to yourself")
    
    if transfer_data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    if sender.balance < Decimal(str(transfer_data.amount)):
        raise HTTPException(
            status_code=400, 
            detail="Insufficient balance",
            headers={"current_balance": float(sender.balance), "required_amount": transfer_data.amount}
        )
    
    # Create transfer ID
    transfer_id = str(uuid.uuid4())
    
    # Create sender transaction (TRANSFER_OUT)
    sender_transaction = Transaction(
        user_id=sender.id,
        transaction_type="TRANSFER_OUT",
        amount=Decimal(str(transfer_data.amount)),
        description=f"Transfer to {recipient.username}: {transfer_data.description}",
        recipient_user_id=recipient.id
    )
    
    # Create recipient transaction (TRANSFER_IN)
    recipient_transaction = Transaction(
        user_id=recipient.id,
        transaction_type="TRANSFER_IN",
        amount=Decimal(str(transfer_data.amount)),
        description=f"Transfer from {sender.username}: {transfer_data.description}",
        recipient_user_id=sender.id
    )
    
    # Update balances
    sender.balance -= Decimal(str(transfer_data.amount))
    recipient.balance += Decimal(str(transfer_data.amount))
    sender.updated_at = datetime.utcnow()
    recipient.updated_at = datetime.utcnow()
    
    # Link transactions
    sender_transaction.reference_transaction_id = recipient_transaction.id
    recipient_transaction.reference_transaction_id = sender_transaction.id
    
    db.add(sender_transaction)
    db.add(recipient_transaction)
    db.commit()
    db.refresh(sender_transaction)
    db.refresh(recipient_transaction)
    db.refresh(sender)
    db.refresh(recipient)
    
    return {
        "transfer_id": transfer_id,
        "sender_transaction_id": sender_transaction.id,
        "recipient_transaction_id": recipient_transaction.id,
        "amount": transfer_data.amount,
        "sender_new_balance": float(sender.balance),
        "recipient_new_balance": float(recipient.balance),
        "status": "completed"
    }

def get_transfer_details(db: Session, transfer_id: str):
    # Since we don't have a separate transfers table, we'll need to implement this
    # based on the transaction pairs. For now, return a placeholder
    return {
        "transfer_id": transfer_id,
        "message": "Transfer details endpoint not fully implemented"
    }

