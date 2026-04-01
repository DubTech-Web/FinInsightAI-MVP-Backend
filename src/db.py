from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import sys, os
from dotenv import load_dotenv

# Ensure this folder is treated as a package
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def init_db():
    """Create all tables in the PostgreSQL database."""
    # Import models from the same folder
    from src.models import Base
    print("🚀 Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully.")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()