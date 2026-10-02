from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict

def _pw_len(v: str) -> str:
    if len(v.encode()) > 72:
        raise ValueError("Password must be 72 bytes or fewer")
    return v

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)

    @field_validator("username")
    @classmethod
    def clean_username(cls, v): return v.strip()
    @field_validator("email")
    @classmethod
    def lower_email(cls, v): return v.strip().lower()
    _pw = field_validator("password")(_pw_len)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def lower_email(cls, v): return v.strip().lower()

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
