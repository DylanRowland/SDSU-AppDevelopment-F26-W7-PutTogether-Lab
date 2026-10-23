"""Pydantic models for validating API input and output."""

# Pydantic validates incoming JSON before route logic runs.
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    # The API accepts a plain password temporarily so the service can hash it.
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    # The update request uses the same editable fields as creation.
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    # These are the only fields returned to the browser.
    user_id: int
    username: str
    email: EmailStr

    # Allow Pydantic to read values from a SQLAlchemy User object.
    model_config = {"from_attributes": True}
