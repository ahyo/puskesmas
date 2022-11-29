from typing import Optional, Any

from beanie import Document
from pydantic import BaseModel, EmailStr


class Poli(Document):
    nama: str  
    alias: str
    antrian: str = None

    class Config:
        schema_extra = {
            "example": {
                "nama": "Poli Anak",
                "alias": "A",
                "antrian": "0001"
            }
        }


class UpdatePoliModel(BaseModel):
    nama: Optional[str]
    alias: Optional[str]
    antrian: Optional[str]
    
    class Config:
        schema_extra = {
            "example": {
                "nama": "Poli Anak",
                "alias": "A",
                "antrian": "0001"
            }
        }


class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

    class Collection:
        name = "poli"

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": "Sample data"
            }
        }
