import asyncio
import json
from fastapi import FastAPI, Depends, WebSocket

from auth.jwt_bearer import JWTBearer
from database.database import retrieve_polis
from routes.poli import get_polis
from config.config import initiate_database
from routes.admin import router as AdminRouter
from routes.pendaftaran import router as PendaftaranRouter
from routes.poli import router as PoliRouter
from routes.pasien import router as PasienRouter
from routes.kunjungan import router as KunjunganRouter
from routes.diagnosa import router as DiagnosaRouter
from routes.public import router as PublicRouter
import random

app = FastAPI()

token_listener = JWTBearer()


@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Puskesmas."}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(1)
        payload = await retrieve_polis()
        ret = []
        for val in payload:
            ret.append({
                '_id': str(val.id),
                'nama': val.nama,
                'antrian': val.antrian})
        # print(ret)
        await websocket.send_json(ret)

app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin")
app.include_router(PublicRouter, tags=["Public"], prefix="/public")
app.include_router(PoliRouter, tags=["Poli"], prefix="/poli")
#    , dependencies=[Depends(token_listener)])
app.include_router(PasienRouter, tags=[
                   "Pasien"], prefix="/pasien", dependencies=[Depends(token_listener)])
app.include_router(PendaftaranRouter, tags=[
                   "Pendaftaran"], prefix="/pendaftaran", dependencies=[Depends(token_listener)])
app.include_router(KunjunganRouter, tags=["Kunjungan"], prefix="/kunjungan")
app.include_router(DiagnosaRouter, tags=[
                   "Diagnosa"], prefix="/diagnosa", dependencies=[Depends(token_listener)])
