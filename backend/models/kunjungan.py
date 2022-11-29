from datetime import datetime
from lib2to3.pgen2.token import OP
from typing import Optional, Any

from beanie import Document
from pydantic import BaseModel, EmailStr

from models.poli import Poli


class Kunjungan(Document):
    nomor: str
    no_mr: str
    nama_kk: str
    poli: str
    status: str = "Waiting"
    tanggal: str
    jam: str
    poli_id: str
    alamat: str

    class Config:
        schema_extra = {
            "example": {
                "nomor": "001",
                "no_mr": "22001",
                "nama_kk": "Pasien",
                "poli": "Umum",
                "status": "Waiting",
                "tanggal": "2022-10-01",
                "jam": "10:00:00",
                "poli_id": 1,
                "alamat": "Bogor"
            }
        }


class KunjunganWithPoli(Kunjungan):
    poli: Optional[Poli] = None


class UpdateKunjunganModel(BaseModel):
    nomor: Optional[str]
    poli: Optional[str]
    poli_id: Optional[str]
    status: Optional[str]
    tanggal: Optional[str]
    jam: Optional[str]
    no_mr: Optional[str]
    nama_kk: Optional[str]
    alamat: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "nomor": "001",
                "no_mr": "22001",
                "nama_kk": "Pasien",
                "poli": "Umum",
                "status": "Waiting",
                "tanggal": "2022-10-01",
                "jam": "10:00:00",
                "poli_id": 1,
                "alamat": "Bogor"
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
