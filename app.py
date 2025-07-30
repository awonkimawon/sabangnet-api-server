from flask import Flask, request, jsonify
import hmac, hashlib, base64, requests
from datetime import datetime

app = Flask(__name__)

# 사방넷 풀필먼트 API 인증 정보 (Sandbox)
COMPANY_CODE = "G001"
ACCESS_KEY    = "TC1Fx3PzgiTqc5rG"    # Sandbox용 api-access-key
SECRET_KEY    = "NUr8ogvT9Fhs5i6RY7Dr" # Sandbox용 api-secret-key
API_URL       = "https://napi.sbfulfillment.co.kr/v2/inventory/receiving_plan"

def generate_signature(access_key, secret_key, yyyymmdd):
    # 1) DateKey = HMAC-SHA256(secret_key, date)
    datekey = hmac.new(secret_key.encode(), yyyymmdd.encode(), hashlib.sha256).digest()
    # 2) SignKey = HMAC-SHA256(DateKey, access_key)
    signkey = hmac.new(datekey, access_key.encode(), hashlib.sha256).digest()
    # 3) Signature = Base64(SignKey)
    return base64.b64encode(signkey).decode()

@app.route('/register-incoming', methods=['POST'])
def register_incoming():
    try:
        incoming = request.json
        today = datetime.now().strftime("%Y%m%d")

        # 인증용 시그니처 생성
        signature = generate_signature(ACCESS_KEY, SECRET_KEY, today)

        # 요청 바디는 Apps Script에서 그대로 전달된 JSON 사용
        body = incoming

        # Sandbox 환경용 인증 헤더
        headers = {
            "Authorization": "API.SENDBOX-HMAC-SHA256",
            "Credential":    f"{COMPANY_CODE}/{ACCESS_KEY}/{today}/srwms_request",
            "Signature":     signature,
            "Content-Type":  "application/json"
        }

        # 요청 및 로그
        app.logger.info("▶ 요청 데이터: %s", body)
        res = requests.post(API_URL, json=body, headers=headers)
        app.logger.info("▶ 사방넷 응답: %s %s", res.status_code, res.text)

        return jsonify({"status": "ok", "response": res.json()}), 200

    except Exception as e:
        app.logger.error("▶ 오류 발생: %s", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
