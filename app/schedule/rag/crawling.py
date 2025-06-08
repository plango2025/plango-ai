import requests
import json
import time
import math
import os

# API 기본 정보
API_URL_INFO = "https://api.visitkorea.or.kr/hub/getTourInfo.do" # 데이터 목록 조회 API
API_URL_COUNT = "https://api.visitkorea.or.kr/hub/getTourInfoCnt.do" # 총 개수 조회 API

# 모든 카테고리 ID와 이름 매핑 정의
ALL_CONTENT_TYPES_MAP = {
    "12": "관광지",
    "14": "문화시설",
    "15": "축제공연행사",
    "25": "여행코스",
    "28": "레포츠",
    "32": "숙박",
    "38": "쇼핑",
    "39": "음식점"
}

# 제외할 카테고리 ID 정의
EXCLUDE_CONTENT_TYPE_IDS = ["15", "25"] # 축제공연행사, 여행코스

# 포함할 카테고리 ID 및 이름 필터링
INCLUDED_CONTENT_TYPE_IDS = []
INCLUDED_CONTENT_TYPE_NAMES = []
for _id, name in ALL_CONTENT_TYPES_MAP.items():
    if _id not in EXCLUDE_CONTENT_TYPE_IDS:
        INCLUDED_CONTENT_TYPE_IDS.append(_id)
        INCLUDED_CONTENT_TYPE_NAMES.append(name)

# 기본 요청 payload 설정 (데이터 목록 조회용)
# searchStart: 0 제거!
base_payload_info = {
    "langDiv": "kor",
    "contentTypeId": INCLUDED_CONTENT_TYPE_IDS,
    "contentTypeName": INCLUDED_CONTENT_TYPE_NAMES,
    "cat1List": [
        {"cd":None,"cdNm":None,"contentTypeId":None,"comConcomContentTypeId":None,"contentTypeIdList":None,"cat1":"A01","cat2":None,"cat3":None,"catName1":"자연","catName2":None,"catName3":None,"langDiv":None,"cnt":0,"subName":None,"areaCd":None,"signguCd":None,"title":None},
        {"cd":None,"cdNm":None,"contentTypeId":None,"comConcomContentTypeId":None,"contentTypeIdList":None,"cat1":"A02","cat2":None,"cat3":None,"catName1":"인문(문화/예술/역사)","cat2":None,"cat3":None,"catName3":None,"langDiv":None,"cnt":0,"subName":None,"areaCd":None,"signguCd":None,"title":None},
        {"cd":None,"cdNm":None,"contentTypeId":None,"comConcomContentTypeId":None,"contentTypeIdList":None,"cat1":"A03","cat2":None,"cat3":None,"catName1":"레포츠","cat2":None,"cat3":None,"catName3":None,"langDiv":None,"cnt":0,"subName":None,"areaCd":None,"signguCd":None,"title":None},
        {"cd":None,"cdNm":None,"contentTypeId":None,"comConcomContentTypeId":None,"contentTypeIdList":None,"cat1":"A04","cat2":None,"cat3":None,"contentTypeIdList":None,"catName1":"쇼핑","cat2":None,"cat3":None,"catName3":None,"langDiv":None,"cnt":0,"subName":None,"areaCd":None,"signguCd":None,"title":None},
        {"cd":None,"cdNm":None,"contentTypeId":None,"comConcomContentTypeId":None,"contentTypeIdList":None,"cat1":"A05","cat2":None,"cat3":None,"catName1":"음식","cat2":None,"cat3":None,"catName3":None,"langDiv":None,"cnt":0,"subName":None,"areaCd":None,"signguCd":None,"title":None},
        {"cd":None,"cdNm":None,"contentTypeId":None,"comConcomContentTypeId":None,"contentTypeIdList":None,"cat1":"B02","cat2":None,"cat3":None,"catName1":"숙박","cat2":None,"cat3":None,"catName3":None,"langDiv":None,"cnt":0,"subName":None,"areaCd":None,"signguCd":None,"title":None},
        {"cd":None,"cdNm":None,"contentTypeId":None,"comConcomContentTypeId":None,"contentTypeIdList":None,"cat1":"C01","cat2":None,"cat3":None,"catName1":"추천코스","cat2":None,"cat3":None,"catName3":None,"langDiv":None,"cnt":0,"subName":None,"areaCd":None,"signguCd":None,"title":None}
    ],
    "cat1": "",
    "catName1": "",
    "cat2List": [],
    "cat2": "",
    "catName2": "",
    "cat3List": [],
    "cat3": "",
    "catName3": "",
    "selCatList": [],
    "areaCd": "",
    "signguCd": "",
    "emdCd": "",
    "title": "",
    "searchCateg": "",
    "arrange": "NEW",
    "selectService": "",
    "searchCnt": 100, # 페이지당 100개 아이템
    "pageNo": 1, # 초기 pageNo는 1로 설정, 이후 루프에서 업데이트
    "pageCnt": 1, # 이 값은 서버에서 주는 값으로, 요청 시에는 크게 중요하지 않을 수 있음
    "mainYn": "N",
    "contAll": INCLUDED_CONTENT_TYPE_IDS,
    "contNm": INCLUDED_CONTENT_TYPE_NAMES
}

# 총 개수 조회용 payload (데이터 목록 조회 payload와 동일하게 설정)
# searchStart는 count에서는 의미 없을 수 있으나, 일관성을 위해 제거 유지
base_payload_count = base_payload_info.copy()

