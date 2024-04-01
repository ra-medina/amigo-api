from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    """Base User model representing both patients and clinicians."""

    __tablename__ = "users"
    __mapper_args__ = {"polymorphic_identity": "user", "polymorphic_on": "user_type"}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    dob = Column(Date)
    user_type = Column(String)


class Patient(User):
    """Patient subclass inheriting from User. Has patient-specific features."""

    __tablename__ = "patient"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "patient"}

    gender = Column(String)
    phone_number = Column(String)
    emergency_contact = Column(String)

    # Specify the foreign_keys to clear any ambiguity
    appointments = relationship(
        "Appointment",
        foreign_keys="[Appointment.patient_id]",
        backref="patient_appointments",
    )
    billings = relationship(
        "Billing", foreign_keys="[Billing.patient_id]", backref="patient_billings"
    )
    medical_records = relationship(
        "MedicalRecord",
        foreign_keys="[MedicalRecord.patient_id]",
        backref="patient_records",
    )


class Clinician(User):
    """Clinician subclass inheriting from User. Has clinician-specific features."""

    __tablename__ = "clinician"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "clinician"}

    specialization = Column(String)
    license_number = Column(String)

    # Specify the foreign_keys to clear any ambiguity
    appointments = relationship(
        "Appointment",
        foreign_keys="[Appointment.clinician_id]",
        backref="clinician_appointments",
    )
    billings = relationship(
        "Billing", foreign_keys="[Billing.clinician_id]", backref="clinician_billings"
    )
    notes = relationship(
        "Note", foreign_keys="[Note.author_id]", backref="author_notes"
    )


class ClinicianSuperuser(Clinician):
    """ClinicianSuperuser subclass inheriting from Clinician. Has superuser-specific features."""

    __mapper_args__ = {"polymorphic_identity": "clinician_superuser"}


class Appointment(Base):
    """
    Appointment model for scheduling.
    """

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    clinician_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    description = Column(String)
    notes = Column(String)

    patient = relationship("Patient", foreign_keys=[patient_id])
    clinician = relationship("Clinician", foreign_keys=[clinician_id])


class Billing(Base):
    """
    Billing model for handling payments and invoices.
    """

    __tablename__ = "billings"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    clinician_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    date = Column(Date)
    description = Column(String)
    is_paid = Column(Boolean, default=False)

    patient = relationship(
        "User", foreign_keys=[patient_id], backref="patient_billings"
    )
    clinician = relationship(
        "User", foreign_keys=[clinician_id], backref="clinician_billings"
    )


class MedicalRecord(Base):
    """
    MedicalRecord model for storing patient health records.
    """

    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    record_data = Column(String)

    # Relationship to the User model, with a backref for easy reverse access
    patient = relationship(
        "User", foreign_keys=[patient_id], backref="patient_medical_records"
    )


class Note(Base):
    """
    Note model for clinicians to add notes about patients or treatments.
    """

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    patient_id = Column(Integer, ForeignKey("users.id"))
    note_content = Column(String)
    date = Column(Date)

    author = relationship("User", foreign_keys=[author_id], backref="notes_written")
    patient = relationship("User", foreign_keys=[patient_id], backref="notes_received")
