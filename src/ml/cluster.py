"""
Cluster users by behavior and optionally persist cluster labels back to DB.
Run with: python -m src.ml.cluster
"""

from __future__ import annotations
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import joblib
import pandas as pd
import numpy as np
import os

# relative imports inside package
from ..db import SessionLocal
from ..models import User

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, "kmeans_user_clusters.joblib")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.joblib")


def get_user_features_df() -> pd.DataFrame:
    """
    Query users from DB and return feature dataframe.
    Must return a DataFrame with one row per user_id.
    """
    session = SessionLocal()
    users = session.query(User).all()
    session.close()

    rows = []
    for u in users:
        rows.append({
            "user_id": u.user_id,
            "monthly_income": float(u.monthly_income or 0),
            "monthly_spending": float(u.monthly_spending or 0),
            "savings": float(u.savings or 0),
            "credit_score": float(u.credit_score or 650),
            "spending_ratio": float(u.spending_ratio or 0),
            "avg_transaction": float(u.avg_transaction or 0),
            "transaction_count": int(u.transaction_count or 0),
            "account_balance": float(u.account_balance or 0)
        })

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("No users found in DB to cluster.")
    return df


def prepare_features(df: pd.DataFrame) -> tuple[pd.DataFrame, StandardScaler]:
    """
    Select and scale numeric features. Returns scaled array and scaler.
    """
    feature_cols = ["monthly_income", "monthly_spending", "savings",
                    "credit_score", "spending_ratio", "avg_transaction",
                    "transaction_count", "account_balance"]
    # ensure columns exist
    for c in feature_cols:
        if c not in df.columns:
            df[c] = 0.0

    X = df[feature_cols].fillna(0.0).astype(float)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, scaler


def train_kmeans(X_scaled: np.ndarray, n_clusters: int = 4) -> KMeans:
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    model.fit(X_scaled)
    return model


def save_model_and_scaler(model: KMeans, scaler: StandardScaler):
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    print("Saved model to", MODEL_PATH)


def load_model_and_scaler():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        return None, None
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler


def assign_clusters_to_db(df: pd.DataFrame, labels: np.ndarray, column_name: str = "cluster_id"):
    """
    Add labels as a textual column in users table (re-using loan_status or add new property).
    For simplicity we will write cluster id into user's loan_status prefixed with 'cluster:'.
    You can change to a dedicated column if you prefer (requires DB migration).
    """
    session = SessionLocal()
    for uid, lab in zip(df["user_id"].tolist(), labels.tolist()):
        user = session.query(User).filter(User.user_id == int(uid)).first()
        if user:
            # store cluster info safely; change this line if you have a dedicated column
            user.loan_status = f"cluster:{int(lab)}"
    session.commit()
    session.close()
    print("Cluster labels saved to DB (in users.loan_status).")


def run_training(n_clusters: int = 4):
    df = get_user_features_df()
    X_scaled, scaler = prepare_features(df)
    model = train_kmeans(X_scaled, n_clusters=n_clusters)
    labels = model.predict(X_scaled)
    df["cluster"] = labels
    save_model_and_scaler(model, scaler)
    assign_clusters_to_db(df, labels)
    return df, model, scaler


def run_predict_and_save():
    """Load model+scaler and score current users, then save labels to DB."""
    model, scaler = load_model_and_scaler()
    if model is None:
        raise RuntimeError("No trained model found. Run training first.")
    df = get_user_features_df()
    # prepare features but use existing scaler
    feature_cols = ["monthly_income", "monthly_spending", "savings",
                    "credit_score", "spending_ratio", "avg_transaction",
                    "transaction_count", "account_balance"]
    X = df[feature_cols].fillna(0.0).astype(float)
    X_scaled = scaler.transform(X)
    labels = model.predict(X_scaled)
    df["cluster"] = labels
    assign_clusters_to_db(df, labels)
    return df


if __name__ == "__main__":
    # Default behavior: train model and persist labels
    print("Clustering users and persisting labels...")
    df, model, scaler = run_training(n_clusters=4)
    print(df[["user_id", "cluster"]].head())