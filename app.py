from flask import Flask, request
from decouple import config
import pprint
import requests
app = Flask(__name__)
API_TOKEN = config('API_TOKEN')  # 상수는 대문자

# POST 요청 - 회원가입 등 정보를 숨겨야 할 때 


@app.route('/')
def hello():
    return 'Hello World'


@app.route('/greeting/<name>')
def greeting(name):
    return f'Hello, {name}'


@app.route(f'/{API_TOKEN}', methods=['POST'])
def telegram():
    from_telegram = request.get_json() 
    # pprint.pprint(from_telegram)
    if from_telegram.get('message') is not None:
        # 우리가 원하는 로직
        chat_id = from_telegram.get('message').get('chat').get('id')
        text = from_telegram.get('message').get('text')

        if text == '점심메뉴':
            text = '짜장면이나 먹어'

        # Send Message API URL 
        base_url = 'https://api.telegram.org'
        api_url = f'{base_url}/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={text}'
        requests.get(api_url)
    
    return '', 200


if __name__ == '__main__':
    app.run(debug=True)