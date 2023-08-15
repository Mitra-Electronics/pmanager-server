from pydantic import BaseModel, EmailStr, PastDate, HttpUrl
from typing import Optional, Literal

from sqlmodel import Field, SQLModel

countries = Literal["Australia", "Afghanisthan", "Bangladesh", "Bhutan",
                    "Brazil", "Ethiopia", "France", "Germany", "India",
                    "Italy", "Malaysia", "Maldives", "Myanmar",
                    "Nepal", "Pakistan", "Poland", "Singapore",
                    "South Africa", "Spain", "Sri Lanka", "Thailand",
                    "United States", "United Kingdom"]


class People(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: Optional[EmailStr]
    phone: Optional[str] = Field(None, max_length=15, min_length=10)
    country: Optional[str] = Field(None, max_length=20)
    birthday: Optional[PastDate]
    label: Optional[str] = Field(None, max_length=40)
    twitter: Optional[str] = Field(None, max_length=15, min_length=4)
    instagram: Optional[str] = Field(None, max_length=30, min_length=1)
    github: Optional[str] = Field(None, max_length=39, min_length=1)
    img: Optional[HttpUrl]

    class Config:
        schema_extra = {
            "examples": [
                {
                    "first_name": "string",
                    "last_name": "string",
                    "email": "user@example.com",
                    "phone": "5426565984",
                    "country": "India",
                    "birthday": "2022-07-29",
                    "label": "string",
                    "twitter": "string",
                    "instagram": "string",
                    "github": "string"
                }
            ]
        }


class Login(BaseModel):
    email: EmailStr
    password: str


class User(SQLModel, table=True):
    first_name: str = Field(..., max_length=30, min_length=1)
    last_name: str = Field(..., max_length=30, min_length=1)
    email: EmailStr
    hashed_password: str
    country: str
