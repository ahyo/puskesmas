from dataclasses import dataclass
from datetime import datetime
from fastapi import APIRouter, Body, Depends, File, Form, Request, UploadFile
from typing import List
from database.database import *
from models.diagnosa import *
from ml.klasifikasi import validate_file

router = APIRouter()


@router.get("/", response_description="Data retrieved", response_model=Response)
async def get_diagnosa():
    data = await retrieve_list_diagnosa()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Kunjungan data retrieved successfully",
        "data": data
    }


@router.get("/{id}", response_description="Data retrieved", response_model=Response)
async def get_diagnosa_data(id: PydanticObjectId):
    data = await retrieve_diagnosa(id)
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
async def add_diagnosa_data(params: Diagnosa = Body(...)):
    data = await add_diagnosa(params)
    # print(data)
    # with open("/app/files/diagnosa.txt", "a") as file_object:
    #     # Append 'hello' at the end of file
    #     file_object.write("hello")
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Kunjungan berhasih disimpan",
        "data": data
    }


@router.post("/upload", response_description="Upload diagnosa", response_model=Response)
async def add_diagnosa_upload(rekaman: List[UploadFile] = File()):

    for rek in rekaman:
        file_upload = os.getcwd()+"/files/"+rek.filename
        with open(file_upload, "wb") as upl:
            upl.write(rek.file.read())

    # file_paru = os.getcwd()+"/files/"+suara_paru.filename
    # with open(file_paru, "wb") as paru:
    #     paru.write(suara_paru.file.read())
    # validate file pertama

    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Upload data berhasil",
        "data": "Success"
    }


@router.post("/klasifikasi", response_description="Upload diagnosa", response_model=Response)
async def add_diagnosa_upload(rekaman: List[UploadFile] = File()):

    for rek in rekaman:
        file_upload = os.getcwd()+"/files/"+rek.filename
        with open(file_upload, "wb") as upl:
            upl.write(rek.file.read())
    # time.sleep(3)
    # file0 = file_upload
    # proc = subprocess.Popen(['python3', os.getcwd()+'/klasifikasi.py',  '-f '+file0],
    #                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # result = proc.communicate()[0]
    result = validate_file(file_upload)

    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Upload data berhasil",
        "data": result
    }


@router.delete("/{id}", response_description="Data deleted from the database")
async def delete_diagnosa_data(id: PydanticObjectId):
    data = await delete_diagnosa(id)
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
async def update_diagnosa(id: PydanticObjectId, req: UpdateDiagnosaModel = Body(...)):
    data = await update_diagnosa_data(id, req.dict())
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
