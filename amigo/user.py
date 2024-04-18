from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from amigo.auth import auth_service
from amigo.auth.auth_service import AuthService
from amigo.auth.dependencies import get_current_user

from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data: schemas.UserCreate,
    current_user: Optional[str] = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> models.User:
    """
    Register a new user (patient, clinician, or clinician superuser).
    Parameters:
    - user: UserCreate schema with user's email, full name, password, and user type
    - db: Session dependency to interact with the database
    Returns:
    - The created User model instance
    """
    # Check if the email is already registered
    existing_user = (
        db.query(models.User).filter(models.User.email == user_data.email).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check if the current user is authorized to register a new user
    if current_user is None:
        raise HTTPException(
            status_code=403, detail="Unauthorized to register a new user"
        )

    # Hash the password
    hashed_password = auth_service.get_password_hash(user_data.password)

    # Create a new user instance
    new_user = models.User(
        email=user_data.email,
        full_name=user_data.full_name,
        dob=user_data.dob,
        hashed_password=hashed_password,
    )

    # Create instances of the appropriate user type (Patient, Clinician, or ClinicianSuperuser)
    if user_data.user_type == "patient":
        db_patient = models.Patient(
            user=new_user,
            gender=user_data.gender,
            phone_number=user_data.phone_number,
            emergency_contact=user_data.emergency_contact,
        )
        db.add(db_patient)
    elif user_data.user_type == "clinician":
        db_clinician = models.Clinician(
            user=new_user,
            specialization=user_data.specialization,
            license_number=user_data.license_number,
        )
        db.add(db_clinician)
    elif user_data.user_type == "clinician_superuser":
        db_clinician = models.Clinician(
            user=new_user,
            specialization=user_data.specialization,
            license_number=user_data.license_number,
        )
        db_superuser = models.ClinicianSuperuser(clinician=db_clinician)
        db.add(db_clinician)
        db.add(db_superuser)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.put("/users/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int, user_data: schemas.UserUpdate, db: Session = Depends(get_db)
) -> models.User:
    """
    Update user information.
    Parameters:
    - user_id: integer representing the User ID
    - user_data: UserUpdate schema with user's information to update
    - db: Session dependency to interact with the database
    Returns:
    - The updated User model instance
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user_data.full_name is not None:
        db_user.full_name = user_data.full_name
    if user_data.dob is not None:
        db_user.dob = user_data.dob

    # Update user-specific fields based on user type
    user_type = db_user.__mapper__.polymorphic_identity
    if user_type == "patient":
        db_patient = (
            db.query(models.Patient).filter(models.Patient.id == user_id).first()
        )
        if db_patient is None:
            raise HTTPException(status_code=404, detail="Patient not found")

        if user_data.gender is not None:
            db_patient.gender = user_data.gender
        if user_data.phone_number is not None:
            db_patient.phone_number = user_data.phone_number
        if user_data.emergency_contact is not None:
            db_patient.emergency_contact = user_data.emergency_contact

    elif user_type == "clinician":
        db_clinician = (
            db.query(models.Clinician).filter(models.Clinician.id == user_id).first()
        )
        if db_clinician is None:
            raise HTTPException(status_code=404, detail="Clinician not found")

        if user_data.specialization is not None:
            db_clinician.specialization = user_data.specialization
        if user_data.license_number is not None:
            db_clinician.license_number = user_data.license_number

    elif user_type == "clinician_superuser":
        db_superuser = (
            db.query(models.ClinicianSuperuser)
            .filter(models.ClinicianSuperuser.id == user_id)
            .first()
        )
        if db_superuser is None:
            raise HTTPException(status_code=404, detail="Clinician Superuser not found")

        db_clinician = db_superuser.clinician
        if user_data.specialization is not None:
            db_clinician.specialization = user_data.specialization
        if user_data.license_number is not None:
            db_clinician.license_number = user_data.license_number

    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/register/patient", response_model=schemas.Patient)
def register_patient(
    patient_data: schemas.PatientCreate, db: Session = Depends(get_db)
):
    db_user = models.User(
        email=patient_data.email,
        full_name=patient_data.full_name,
        dob=patient_data.dob,
        hashed_password=AuthService.get_password_hash(patient_data.password),
    )
    db_patient = models.Patient(
        user=db_user,
        gender=patient_data.gender,
        phone_number=patient_data.phone_number,
        emergency_contact=patient_data.emergency_contact,
    )
    db.add(db_user)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.post("/register/clinician", response_model=schemas.Clinician)
def register_clinician(
    clinician_data: schemas.ClinicianCreate, db: Session = Depends(get_db)
):
    db_user = models.User(
        email=clinician_data.email,
        full_name=clinician_data.full_name,
        dob=clinician_data.dob,
        hashed_password=AuthService.get_password_hash(clinician_data.password),
    )
    db_clinician = models.Clinician(
        user=db_user,
        specialization=clinician_data.specialization,
        license_number=clinician_data.license_number,
    )
    db.add(db_user)
    db.add(db_clinician)
    db.commit()
    db.refresh(db_clinician)
    return db_clinician


@router.post("/register/clinician-superuser", response_model=schemas.ClinicianSuperuser)
def register_clinician_superuser(
    superuser_data: schemas.ClinicianSuperuserCreate, db: Session = Depends(get_db)
):
    db_user = models.User(
        email=superuser_data.email,
        full_name=superuser_data.full_name,
        dob=superuser_data.dob,
        hashed_password=AuthService.get_password_hash(superuser_data.password),
    )
    db_clinician = models.Clinician(
        user=db_user,
        specialization=superuser_data.specialization,
        license_number=superuser_data.license_number,
    )
    db_superuser = models.ClinicianSuperuser(clinician=db_clinician)
    db.add(db_user)
    db.add(db_clinician)
    db.add(db_superuser)
    db.commit()
    db.refresh(db_superuser)
    return db_superuser


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    """
    Deletes a user.
    Parameters:
    - user_id: integer representing the User ID
    - db: Session dependency to interact with the database
    Returns:
    - 204 Code meaning User was deleted.
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_type = db_user.__mapper__.polymorphic_identity
    if user_type == "patient":
        db_patient = (
            db.query(models.Patient).filter(models.Patient.id == user_id).first()
        )
        if db_patient is not None:
            db.delete(db_patient)

    elif user_type == "clinician":
        db_clinician = (
            db.query(models.Clinician).filter(models.Clinician.id == user_id).first()
        )
        if db_clinician is not None:
            db.delete(db_clinician)

    elif user_type == "clinician_superuser":
        db_superuser = (
            db.query(models.ClinicianSuperuser)
            .filter(models.ClinicianSuperuser.id == user_id)
            .first()
        )
        if db_superuser is not None:
            db_clinician = db_superuser.clinician
            db.delete(db_superuser)
            db.delete(db_clinician)

    db.delete(db_user)
    db.commit()

    # You can optionally return a success message
    return {"message": "User deleted successfully"}
