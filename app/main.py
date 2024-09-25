from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.api.router import router as api_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis = aioredis.from_url("redis://redis")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(title='weather-api', lifespan=lifespan)
app.include_router(api_router)


@app.get('/')
async def index():
    return {'msg': 'ok'}
