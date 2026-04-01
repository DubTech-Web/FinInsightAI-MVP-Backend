from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    
    db_user = models.User(
        name=user.name,
        email=user.email,
        occupation=user.occupation
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def save_recommendation(db: Session, user_id: int, prompt: str, response: str, request_type: str = "analyze", model: str = "gemini"):
    rec = models.Recommendation(
        user_id=user_id,
        prompt=prompt[:4000],
        response=response[:8000],
        request_type=request_type,
        model=model
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec