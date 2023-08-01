from pydantic import EmailStr, PastDate
from typing import Optional, Literal

from sqlmodel import Field, SQLModel

countries = Literal["Australia", "Afghanisthan", "Bangladesh", "Bhutan", "Brazil", "Ethiopia", 
                    "France", "Germany", "India", "Italy", "Malaysia", "Maldives", "Myanmar", 
                    "Nepal", "Pakistan", "Poland", "Singapore", "South Africa", "Spain", 
                    "Sri Lanka", "Thailand", "United States", "United Kingdom"]


class People(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    country: countries
    birthday: PastDate
    label: str
    twitter: str
    instagram: str = Field(..., max_length=30)
    github: str

    class Config:
        schema_extra = {
            "examples": [
                {
                    "first_name": "string",
                    "last_name": "string",
                    "email": "user@example.com",
                    "phone": "5426565984",
                    "country":"India",
                    "birthday": "2022-07-29",
                    "label": "string",
                    "twitter": "string",
                    "instagram": "string",
                    "github": "string"
                }
            ]
        }
