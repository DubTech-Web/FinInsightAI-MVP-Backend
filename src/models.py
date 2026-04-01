from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .db import Base
import datetime


class Recommendation(Base):
    __tablename__ = "recommendations"

    rec_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    request_type = Column(String)       # 'analyze' or 'recommend'
    prompt = Column(Text)              # the prompt sent to LLM (store sanitized)
    response = Column(Text)            # LLM text output (store sanitized)
    model = Column(String)             # model used e.g., gemini-1.5-pro
    note = Column(String)

    user = relationship("User", back_populates="recommendations")


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    occupation = Column(String)
    monthly_income = Column(Float)
    monthly_spending = Column(Float)
    savings = Column(Float)
    account_balance = Column(Float)
    loan_status = Column(String)
    credit_score = Column(Integer)
    transaction_count = Column(Integer)
    date_joined = Column(DateTime, default=datetime.datetime.utcnow)
    spending_ratio = Column(Float)
    avg_transaction = Column(Float)

    loans = relationship("Loan", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True)  # ✅ was Integer before
    user_id = Column(Integer, ForeignKey("users.user_id"))
    date = Column(Date)
    type = Column(String)
    amount = Column(Float)
    category = Column(String)
    description = Column(String)
    merchant = Column(String)
    location = Column(String)
    balance_after = Column(Float)

    user = relationship("User", back_populates="transactions")


class Loan(Base):
    __tablename__ = "loans"

    loan_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    loan_amount = Column(Float)
    interest_rate = Column(Float)
    tenure_months = Column(Integer)
    monthly_repayment = Column(Float)
    loan_status = Column(String)
    start_date = Column(String)

    user = relationship("User", back_populates="loans")