from typing import Union, List
from pydantic import BaseModel

# keyword_search_info
from .keyword_search_info import KeywordSearchItem

# common_Info
from .common_info import CommonInfoItem

# image_info
from .image_info import ImageInfoItem

# intro_info
from .intro_info.course import CourseIntro
from .intro_info.culture import CultureIntro
from .intro_info.festival import FestivalIntro
from .intro_info.food import FoodIntro
from .intro_info.leports import LeportsIntro
from .intro_info.lodging import LodgingIntro
from .intro_info.shopping import ShoppingIntro
from .intro_info.tour import TourIntro

# repeat_info
from .repeat_info.course import RepeatCourseItem
from .repeat_info.default import RepeatInfoItem
from .repeat_info.room import LodgingRoomItem

class llmInputView(BaseModel):
    contentid: int
    contenttypeid: int

    keyword_search_info: KeywordSearchItem

    common_info: CommonInfoItem

    intro_info: Union[
        CourseIntro,
        CultureIntro,
        FestivalIntro,
        FoodIntro,
        LeportsIntro,
        LodgingIntro,
        ShoppingIntro,
        TourIntro
    ]

    repeat_info: Union[
        RepeatCourseItem,
        RepeatInfoItem,
        LodgingRoomItem
    ]

    images: List[ImageInfoItem]


