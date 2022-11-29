from typing import Optional, Any

from beanie import Document
from pydantic import BaseModel, EmailStr


class Pasien(Document):
    nomor: str
    no_ktp: str
    nama: str
    alamat: str
    tempat_lahir: str
    tanggal_lahir: str
    jenis_kelamin: str

    class Config:
        schema_extra = {
            "example": {
                "nomor": "P0000000001",
                "no_ktp": "3471072708810002",
                "nama": "Ahyo",
                "alamat": "Bogor",
                "tempat_lahir": "Jakarta",
                "tanggal_lahir": "2001-01-01",
                "jenis_kelamin": "Pria",
            }
        }


class UpdatePasienModel(BaseModel):
    nomor: Optional[str]
    no_ktp: Optional[str]
    nama: Optional[str]
    alamat: Optional[str]
    tempat_lahir: Optional[str]
    tanggal_lahir: Optional[str]
    jenis_kelamin: Optional[str]

    class Collection:
        name = "pasien"

    class Config:
        schema_extra = {
            "example": {
                "nomor": "P0000000001",
                "no_ktp": "3471072708810002",
                "nama": "Ahyo",
                "alamat": "Bogor",
                "tempat_lahir": "Jakarta",
                "tanggal_lahir": "2001-01-01",
                "jenis_kelamin": "Pria",
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


class ParamsNomor(BaseModel):
    nomor: str
