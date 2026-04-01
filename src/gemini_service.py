# src/gemini_service.py
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-2.5-flash"


def query_gemini(prompt: str, temperature: float = 0.6) -> str:
    """
    Send a prompt to Gemini and return the AI-generated advisory response.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return "Sorry, I couldn't generate a response at this time."