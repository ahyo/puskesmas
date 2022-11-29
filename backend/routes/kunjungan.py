from dataclasses import dataclass
from datetime import datetime
from fastapi import APIRouter, Body, Request
from requests import request

from database.database import *
from models.kunjungan import *

router = APIRouter()


@router.get("/", response_description="Data retrieved", response_model=Response)
async def get_kunjungan():
    data = await retrieve_list_kunjungan()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Kunjungan data retrieved successfully",
        "data": data
    }


@router.get("/list_poli", response_description="Data retrieved", response_model=Response)
async def get_poli_kunjungan():
    data = await retrieve_polis()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Kunjungan data retrieved successfully",
        "data": data
    }    


@router.get("/nomor_antrian", response_description="Data retrieved", response_model=Response)
async def get_kunjungan_antrian(params: Parameter):
    data = await retrieve_nomor_antrian(params)
    poli = await retrieve_poli(params.poli)
    if data:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Nomor antrian",
            "data": {
                'nomor':poli.alias+'-'+str(data).zfill(3),
                'alias':poli.alias,
                'params':params
            }
        }
    return {
        "status_code": 200,
            "response_type": "success",
            "description": "Nomor antrian ",
            "data": {
                'nomor':poli.alias+'-'+"-001",
                'alias':poli.alias
            }
    }  

@router.get("/poli/", response_description="Data retrieved", response_model=Response)
async def get_kunjungan_poli_data(params: Parameter):
    data = await retrieve_kunjungan_poli(params)
    if data:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Kunjungan Per Poli",
            "data": data
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Tidak ada kunjungan poli ",
    } 

@router.get("/{id}", response_description="Data retrieved", response_model=Response)
async def get_kunjungan_data(id: PydanticObjectId):
    data = await retrieve_kunjungan(id)
    if data:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Daftar Kunjungan",
            "data": data
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Tidak ada kunjungan",
    }  



@router.post("/", response_description="Data added into the database", response_model=Response)
async def add_kunjungan_data(params: Kunjungan = Body(...)):
    data = await add_kunjungan(params)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Kunjungan berhasil ditambahkan",
        "data": data
    }


@router.delete("/{id}", response_description="Data deleted from the database")
async def delete_kunjungan_data(id: PydanticObjectId):
    data = await delete_kunjungan(id)
    if data:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Data with ID: {} removed".format(id),
            "data": data
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Data with id {0} doesn't exist".format(id),
        "data": False
    }


@router.put("/{id}", response_model=Response)
async def update_kunjungan(id: PydanticObjectId, req: UpdateKunjunganModel = Body(...)):
    data = await update_kunjungan_data(id, req.dict())
    if data:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Data with ID: {} updated".format(id),
            "data": data
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "An error occurred. poli with ID: {} not found".format(id),
        "data": False
    }
