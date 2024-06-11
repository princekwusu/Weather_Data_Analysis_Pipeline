import requests
from datetime import datetime
import pandas as pd
import boto3
from datetime import timezone
import io
import os
from dotenv import load_dotenv


load_dotenv()



# OpenWeather API details
API_KEY = os.getenv("API_KEY")  # Replace with your actual API key
CITY = 'London'  # City for which the forecast is needed
DAYS = 5  # Number of days for the forecast (5 days)
BASE_URL = 'https://api.openweathermap.org/data/2.5/forecast'
CURRENT_WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'

# AWS S3 details
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.getenv("s3_bucket")
FOLDER_NAME = os.getenv("s3_folder")  # Folder to store the data in S3

def fetch_weather_data(city, api_key, days):
    params = {
        'q': city,
        'cnt': days * 8,  # 8 forecasts per day (3-hour intervals)
        'appid': api_key,
        'units': 'metric'  # Get temperature in Celsius
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

def fetch_current_weather_data(city, api_key):
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # Get temperature in Celsius
    }
    response = requests.get(CURRENT_WEATHER_URL, params=params)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

def parse_weather_data(data):
    forecast_list = data['list']
    forecast_data = []

    for forecast in forecast_list:
        dt = datetime.utcfromtimestamp(forecast['dt']).replace(tzinfo=timezone.utc)
        # date_str = dt.strftime('%Y-%m-%d')
        # time_str = dt.strftime('%H:%M:%S')
        day_name = dt.strftime('%A')
        month_name = dt.strftime('%B')
        
        temp = forecast['main']['temp']
        feels_like = forecast['main']['feels_like']
        weather_description = forecast['weather'][0]['description']
        humidity = forecast['main']['humidity']
        wind_speed = forecast['wind']['speed']
        wind_direction = forecast['wind'].get('deg', None)
        cloudiness = forecast['clouds']['all']
        precipitation = forecast.get('rain', {}).get('3h', 0) + forecast.get('snow', {}).get('3h', 0)
        pressure = forecast['main']['pressure']

        forecast_data.append({
            'DATETIME': dt,
            # 'TIME': time_str,
            'DAY_NAME': day_name,
            'MONTH_NAME': month_name,
            'TEMP (°C)': temp,
            'FEELS_LIKE (°C)': feels_like,
            'DESCRIPTION': weather_description,
            'PRESSURE (hPa)': pressure,
            'HUMIDITY (%)': humidity,
            'WINDSPEED (m/s)': wind_speed,
            'WIND_DIRECTION (°)': wind_direction,
            'CLOUDINESS (%)': cloudiness,
            'PRECIPITATION (mm)': precipitation
        })

    return forecast_data

def save_to_s3(csv_buffer, filename):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3.put_object(Bucket=BUCKET_NAME, Key=f"{FOLDER_NAME}/{filename}", Body=csv_buffer.getvalue())

def main():
    weather_data = fetch_weather_data(CITY, API_KEY, DAYS)
    current_weather_data = fetch_current_weather_data(CITY, API_KEY)
    forecast_data = parse_weather_data(weather_data)
    
    # Convert to DataFrame
    df = pd.DataFrame(forecast_data)
    

# Convert DATE and TIME columns to appropriate types
    # df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%m-%d').dt.date
    # df['TIME'] = pd.to_datetime(df['TIME'], format='%H:%M:%S').dt.time

    
    # Convert to CSV and upload to S3
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    
    # Format the datetime string for filename
    datetime_str = datetime.now().strftime('%d_%m_%Y %H:%M:%S')
    filename = f"{datetime_str}_forecast.csv"
    save_to_s3(csv_buffer, filename)

if __name__ == '__main__':
    main()
