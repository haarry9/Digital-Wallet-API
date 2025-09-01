from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

# User schemas
class UserBase(BaseModel):
    username: str
    email: str
    phone_number: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    phone_number: Optional[str] = None

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    phone_number: Optional[str]
    balance: float
    created_at: datetime

# Wallet schemas
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

class WalletAddMoneyResponse(BaseModel):
    transaction_id: int
    user_id: int
    amount: float
    new_balance: float
    transaction_type: str

# Transaction schemas
class TransactionBase(BaseModel):
    transaction_type: str
    amount: float
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    user_id: int

class TransactionResponse(BaseModel):
    transaction_id: int
    transaction_type: str
    amount: float
    description: Optional[str]
    created_at: datetime

class TransactionDetail(BaseModel):
    transaction_id: int
    user_id: int
    transaction_type: str
    amount: float
    description: Optional[str]
    recipient_user_id: Optional[int]
    reference_transaction_id: Optional[int]
    created_at: datetime

class TransactionHistoryResponse(BaseModel):
    transactions: List[TransactionResponse]
    total: int
    page: int
    limit: int

# Transfer schemas
class TransferCreate(BaseModel):
    sender_user_id: int
    recipient_user_id: int
    amount: float
    description: str

class TransferResponse(BaseModel):
    transfer_id: str
    sender_transaction_id: int
    recipient_transaction_id: int
    amount: float
    sender_new_balance: float
    recipient_new_balance: float
    status: str

class TransferDetail(BaseModel):
    transfer_id: str
    sender_user_id: int
    recipient_user_id: int
    amount: float
    description: str
    status: str
    created_at: datetime

# Error response
class ErrorResponse(BaseModel):
    error: str
    current_balance: Optional[float] = None
    required_amount: Optional[float] = None