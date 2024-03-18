from fastapi import FastAPI

from .models import Base
from .routers import include_routers

from .database import engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

include_routers(app)
