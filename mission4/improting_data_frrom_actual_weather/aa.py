import requests, pandas as pd

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 36.433,
    "longitude": 10.083,
    "hourly": "temperature_2m,precipitation,wind_speed_10m,relative_humidity_2m",
    "forecast_days": 2,
    "timezone": "auto"
}

r = requests.get(url, params=params)
r.raise_for_status()
data = r.json()["hourly"]

df = pd.DataFrame(data)
df.rename(columns={
    "temperature_2m": "temperature",
    "precipitation": "rain",
    "wind_speed_10m": "wind_speed",
    "relative_humidity_2m": "humidity"
}, inplace=True)

df.to_csv("zaghouan_weather.csv", index=False)
print("✅ Saved zaghouan_weather.csv with", len(df), "rows")
