import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import httpx
from datetime import datetime, timedelta

load_dotenv()

app = FastAPI()

OPENWEATHER_API_KEY = os.getenv("Open_Weather_Map_Api_Key")

async def get_current_weather(city: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            description = data['weather'][0]['description']
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            return (
                f"Right now in {city}, it's {description} with a temperature of {temp}°C. "
                f"Humidity is {humidity}% and wind speed is {wind_speed} m/s."
            )
        else:
            return f"Sorry, I couldn't fetch the weather for {city}. Please check the city name."

async def get_forecast_weather(city: str, date_str: str):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            try:
                target_date = datetime.fromisoformat(date_str)
            except Exception:
                return "Invalid date format. Please use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS."
            forecasts = data['list']
            # Find the forecast closest to the target date
            closest = min(forecasts, key=lambda x: abs(datetime.fromtimestamp(x['dt']) - target_date))
            forecast_time = datetime.fromtimestamp(closest['dt'])
            description = closest['weather'][0]['description']
            temp = closest['main']['temp']
            humidity = closest['main']['humidity']
            wind_speed = closest['wind']['speed']
            return (
                f"The forecast for {city} on {forecast_time.strftime('%Y-%m-%d %H:%M')} is {description} "
                f"with a temperature of {temp}°C, humidity at {humidity}%, and wind speed of {wind_speed} m/s."
            )
        else:
            return f"Sorry, I couldn't fetch the forecast for {city}. Please check the city name."

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    # Extract parameters from Dialogflow's request structure
    parameters = data.get("queryResult", {}).get("parameters", {})
    city = parameters.get("city", "London")
    date_str = parameters.get("date-time") or parameters.get("date")
    if date_str:
        try:
            target_date = datetime.fromisoformat(date_str)
            now = datetime.now()
            print(f"[DEBUG] target_date: {target_date}, now: {now}")
            if now.date() <= target_date.date() <= (now + timedelta(days=5)).date():
                weather_info = await get_forecast_weather(city, date_str)
            else:
                weather_info = f"The date {target_date.date()} is out of forecast range (today to 5 days ahead). Showing current weather instead.\n" + await get_current_weather(city)
        except Exception as e:
            weather_info = f"Invalid date format or error: {str(e)}. Please use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS."
    else:
        weather_info = await get_current_weather(city)
    return JSONResponse(content={"fulfillmentText": weather_info})
