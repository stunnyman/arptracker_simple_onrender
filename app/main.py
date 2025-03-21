from fastapi import FastAPI
import asyncio
from app.database.db import setup_database, close_pool
from app.services.arp_service import background_monitor
from app.api.routes import router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await setup_database()
    asyncio.create_task(background_monitor())

@app.on_event("shutdown")
async def shutdown_event():
    await close_pool()

app.include_router(router) 