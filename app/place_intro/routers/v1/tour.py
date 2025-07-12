from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
from fastapi import Query
import asyncio
import json

from app.place_intro.services.tour_data_loader import first_tour_data_loader, second_tour_data_loader
from app.place_intro.services.tour_service import get_preview_info, get_detail_info, get_llm_input

router = APIRouter(prefix="/api")

@router.get("/tour", response_class=StreamingResponse)
async def stream_tour_info(keyword: str = Query(..., description="검색 키워드")) -> StreamingResponse:
    async def event_stream() -> AsyncGenerator[bytes, None]:
        # [첫번째 할일] searchKeyword1 → preview
        keyword_items = await first_tour_data_loader(keyword)
        preview_view = await get_preview_info(keyword_items) 
        contentid = keyword_items[0].contentid
        contenttypeid = keyword_items[0].contenttypeid


        # 프리뷰 먼저 반환
        await asyncio.sleep(2)  # 🔸 test-  2초 대기
        yield json.dumps({
            "type": "preview",
            "data": preview_view.model_dump()
        }, ensure_ascii=False).encode("utf-8") + b"\n"
        print("PREVIEW_JSON:")
        print(json.dumps(preview_view.model_dump(), ensure_ascii=False))
        print()
        print()
        print()
        



        # [두번째/세번째 할일] 비동기 병렬 시작
        second_task = asyncio.create_task(
            second_tour_data_loader(contentid, contenttypeid)
        )

        async def run_detail_and_llm():
            common_info, image_info, intro_info, repeat_info = await second_task

            detail_task = asyncio.create_task(
                get_detail_info(contentid, contenttypeid, common_info, image_info, intro_info, repeat_info)
            )
            llm_task = asyncio.create_task(
                get_llm_input(contentid, contenttypeid, keyword_items[0], common_info, image_info, intro_info, repeat_info)
            )

            detail_result, llm_result = await asyncio.gather(detail_task, llm_task)

            await asyncio.sleep(5)  # 🔸 test-  2초 대기
            yield json.dumps({
                "type": "detail",
                "data": detail_result.model_dump()
            }, ensure_ascii=False).encode("utf-8") + b"\n"
            print("DETAIL_JSON:")
            print(json.dumps(detail_result.model_dump(), ensure_ascii=False))
            print()
            print()
            print()


            await asyncio.sleep(5)  # 🔸 test-  2초 대기
            yield json.dumps({
                "type": "llm_input",
                "data": llm_result.model_dump()
            }, ensure_ascii=False).encode("utf-8") + b"\n"
            print("LLM_JSON:")
            print(json.dumps(llm_result.model_dump(), ensure_ascii=False))
            print()
            print()
            print()



        async for chunk in run_detail_and_llm():
            yield chunk

    return StreamingResponse(event_stream(), media_type="application/json; charset=utf-8")
