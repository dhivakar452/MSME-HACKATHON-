import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Resolve path for the SQLite database within the project structure
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "database.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# For SQLite, we set check_same_thread to False to allow multi-threaded access in FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency injection function to obtain database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
