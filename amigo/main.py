from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models
from .database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/test_db")
def test_db(db: Session = Depends(get_db)):
    """
    Endpoint to test the database connection.
    """
    return {"message": "Successfully connected to the database!"}
