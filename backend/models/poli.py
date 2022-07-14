from typing import Optional, Any

from beanie import Document
from pydantic import BaseModel, EmailStr


class Poli(Document):
    name: str  

    class Config:
        schema_extra = {
            "example": {
                "name": "Poli Anak",
            }
        }


class UpdatePoliModel(BaseModel):
    name: Optional[str]

    class Collection:
        name = "poli"
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Poli Anak",
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
