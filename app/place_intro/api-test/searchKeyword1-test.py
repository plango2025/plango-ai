# 키워드 검색 조회 테스트 코드 입니다.

import requests
from app.config.settings import settings
service_key =  settings.TOURAPI_KEY

url = f"http://apis.data.go.kr/B551011/KorService1/searchKeyword1?serviceKey={service_key}"

params = {
    "MobileApp": "plango",
    "MobileOS": "ETC",
    "numOfRows": 3,
    "pageNo": 1,
    "listYN": "Y",
    "arrange": "A",
    "keyword": "경복궁",
    "_type": "json"
}

response = requests.get(url, params=params)

print(response.request.url)
print(response.status_code)

# dict = response.json()
# print(dict)

print(response.text)

