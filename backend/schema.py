from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    username: str
    email: str
    phone_number: str
    balance: float
    created_at: datetime
    updated_at: datetime

class UserUpdate(BaseModel):
    username: str
    phone_number: str

class WalletBalance(BaseModel):
    user_id: int
    balance: float
    last_updated: datetime

class WalletAddMoney(BaseModel):
    amount: float
    description: str

class WalletWithdraw(BaseModel):
    amount: float
    description: str

class WalletTransfer(BaseModel):
    amount: float
    description: str
    recipient_user_id: int

class WalletTransferResponse(BaseModel):
    transaction_id: int
    user_id: int
    amount: float
    new_balance: float
    transaction_type: str
    
class Transaction(BaseModel):
    transaction_id: int
    transaction_type: str
    amount: float
    description: str
    created_at: datetime

class TransactionDetail(BaseModel):
    transaction_id: int
    user_id: int
    transaction_type: str
    amount: float
    description: str
    recipient_user_id: int
    reference_transaction_id: int
    created_at: datetime

class TransactionCreate(BaseModel):
    user_id: int
    transaction_type: str
    amount: float
    description: str    

class WalletTransferCreate(BaseModel):
    sender_user_id: int
    recipient_user_id: int
    amount: float
    description: str

class WalletTransferResponse(BaseModel):
    transfer_id: str
    sender_transaction_id: int
    recipient_transaction_id: int

class WalletTransferDetail(BaseModel):
    transfer_id: str
    sender_user_id: int
    recipient_user_id: int
    amount: float
    description: str
    status: str
    created_at: datetime