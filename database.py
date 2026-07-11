import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# By default use SQLite
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./instagram_scraper.db")

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
