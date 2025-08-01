from flask import Flask, request, jsonify
import requests
import hmac
import hashlib
import base64
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return 'Sabangnet API Server is running!'

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        access_key = data["access_key"]
        secret_key = data["secret_key"]
        company_code = "G001"
        member_id = "G0542"
        today = datetime.datetime.now().strftime('%Y%m%d')

        # Step 1: Signature 생성
        datekey = hmac.new(secret_key.encode(), today.encode(), hashlib.sha256).digest()
        signkey = hmac.new(datekey, access_key.encode(), hashlib.sha256).digest()
        signature = base64.b64encode(signkey).decode()

        # Step 2: 헤더 구성
        headers = {
            "Content-Type": "application/json",
            "Authorization": "LIVE-HMAC-SHA256",
            "Credential": f"LIVE/{company_code}/{access_key}/{today}/swms_request",
            "Signature": signature
        }

        # Step 3: Body 구성
        payload = {
            "member_id": member_id,
            "receiving_plan_code": data["receiving_plan_code"],
            "plan_date": data["plan_date"],
            "memo": data["memo"],
            "plan_product_list": data["plan_product_list"]
        }

        # Step 4: 요청
        url = "https://napi.sbfulfilment.co.kr/v2/inventory/receiving_plan"
        res = requests.post(url, headers=headers, json=payload)

        return jsonify(res.json())

    except Exception as e:
        return jsonify({"code": "9999", "message": str(e)}), 500