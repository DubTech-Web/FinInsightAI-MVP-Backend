import pandas as pd
from ..db import SessionLocal, init_db
from ..models import User, Loan, Transaction
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def load_users():
    df = pd.read_csv("data/clean_users.csv")
    session = SessionLocal()

    for _, row in df.iterrows():
        user = User(
            user_id=int(row["user_id"]),
            name=row["name"],
            email=row["email"],
            occupation=row["occupation"],
            monthly_income=float(row["monthly_income"]),
            monthly_spending=float(row["monthly_spending"]),
            savings=float(row["savings"]),
            account_balance=float(row["account_balance"]),
            loan_status=row["loan_status"],
            credit_score=int(row["credit_score"]),
            transaction_count=int(row["transaction_count"]),
            date_joined=row["date_joined"],
            spending_ratio=float(row["spending_ratio"]),
            avg_transaction=float(row["avg_transaction"]),
        )
        session.merge(user)  # avoids duplicates if rerun

    session.commit()
    session.close()
    print("✅ Users loaded successfully.")


def load_transactions():
    df = pd.read_csv("data/clean_transactions.csv")
    session = SessionLocal()

    for _, row in df.iterrows():
        txn = Transaction(
            transaction_id=row["transaction_id"],  # ✅ No int() here
            user_id=int(row["user_id"]),
            date=row["date"],
            type=row["type"],
            amount=float(row["amount"]),
            category=row["category"],
            description=row["description"],
            merchant=row["merchant"],
            location=row["location"],
            balance_after=float(row["balance_after"]),
        )
        session.merge(txn)

    session.commit()
    session.close()
    print("✅ Transactions loaded successfully.")


def load_loans():
    df = pd.read_csv("data/clean_loans.csv")
    session = SessionLocal()

    for _, row in df.iterrows():
        loan = Loan(
            user_id=int(row["user_id"]),
            loan_amount=float(row["loan_amount"]),
            interest_rate=float(row["interest_rate"]),
            tenure_months=int(row["tenure_months"]),
            monthly_repayment=float(row["monthly_repayment"]),
            loan_status=row["loan_status"],
            start_date=row["start_date"],
        )
        session.add(loan)

    session.commit()
    session.close()
    print("✅ Loans loaded successfully.")


if __name__ == "__main__":
    print("🚀 Initializing database...")
    init_db()
    load_users()
    load_transactions()
    load_loans()
    print("🎉 All data loaded successfully!")