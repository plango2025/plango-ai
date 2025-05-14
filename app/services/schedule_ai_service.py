import textwrap
import logging as logger

from fastapi import HTTPException
from pydantic import ValidationError
from openai import OpenAI, OpenAIError

from app.schemas.schedule import Schedule
from app.schemas.schedule_request import ScheduleRequest
from app.services.tour_place_service import search_place_info
from app.config import settings


class ScheduleAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_schedule(self, request: ScheduleRequest) -> Schedule :
        """
        사용자의 여행 조건에 따라 AI가 추천하는 여행 일정을 생성합니다.
        """
        # 필수 장소 리스트를 문자열로 변환
        if not request.required_places:
            required_place_str = "없음"
        else:
            required_place_str = ", ".join(
                f"{p.name} ({p.address})" for p in request.required_places
            )

        # None 값에 기본값 설정
        destination = request.destination or "랜덤"
        duration = request.duration or "랜덤"
        companion = request.companion or "지정 안 함"
        style = request.style or "랜덤"
        schedule_count = request.schedule_count if request.schedule_count is not None else 5
        budget = f"{request.budget}만원" if request.budget is not None else "제한 없음"
        extra = request.extra or "없음"

        # 프롬프트 작성
        prompt = textwrap.dedent(f"""\ 
            다음 조건에 맞춰 여행 일정을 JSON으로 작성하세요.

            - 필수 장소: {required_place_str}
            - 지역: {destination}
            - 기간: {duration}
            - 동행: {companion}
            - 스타일: {style}
            - 하루 일정 수: {schedule_count}
            - 예산: {budget}
            - 비고: {extra}

            응답은 아래 JSON 형식만 사용하세요:
            {{
              "title": "...",
              "days": [
                {{
                  "day": 1,
                  "places": [
                    {{
                      "order": 1,
                      "name": "...",
                      "description": "...",
                      "image": null,
                      "latitude": null,
                      "longitude": null
                    }}
                  ]
                }}
              ]
            }}
        """)

        try:
            # LLM 호출
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a travel itinerary generator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            # 응답 파싱
            content = response.choices[0].message.content.strip()
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            elif content.startswith("```"):
                content = content.replace("```", "").strip()

            schedule = Schedule.model_validate_json(content)

            # 장소 정보 보완
            for day in schedule.days:
                for place in day.places:
                    place_info = search_place_info(place.name)
                    place.image = place_info.firstimage2 or place_info.firstimage
                    place.latitude = float(place_info.mapy) if place_info.mapy else None
                    place.longitude = float(place_info.mapx) if place_info.mapx else None

            return schedule

        except OpenAIError as e:
            logger.error(f"OpenAI API 호출 실패: {str(e)}")
            raise HTTPException(status_code=502, detail=f"OpenAI 호출 실패: {str(e)}")

        except ValidationError as e:
            logger.error(f"AI 응답 형식 오류: {str(e)}")
            raise HTTPException(status_code=502, detail="AI의 응답 형식이 올바르지 않습니다.")

        except Exception as e:
            logger.error(f"서버 내부 오류: {str(e)}")
            raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


schedule_ai_service = ScheduleAIService()