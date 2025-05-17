from schemas.api.keyword_search_info import KeywordSearchItem as ApiKeywordSearchItem
from schemas.api.common_info import CommonInfoItem as ApiCommonInfoItem
from schemas.api.image_info import ImageInfoItem as ApiImageInfoItem
from schemas.api.intro_info.base import IntroBase as ApiIntroBase
from schemas.api.repeat_info.base import RepeatInfoBase as ApiRepeatInfoBase

from schemas.view.client_preview_view.client_preview_view import clientPreviewView
from schemas.view.client_preview_view.keyword_search_info import KeywordSearchItem as PreviewKeywordSearchItem

from schemas.view.client_detail_view.client_detail_view import ClientDetailView
from schemas.view.client_detail_view.common_info import CommonInfoItem as ViewCommonInfoItem
from schemas.view.client_detail_view.image_info import ImageInfoItem as ViewImageInfoItem

from schemas.view.llm_input_view.llm_input_view import llmInputView
from schemas.view.llm_input_view.keyword_search_info import KeywordSearchItem as LLMKeywordSearchItem
from schemas.view.llm_input_view.common_info import CommonInfoItem as ViewCommonInfoItem
from schemas.view.llm_input_view.image_info import ImageInfoItem as ViewImageInfoItem


from utils.parser_view import get_client_detail_intro_model, get_client_detail_repeat_model
from utils.parser_view import get_llm_input_intro_model, get_llm_input_repeat_model



def assemble_client_detail_view(
    contentid: int,
    contenttypeid: int,
    common_info_data: ApiCommonInfoItem,
    image_info_data: list[ApiImageInfoItem],
    intro_info_data: ApiIntroBase,
    repeat_info_data: ApiRepeatInfoBase
):
    # intro/repeat용 View 스키마 클래스 불러오기
    IntroModel = get_client_detail_intro_model(contenttypeid)
    RepeatModel = get_client_detail_repeat_model(contenttypeid)

    # 공통 정보 변환
    view_common_info = ViewCommonInfoItem(**common_info_data.model_dump())

    # 이미지 목록 변환
    view_images = [ViewImageInfoItem(**img.model_dump()) for img in image_info_data]

    # 소개 정보 변환 (단건)
    view_intro_info = IntroModel(**intro_info_data.model_dump())

    # 반복 정보 변환 (여러 개지만 대부분 1개만 있음)
    view_repeat_info = RepeatModel(**repeat_info_data.model_dump())

    return ClientDetailView(
        contentid=contentid,
        contenttypeid=contenttypeid,
        common_info=view_common_info.model_dump(),
        images=[img.model_dump() for img in image_info_data],
        intro_info=view_intro_info.model_dump(),
        repeat_info=view_repeat_info.model_dump()
    )


def assemble_llm_input_view(
    contentid: int,
    contenttypeid: int,
    keyword_info_data: ApiKeywordSearchItem,
    common_info_data: ApiCommonInfoItem,
    image_info_data: list[ApiImageInfoItem],
    intro_info_data: ApiIntroBase,
    repeat_info_data: ApiRepeatInfoBase
):
    # intro/repeat용 View 스키마 클래스 불러오기
    IntroModel = get_llm_input_intro_model(contenttypeid)
    RepeatModel = get_llm_input_repeat_model(contenttypeid)

    # 각 항목 View 스키마로 변환
    view_keyword_info = LLMKeywordSearchItem(**keyword_info_data.model_dump())
    view_common_info = ViewCommonInfoItem(**common_info_data.model_dump())
    view_images = [ViewImageInfoItem(**img.model_dump()) for img in image_info_data]
    view_intro_info = IntroModel(**intro_info_data.model_dump())
    view_repeat_info = RepeatModel(**repeat_info_data.model_dump())

    return llmInputView(
        contentid=contentid,
        contenttypeid=contenttypeid,
        keyword_search_info=view_keyword_info.model_dump(),
        common_info=view_common_info.model_dump(),
        intro_info=view_intro_info.model_dump(),
        repeat_info=view_repeat_info.model_dump(),
        images=[img.model_dump() for img in view_images]
    )





def assemble_client_preview_view(
    contentid: int,
    contenttypeid: int,
    keyword_info_data: ApiKeywordSearchItem
):

    view_keyword_info = PreviewKeywordSearchItem(**keyword_info_data.model_dump(exclude_unset=True))

    return clientPreviewView(
        contentid=contentid,
        contenttypeid=contenttypeid,
        keyword_search_info=view_keyword_info.model_dump()
    )