from app.place_intro.schemas.enums.content_type import ContentTypeId

# client_detail_view - intro_info
from app.place_intro.schemas.view.client_detail_view.intro_info.tour import TourIntro
from app.place_intro.schemas.view.client_detail_view.intro_info.culture import CultureIntro
from app.place_intro.schemas.view.client_detail_view.intro_info.festival import FestivalIntro
from app.place_intro.schemas.view.client_detail_view.intro_info.food import FoodIntro
from app.place_intro.schemas.view.client_detail_view.intro_info.leports import LeportsIntro
from app.place_intro.schemas.view.client_detail_view.intro_info.lodging import LodgingIntro
from app.place_intro.schemas.view.client_detail_view.intro_info.shopping import ShoppingIntro
from app.place_intro.schemas.view.client_detail_view.intro_info.course import CourseIntro

# client_detail_view - repeat_info
from app.place_intro.schemas.view.client_detail_view.repeat_info.course import RepeatCourseItem
from app.place_intro.schemas.view.client_detail_view.repeat_info.room import LodgingRoomItem
from app.place_intro.schemas.view.client_detail_view.repeat_info.default import RepeatInfoItem

# LLM Input View - intro_info
from app.place_intro.schemas.view.llm_input_view.intro_info.tour import TourIntro as LLMTourIntro
from app.place_intro.schemas.view.llm_input_view.intro_info.culture import CultureIntro as LLMCultureIntro
from app.place_intro.schemas.view.llm_input_view.intro_info.festival import FestivalIntro as LLMFestivalIntro
from app.place_intro.schemas.view.llm_input_view.intro_info.food import FoodIntro as LLMFoodIntro
from app.place_intro.schemas.view.llm_input_view.intro_info.leports import LeportsIntro as LLMLeportsIntro
from app.place_intro.schemas.view.llm_input_view.intro_info.lodging import LodgingIntro as LLMLodgingIntro
from app.place_intro.schemas.view.llm_input_view.intro_info.shopping import ShoppingIntro as LLMShoppingIntro
from app.place_intro.schemas.view.llm_input_view.intro_info.course import CourseIntro as LLMCourseIntro

# LLM Input View - repeat_info
from app.place_intro.schemas.view.llm_input_view.repeat_info.course import RepeatCourseItem as LLMRepeatCourseItem
from app.place_intro.schemas.view.llm_input_view.repeat_info.room import LodgingRoomItem as LLMLodgingRoomItem
from app.place_intro.schemas.view.llm_input_view.repeat_info.default import RepeatInfoItem as LLMRepeatInfoItem

def get_client_detail_intro_model(contenttypeid: int):
    match contenttypeid:
        case ContentTypeId.TOURIST_SPOT.value:
            return TourIntro
        case ContentTypeId.CULTURAL_FACILITY.value:
            return CultureIntro
        case ContentTypeId.FESTIVAL.value:
            return FestivalIntro
        case ContentTypeId.FOOD.value:
            return FoodIntro
        case ContentTypeId.LEPORTS.value:
            return LeportsIntro
        case ContentTypeId.ACCOMMODATION.value:
            return LodgingIntro
        case ContentTypeId.SHOPPING.value:
            return ShoppingIntro
        case ContentTypeId.TRAVEL_COURSE.value:
            return CourseIntro
        case _:
            raise ValueError(f"Unsupported contentTypeId for client detail intro: {contenttypeid}")


def get_client_detail_repeat_model(contenttypeid: int):
    match contenttypeid:
        case ContentTypeId.TRAVEL_COURSE.value:
            return RepeatCourseItem
        case ContentTypeId.ACCOMMODATION.value:
            return LodgingRoomItem
        case ContentTypeId.TOURIST_SPOT.value \
           | ContentTypeId.CULTURAL_FACILITY.value \
           | ContentTypeId.FESTIVAL.value \
           | ContentTypeId.LEPORTS.value \
           | ContentTypeId.SHOPPING.value \
           | ContentTypeId.FOOD.value:
            return RepeatInfoItem
        case _:
            raise ValueError(f"Unsupported contentTypeId for client detail repeat: {contenttypeid}")


def get_llm_input_intro_model(contenttypeid: int):
    match contenttypeid:
        case ContentTypeId.TOURIST_SPOT.value:
            return LLMTourIntro
        case ContentTypeId.CULTURAL_FACILITY.value:
            return LLMCultureIntro
        case ContentTypeId.FESTIVAL.value:
            return LLMFestivalIntro
        case ContentTypeId.FOOD.value:
            return LLMFoodIntro
        case ContentTypeId.LEPORTS.value:
            return LLMLeportsIntro
        case ContentTypeId.ACCOMMODATION.value:
            return LLMLodgingIntro
        case ContentTypeId.SHOPPING.value:
            return LLMShoppingIntro
        case ContentTypeId.TRAVEL_COURSE.value:
            return LLMCourseIntro
        case _:
            raise ValueError(f"Unsupported contentTypeId for LLM input intro: {contenttypeid}")


def get_llm_input_repeat_model(contenttypeid: int):
    match contenttypeid:
        case ContentTypeId.TRAVEL_COURSE.value:
            return LLMRepeatCourseItem
        case ContentTypeId.ACCOMMODATION.value:
            return LLMLodgingRoomItem
        case ContentTypeId.TOURIST_SPOT.value \
           | ContentTypeId.CULTURAL_FACILITY.value \
           | ContentTypeId.FESTIVAL.value \
           | ContentTypeId.LEPORTS.value \
           | ContentTypeId.SHOPPING.value \
           | ContentTypeId.FOOD.value:
            return LLMRepeatInfoItem
        case _:
            raise ValueError(f"Unsupported contentTypeId for LLM input repeat: {contenttypeid}")