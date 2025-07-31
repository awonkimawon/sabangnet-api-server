from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'Sabangnet API Server is running!'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # 입력된 값 확인용 로그
    app.logger.info(f"입력된 데이터: {data}")

    # TODO: 실제 사방넷 API 호출을 여기에 작성할 예정
    dummy_result = {
        "status": "success",
        "message": "이건 테스트 응답입니다. 사방넷 API 연동 예정"
    }
    return jsonify(dummy_result)

if __name__ == '__main__':
    app.run(debug=True)
