# TourAPI - detailImage1 (이미지정보조회) 응답 중 필요한 필드만 골라 담은 스키마

from typing import Any
from pydantic import BaseModel


class ImageInfoItem(BaseModel):
    contentid: int                        # 콘텐츠 ID
    imgname: Any | None = None                # 이미지명
    originimgurl: Any | None = None           # 원본 이미지 URL (약 500x333)
    serialnum: Any | None = None              # 이미지 일련번호
    cpyrhtDivCd: Any | None = None            # 저작권 유형 (Type1, Type3)
    smallimageurl: Any | None = None          # 썸네일 이미지 URL (약 160x100)



