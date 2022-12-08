from dataclasses import dataclass
from datetime import datetime
from fastapi import APIRouter, Body, Request
from requests import request

from database.database import *
from models.poli import *

router = APIRouter()


@router.get("/antrian", response_description="Data retrieved", response_model=Response)
async def get_antrian_public():
    data = await retrieve_list_antrian()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Kunjungan data retrieved successfully",
        "data": data
    }


@router.get("/pasien/{nomor}", response_description="Pasien data retrieved", response_model=Response)
async def get_pasien_data(nomor: str):
    pasien = await cek_pasien(nomor)
    if pasien:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Pasien data retrieved successfully",
            "data": pasien
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Pasien doesn't exist",
    }
