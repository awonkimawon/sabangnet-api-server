from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'Sabangnet API Server is running!'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # 사방넷 입고예정등록 API 엔드포인트
    sabangnet_url = "https://wms.sabangnet.co.kr/v2/inventory/receiving_plan"

    # 요청 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "access-key": data["access_key"],
        "secret-key": data["secret_key"],
        "code": data["company_code"]  # 시트에서 입력받은 회사코드 (예: G001)
    }

    # 요청 바디 구성
    payload = {
        "member_id": data["member_id"],
        "receiving_plan_code": data["receiving_plan_code"],  # 예: 20250802_1
        "plan_date": data["plan_date"],                     # YYYYMMDD
        "memo": data["memo"],
        "plan_product_list": data["plan_product_list"]      # 상품 리스트 배열
    }

    try:
        # 사방넷 API 호출
        res = requests.post(sabangnet_url, headers=headers, json=payload)
        return jsonify(res.json())
    except Exception as e:
        # 에러 발생 시 메시지 반환
        return jsonify({"code": "9998", "message": str(e)}), 500

# ✅ Render 환경에서 외부 접속 가능하도록 설정
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10000)