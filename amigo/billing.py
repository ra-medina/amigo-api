from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db

router = APIRouter()


@router.post(
    "/billings/",
    response_model=schemas.Billing,
    status_code=status.HTTP_201_CREATED,
)
def create_billing(billing: schemas.BillingCreate, db: Session = Depends(get_db)) -> models.Billing:
    """
    Create a new billing record.

    Parameters:
    - billing: BillingCreate schema containing the billing details
    - db: Database session dependency

    Returns:
    - The created billing record as a Billing model instance
    """
    new_billing = models.Billing(**billing.model_dump())
    db.add(new_billing)
    db.commit()
    db.refresh(new_billing)
    return new_billing


@router.get("/billings/", response_model=List[schemas.Billing])
def get_billings(db: Session = Depends(get_db)) -> List[models.Billing]:
    """
    Retrieve all billing records from the database.

    Parameters:
    - db: Database session dependency

    Returns:
    - A list of billing records as Billing model instances
    """
    return db.query(models.Billing).all()


@router.get("/billings/{billing_id}", response_model=schemas.Billing)
def get_billing(billing_id: int, db: Session = Depends(get_db)) -> models.Billing:
    """
    Retrieve a specific billing record by its ID.

    Parameters:
    - billing_id: The ID of the billing record to retrieve
    - db: Database session dependency

    Returns:
    - The requested billing record as a Billing model instance

    Raises:
    - HTTPException: 404 error if the billing record is not found
    """
    billing = db.query(models.Billing).filter(models.Billing.id == billing_id).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Billing record not found")
    return billing


@router.put("/billings/{billing_id}", response_model=schemas.Billing)
def update_billing(billing_id: int, billing: schemas.BillingUpdate, db: Session = Depends(get_db)) -> models.Billing:
    """
    Update an existing billing record.

    Parameters:
    - billing_id: The ID of the billing record to update
    - billing: BillingUpdate schema containing the updated billing details
    - db: Database session dependency

    Returns:
    - The updated billing record as a Billing model instance

    Raises:
    - HTTPException: 404 error if the billing record is not found
    """
    existing_billing = db.query(models.Billing).filter(models.Billing.id == billing_id).first()
    if not existing_billing:
        raise HTTPException(status_code=404, detail="Billing record not found")

    for key, value in billing.model_dump(exclude_unset=True).items():
        setattr(existing_billing, key, value)

    db.commit()
    return existing_billing


@router.delete("/billings/{billing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_billing(billing_id: int, db: Session = Depends(get_db)) -> None:
    """
    Delete a billing record from the database.

    Parameters:
    - billing_id: The ID of the billing record to delete
    - db: Database session dependency

    Returns:
    - None

    Raises:
    - HTTPException: 404 error if the billing record is not found
    """
    billing = db.query(models.Billing).filter(models.Billing.id == billing_id).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Billing record not found")

    db.delete(billing)
    db.commit()
