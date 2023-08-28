from pydantic import BaseModel, EmailStr, Field


class UserInsert(BaseModel):
    first_name: str = Field(..., max_length=30, min_length=1)
    last_name: str = Field(..., max_length=30, min_length=1)
    email: EmailStr
    password: str
    country: str
