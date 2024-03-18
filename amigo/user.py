
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine
from .security import get_password_hash

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


# Dependency to get the database session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> models.User:
    """
    Create a new user in the database.

    Parameters:
    - user: UserCreate schema with user's email, full name, and password
    - db: Session dependency to interact with the database

    Returns:
    - The created User model instance
    """
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        email=user.email, full_name=user.full_name, hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)) -> models.User:
    """
    Retrieve a user by ID.

    Parameters:
    - user_id: integer representing the User ID
    - db: Session dependency to interact with the database

    Returns:
    - The User model instance
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)
) -> models.User:
    """
    Update user information.

    Parameters:
    - user_id: integer representing the User ID
    - user: UserUpdate schema with user's email and/or full name
    - db: Session dependency to interact with the database

    Returns:
    - The updated User model instance
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Update model instance with the new data
    if user.email:
        db_user.email = user.email
    if user.full_name:
        db_user.full_name = user.full_name

    db.commit()
    db.refresh(db_user)
    return db_user
