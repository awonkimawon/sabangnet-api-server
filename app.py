from flask import Flask, request, jsonify
import hmac
import hashlib
import base64
import requests
from datetime import datetime

app = Flask(__name__)

# 사방넷 API 인증 정보
COMPANY_CODE = "G001"
ACCESS_KEY = "SKg5MDG8IQ9dVAVW"
SECRET_KEY = "IcEkOraMj4gaoByCopSB"
API_URL = "https://napi.sbfulfillment.co.kr/v2/inventory/receiving_plan"

# 시그니처 생성 함수
def generate_signature(access_key, secret_key, yyyymmdd):
    datekey = hmac.new(secret_key.encode(), yyyymmdd.encode(), hashlib.sha256).digest()
    signkey = hmac.new(datekey, access_key.encode(), hashlib.sha256).digest()
    signature = base64.b64encode(signkey).decode()
    return signature

@app.route('/register-incoming', methods=['POST'])
def register_incoming():
    try:
        data = request.json  # Google Apps Script에서 전달한 JSON 데이터

        # 오늘 날짜 (서버 기준)
        today = datetime.now().strftime("%Y%m%d")

        # 시그니처 생성
        signature = generate_signature(ACCESS_KEY, SECRET_KEY, today)

        headers = {
            "Authorization": "LIVE-HMAC-SHA256",
            "Credential": f"{COMPANY_CODE}/{ACCESS_KEY}/{today}/srwms_request",
            "Signature": signature,
            "Content-Type": "application/json"
        }

        # 사방넷 API로 POST 요청
        response = requests.post(API_URL, json=data, headers=headers)

        print("▶ 요청 데이터:", data)
        print("▶ 사방넷 응답:", response.status_code, response.text)

        return jsonify({"status": "ok", "response": response.json()}), 200

    except Exception as e:
        print("▶ 오류 발생:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
