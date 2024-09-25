from fastapi import APIRouter

from app.api.weather.router import router as weather_router


router = APIRouter(
    prefix='/api'
)
router.include_router(weather_router)
