from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
import datetime

class TransactionIn(BaseModel):
    transaction_id: str
    date: Optional[datetime.date]
    type: Optional[str]
    amount: float
    category: Optional[str]
    merchant: Optional[str]
    location: Optional[str]
    balance_after: Optional[float]

class TransactionResponse(BaseModel):
    transaction_id: str
    date: Optional[datetime.date] = None
    type: Optional[str] = None
    amount: float
    category: Optional[str] = None
    merchant: Optional[str] = None
    location: Optional[str] = None
    balance_after: Optional[float] = None

    class Config:
        from_attributes = True


class AnalyzeRequest(BaseModel):
    user_id: Optional[int] = None
    user_profile: Optional[dict] = None   # you can pass partial profile
    request_type: Optional[str] = "auto"  # e.g., "transactions", "loan", "savings", "investment"
    transactions: Optional[List[TransactionIn]] = None

    class Config:
        from_attributes = True

class AnalyzeResponse(BaseModel):
    summary: str
    recommendations: List[str]

class RecommendRequest(BaseModel):
    user_id: Optional[int] = None
    context: Optional[dict] = None

class RecommendResponse(BaseModel):
    products: List[dict] 

class UserBase(BaseModel):
    name: str
    email: EmailStr
    occupation: Optional[str] = None

class UserCreate(UserBase):
    email: EmailStr
    

class UserLogin(BaseModel):
    email: EmailStr

class LoanResponse(BaseModel):
    loan_id: int
    user_id: Optional[int] = None
    loan_amount: Optional[float] = None
    interest_rate: Optional[float] = None
    tenure_months: Optional[int] = None
    monthly_repayment: Optional[float] = None
    loan_status: Optional[str] = None
    start_date: Optional[str] = None

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    user_id: int
    monthly_income: Optional[float] = None
    monthly_spending: Optional[float] = None
    savings: Optional[float] = None
    account_balance: Optional[float] = None
    loans: List[LoanResponse] = []
    transactions: List[TransactionResponse] = []
    date_joined: datetime.datetime

    class Config:
        from_attributes = True