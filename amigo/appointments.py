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
    Retrieve a single appointment from the database.

    Args:
        appointment_id (int): The ID of the appointment to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        models.Appointment: The retrieved appointment.

    Raises:
        HTTPException: If the appointment with the specified ID is not found.
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

    This function is a PUT router that updates an appointment with the provided appointment_id.
    It takes in the appointment_id, the updated_appointment data, and the database session as parameters.

    Parameters:
    - appointment_id (int): The ID of the appointment to be updated.
    - updated_appointment (schemas.AppointmentUpdate): The updated appointment data.
    - db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
    - models.Appointment: The updated appointment.

    Raises:
    - HTTPException: If the appointment with the provided appointment_id is not found.
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
