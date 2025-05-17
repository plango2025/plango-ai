from clients.tour_api_client import (
    search_keyword,
    get_common_info,
    get_image_info,
    get_intro_info,
    get_repeat_info
)

from schemas.api.keyword_search_info import KeywordSearchItem
from schemas.api.common_info import CommonInfoItem
from schemas.api.image_info import ImageInfoItem
from schemas.api.intro_info.base import IntroBase
from schemas.api.repeat_info.base import RepeatInfoBase

import asyncio

async def first_tour_data_loader(keyword: str) -> list[KeywordSearchItem]:
    # searchKeyword1 API 호출 → Pydantic 객체 리스트 반환
    keyword_items: list[KeywordSearchItem] = await search_keyword(keyword=keyword, num_of_rows=1)

    if not keyword_items:
        raise ValueError(f"No result found for keyword: {keyword}")

    return keyword_items


async def second_tour_data_loader(contentid: int,contenttypeid: int) -> tuple[CommonInfoItem, list[ImageInfoItem], IntroBase, RepeatInfoBase]:
   
    common_info, image_info, intro_info, repeat_info = await asyncio.gather(
        get_common_info(contentid, contenttypeid),
        get_image_info(contentid),
        get_intro_info(contentid, contenttypeid),
        get_repeat_info(contentid, contenttypeid)
    )

    return common_info, image_info, intro_info, repeat_info

