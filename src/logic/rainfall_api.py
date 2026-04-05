import requests
import pandas as pd
from datetime import datetime, timedelta

DEHRADUN_LAT = 30.3165
DEHRADUN_LON = 78.0469


def get_current_rainfall():
    """Fetch real rainfall data from Open-Meteo API - no API key needed"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": DEHRADUN_LAT,
        "longitude": DEHRADUN_LON,
        "hourly": "precipitation,rain",
        "daily": "precipitation_sum,rain_sum,precipitation_hours",
        "timezone": "Asia/Kolkata",
        "past_days": 7,
        "forecast_days": 3
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        hourly_times = data["hourly"]["time"]
        hourly_precip = data["hourly"]["precipitation"]

        now = datetime.now()
        current_hour = now.strftime("%Y-%m-%dT%H:00")
        last_24h_start = (now - timedelta(hours=24)).strftime("%Y-%m-%dT%H:00")

        recent_rainfall = []
        for t, p in zip(hourly_times, hourly_precip):
            if last_24h_start <= t <= current_hour:
                recent_rainfall.append(p or 0)

        total_24h = sum(recent_rainfall)
        current_intensity = recent_rainfall[-1] if recent_rainfall else 0

        daily_dates = data["daily"]["time"]
        daily_rain = data["daily"]["precipitation_sum"]

        daily_df = pd.DataFrame({
            "date": daily_dates,
            "rainfall_mm": [r or 0 for r in daily_rain]
        })

        return {
            "current_intensity_mm_hr": round(current_intensity, 2),
            "total_24h_mm": round(total_24h, 2),
            "daily_df": daily_df,
            "status": "success",
            "last_updated": now.strftime("%Y-%m-%d %H:%M:%S")
        }

    except Exception as e:
        return {
            "current_intensity_mm_hr": 0,
            "total_24h_mm": 0,
            "daily_df": pd.DataFrame(),
            "status": f"error: {str(e)}",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


def classify_rainfall(mm_per_hr):
    """IMD rainfall classification"""
    if mm_per_hr < 2.5:
        return "Light Rain", "#00FF00"
    elif mm_per_hr < 7.5:
        return "Moderate Rain", "#FFFF00"
    elif mm_per_hr < 35.5:
        return "Heavy Rain", "#FFA500"
    elif mm_per_hr < 64.5:
        return "Very Heavy Rain", "#FF4500"
    else:
        return "Extremely Heavy Rain", "#FF0000"