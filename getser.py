import requests

IMEI_CHECK_API_URL = "https://api.imeicheck.net/v1/services"
IMEI_CHECK_API_TOKEN = "e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b"

headers = {
    "Authorization": f"Bearer {IMEI_CHECK_API_TOKEN}",
    "Accept-Language": "en",
}

response = requests.get(IMEI_CHECK_API_URL, headers=headers)

print("Статус код:", response.status_code)
print("Ответ API:", response.json())
