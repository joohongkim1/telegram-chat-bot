from flask import Flask, request
from decouple import config
import pprint
import requests
app = Flask(__name__)

API_TOKEN = config('API_TOKEN')  # 상수는 대문자
NAVER_CLIENT_ID = config('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = config('NAVER_CLIENT_SECRET')
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
        text = from_telegram.get('message').get('text')  # 사용자가 보낸 텍스트

        # 첫 네글자가 '/한영 ' 일 때 확인
        if text[0:4] == '/한영 ':  # str값도 인덱스로 접근 가능, 각각의 캐릭터로 접근
            headers = {  # 요청에 대한 정보가 저장
                'X-Naver-Client-Id': NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,  # 끝에 , 넣어주면 좋음
            }
            data = {
                'source': 'ko',
                'target': 'en',
                'text': text[4:] # '/번역 ' 이후의 문자열만 대상으로 번역
            }
            papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
            papago_res = requests.post(papago_url, headers=headers, data=data)
            pprint.pprint(papago_res.json())
            text = papago_res.json().get('message').get('result').get('translatedText')

        elif text[0:4] == '/영한 ':  # str값도 인덱스로 접근 가능, 각각의 캐릭터로 접근
            headers = {  # 요청에 대한 정보가 저장
                'X-Naver-Client-Id': NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,  # 끝에 , 넣어주면 좋음
            }
            data = {
                'source': 'en',
                'target': 'ko',
                'text': text[4:] # '/번역 ' 이후의 문자열만 대상으로 번역
            }
            papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
            papago_res = requests.post(papago_url, headers=headers, data=data)
            pprint.pprint(papago_res.json())
            text = papago_res.json().get('message').get('result').get('translatedText')

        # Send Message API URL 
        base_url = 'https://api.telegram.org'
        api_url = f'{base_url}/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={text}'
        requests.get(api_url)
    
    return '', 200



if __name__ == '__main__':
    app.run(debug=True)