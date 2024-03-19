from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import get_db

router = APIRouter()


@router.post(
    "/appointments/",
    response_model=schemas.Appointment,
    status_code=status.HTTP_201_CREATED,
)
def create_appointment(
    appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)
) -> models.Appointment:
    """
    Create a new appointment in the database.
    """
    new_appointment = models.Appointment(**appointment.model_dump())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment


@router.get("/appointments/", response_model=List[schemas.Appointment])
def get_appointments(db: Session = Depends(get_db)) -> models.Appointment:
    """
    Retrieve all appointments from the database.
    """
    appointments = db.query(models.Appointment).all()
    return appointments


@router.get("/appointments/{appointment_id}", response_model=schemas.Appointment)
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


@router.put("/appointments/{appointment_id}", response_model=schemas.Appointment)
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
    appointment_data = updated_appointment.dict(exclude_unset=True)
    for key, value in appointment_data.items():
        setattr(appointment, key, value)
    db.commit()
    return appointment


@router.delete("/appointments/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
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
    return {"ok": True}
