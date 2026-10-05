import json
import urllib.request

# 1. Récupérer 20 relevés horaires de température (Paris)
url = ("https://api.open-meteo.com/v1/forecast"
       "?latitude=48.85&longitude=2.35&hourly=temperature_2m&forecast_hours=20")
with urllib.request.urlopen(url) as r:
    hourly = json.load(r)["hourly"]

# 2. Les envoyer au node 1 (qui les réplique tout seul)
for t, temp in zip(hourly["time"], hourly["temperature_2m"]):
    body = json.dumps({"key": t, "value": f"{temp} °C"}).encode()
    req = urllib.request.Request(
        "http://localhost:8080/data",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    print(urllib.request.urlopen(req).read().decode())