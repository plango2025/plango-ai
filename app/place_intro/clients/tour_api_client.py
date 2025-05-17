from app.place_intro.schemas.api.keyword_search_info import KeywordSearchItem
from app.place_intro.schemas.api.common_info import CommonInfoItem
from app.place_intro.schemas.api.image_info import ImageInfoItem
from app.place_intro.schemas.api.intro_info.base import IntroBase
from app.place_intro.schemas.api.repeat_info.base import RepeatInfoBase

from app.place_intro.utils.parser_api import get_intro_model
from app.place_intro.utils.parser_api import get_repeat_model

import httpx
from urllib.parse import unquote


from app.config.settings import settings

BASE_URL = settings.TOURAPI_BASE_URL
SERVICE_KEY = settings.TOURAPI_KEY
DECODED_SERVICE_KEY = unquote(SERVICE_KEY)
TIMEOUT = settings.timeout


from app.place_intro.schemas.api.keyword_search_info import KeywordSearchItem

async def search_keyword(keyword: str, num_of_rows: int = 2) -> list[KeywordSearchItem]:
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.get(
            f"{BASE_URL}/KorService1/searchKeyword1",
            params={
                "serviceKey": DECODED_SERVICE_KEY,
                "MobileApp": "plango",
                "MobileOS": "ETC",
                "numOfRows": num_of_rows,
                "pageNo": 1,
                "listYN": "Y",
                "arrange": "A",
                "keyword": keyword,
                "_type": "json"
            }
        )
        response.raise_for_status()
        print(response.request.url)
        data = response.json()

    try:
        items = data["response"]["body"]["items"]["item"]
        if isinstance(items, dict):
            items = [items]  # 단일 객체인 경우에도 리스트로 처리
        return [KeywordSearchItem(**item) for item in items]
    except (KeyError, TypeError):
        return []



async def get_common_info(content_id: int, content_type_id: int) -> CommonInfoItem:
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.get(
            f"{BASE_URL}/KorService1/detailCommon1",
            params={
                "serviceKey": DECODED_SERVICE_KEY,
                "MobileApp": "plango",
                "MobileOS": "ETC",
                "numOfRows": 1,
                "pageNo": 1,
                "contentId": content_id,
                "contentTypeId": content_type_id,
                "defaultYN": "Y",
                "firstImageYN": "Y",
                "addrinfoYN": "Y",
                "mapinfoYN": "Y",
                "overviewYN": "Y",
                "areacodeYN": "N",
                "catcodeYN": "N",
                "_type": "json"
            }
        )
        response.raise_for_status()
        data = response.json()

    try:
        item = data["response"]["body"]["items"]["item"]
        if isinstance(item, list):  # ✅ 리스트인 경우 첫 번째 요소 사용
            item = item[0]
        return CommonInfoItem(**item)
    except (KeyError, TypeError) as e:
        raise ValueError(f"Failed to parse detailCommon1 response: {e}")


async def get_intro_info(content_id: int, content_type_id: int) -> IntroBase:
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.get(
            f"{BASE_URL}/KorService1/detailIntro1",
            params={
                "serviceKey": DECODED_SERVICE_KEY,
                "MobileApp": "plango",
                "MobileOS": "ETC",
                "numOfRows": 1,
                "pageNo": 1,
                "contentId": content_id,
                "contentTypeId": content_type_id,
                "_type": "json"
            }
        )
        response.raise_for_status()
        data = response.json()

    try:
        item = data["response"]["body"]["items"]["item"]
        if isinstance(item, list):  # ✅ 리스트일 경우 첫 번째 항목만 사용
            item = item[0]
        IntroModel = get_intro_model(content_type_id)  # contentTypeId에 맞는 스키마 반환
        return IntroModel(**item)
    
    except (KeyError, TypeError, ValueError) as e:
        raise ValueError(f"Failed to parse detailIntro1 for contentTypeId={content_type_id}: {e}")


async def get_repeat_info(content_id: int, content_type_id: int) -> RepeatInfoBase:
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.get(
            f"{BASE_URL}/KorService1/detailInfo1",
            params={
                "serviceKey": DECODED_SERVICE_KEY,
                "MobileApp": "plango",
                "MobileOS": "ETC",
                "numOfRows": 10,
                "pageNo": 1,
                "contentId": content_id,
                "contentTypeId": content_type_id,
                "_type": "json"
            }
        )
        response.raise_for_status()
        data = response.json()

    try:
        items = data["response"]["body"]["items"]["item"]
        if isinstance(items, list):  # ✅ 리스트일 경우 첫 번째 항목만 사용
            item = items[0]
        RepeatModel = get_repeat_model(content_type_id)
        return RepeatModel(**item)
    
    except (KeyError, TypeError, ValueError) as e:
        raise ValueError(f"Failed to parse detailInfo1 for contentTypeId={content_type_id}: {e}")


async def get_image_info(content_id: int) -> list[ImageInfoItem]:
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.get(
            f"{BASE_URL}/KorService1/detailImage1",
            params={
                "serviceKey": DECODED_SERVICE_KEY,
                "MobileApp": "plango",
                "MobileOS": "ETC",
                "numOfRows": 10,
                "pageNo": 1,
                "contentId": content_id,
                "imageYN": "Y",
                "subImageYN": "Y",
                "_type": "json"
            }
        )
        response.raise_for_status()
        data = response.json()

    try:
        items = data["response"]["body"]["items"]["item"]
        if isinstance(items, dict):
            items = [items]  # 단일 이미지도 리스트로 처리
        return [ImageInfoItem(**item) for item in items]
    
    except (KeyError, TypeError):
        return []
