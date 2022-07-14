from typing import List, Union

from beanie import PydanticObjectId

from models.poli import Poli
from models.admin import Admin
from models.student import Student

admin_collection = Admin
student_collection = Student
poli_collection = Poli


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
    polis = await poli_collection.all().to_list()
    return polis


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
