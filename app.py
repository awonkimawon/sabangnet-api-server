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

    sabangnet_url = "https://wms.sabangnet.co.kr/v2/inventory/receiving_plan"

    headers = {
        "Content-Type": "application/json",
        "access-key": data["access_key"],
        "secret-key": data["secret_key"],
        "code": data["company_code"]  # 시트에서 입력된 회사코드 사용
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

# ✅ Render가 요구하는 포트 환경변수 사용 (필수!)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)