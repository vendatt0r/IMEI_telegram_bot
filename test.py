import requests

IMEI_CHECK_API_URL = "https://api.imeicheck.net/v1/checks"
IMEI_CHECK_API_TOKEN = "e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b"

imei = "356454105825698"

headers = {
    "Authorization": f"Bearer {IMEI_CHECK_API_TOKEN}",
    "Accept-Language": "en",
    "Content-Type": "application/json"
}

data = {
    "deviceId": imei,
    "serviceId": 12
}


response = requests.post(IMEI_CHECK_API_URL, json=data, headers=headers)


print("Статус код:", response.status_code)
print("Ответ API:", response.json())
