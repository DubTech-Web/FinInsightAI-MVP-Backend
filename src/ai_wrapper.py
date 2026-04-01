from .advisor_engine import AdvisorEngine, UserProfile
from .gemini_service import query_gemini
import html
import os

def sanitize_text_for_storage(text: str) -> str:
    # remove or mask sensitive items (NA example) — adapt as needed
    return text.replace("\n", " ").strip()

def analyze_user(profile: UserProfile, transactions: list = None) -> dict:
    engine = AdvisorEngine()
    prompt = engine.create_prompt(profile, request_type="savings")  # or auto
    # optionally append transaction summary
    if transactions:
        tx_summary = f"\nRecent {len(transactions)} transactions. First sample: {transactions[:3]}"
        prompt += tx_summary

    raw = query_gemini(prompt)  # your gemini wrapper returns text
    return {"prompt": prompt, "response": raw, "summary": raw[:1000]}

def recommend_products(profile: UserProfile) -> dict:
    engine = AdvisorEngine()
    prompt = engine.create_prompt(profile, request_type="investment")
    raw = query_gemini(prompt)
    return {"prompt": prompt, "response": raw}