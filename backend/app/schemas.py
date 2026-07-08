"""Pydantic schemas for the MSME Decision Support API.

These schemas define request and response models for user authentication and
factory data management. They are deliberately simple for the prototype but
include field validation and example data to make the API self‑documenting.
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, validator

# ---------- User schemas ----------
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, example="factory_owner")
    email: Optional[str] = Field(None, example="owner@example.com")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, example="strongpassword")

class UserRead(UserBase):
    id: int
    is_active: bool = True

    class Config:
        orm_mode = True

# ---------- Factory data schemas ----------
class FactoryDataBase(BaseModel):
    date: date = Field(default_factory=date.today, example="2023-01-31")
    production_volume: float = Field(..., gt=0, example=1200.5)
    profit: float = Field(..., example=25000.0)
    inventory: int = Field(..., ge=0, example=350)
    utility_cost: float = Field(..., ge=0, example=1500.75)
    downtime_hours: float = Field(..., ge=0, example=2.5)

    @validator("production_volume", "profit", "utility_cost", "downtime_hours")
    def non_negative(cls, v):
        if v < 0:
            raise ValueError("must be non‑negative")
        return v

class FactoryDataCreate(FactoryDataBase):
    pass

class FactoryDataRead(FactoryDataBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
