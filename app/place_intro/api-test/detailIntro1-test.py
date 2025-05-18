# 소개정보조회 테스트 코드 입니다.

import requests
from app.config.settings import settings
service_key =  settings.TOURAPI_KEY

url = f"http://apis.data.go.kr/B551011/KorService1/detailIntro1?serviceKey={service_key}"

params = {
    "MobileApp": "plango",
    "MobileOS": "ETC",
    "numOfRows": 1,
    "pageNo": 1,
    "contentId": 126508,
    "contentTypeId": 12,
    "_type": "json"
}

response = requests.get(url, params=params)

print(response.status_code)

# dict = response.json()
# print(dict)

print(response.text)


