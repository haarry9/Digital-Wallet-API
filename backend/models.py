from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text, Numeric
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(15))
    balance = Column(Numeric(10, 2), default=0.00)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transaction_type = Column(Enum("CREDIT", "DEBIT", "TRANSFER_IN", "TRANSFER_OUT", name="transaction_type"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(Text)
    reference_transaction_id = Column(Integer, ForeignKey("transactions.id"))
    recipient_user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="transactions")
    recipient = relationship("User", foreign_keys=[recipient_user_id])
    reference_transaction = relationship("Transaction", remote_side=[id])



