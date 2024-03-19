from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None
    role: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    role: Optional[str] = None


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int
    is_active: bool
    is_clinician: bool

    class Config:
        orm_mode = True


# Properties to return to client
class User(UserInDBBase):
    pass


# Properties properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str


# Appointment schemas
class AppointmentBase(BaseModel):
    start_time: datetime
    end_time: datetime
    description: Optional[str] = None
    notes: Optional[str] = None
    user_id: int


class AppointmentCreate(AppointmentBase):
    pass


class Appointment(AppointmentBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


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

    class Config:
        orm_mode = True


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

    class Config:
        orm_mode = True


# Note schemas
class NoteBase(BaseModel):
    content: str
    created_at: datetime


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True
