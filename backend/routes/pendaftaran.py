from dataclasses import dataclass
from datetime import datetime
from fastapi import APIRouter, Body, Request
from requests import request

from database.database import *
from models.pendaftaran import *

router = APIRouter()


@router.get("/", response_description="Data retrieved", response_model=Response)
async def get_pendaftaran():
    data = await retrieve_pendaftaran()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Pendafrtaran data retrieved successfully",
        "data": data
    }

@router.get("/list_antrian", response_description="Data retrieved", response_model=Response)
async def get_list_antrian():
    data = await retrieve_list_antrian()
    if data:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Pasien data retrieved successfully",
            "data": data
        }
    return {
        "status_code": 200,
            "response_type": "success",
            "description": "Pasien data retrieved successfully",
            "data": "Belum ada antrian"
    }  

@router.get("/tambah_antrian", response_description="Data retrieved", response_model=Response)
async def get_pendaftaran_antrian(params: Parameter):
    data = await retrieve_nomor_antrian(params)
    if data:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Pasien data retrieved successfully",
            "data": params.poli+"-"+str(data).zfill(4)
        }
    return {
        "status_code": 200,
            "response_type": "success",
            "description": "Pasien data retrieved successfully",
            "data": params.poli+"-0001"
    }  

@router.get("/{id}", response_description="Data retrieved", response_model=Response)
async def get_pendaftaran_data(id: PydanticObjectId):
    data = await retrieve_pendaftaran(id)
    if data:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Pasien data retrieved successfully",
            "data": data
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Pasien doesn't exist",
    }  


@router.post("/", response_description="Data added into the database", response_model=Response)
async def add_pendaftaran_data(pendaftaran: Pendaftaran = Body(...)):
    data = await add_pendaftaran(pendaftaran)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Pasien created successfully",
        "data": data
    }


@router.delete("/{id}", response_description="Data deleted from the database")
async def delete_pendaftaran_data(id: PydanticObjectId):
    data = await delete_pendaftaran(id)
    if data:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "poli with ID: {} removed".format(id),
            "data": data
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "poli with id {0} doesn't exist".format(id),
        "data": False
    }


@router.put("{id}", response_model=Response)
async def update_pendaftaran(id: PydanticObjectId, req: UpdatePendaftaranModel = Body(...)):
    data = await update_pendaftaran_data(id, req.dict())
    if data:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "poli with ID: {} updated".format(id),
            "data": data
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "An error occurred. poli with ID: {} not found".format(id),
        "data": False
    }
