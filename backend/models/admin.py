from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr


class Admin(Document):
    fullname: str
    email: EmailStr
    password: str

    class Collection:
        name = "admin"

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Ahyo Haryanto",
                "email": "ahyo.haryanto@gmail.com",
                "password": "ayocool"
            }
        }


class AdminSignIn(HTTPBasicCredentials):
    class Config:
        schema_extra = {
            "example": {
                "username": "ahyo.haryanto@gmail.com",
                "password": "ayocool"
            }
        }


class AdminData(BaseModel):
    fullname: str
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Ahyo Haryanto",
                "email": "ahyo.haryanto@gmail.com",
            }
        }
