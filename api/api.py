from flask import Flask, request, jsonify
import requests
from api.config import IMEI_CHECK_API_URL, IMEI_CHECK_API_TOKEN, SERVICE_ID, \
    API_AUTH_TOKEN

app = Flask(__name__)


def check_imei(imei: str):
    headers = {
        "Authorization": f"Bearer {IMEI_CHECK_API_TOKEN}",
        "Accept-Language": "en",
        "Content-Type": "application/json"
    }
    data = {"deviceId": imei, "serviceId": SERVICE_ID}

    response = requests.post(IMEI_CHECK_API_URL, json=data, headers=headers)
    return response.json()


@app.route('/api/check-imei', methods=['POST'])
def api_check_imei():
    data = request.json
    imei = data.get("imei")
    token = data.get("token")

    if token != API_AUTH_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    if not imei or len(imei) != 15 or not imei.isdigit():
        return jsonify({"error": "Invalid IMEI"}), 400

    result = check_imei(imei)
    if "error" in result:
        return jsonify({"error": result["error"]}), 400

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
