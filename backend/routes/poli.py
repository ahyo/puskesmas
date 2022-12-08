from fastapi import APIRouter, Body

from database.database import *
from models.poli import *

router = APIRouter()


@router.get("/", response_description="Poli retrieved", response_model=Response)
async def get_polis():
    polis = await retrieve_polis()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Poli data retrieved successfully",
        "data": polis
    }


@router.get("/first", response_description="Poli retrieved", response_model=Response)
async def get_first_poli():
    poli = await retrieve_one_poli()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Poli data retrieved successfully",
        "data": poli
    }


@router.get("/{id}", response_description="Poli data retrieved", response_model=Response)
async def get_poli_data(id: PydanticObjectId):
    poli = await retrieve_poli(id)
    if poli:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Poli data retrieved successfully",
            "data": poli
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Poli doesn't exist",
    }


@router.post("/", response_description="Poli data added into the database", response_model=Response)
async def add_poli_data(poli: Poli = Body(...)):
    new_poli = await add_poli(poli)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Poli created successfully",
        "data": new_poli
    }


@router.delete("/{id}", response_description="poli data deleted from the database")
async def delete_poli_data(id: PydanticObjectId):
    deleted_poli = await delete_poli(id)
    if deleted_poli:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "poli with ID: {} removed".format(id),
            "data": deleted_poli
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "poli with id {0} doesn't exist".format(id),
        "data": False
    }


@router.put("/{id}", response_model=Response)
async def update_poli(id: PydanticObjectId, req: UpdatePoliModel = Body(...)):
    updated_poli = await update_poli_data(id, req.dict())
    if updated_poli:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "poli with ID: {} updated".format(id),
            "data": updated_poli
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "An error occurred. poli with ID: {} not found".format(id),
        "data": False
    }
