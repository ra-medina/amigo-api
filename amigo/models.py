from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Numeric,
    Boolean,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User model representing both patients and clinicians.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_clinician = Column(Boolean, default=False)

    appointments = relationship("Appointment", back_populates="user")
    billings = relationship("Billing", back_populates="user")
    medical_records = relationship("MedicalRecord", back_populates="user")
    notes = relationship("Note", back_populates="author")


class Appointment(Base):
    """
    Appointment model for scheduling.
    """

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="appointments")


class Billing(Base):
    """
    Billing model for handling payments and invoices.
    """

    __tablename__ = "billings"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2))
    date = Column(DateTime)
    paid = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="billings")


class MedicalRecord(Base):
    """
    MedicalRecord model for storing patient health records.
    """

    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    record = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="medical_records")


class Note(Base):
    """
    Note model for clinicians to add notes about patients or treatments.
    """

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="notes")
