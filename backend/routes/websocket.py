import asyncio
from fastapi import Body, APIRouter, HTTPException
from fastapi_websocket_pubsub import PubSubEndpoint

router = APIRouter()

endpoint = PubSubEndpoint()
endpoint.register_route(router)


async def events():
    await asyncio.sleep(1)
    # Publish multiple topics (without data)
    await endpoint.publish(["guns", "germs"])
    await asyncio.sleep(1)
    # Publish single topic (without data)
    await endpoint.publish(["germs"])
    await asyncio.sleep(1)
    # Publish single topic (with data)
    await endpoint.publish(["steel"], data={"author": "Jared Diamond"})

@router.get("/trigger")
async def trigger_events():
    asyncio.create_task(events())
