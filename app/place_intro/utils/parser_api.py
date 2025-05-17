from app.place_intro.schemas.enums.content_type import ContentTypeId

# intro_info
from app.place_intro.schemas.api.intro_info.tour import TourIntro
from app.place_intro.schemas.api.intro_info.culture import CultureIntro
from app.place_intro.schemas.api.intro_info.festival import FestivalIntro
from app.place_intro.schemas.api.intro_info.course import CourseIntro
from app.place_intro.schemas.api.intro_info.leports import LeportsIntro
from app.place_intro.schemas.api.intro_info.lodging import LodgingIntro
from app.place_intro.schemas.api.intro_info.shopping import ShoppingIntro
from app.place_intro.schemas.api.intro_info.food import FoodIntro

# repeat_info
from app.place_intro.schemas.api.repeat_info.course import RepeatCourseItem
from app.place_intro.schemas.api.repeat_info.room import LodgingRoomItem
from app.place_intro.schemas.api.repeat_info.default import RepeatInfoItem


def get_intro_model(contenttypeid: int):
    match contenttypeid:
        case ContentTypeId.TOURIST_SPOT.value:
            return TourIntro
        case ContentTypeId.CULTURAL_FACILITY.value:
            return CultureIntro
        case ContentTypeId.FESTIVAL.value:
            return FestivalIntro
        case ContentTypeId.TRAVEL_COURSE.value:
            return CourseIntro
        case ContentTypeId.LEPORTS.value:
            return LeportsIntro
        case ContentTypeId.ACCOMMODATION.value:
            return LodgingIntro
        case ContentTypeId.SHOPPING.value:
            return ShoppingIntro
        case ContentTypeId.FOOD.value:
            return FoodIntro
        case _:
            raise ValueError(f"Unsupported contentTypeId for intro: {contenttypeid}")


def get_repeat_model(contenttypeid: int):
    match contenttypeid:
        case ContentTypeId.TRAVEL_COURSE.value:
            return RepeatCourseItem
        case ContentTypeId.ACCOMMODATION.value:
            return LodgingRoomItem
        case (ContentTypeId.TOURIST_SPOT.value
              | ContentTypeId.CULTURAL_FACILITY.value
              | ContentTypeId.FESTIVAL.value
              | ContentTypeId.LEPORTS.value
              | ContentTypeId.SHOPPING.value
              | ContentTypeId.FOOD.value):
            return RepeatInfoItem
        case _:
            raise ValueError(f"Unsupported contentTypeId for repeat: {contenttypeid}")
