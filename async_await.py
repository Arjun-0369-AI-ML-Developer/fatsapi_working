import asyncio
import time
from fastapi import FastAPI
app=FastAPI()


@app.get("/")
async def task():
    await asyncio.sleep(3)
    print("-=-=- Arjun -=--=-")
    return {
        "message":"Async API"
    }
