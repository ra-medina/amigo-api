from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import Base
from .routers import include_routers

from .database import engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

include_routers(app)
