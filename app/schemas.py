from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models import UserRole, TransactionType


# Auth 

class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    email: str
    password: str


# Users 

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole = UserRole.viewer


class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Financial Records 

class RecordCreate(BaseModel):
    amount: float
    type: TransactionType
    category: str
    date: datetime
    notes: Optional[str] = None


class RecordUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[TransactionType] = None
    category: Optional[str] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None


class RecordOut(BaseModel):
    id: int
    amount: float
    type: TransactionType
    category: str
    date: datetime
    notes: Optional[str]
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True