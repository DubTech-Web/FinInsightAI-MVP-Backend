from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from . import db, schemas, crud, models

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, database: Session = Depends(db.get_db)):
    existing_user = crud.get_user_by_email(database, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(database, user)

@router.post("/login", response_model=schemas.UserResponse)
def login(user: schemas.UserLogin, database: Session = Depends(db.get_db)):
    db_user = database.query(models.User).options(selectinload(models.User.loans), selectinload(models.User.transactions)).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/user/me", response_model=schemas.UserResponse)
def get_current_user(token: str, database: Session = Depends(db.get_db)):
    user = crud.get_user_by_email(database, token)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user