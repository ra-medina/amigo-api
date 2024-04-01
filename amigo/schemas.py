from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None
    dob: date


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    full_name: Optional[str] = None
    dob: Optional[date] = None


class PatientBase(UserBase):
    gender: str
    phone_number: str
    emergency_contact: str


class PatientCreate(PatientBase):
    password: str


class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    emergency_contact: Optional[str] = None


class Patient(PatientBase):
    id: int
    email: str
    full_name: str
    dob: date

    class Config:
        from_attributes = True


class ClinicianBase(UserBase):
    specialization: str
    license_number: str


class ClinicianCreate(ClinicianBase):
    password: str


class ClinicianUpdate(BaseModel):
    full_name: Optional[str] = None
    dob: Optional[date] = None
    specialization: Optional[str] = None
    license_number: Optional[str] = None


class ClinicianSuperuserBase(ClinicianBase):
    pass


class ClinicianSuperuserCreate(ClinicianSuperuserBase):
    password: str


class ClinicianSuperuserUpdate(BaseModel):
    full_name: Optional[str] = None
    dob: Optional[date] = None
    specialization: Optional[str] = None
    license_number: Optional[str] = None


class Clinician(ClinicianBase):
    id: int
    email: str
    full_name: str
    dob: date
    specialization: str
    license_number: str

    class Config:
        from_attributes = True


class ClinicianSuperuser(ClinicianBase):
    id: int
    email: str
    full_name: str
    dob: date
    specialization: str
    license_number: str

    class Config:
        from_attributes = True


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int
    is_active: bool
    is_clinician: bool

    class ConfigDict:
        from_attributes = True


# Properties to return to client
class User(UserInDBBase):
    pass


# Properties properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
    is_admin: bool = False


# Appointment schemas
class AppointmentBase(BaseModel):
    start_time: datetime
    end_time: datetime
    description: Optional[str] = None
    notes: Optional[str] = None
    user_id: int


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(AppointmentBase):
    pass


class Appointment(AppointmentBase):
    id: int
    user_id: int

    class ConfigDict:
        from_attributes = True


# Billing schemas
class BillingBase(BaseModel):
    amount: float
    date: datetime
    paid: bool = False


class BillingCreate(BillingBase):
    user_id: int


class BillingUpdate(BillingBase):
    pass


class Billing(BillingBase):
    id: int
    user_id: int

    class ConfigDict:
        from_attributes = True


# MedicalRecord schemas
class MedicalRecordBase(BaseModel):
    record: str
    diagnosis: Optional[str] = None
    treatment_history: Optional[List[str]] = None
    medications: Optional[List[str]] = None


class MedicalRecordCreate(MedicalRecordBase):
    pass


class MedicalRecord(MedicalRecordBase):
    id: int
    user_id: int

    class ConfigDict:
        from_attributes = True


# Note schemas
class NoteBase(BaseModel):
    content: str
    created_at: datetime


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    author_id: int

    class ConfigDict:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
