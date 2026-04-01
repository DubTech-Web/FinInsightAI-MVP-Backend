# src/advisor_integration.py
from src.db import SessionLocal
from src.models import User, Loan
from advisor_engine import AdvisorEngine, UserProfile
from gemini_service import query_gemini


def fetch_user_profile(user_id: int) -> UserProfile:
    session = SessionLocal()
    user = session.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise ValueError(f"User with ID {user_id} not found.")
    
    active_loans = session.query(Loan).filter(Loan.user_id == user_id).count()

    profile = UserProfile(
        user_id=user.user_id,
        name=user.name,
        user_type=user.user_type,
        monthly_income=user.monthly_income,
        monthly_spending=user.monthly_spending,
        savings_balance=user.savings_balance,
        credit_score=user.credit_score or 650,
        active_loans=active_loans,
        financial_goals=user.financial_goals or "Improve financial stability"
    )

    session.close()
    return profile


def generate_user_advice(user_id: int, request_type: str = "auto"):
    profile = fetch_user_profile(user_id)
    advisor = AdvisorEngine()
    prompt = advisor.create_prompt(profile, request_type=request_type)

    print(f"🧠 Generated advisory prompt for {profile.name}:\n")
    print(prompt)

    print("\n💬 Generating Gemini Response...\n")
    advice = query_gemini(prompt)
    print(f"💡 AI Advisor Recommendation:\n{advice}")

    return advice


if __name__ == "__main__":
    generate_user_advice(user_id=1)