# TourAPI - detailIntro1 (소개정보조회)중 여행코스(contentTypeId=25) 응답 스키마

from typing import Any
from .base import IntroBase


class CourseIntro(IntroBase):
    distance: Any | None = None                  # 코스 총 거리
    infocentertourcourse: Any | None = None      # 문의 및 안내
    schedule: Any | None = None                  # 코스 일정
    taketime: Any | None = None                  # 코스 총 소요시간
    theme: Any | None = None                     # 코스 테마

