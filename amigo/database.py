from os import getenv

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load environment variables
load_dotenv()

# Use global variables for the connection details
PGUSER = getenv("PGUSER")
PGPASSWORD = getenv("PGPASSWORD")
PGHOST = getenv("PGHOST")
PGDATABASE = getenv("PGDATABASE")

# Create the connection string
connection_string = URL.create(
    "postgresql",
    username=PGUSER,
    password=PGPASSWORD,
    host=PGHOST,
    database=PGDATABASE,
    query={"sslmode": "require"},
)

engine = create_engine(connection_string)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()
