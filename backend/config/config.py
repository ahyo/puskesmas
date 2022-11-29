from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings
from models.pendaftaran import Pendaftaran
from models.pasien import Pasien
from models.poli import Poli
from models.admin import Admin
from models.kunjungan import Kunjungan
from models.diagnosa import Diagnosa


class Settings(BaseSettings):
    # database configurations
    DATABASE_URL: Optional[str] = "mongodb://puskesmas:puskesmba@mongodb:27017/puskesmas"

    # JWT
    secret_key: str
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"
        orm_mode = True


async def initiate_database():
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(database=client.get_default_database(),
                      document_models=[Admin,  Poli, Pasien, Pendaftaran, Kunjungan, Diagnosa])
