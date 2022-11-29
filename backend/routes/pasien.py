from fastapi import APIRouter, Body

from database.database import *
from models.pasien import *

router = APIRouter()


@router.get("/", response_description="Pasien retrieved", response_model=Response)
async def get_pasien():
    pasien = await retrieve_pasiens()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Poli data retrieved successfully",
        "data": pasien
    }


@router.get("/nomor", response_description="Nomor Pasien", response_model=Response)
async def get_nomor_pasien():
    data = await retrieve_nomor_pasien()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Nomor pasien",
        "data": str(data).zfill(5)
    }


@router.get("/{id}", response_description="Pasien data retrieved", response_model=Response)
async def get_pasien_data(id: PydanticObjectId):
    pasien = await retrieve_pasien(id)
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


@router.post("/", response_description="Pasien data added into the database", response_model=Response)
async def add_pasien_data(pasien: Pasien = Body(...)):
    new_pasien = await add_pasien(pasien)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Pasien created successfully",
        "data": new_pasien
    }


@router.post("/check-nomor", response_description="Cek nomor pasien", response_model=Response)
async def cek_pasien_data(params: ParamsNomor):
    data = await cek_pasien(params)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Pasien created successfully",
        "data": data
    }


@router.delete("/{id}", response_description="Pasien data deleted from the database")
async def delete_pasien_data(id: PydanticObjectId):
    deleted_pasien = await delete_pasien(id)
    if deleted_pasien:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "poli with ID: {} removed".format(id),
            "data": deleted_pasien
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "poli with id {0} doesn't exist".format(id),
        "data": False
    }


@router.put("/{id}", response_model=Response)
async def update_pasien(id: PydanticObjectId, req: UpdatePasienModel = Body(...)):
    updated_pasien = await update_pasien_data(id, req.dict())
    if updated_pasien:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Pasien with ID: {} updated".format(id),
            "data": updated_pasien
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "An error occurred. Pasien with ID: {} not found".format(id),
        "data": False
    }
