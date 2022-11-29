from datetime import datetime
from typing import Optional, Any

from beanie import Document
from fastapi import File, UploadFile
from pydantic import BaseModel, EmailStr


class Diagnosa(Document):
    pasien_id: str
    poli_id: str
    kunjungan_id: str 
    tanggal: str = datetime.now().strftime("%Y-%m-%d")
    jam: str = datetime.now().strftime("%H:%M:%S")
    diagnosa: str 

    class Config:
        schema_extra = {
            "example": {
                "pasien_id": "1",
                "poli_id": "1",
                "kunjungan_id": "1",
                "tanggal": "2022-07-15",
                "jam": "08:11:00",
                "diagnosa": "test"
            }
        }

class UpdateDiagnosaModel(BaseModel):
    pasien_id: Optional[str]
    poli_id: Optional[str]
    kunjungan_id: Optional[str]
    tanggal:Optional[str]
    jam: Optional[str]
    diagnosa: Optional[str]


    class Collection:
        name = "diagnosa"

    class Config:
        schema_extra = {
             "example": {
                "pasien_id": "1",
                "poli_id": "1",
                "kunjungan_id": "1",
                "tanggal": "2022-07-15",
                "jam": "08:11:00",
                "diagnosa": "test"
            }
        }

class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": "Sample data"
            }
        }
