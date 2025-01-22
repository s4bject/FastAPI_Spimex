import asyncio
from datetime import datetime, time, timedelta
import logging
from fastapi import FastAPI
from api.routes import router
import uvicorn

from database.redis_client import redis_client as redis, init_redis, close_redis, get_redis_client

logging.basicConfig(level=logging.INFO)
app = FastAPI()
app.include_router(router)


async def clear_cache():
    while True:
        now = datetime.now()
        reset_time = datetime.combine(now.date(), time(14, 11))
        if now > reset_time:
            reset_time += timedelta(days=1)
        await asyncio.sleep((reset_time - now).total_seconds())

        redis = get_redis_client()
        await redis.flushdb()
        print("Кэш очищен в 14:11")


@app.on_event("startup")
async def startup_event():
    await init_redis()
    asyncio.create_task(clear_cache())


@app.on_event("shutdown")
async def shutdown_event():
    await close_redis()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
