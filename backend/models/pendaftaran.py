from datetime import datetime
from typing import Optional, Any

from beanie import Document
from pydantic import BaseModel, EmailStr


class Pendaftaran(Document):
    nomor: str
    nama: str
    alamat: str
    poli: str
    status: str = "Waiting"
    tanggal: str = datetime.now().strftime("%Y-%m-%d")
    jam: str = datetime.now().strftime("%H:%M:%S")
    pasien_id: str = "-"


    class Config:
        schema_extra = {
            "example": {
                "nomor": "1",
                "nama": "Ahyo",
                "alamat": "Bogor",
                "poli": "Poli Umum",
                "status": "Menunggu",
                "tanggal": "2022-07-15",
                "jam": "08:11:00"
            }
        }

class UpdatePendaftaranModel(BaseModel):
    nomor: Optional[str]
    nama: Optional[str]
    alamat: Optional[str]
    poli: Optional[str]
    status: Optional[str]
    tanggal: Optional[str]
    jam: Optional[str]
    pasien_id: Optional[str]

    class Collection:
        name = "pendaftaran"

    class Config:
        schema_extra = {
             "example": {
                "nomor": "1",
                "nama": "Ahyo",
                "alamat": "Bogor",
                "poli": "Poli Umum",
                "status": "Menunggu",
                "tanggal": "2022-07-15",
                "jam": "08:11:00"
            }
        }

class Parameter(BaseModel):
    tanggal: str
    poli: str

class Antrian(BaseModel):
    poli: str
    nomor: str    

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
