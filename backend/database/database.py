import os
from datetime import date, datetime
from typing import Dict, List, Union
from beanie import PydanticObjectId
from models.kunjungan import KunjunganWithPoli
from models.diagnosa import Diagnosa
from models.kunjungan import Kunjungan
from models.pendaftaran import Antrian
from models.pendaftaran import Parameter
from models.pendaftaran import Pendaftaran
from models.pasien import Pasien
from models.poli import Poli
from models.admin import Admin
from models.student import Student

admin_collection = Admin
student_collection = Student
poli_collection = Poli
pasien_collection = Pasien
pendaftaran_collection = Pendaftaran
kunjungan_collection = Kunjungan
diagnosa_collection = Diagnosa


# ADMIN
async def add_admin(new_admin: Admin) -> Admin:
    admin = await new_admin.create()
    return admin


async def retrieve_students() -> List[Student]:
    students = await student_collection.all().to_list()
    return students


async def add_student(new_student: Student) -> Student:
    student = await new_student.create()
    return student


async def retrieve_student(id: PydanticObjectId) -> Student:
    student = await student_collection.get(id)
    if student:
        return student


async def delete_student(id: PydanticObjectId) -> bool:
    student = await student_collection.get(id)
    if student:
        await student.delete()
        return True


async def update_student_data(id: PydanticObjectId, data: dict) -> Union[bool, Student]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in des_body.items()
    }}
    student = await student_collection.get(id)
    if student:
        await student.update(update_query)
        return student
    return False


async def retrieve_polis() -> List[Poli]:
    ret = await poli_collection.all().to_list()
    return ret


async def retrieve_one_poli() -> Poli:
    ret = await poli_collection.find().first_or_none()
    return ret


async def add_poli(new_poli: Poli) -> Poli:
    poli = await new_poli.create()
    return poli


async def retrieve_poli(id: PydanticObjectId) -> Poli:
    poli = await poli_collection.get(id)
    if poli:
        return poli


async def delete_poli(id: PydanticObjectId) -> bool:
    poli = await poli_collection.get(id)
    if poli:
        await poli.delete()
        return True


async def update_poli_data(id: PydanticObjectId, data: dict) -> Union[bool, Poli]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in des_body.items()
    }}
    poli = await poli_collection.get(id)
    if poli:
        await poli.update(update_query)
        return poli
    return False

# PASIEN


async def retrieve_pasiens() -> List[Pasien]:
    pasien = await pasien_collection.all().to_list()
    return pasien


async def retrieve_nomor_pasien() -> str:
    pasien = await pasien_collection.all().count()+1
    return pasien


async def add_pasien(new_pasien: Pasien) -> Pasien:
    pasien = await new_pasien.create()
    return pasien


async def retrieve_pasien(id: PydanticObjectId) -> Pasien:
    pasien = await pasien_collection.get(id)
    if pasien:
        return pasien


async def cek_pasien(nomor: str) -> Pasien:
    data = await pasien_collection.find_one(Pasien.nomor == nomor)
    return data


async def delete_pasien(id: PydanticObjectId) -> bool:
    pasien = await pasien_collection.get(id)
    if pasien:
        await pasien.delete()
        return True


async def update_pasien_data(id: PydanticObjectId, data: dict) -> Union[bool, Pasien]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in des_body.items()
    }}
    print(update_query)
    pasien = await pasien_collection.get(id)
    if pasien:
        await pasien.update(update_query)
        return pasien
    return False

# KUNJUNGAN


async def retrieve_list_kunjungan() -> List[Kunjungan]:
    data = await kunjungan_collection.find(Kunjungan.status == 'Waiting', Kunjungan.tanggal == date.today().strftime("%Y-%m-%d")).to_list()
    return data


async def retrieve_kunjungan_poli(params: Parameter) -> List[Kunjungan]:
    ret = await kunjungan_collection.find(Kunjungan.status == 'Waiting', Kunjungan.poli_id == params.poli, Kunjungan.tanggal == date.today().strftime("%Y-%m-%d")).to_list()
    return ret


async def add_kunjungan(data: Kunjungan) -> Kunjungan:
    new = await data.create()
    return new


async def retrieve_kunjungan(id: PydanticObjectId) -> Kunjungan:
    data = await kunjungan_collection.get(id)
    if data:
        return data


async def retrieve_nomor_antrian(params: Parameter) -> Kunjungan:
    data = await kunjungan_collection.find(Kunjungan.tanggal == params.tanggal, Kunjungan.poli == params.poli).count()+1
    return data


async def delete_kunjungan(id: PydanticObjectId) -> bool:
    data = await kunjungan_collection.get(id)
    if data:
        await data.delete()
        return True


async def update_kunjungan_data(id: PydanticObjectId, data: dict) -> Union[bool, Kunjungan]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in des_body.items()
    }}
    data = await kunjungan_collection.get(id)
    if data:
        await data.update(update_query)
        return data
    return False

# PENDAFTARAN


async def retrieve_pendaftaran() -> List[Pendaftaran]:
    pendaftaran = await pendaftaran_collection.all().to_list()
    return pendaftaran


async def add_pendaftaran(new_pendaftaran: Pendaftaran) -> Pendaftaran:
    pendaftaran = await new_pendaftaran.create()
    return pendaftaran


async def retrieve_pendaftaran(id: PydanticObjectId) -> Pendaftaran:
    ret = await pendaftaran_collection.get(id)
    if ret:
        return ret


async def retrieve_nomor_antrian(params: Parameter) -> Kunjungan:
    ret = await kunjungan_collection.find(Kunjungan.tanggal == params.tanggal, Kunjungan.poli_id == params.poli).count()
    return ret+1


async def retrieve_list_antrian() -> List[Poli]:
    # cek antrian tiap poli
    data = await poli_collection.all().to_list()
    # for poli in polis:
    #     antri = await pendaftaran_collection.find(Pendaftaran.poli==poli["name"]).sort("-nomor")
    #     data.append({"Poli": poli["name"], "Antrian": antri})

    return data


async def delete_pendaftaran(id: PydanticObjectId) -> bool:
    pendaftaran = await pendaftaran_collection.get(id)
    if pendaftaran:
        await pendaftaran.delete()
        return True


async def update_pendaftaran_data(id: PydanticObjectId, data: dict) -> Union[bool, Pendaftaran]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in des_body.items()
    }}
    pendaftaran = await pendaftaran_collection.get(id)
    if pendaftaran:
        await pendaftaran.update(update_query)
        return pendaftaran
    return False


# DIAGNOSA
async def retrieve_list_diagnosa() -> List[Diagnosa]:
    ret = await diagnosa_collection.all().to_list()
    return ret


async def add_diagnosa(new: Diagnosa) -> Diagnosa:
    ret = await new.create()
    return ret


async def retrieve_diagnosa(id: PydanticObjectId) -> Diagnosa:
    ret = await diagnosa_collection.get(id)
    if ret:
        return ret


async def delete_diagnosa(id: PydanticObjectId) -> bool:
    ret = await diagnosa_collection.get(id)
    if ret:
        await ret.delete()
        return True


async def update_diagnosa_data(id: PydanticObjectId, data: dict) -> Union[bool, Diagnosa]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in des_body.items()
    }}
    ret = await diagnosa_collection.get(id)
    if ret:
        await ret.update(update_query)
        return ret
    return False
