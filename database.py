from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Docker uses /app/data_vol, local uses project dir
_data_dir = "/app/data_vol" if os.path.isdir("/app/data_vol") else os.path.dirname(os.path.abspath(__file__))
_db_path = os.path.join(_data_dir, "study.db")
DATABASE_URL = f"sqlite:///{_db_path}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
