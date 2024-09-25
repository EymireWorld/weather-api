from fastapi import APIRouter
from fastapi_cache.decorator import cache
from httpx import AsyncClient

from app.settings import API_KEY


router = APIRouter(
    prefix='/weather',
    tags=['Weather']
)


@router.get('')
@cache(expire=3600)
async def get_weather(city: str):
    async with AsyncClient() as client:
        city_request = await client.get('http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={appid}'.format(
            city=city,
            appid=API_KEY
        ))
        city_data = city_request.json()[0]
        weather_request = await client.get('https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={appid}'.format(
            lat=city_data['lat'],
            lon=city_data['lon'],
            appid=API_KEY
        ))
        weather_data = weather_request.json()

    return {
        'temperature': str(weather_data['main']['temp']) + ' °C',
        'weather_conditions': [x['main'] for x in weather_data['weather']],
        'visibility': str(round(weather_data['visibility'] / 1000, 2)) + ' km',
        'humidity': str(weather_data['main']['humidity']) + '%',
        'pressure': str(weather_data['main']['pressure']) + ' hPa',
        'wind_speed': str(weather_data['wind']['speed']) + ' m/s'
    }
