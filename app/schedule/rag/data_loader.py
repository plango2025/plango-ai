import json
from typing import List
from langchain_core.documents import Document

def load_tourism_documents(file_path: str) -> List[Document]:
    """
    주어진 JSONL 파일에서 관광 데이터를 로드하여 Langchain Document 객체 리스트로 반환합니다.
    """
    documents = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line.strip())
                
                # 'outl' 필드가 문서의 주요 내용이 됩니다.
                page_content = str(data.get('outl') or '')
                
                # 메타데이터를 구성합니다.
                metadata = {
                    "title": data.get('title', 'N/A'),
                    "contentTypeName": data.get('content_type', 'N/A'), # 'content_type'을 'contentTypeName'으로 매핑
                    "addr1": data.get('addr1', 'N/A'),
                    # 필요한 다른 메타데이터 필드가 있다면 여기에 추가합니다.
                }
                
                # content_type이 없는 경우 기본값으로 "기타"를 사용
                if metadata["contentTypeName"] == "N/A":
                    print(f"경고: '{data.get('title', '제목 없음')}' 문서에 'content_type'이 없습니다. '기타'로 설정합니다.")
                    metadata["contentTypeName"] = "기타"

                # Langchain Document 객체 생성
                doc = Document(page_content=page_content, metadata=metadata)
                documents.append(doc)
    except FileNotFoundError:
        print(f"오류: 파일을 찾을 수 없습니다 - {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"오류: JSONL 파일 파싱 중 오류 발생 - {e}")
        return []
    except Exception as e:
        print(f"문서 로드 중 알 수 없는 오류 발생: {e}")
        return []

    print(f"총 {len(documents)}개의 관광 문서를 로드했습니다.")
    return documents

# 이 부분은 data_loader.py를 직접 실행하여 테스트할 때 유용합니다.
if __name__ == "__main__":
    import os
    # 현재 파일의 디렉토리
    current_dir = os.path.dirname(__file__)
    # public_tourism_data.jsonl 파일의 절대 경로
    # 예시: app/schedule/rag/crawled_data/public_tourism_data.jsonl
    data_file_path = os.path.abspath(os.path.join(current_dir, 'crawled_data', 'public_tourism_data.jsonl'))

    print(f"데이터 파일 경로: {data_file_path}")

    # 함수 테스트
    loaded_docs = load_tourism_documents(data_file_path)
    if loaded_docs:
        print("\n--- 로드된 문서 샘플 (첫 2개) ---")
        for i, doc in enumerate(loaded_docs[:2]):
            print(f"문서 {i+1}:")
            print(f"  Title: {doc.metadata.get('title')}")
            print(f"  Content Type: {doc.metadata.get('contentTypeName')}")
            print(f"  Address: {doc.metadata.get('addr1')}")
            print(f"  Page Content (첫 100자): {doc.page_content[:100]}...")
            print("-" * 30)
    else:
        print("문서를 로드하지 못했습니다.")