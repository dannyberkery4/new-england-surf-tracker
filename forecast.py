import csv, requests
from spots import SPOTS

URL = "https://marine-api.open-meteo.com/v1/marine"
rows = []

for name, (lat, lon) in SPOTS.items():
    r = requests.get(URL, params={
        "latitude": lat, "longitude": lon,
        "daily": "wave_height_max,wave_period_max,wave_direction_dominant",
        "length_unit": "imperial", "timezone": "America/New_York",
    }).json()["daily"]
    for i, day in enumerate(r["time"]):
        rows.append([name, day, r["wave_height_max"][i],
                     r["wave_period_max"][i], r["wave_direction_dominant"][i]])

with open("forecast.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["spot", "date", "wave_height_ft", "period_s", "direction_deg"])
    w.writerows(rows)

print(f"Saved {len(rows)} rows to forecast.csv")
