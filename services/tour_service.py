from schemas.api.keyword_search_info import KeywordSearchItem
from schemas.api.common_info import CommonInfoItem
from schemas.api.image_info import ImageInfoItem
from schemas.api.intro_info.base import IntroBase
from schemas.api.repeat_info.base import RepeatInfoBase

from schemas.view.client_preview_view.client_preview_view import clientPreviewView
from schemas.view.client_detail_view.client_detail_view import ClientDetailView
from schemas.view.llm_input_view.llm_input_view import llmInputView

from services.assembler import assemble_client_preview_view
from services.assembler import assemble_client_detail_view
from services.assembler import assemble_llm_input_view



async def get_preview_info(keyword_items: list[KeywordSearchItem]) -> clientPreviewView:
   
    # 첫 번째 결과 기준으로 preview 조립
    keyword_item = keyword_items[0]

    preview_view = assemble_client_preview_view(
        contentid=keyword_item.contentid,
        contenttypeid=keyword_item.contenttypeid,
        keyword_info_data=keyword_item
    )

    return preview_view


async def get_detail_info(
    contentid: int,
    contenttypeid: int,
    common_info: CommonInfoItem,
    image_info: list[ImageInfoItem],
    intro_info: IntroBase,
    repeat_info: RepeatInfoBase,
) -> ClientDetailView:

    # client_detail_view 조립
    detail_view = assemble_client_detail_view(
        contentid=contentid,
        contenttypeid=contenttypeid,
        common_info_data=common_info,
        image_info_data=image_info,
        intro_info_data=intro_info,
        repeat_info_data=repeat_info
    )

    return detail_view



async def get_llm_input(
    contentid: int,
    contenttypeid: int,
    keyword_info: KeywordSearchItem,
    common_info: CommonInfoItem,
    image_info: list[ImageInfoItem],
    intro_info: IntroBase,
    repeat_info: RepeatInfoBase
) -> llmInputView:
    # 조립기 호출
    llm_input = assemble_llm_input_view(
        contentid=contentid,
        contenttypeid=contenttypeid,
        keyword_info_data=keyword_info,
        common_info_data=common_info,
        image_info_data=image_info,
        intro_info_data=intro_info,
        repeat_info_data=repeat_info
    )

    return llm_input