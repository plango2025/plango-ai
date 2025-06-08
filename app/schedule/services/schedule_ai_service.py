from fastapi import HTTPException
from pydantic import ValidationError
from openai import OpenAI, OpenAIError
from typing import List
import logging as logger
import json

from app.schedule.schemas.schedule import Schedule
from app.schedule.schemas.schedule_create_request import ScheduleCreateRequest
from app.schedule.services.tour_place_service import search_place_info
from app.config.settings import settings
from app.schedule.rag.vector_store import vector_store

from app.schedule.prompts.prompts import (
    GENERATE_SCHEDULE_PROMPT_TEMPLATE,
    UPDATE_SCHEDULE_PROMPT_TEMPLATE,
    REGENERATE_SCHEDULE_PROMPT_TEMPLATE,
)

class ScheduleAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.vector_store = vector_store

    async def generate_schedule(self, request: ScheduleCreateRequest) -> Schedule :
        """
        사용자의 여행 조건에 따라 AI가 추천하는 여행 일정을 생성합니다.
        """

        # 1. 여행 파라미터 포맷팅
        required_place_names = [place.name for place in request.required_places] if request.required_places else []
        required_place_str = ", ".join(required_place_names) if required_place_names else "없음"

        # 2. 검색할 총 장소 개수 계산
        # (하루 당 일정 개수 * 여행 다녀오는 일수 * 2)
        # request.schedule_count가 None일 경우 기본값 설정 (예: 3)
        effective_schedule_count = request.schedule_count if request.schedule_count is not None else 3
        
        # 각 쿼리당 검색할 장소 개수
        num_places_per_query = effective_schedule_count * request.duration * 2

        # 3. 벡터 DB 검색 쿼리 및 필터링
        context_places_info = ""

        # Query 0: 필수 장소
        if required_place_names:
            query_required = required_place_str
            
            retrieved_docs_required = await self.vector_store.search_documents(
                query_required,
                top_k=len(required_place_names),
            )
            context_places_info += f"\n** --- 필수 방문 장소 --- **\n"
            # 각 doc에서 title만 추출하여 추가
            for doc in retrieved_docs_required:
                title = doc.metadata.get("title")
                if title: # 빈 문자열이 아니면 추가
                    context_places_info += "- " + title + "\n"


        # Query 1: 관광지 | 문화시설 | 레포츠 | 쇼핑
        query_general = f"카테고리: 관광지, 문화 시설, 레포츠, 쇼핑, {request.destination}"
        general_content_filter = ["관광지", "문화시설", "레포츠", "쇼핑"]
            
        retrieved_docs_general = await self.vector_store.search_documents(
            query_general,
            top_k=num_places_per_query * 4,
            content_type_filter=general_content_filter
        )
        context_places_info += f"\n** --- {request.destination} 일반 장소 (관광/문화/레포츠/쇼핑) --- **\n"


        # 각 doc에서 title만 추출하여 추가
        for doc in retrieved_docs_general:
            title = doc.metadata.get("title")
            if title: # 빈 문자열이 아니면 추가
                context_places_info += "- " + title + "\n"

        # Query 2: 음식점 (후식 말고 제대로 식사가 가능한 곳)
        query_restaurants = f"{request.destination}에서 {request.companion}와 함께 갈 만한 음식점(후식 말고 제대로 식사가 가능한 곳) 추천해줘."
        restaurant_content_filters = ["음식점"]
        
        retrieved_docs_restaurants = await self.vector_store.search_documents(
            query_restaurants,
            top_k=num_places_per_query,
            content_type_filter=restaurant_content_filters
        )
        context_places_info += f"\n** --- {request.destination} 음식점 --- **\n"
        # 각 doc에서 title만 추출하여 추가
        for doc in retrieved_docs_restaurants:
            title = doc.metadata.get("title")
            if title: # 빈 문자열이 아니면 추가
                context_places_info += "- " + title + "\n"


        # Query 3: 카페
        query_cafes = f"{request.destination}에서 {request.companion}와 함께 갈 만한 카페 추천해줘."
        cafe_content_filters = ["음식점"] 
        
        retrieved_docs_cafes = await self.vector_store.search_documents(
            query_cafes,
            top_k=num_places_per_query,
            content_type_filter=cafe_content_filters
        )
        context_places_info += f"\n** --- {request.destination} 카페 --- **\n"
        # 각 doc에서 title만 추출하여 추가
        for doc in retrieved_docs_cafes:
            title = doc.metadata.get("title")
            if title: # 빈 문자열이 아니면 추가
                context_places_info += "- " + title + "\n"
                
        # Query 4: 숙소
        query_accommodations = f"{request.destination}에서 {request.companion}와 함께 갈 만한 숙박 업소 추천해줘."
        accommodation_content_filters = ["숙박"]
        
        retrieved_docs_accommodations = await self.vector_store.search_documents(
            query_accommodations,
            top_k=num_places_per_query,
            content_type_filter=accommodation_content_filters
        )
        context_places_info += f"\n** --- {request.destination} 숙소 --- **\n"
        # 각 doc에서 title만 추출하여 추가
        for doc in retrieved_docs_accommodations:
            title = doc.metadata.get("title")
            if title: # 빈 문자열이 아니면 추가
                context_places_info += "- " + title + "\n"


        # 3. 프롬프트 포맷팅
        duration_str = f"{request.duration-1}박 {request.duration}일" if request.duration is not None and request.duration > 1 else "당일치기"
        budget_str = f"{request.budget}만원" if request.budget is not None else "예산 없음"
        
        prompt = GENERATE_SCHEDULE_PROMPT_TEMPLATE.format(
            context_places_info=context_places_info,
            required_place_str=required_place_str,
            destination=request.destination,
            duration=duration_str,
            companion=request.companion,
            style=request.style,
            schedule_count=request.schedule_count,
            budget=budget_str,
            extra=request.extra,
        )

        # 디버깅용 출력
        print(f"Generated Prompt:\n{prompt}")

        # LLM 호출
        schedule = self._generate_schedule_from_prompt(prompt)
        
        # 장소 정보 보완
        schedule = self._fill_place_details(schedule)
        
        # 생성된 일정 반환
        return schedule


    async def update_schedule_with_feedback(
        self, 
        parameters: ScheduleCreateRequest, 
        schedule: Schedule, 
        pinned_places: List[str], 
        banned_places: List[str], 
        new_feedback: str, 
        feedback_history: List[str]
    ) -> Schedule:
        """
        사용자의 피드백을 바탕으로 AI가 기존 여행 일정을 수정합니다.
        """

        # 프롬프트 작성
        prompt = UPDATE_SCHEDULE_PROMPT_TEMPLATE.format(
            parameters=parameters,
            schedule=schedule,
            pinned_places=pinned_places,
            banned_places=banned_places,
            new_feedback=new_feedback,
            feedback_history=feedback_history,
        )
    
        # LLM 호출
        schedule = self._generate_schedule_from_prompt(prompt)
        
        # 장소 정보 보완
        schedule = self._fill_place_details(schedule)
        
        # 생성된 일정 반환
        return schedule
    

    async def regenerate_schedule(
        self, 
        parameters: ScheduleCreateRequest, 
        pinned_places: List[str], 
        banned_places: List[str], 
        feedback_history: List[str]
    )-> Schedule:
        """
        기존 요구 사항을 바탕으로 여행 일정을 새로 생성합니다.
        """

        # 프롬프트 작성
        prompt = REGENERATE_SCHEDULE_PROMPT_TEMPLATE.format(
            parameters=parameters,
            pinned_places=pinned_places,
            banned_places=banned_places,
            feedback_history=feedback_history,
        )

        # LLM 호출
        schedule = self._generate_schedule_from_prompt(prompt)
        
        # 장소 정보 보완
        schedule = self._fill_place_details(schedule)
        
        # 생성된 일정 반환
        return schedule

    
    def _generate_schedule_from_prompt(self, prompt: str) -> Schedule:
        """
        주어진 프롬프트를 기반으로 AI가 여행 일정을 생성합니다.
        """

        try:
            # LLM 호출
            response = self.client.chat.completions.create(
                model="gpt-4o",
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

            # 모델 파싱
            schedule = Schedule.model_validate_json(content)

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


    def _fill_place_details(self, schedule: Schedule) -> Schedule:
        """
        Schedule 객체의 각 장소에 대해 이미지, 위도, 경도 등의 세부 정보를 채웁니다.
        """
        for day in schedule.days:
            for place in day.places:
                place_info = search_place_info(place.name)
                place.image = place_info.firstimage2 or place_info.firstimage
                place.latitude = float(place_info.mapy) if place_info.mapy else None
                place.longitude = float(place_info.mapx) if place_info.mapx else None
        
        return schedule


# 싱글턴 인스턴스 생성
schedule_ai_service = ScheduleAIService()