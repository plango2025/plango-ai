import textwrap

from dotenv import load_dotenv
from fastapi import HTTPException
from pydantic import ValidationError
from openai import OpenAI, OpenAIError

from app.schemas.schedule_request import ScheduleRequest
from app.schemas.schedule_response import ScheduleResponse

from app.config import settings

load_dotenv()
client = OpenAI(api_key=settings.OPENAI_API_KEY)


async def generate_schedule(request: ScheduleRequest) -> ScheduleResponse:
    """
    사용자의 여행 조건에 따라 AI가 추천하는 여행 일정을 생성합니다.

    - 필수 장소, 여행지, 기간, 동행자, 스타일, 일정 수, 예산 등을 기반으로 
      여행 일정을 구성하도록 프롬프트를 생성합니다.
    - OpenAI의 GPT 모델을 호출하여 추천 일정을 생성하고,
      결과를 ScheduleResponse 모델로 파싱하여 반환합니다.

    Args:
        ScheduleRequest: 여행 일정 생성을 위한 사용자 입력 정보

    Returns:
        ScheduleResponse: 추천된 여행 일정 정보

    Raises:
        HTTPException(502): OpenAI API 호출 실패 또는 AI 응답 형식 오류
        HTTPException(500): 기타 서버 내부 오류
    """

    # 필수 장소 리스트를 문자열로 변환
    if not request.required_places:
        # 필수 장소가 없는 경우
        required_place_str = "없음"
    else:
        # 필수 장소가 있는 경우, 리스트를 문자열로 변환
        required_place_str = ", ".join(
            f"{p.name} ({p.address})" for p in request.required_places
        )

    # 각 항목이 None이면 기본값으로 대체
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
        - 예산: {budget}만원
        - 비고: {extra}

        응답은 아래 JSON 형식만 사용하세요:
        {{
          "title": "...",
          "days": [
            {{
              "day": 1,
              "schedules": [
                {{
                  "order": 1,
                  "name": "...",
                  "description": "...",
                  "image": "https://..."
                }}
              ]
            }}
          ]
        }}
    """)

    try:
        # LLM 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a travel itinerary generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        # LLM 응답 문자열 처리
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        elif content.startswith("```"):
            content = content.replace("```", "").strip()

        # ScheduleResponse로 파싱
        return ScheduleResponse.model_validate_json(content)

    except OpenAIError as e:
        # Bad Gateway (502)
        raise HTTPException(status_code=502, detail=f"OpenAI 호출 실패: {str(e)}")

    except ValidationError as e:
        # Bad Gateway (502)
        raise HTTPException(status_code=502, detail="AI의 응답 형식이 올바르지 않습니다.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")