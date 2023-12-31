from typing import Optional
from pydantic import BaseModel, EmailStr, Field, HttpUrl, PastDate


class PeopleSchema(BaseModel):
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
