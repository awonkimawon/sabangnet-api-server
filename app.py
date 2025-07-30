from flask import Flask, request, jsonify
import hmac, hashlib, base64, requests
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
        incoming_data = request.json
        today = datetime.now().strftime("%Y%m%d")
        signature = generate_signature(ACCESS_KEY, SECRET_KEY, today)

        # 필수 필드 구성 (실제 사방넷 API에 맞는 형식으로 구성)
        body = {
            "member_id": 0,  # 물류사 관련 아니면 생략 가능
            "receiving_plan_code": incoming_data.get("receiving_plan_code", "TEST-PLAN-001"),
            "plan_date": incoming_data.get("plan_date", today),
            "memo": incoming_data.get("memo", "테스트 메모"),
            "plan_product_list": [
                {
                    "shipping_product_id": incoming_data.get("shipping_product_id", 123456),
                    "quantity": incoming_data.get("quantity", 10)
                }
            ]
        }

        headers = {
            "Authorization": "LIVE-HMAC-SHA256",
            "Credential": f"{COMPANY_CODE}/{ACCESS_KEY}/{today}/srwms_request",
            "Signature": signature,
            "Content-Type": "application/json"
        }

        app.logger.info("▶ 요청 데이터: %s", body)

        response = requests.post(API_URL, json=body, headers=headers)

        app.logger.info("▶ 사방넷 응답: %s %s", response.status_code, response.text)

        return jsonify({"status": "ok", "response": response.json()}), 200
    except Exception as e:
        app.logger.error("▶ 오류 발생: %s", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)