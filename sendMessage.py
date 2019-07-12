import requests  # 요청을 하기 위한 모듈
import pprint  # indent까지 포함해서 잘 보여지게 만들어줌
from decouple import config # decouple 에서부터 config 호춯

base_url = 'https://api.telegram.org'
token = config('API_TOKEN')  # 토큰값
chat_id = config('CHAT_ID')
text = 'd커플테스트'

api_url = f'{base_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}'

response = requests.get(api_url)  # json 타입
pprint.pprint(response.json())

