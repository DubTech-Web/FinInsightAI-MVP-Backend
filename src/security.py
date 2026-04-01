from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from dotenv import load_dotenv
import os

load_dotenv()
API_USER = os.getenv("API_USER", "admin")
API_PASS = os.getenv("API_PASS", "changeme")

security = HTTPBasic()

def basic_auth(creds: HTTPBasicCredentials = Depends(security)):
    correct_user = secrets.compare_digest(creds.username, API_USER)
    correct_pass = secrets.compare_digest(creds.password, API_PASS)
    if not (correct_user and correct_pass):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return creds.username