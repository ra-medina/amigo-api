from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db

router = APIRouter()


@router.post(
    "/appointments/",
    tags=["appointments"],
    response_model=schemas.Appointment,
    status_code=status.HTTP_201_CREATED,
)
def create_appointment(
    appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)
) -> models.Appointment:
    """
    Create a new appointment in the database.

    This function creates a new appointment in the database based on the provided appointment data.
    The appointment data is passed as a parameter in the form of a `schemas.AppointmentCreate` object.
    The function returns the created appointment as a `models.Appointment` object.

    Parameters:
    - appointment: The appointment data to be created in the database.
    - db: The database session to be used for the operation.

    Returns:
    - The created appointment as a `models.Appointment` object.

    Raises:
    - None.

    Example Usage:
    ```
    appointment_data = {
        "start_time": "03-01-2022 09:00:00",
        "end_time": "03-01-2022 10:00:00",
        "description": "Regular check-up",
        "notes": "Patient is recovering well",
        "user_id": 1,
    }
    created_appointment = create_appointment(appointment_data, db)
    ```
    """
    new_appointment = models.Appointment(**appointment.model_dump())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment


@router.get(
    "/appointments/", tags=["appointments"], response_model=List[schemas.Appointment]
)
def get_appointments(db: Session = Depends(get_db)) -> List[models.Appointment]:
    """
    Retrieve all appointments from the database.

    This function queries the database to retrieve all appointments stored in the database.
    It returns a list of `Appointment` objects, which are defined in the `schemas` module.

    Parameters:
        db (Session): The database session to use for the query. Defaults to the result of `get_db()`.

    Returns:
        List[models.Appointment]: A list of `Appointment` objects representing all appointments in the database.
    """
    appointments = db.query(models.Appointment).all()
    return appointments


@router.get(
    "/appointments/{appointment_id}",
    tags=["appointments"],
    response_model=schemas.Appointment,
)
def get_appointment(
    appointment_id: int, db: Session = Depends(get_db)
) -> models.Appointment:
    """
    Retrieve a specific appointment by its ID.
    """
    appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .first()
    )
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.put(
    "/appointments/{appointment_id}",
    tags=["appointments"],
    response_model=schemas.Appointment,
)
def update_appointment(
    appointment_id: int,
    updated_appointment: schemas.AppointmentUpdate,
    db: Session = Depends(get_db),
) -> models.Appointment:
    """
    Update an existing appointment.
    """
    appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .first()
    )
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appointment_data = updated_appointment.model_dump(exclude_unset=True)
    for key, value in appointment_data.items():
        setattr(appointment, key, value)
    db.commit()
    return appointment


@router.delete(
    "/appointments/{appointment_id}",
    tags=["appointments"],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)) -> None:
    """
    Delete an appointment from the database.
    """
    appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .first()
    )
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appointment)
    db.commit()
