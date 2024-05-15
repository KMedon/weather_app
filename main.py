from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests
from utils import calculate_energy

app = FastAPI()


class WeatherData(BaseModel):
    date: str
    weather_code: int
    min_temp: float
    max_temp: float
    energy: float


@app.get("/weather", response_model=List[WeatherData])
async def get_weather(lat: float, lon: float):
    try:
        response = requests.get(
            f"https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": "temperature_2m_min,temperature_2m_max,shortwave_radiation_sum",
                "timezone": "auto"
            }
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    weather_list = []
    for i in range(7):
        day_data = data['daily'][i]
        energy = calculate_energy(day_data['shortwave_radiation_sum'])
        weather = WeatherData(
            date=day_data['time'],
            weather_code=day_data['weathercode'],
            min_temp=day_data['temperature_2m_min'],
            max_temp=day_data['temperature_2m_max'],
            energy=energy
        )
        weather_list.append(weather)

    return weather_list
@app.get("/sample_weather", response_model=List[WeatherData])
async def get_sample_weather():
    sample_data = [
        {
            "date": "2023-05-01",
            "weather_code": 1,
            "min_temp": 15.0,
            "max_temp": 25.0,
            "energy": 5.0
        },
        {
            "date": "2023-05-02",
            "weather_code": 2,
            "min_temp": 14.0,
            "max_temp": 24.0,
            "energy": 4.8
        },
        {
            "date": "2023-05-03",
            "weather_code": 3,
            "min_temp": 13.0,
            "max_temp": 23.0,
            "energy": 4.5
        },
        {
            "date": "2023-05-04",
            "weather_code": 4,
            "min_temp": 12.0,
            "max_temp": 22.0,
            "energy": 4.2
        },
        {
            "date": "2023-05-05",
            "weather_code": 5,
            "min_temp": 11.0,
            "max_temp": 21.0,
            "energy": 3.9
        },
        {
            "date": "2023-05-06",
            "weather_code": 6,
            "min_temp": 10.0,
            "max_temp": 20.0,
            "energy": 3.7
        },
        {
            "date": "2023-05-07",
            "weather_code": 7,
            "min_temp": 9.0,
            "max_temp": 19.0,
            "energy": 3.5
        }
    ]
    return sample_data