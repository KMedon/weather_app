from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests
from utils import calculate_energy
from flask import Flask, render_template, request
from fastapi.middleware.wsgi import WSGIMiddleware

# FastAPI application
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
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": "temperature_2m_min,temperature_2m_max,shortwave_radiation_sum",
                "timezone": "auto"
            }
        )
        response.raise_for_status()
        data = response.json()['daily']
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    weather_list = []
    for i in range(len(data['time'])):
        energy = calculate_energy(data['shortwave_radiation_sum'][i])
        weather = WeatherData(
            date=data['time'][i],
            weather_code=0,  # Assuming default weather code as Open-Meteo might not provide it directly
            min_temp=data['temperature_2m_min'][i],
            max_temp=data['temperature_2m_max'][i],
            energy=energy
        )
        weather_list.append(weather)

    return weather_list

# Flask application
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return render_template('index.html')

@flask_app.route('/weather', methods=['POST'])
def weather():
    lat = request.form['latitude']
    lon = request.form['longitude']
    try:
        response = requests.get(
            f"https://weather-app-1-hskc.onrender.com",  # Use the actual URL of your deployed backend service
            params={"lat": lat, "lon": lon}
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return f"Error: {e}"

    return render_template('index.html', weather_data=data)

# Mount the Flask application on the FastAPI application
app.mount("/", WSGIMiddleware(flask_app))