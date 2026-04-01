# ===============================================================
# DATA CLEANING AND DATABASE STORAGE SCRIPT
# ===============================================================

import pandas as pd
from sqlalchemy import create_engine, text

# ---------------------------------------------------------------
# STEP 1: Load Raw Data
# ---------------------------------------------------------------
users = pd.read_csv("data/users.csv")
transactions = pd.read_csv("data/transactions.csv")
loans = pd.read_csv("data/loans.csv")

print("✅ Raw data loaded.")


# ---------------------------------------------------------------
# STEP 2: Basic Cleaning
# ---------------------------------------------------------------
def clean_dataframe(df):
    # Remove duplicates
    df = df.drop_duplicates()

    # Remove any completely empty rows
    df = df.dropna(how='all')

    # Trim whitespace from string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()

    return df


users = clean_dataframe(users)
transactions = clean_dataframe(transactions)
loans = clean_dataframe(loans)

# Ensure consistent user_id types
users["user_id"] = users["user_id"].astype(int)
transactions["user_id"] = transactions["user_id"].astype(int)
loans["user_id"] = loans["user_id"].astype(int)


# ---------------------------------------------------------------
# STEP 3: Handle Missing Values
# ---------------------------------------------------------------
# Fill missing categories or merchants with “Unknown”
transactions["category"].fillna("Unknown", inplace=True)
transactions["merchant"].fillna("Unknown", inplace=True)

# Fill missing loan amounts with 0 (for users with no loans)
loans["loan_amount"].fillna(0, inplace=True)
loans["interest_rate"].fillna(0, inplace=True)
loans["monthly_repayment"].fillna(0, inplace=True)

print("✅ Data cleaned.")


# ---------------------------------------------------------------
# STEP 4: Referential Integrity
# ---------------------------------------------------------------
# Only keep transactions and loans for users that exist in users.csv
transactions = transactions[transactions["user_id"].isin(users["user_id"])]
loans = loans[loans["user_id"].isin(users["user_id"])]

print("✅ Referential integrity enforced.")


# ---------------------------------------------------------------
# STEP 5: Optional — Add Derived Columns
# ---------------------------------------------------------------
# Example: Add spending ratio (spending/income)
users["spending_ratio"] = round(users["monthly_spending"] / users["monthly_income"], 2)

# Example: Add average transaction amount per user
avg_tx = transactions.groupby("user_id")["amount"].mean().rename("avg_transaction")
users = users.merge(avg_tx, on="user_id", how="left")

print("✅ Added derived insights to users table.")


# ---------------------------------------------------------------
# STEP 6: Save Cleaned Versions
# ---------------------------------------------------------------
users.to_csv("data/clean_users.csv", index=False)
transactions.to_csv("data/clean_transactions.csv", index=False)
loans.to_csv("data/clean_loans.csv", index=False)

print("💾 Cleaned data saved to /data folder.")

# ---------------------------------------------------------------
# STEP 7: Store Cleaned Data into Database
# ---------------------------------------------------------------

# Example: SQLite (for local testing)
# You can change this to PostgreSQL or MySQL later.
engine = create_engine("sqlite:///data/ai_advisor.db")

# If PostgreSQL:
# engine = create_engine("postgresql+psycopg2://username:password@localhost:5432/ai_advisor")

# Write to database
users.to_sql("users", engine, index=False, if_exists="replace")
transactions.to_sql("transactions", engine, index=False, if_exists="replace")
loans.to_sql("loans", engine, index=False, if_exists="replace")

print("✅ All tables stored in the database!")

# Optional: Test query
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM users"))
    print(f"👥 Total users in database: {list(result)[0][0]}")