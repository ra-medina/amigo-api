from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES_USER = "admin"
POSTGRES_PASSWORD = "BOSTONpatriots123"
DB_NAME = "postgres"

# Replace 'postgres_user', 'postgres_password', 'localhost' and 'amigo_db' with your PostgreSQL credentials and database name
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
