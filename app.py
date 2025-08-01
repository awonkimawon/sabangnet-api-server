from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Sabangnet API Server is running!'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # 사방넷 API 요청 구성
    sabangnet_url = "https://wms.sabangnet.co.kr/v2/inventory/receiving_plan"

    headers = {
        "Content-Type": "application/json",
        "access-key": data["access_key"],
        "secret-key": data["secret_key"],
        "code": data["company_code"]  # ← 시트에서 입력된 회사코드 사용
    }

    payload = {
        "member_id": data["member_id"],
        "receiving_plan_code": data["receiving_plan_code"],
        "plan_date": data["plan_date"],
        "memo": data["memo"],
        "plan_product_list": data["plan_product_list"]
    }

    try:
        res = requests.post(sabangnet_url, headers=headers, json=payload)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"code": "9998", "message": str(e)}), 500

# 🔽 직접 실행 시 필요한 부분 (Render에서는 무시됨)
if __name__ == '__main__':
    app.run(debug=True)