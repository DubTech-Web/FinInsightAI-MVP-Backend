# ==============================================================
# GENERATIVE AI FINANCIAL ADVISOR – FAKE DATA GENERATION SCRIPT
# ==============================================================

from faker import Faker
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# --------------------------------------------------------------
# INITIAL SETUP
# --------------------------------------------------------------
fake = Faker()
Faker.seed(42)
random.seed(42)

# Create data folder
os.makedirs("data", exist_ok=True)

# --------------------------------------------------------------
# USER PROFILE GENERATION
# --------------------------------------------------------------
def generate_user_profiles(n=100):
    """
    Generate synthetic users: salary earners, SME owners, and students.
    """
    users = []
    for i in range(n):
        user_type = random.choice(["salary_earner", "sme_owner", "student"])
        
        if user_type == "salary_earner":
            income = np.random.randint(200_000, 600_000)
            spending = round(income * np.random.uniform(0.6, 0.7))
        elif user_type == "sme_owner":
            income = np.random.randint(800_000, 2_500_000)
            spending = round(income * np.random.uniform(0.7, 0.8))
        else:  # student
            income = np.random.randint(20_000, 70_000)
            spending = round(income * np.random.uniform(0.8, 0.9))

        savings = income - spending
        users.append({
            "user_id": i + 1,
            "name": fake.name(),
            "email": fake.email(),
            "occupation": user_type,
            "monthly_income": income,
            "monthly_spending": spending,
            "savings": savings,
            "account_balance": round(np.random.uniform(10_000, 500_000), 2),
            "loan_status": random.choice(["none", "active", "repaid"]),
            "credit_score": np.random.randint(500, 850),
            "transaction_count": np.random.randint(20, 100),
            "date_joined": fake.date_between(start_date="-2y", end_date="today")
        })

    users_df = pd.DataFrame(users)
    users_df.to_csv("data/users.csv", index=False)
    print(f"✅ Generated {len(users_df)} synthetic users -> data/users.csv")
    return users_df


# --------------------------------------------------------------
# TRANSACTION HISTORY GENERATION (With Spending Categories)
# --------------------------------------------------------------
def generate_transactions(users_df, transactions_per_user=40):
    """
    Generate realistic debit/credit transaction data for each user,
    including spending categories for AI training.
    """
    transactions = []
    
    # Define spending categories and example descriptions
    spending_categories = {
        "Food": ["Groceries", "Restaurant", "Snacks", "Supermarket"],
        "Transport": ["Fuel Refill", "Public Transport", "Ride Hailing", "Car Maintenance"],
        "Utilities": ["Electricity Bill", "Water Bill", "Internet Subscription"],
        "Entertainment": ["Cinema", "Music Streaming", "Gaming", "Event Ticket"],
        "Shopping": ["Online Shopping", "Clothing", "Accessories", "Electronics"],
        "Education": ["School Fees", "Books", "Course Subscription"],
        "Health": ["Pharmacy", "Clinic Visit", "Health Insurance"],
        "Others": ["Airtime Purchase", "Transfer to Friend", "Miscellaneous"]
    }

    for _, user in users_df.iterrows():
        for _ in range(transactions_per_user):
            t_type = np.random.choice(["credit", "debit"], p=[0.4, 0.6])

            if t_type == "credit":
                amount = np.random.randint(20_000, 300_000)
                description = random.choice([
                    "Salary Payment", "POS Inflow", "Business Income",
                    "Transfer from Friend", "Refund", "Loan Disbursement"
                ])
                category = "Income"
            else:
                category = random.choice(list(spending_categories.keys()))
                description = random.choice(spending_categories[category])
                amount = np.random.randint(1_000, 80_000)

            date = fake.date_between(start_date="-90d", end_date="today")

            transactions.append({
                "transaction_id": fake.uuid4(),
                "user_id": user["user_id"],
                "date": date,
                "type": t_type,
                "amount": amount,
                "category": category,
                "description": description,
                "merchant": fake.company(),
                "location": fake.city(),
                "balance_after": user["account_balance"] + np.random.uniform(-5000, 5000)
            })

    tx_df = pd.DataFrame(transactions)
    tx_df.sort_values(by=["user_id", "date"], inplace=True)
    tx_df.to_csv("data/transactions.csv", index=False)
    print(f"✅ Generated {len(tx_df)} transactions -> data/transactions.csv")
    return tx_df


# --------------------------------------------------------------
# LOAN HISTORY GENERATION (Fixed repayment formula)
# --------------------------------------------------------------
def generate_loans(users_df):
    """
    Simulate user-specific loan histories based on affordability.
    """
    loans = []
    for _, user in users_df.iterrows():
        if user["loan_status"] != "none":
            loan_amount = np.random.randint(100_000, user["monthly_income"] * 6)
            interest_rate = round(np.random.uniform(10.0, 18.0), 2)
            tenure_months = np.random.choice([6, 12, 18, 24, 36])

            # --- Fixed repayment calculation ---
            r = interest_rate / 100 / 12
            n = tenure_months
            P = loan_amount

            if r == 0:
                monthly_repayment = P / n
            else:
                monthly_repayment = P * (r * (1 + r)**n) / ((1 + r)**n - 1)

            loans.append({
                "user_id": user["user_id"],
                "loan_amount": round(loan_amount, 2),
                "interest_rate": interest_rate,
                "tenure_months": tenure_months,
                "monthly_repayment": round(monthly_repayment, 2),
                "loan_status": user["loan_status"],
                "start_date": fake.date_between(start_date="-1y", end_date="-1m")
            })

    loans_df = pd.DataFrame(loans)
    loans_df.to_csv("data/loans.csv", index=False)
    print(f"✅ Generated {len(loans_df)} loan records -> data/loans.csv")
    return loans_df


# --------------------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------------------
if __name__ == "__main__":
    print("\n🚀 Generating Synthetic Financial Data with Spending Categories...\n")
    users_df = generate_user_profiles(50)
    tx_df = generate_transactions(users_df, 40)
    loans_df = generate_loans(users_df)
    print("\n🎉 Data generation complete! Files are ready in the /data folder.")