# 요청 헤더 (이전과 동일하게 유지)
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Host": "api.visitkorea.or.kr",
    "Origin": "https://api.visitkorea.or.kr",
    "Referer": "https://api.visitkorea.or.kr/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

# crawling.py가 'app/schedule/rag/' 폴더 내에 있으므로,
# 'crawled_data' 폴더도 'app/schedule/rag/crawled_data/'에 생성되도록 합니다.
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# 최종 데이터 저장 경로 설정: app/schedule/rag/crawled_data/
output_dir = os.path.join(current_script_dir, "crawled_data")

# 디렉토리가 없으면 생성
os.makedirs(output_dir, exist_ok=True)

# 최종 파일명 설정
output_filename = os.path.join(output_dir, "public_tourism_data.jsonl")

print(f"크롤링 데이터를 다음 경로에 저장합니다: {output_filename}")


def get_total_count():
    print("총 데이터 개수 조회 중 (제외된 카테고리: 축제공연행사, 여행코스)...")
    try:
        response = requests.post(API_URL_COUNT, headers=headers, json=base_payload_count, timeout=30)
        response.raise_for_status()
        
        total_count_str = response.text.strip()
        try:
            total_count = int(total_count_str)
            print(f"API에서 확인된 총 데이터 개수: {total_count}개")
            return total_count
        except ValueError:
            print(f"오류: getTourInfoCnt.do 응답이 유효한 숫자가 아닙니다. 응답: '{total_count_str}'")
            return 0
    except requests.exceptions.RequestException as e:
        print(f"총 개수 API 호출 중 오류 발생: {e}")
        return 0

def crawl_tour_data_national():
    all_extracted_data = []
    current_page = 1
    items_per_page = base_payload_info["searchCnt"] # 페이지당 100개

    total_items = get_total_count()

    if total_items == 0:
        print("총 데이터 개수를 가져오지 못했거나 0이므로 크롤링을 중단합니다.")
        return

    total_pages = math.ceil(total_items / items_per_page)
    print(f"총 {total_items}개의 데이터를 위해 {total_pages}페이지를 크롤링합니다. (페이지당 {items_per_page}개)")

    while current_page <= total_pages:
        payload = base_payload_info.copy()
        payload["pageNo"] = current_page
        # searchStart를 현재 페이지에 맞춰 계산하여 추가
        payload["searchStart"] = (current_page - 1) * items_per_page 
        
        print(f"\n데이터 요청 중... (페이지: {current_page}/{total_pages}, 진행률: {(current_page/total_pages)*100:.2f}%, 현재까지 수집된 데이터: {len(all_extracted_data)}개)")
        
        try:
            response = requests.post(API_URL_INFO, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            
            items = []
            if isinstance(data, list):
                items = [entry for entry in data if isinstance(entry, dict) and "contentId" in entry]
            elif isinstance(data, dict):
                if 'response' in data and isinstance(data['response'], dict) and \
                   'body' in data['response'] and isinstance(data['response']['body'], dict) and \
                   'items' in data['response']['body'] and isinstance(data['response']['body']['items'], list):
                    items = data['response']['body']['items']
                elif 'items' in data and isinstance(data['items'], list):
                    items = data['items']
                elif 'data' in data and isinstance(data['data'], list):
                    items = data['data']
            
            if not items:
                print(f"페이지 {current_page}에 데이터가 없습니다. (예상보다 일찍 종료). 크롤링을 종료합니다.")
                break
            
            for item in items:
                content_type_id = item.get("contentTypeId", "")
                content_type_name = ALL_CONTENT_TYPES_MAP.get(content_type_id, "알 수 없음")
                
                extracted = {
                    "title": item.get("title", ""),
                    "content_type": content_type_name,
                    "addr1": item.get("addr1", ""),
                    "outl": item.get("outl", "")
                }
                all_extracted_data.append(extracted)
            
            print(f"페이지 {current_page}에서 {len(items)}개 데이터 수집. 현재까지 총 {len(all_extracted_data)}개.")

            current_page += 1
            time.sleep(0.1) 

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP 오류 발생: {http_err} (페이지: {current_page})")
            print(f"응답 내용: {response.text}")
            if response.status_code == 429:
                print("API 요청 제한에 걸렸습니다. 잠시 후 다시 시도합니다...")
                time.sleep(60)
                continue
            break
        except requests.exceptions.ConnectionError as conn_err:
            print(f"연결 오류 발생: {conn_err} (페이지: {current_page})")
            print("잠시 후 다시 시도합니다...")
            time.sleep(10)
            continue
        except requests.exceptions.Timeout as timeout_err:
            print(f"요청 시간 초과: {timeout_err} (페이지: {current_page})")
            print("잠시 후 다시 시도합니다...")
            time.sleep(10)
            continue
        except requests.exceptions.RequestException as req_err:
            print(f"예기치 않은 요청 오류 발생: {req_err} (페이지: {current_page})")
            break
        except json.JSONDecodeError as json_err:
            print(f"JSON 디코딩 오류 발생: {json_err} (페이지: {current_page})")
            print(f"응답 내용: {response.text[:500]}...")
            print("비정상적인 응답이므로 크롤링을 중단합니다.")
            break
    
    if all_extracted_data:
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                for item in all_extracted_data:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
            print(f"\n크롤링 완료! 총 {len(all_extracted_data)}개의 데이터를 '{output_filename}'에 저장했습니다.")
        except Exception as e:
            print(f"파일 저장 중 오류 발생: {e}")
    else:
        print("수집된 데이터가 없어 파일로 저장할 내용이 없습니다.")

crawl_tour_data_national()