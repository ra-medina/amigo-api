from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .models import Base
from .user import router as user_router
from .appointments import router as appointments_router
from .database import get_db, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(appointments_router)


@app.get("/test_db")
def test_db(db: Session = Depends(get_db)):
    """
    Endpoint to test the database connection.
    """
    return {"message": "Successfully connected to the database!"}
