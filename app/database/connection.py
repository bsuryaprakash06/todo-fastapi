import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.database.models.task import Base, TaskModel

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", "tasks")
    if password:
        DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    else:
        DATABASE_URL = f"postgresql://{user}@{host}:{port}/{db_name}"

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db(db: Session = None) -> None:
    # Automatically create tables if they do not exist
    Base.metadata.create_all(bind=engine)
    
    close_after = False
    if db is None:
        db = SessionLocal()
        close_after = True
        
    try:
        count = db.query(TaskModel).count()
        if count == 0:
            sample_tasks = [
                TaskModel(title="Buy groceries", done=False),
                TaskModel(title="Read documentation", done=True),
                TaskModel(title="Write code", done=False),
            ]
            db.add_all(sample_tasks)
            db.commit()
    finally:
        if close_after:
            db.close()
