import os
from typing import List, Optional
import chromadb
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.schedule.rag.data_loader import load_tourism_documents

class VectorStoreManager:
    def __init__(self, documents: List[Document] = None, chroma_db_path: str = "./chroma_db", collection_name: str = "korean_tourism_collection", embedding_model_name: str = "jhgan/ko-sroberta-multitask"):
        self.chroma_db_path = chroma_db_path
        self.collection_name = collection_name
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        self.client = chromadb.PersistentClient(path=self.chroma_db_path)
        self.vectorstore = self._load_or_create_vectorstore(documents)

    def _load_or_create_vectorstore(self, documents: List[Document] = None):
        print(f"ChromaDB 컬렉션 '{self.collection_name}' 로드 또는 생성 시도 중...")
        
        try:
            # 기존 컬렉션 로드 시도
            # Chroma.from_existing_persist_dir은 실제 파일 시스템에 컬렉션이 존재하는지 확인합니다.
            vectorstore = Chroma(
                persist_directory=self.chroma_db_path,
                embedding_function=self.embeddings,
                collection_name=self.collection_name,
                client=self.client # PersistentClient 사용
            )
            # 컬렉션이 존재하고 문서가 있다면, 추가 적재 없이 로드합니다.
            if vectorstore._collection.count() > 0:
                print(f"컬렉션 '{self.collection_name}'이(가) 로드되었습니다. 현재 {vectorstore._collection.count()}개의 문서가 있습니다.")
                return vectorstore
            else:
                print(f"컬렉션 '{self.collection_name}'이(가) 비어있습니다. 새로 문서를 추가합니다.")
        except Exception as e:
            print(f"컬렉션 '{self.collection_name}'이(가) 없거나 로드에 실패했습니다. 새로 생성합니다. 오류: {e}")
        
        # 컬렉션이 없거나 비어있는 경우, 문서를 사용하여 새로 생성
        if documents:
            print(f"새로운 ChromaDB 컬렉션 '{self.collection_name}' 생성 중 (총 {len(documents)}개 문서)...")
            print("이 과정은 시간이 오래 걸릴 수 있으며, 배치 단위로 진행됩니다.")
            
            # --- 여기부터 배치 처리 및 진행도 표시 로직 ---
            batch_size = 1000 # 한 번에 처리할 문서 수
            num_documents = len(documents)
            
            # 첫 번째 배치로 ChromaDB를 초기화 (from_documents)
            # 이렇게 하면 초기화 시 자동으로 add_documents를 호출합니다.
            if num_documents > 0:
                print(f"배치 1/{((num_documents - 1) // batch_size) + 1} - 0/{num_documents} 문서 처리 중...")
                vectorstore = Chroma.from_documents(
                    documents=documents[:batch_size],
                    embedding=self.embeddings,
                    persist_directory=self.chroma_db_path,
                    collection_name=self.collection_name,
                    client=self.client
                )
                print(f"배치 1/{((num_documents - 1) // batch_size) + 1} - {min(batch_size, num_documents)}/{num_documents} 문서 처리 완료.")
            else:
                # 문서가 없는 경우 빈 vectorstore 반환 또는 에러 처리
                print("초기화할 문서가 제공되지 않았습니다. 빈 ChromaDB 컬렉션을 반환합니다.")
                return Chroma(
                    embedding_function=self.embeddings,
                    persist_directory=self.chroma_db_path,
                    collection_name=self.collection_name,
                    client=self.client
                )

            # 나머지 문서들을 add_documents를 사용하여 추가
            for i in range(batch_size, num_documents, batch_size):
                batch = documents[i:i + batch_size]
                current_batch_num = (i // batch_size) + 1
                total_batches = ((num_documents - 1) // batch_size) + 1
                
                print(f"배치 {current_batch_num}/{total_batches} - {i}/{num_documents} 문서 처리 중...")
                vectorstore.add_documents(batch)
                print(f"배치 {current_batch_num}/{total_batches} - {min(i + batch_size, num_documents)}/{num_documents} 문서 처리 완료.")
            
            print(f"총 {vectorstore._collection.count()}개의 문서로 컬렉션 '{self.collection_name}' 생성 완료.")
            return vectorstore
        else:
            raise ValueError("ChromaDB 컬렉션이 없으며, 초기화할 문서가 제공되지 않았습니다. `documents` 파라미터에 Document 리스트를 제공해주세요.")

    def get_retriever(self, **kwargs):
        if not self.vectorstore:
            raise ValueError("Vectorstore가 초기화되지 않았습니다.")
        return self.vectorstore.as_retriever(**kwargs)

    def get_document_count(self):
        if not self.vectorstore:
            return 0
        return self.vectorstore._collection.count()
    
    async def search_documents(
        self,
        query: str,
        top_k: int = 10,
        content_type_filter: Optional[list] = None,
    ):
        """
        쿼리(query)와 선택적 content_type_filter로 유사한 문서 top_k개를 비동기로 반환합니다.
        """
        retriever = self.get_retriever(search_kwargs={"k": top_k})
        docs = retriever.invoke(query)
        
        if content_type_filter:
            # contentTypeName이 필터에 포함된 것만 반환
            filtered = [
                doc for doc in docs if doc.metadata.get("contentTypeName").strip() in content_type_filter
            ]
            return filtered
        
        return docs


# 싱글턴 인스턴스 생성
vector_store = VectorStoreManager(
    chroma_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'chroma_db'))
)

# 이 파일을 직접 실행하여 ChromaDB 컬렉션을 생성/로드하는 코드 (최초 실행 시 반드시 필요)
if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    data_file_path = os.path.abspath(os.path.join(current_dir, 'crawled_data', 'public_tourism_data.jsonl')) # 경로 수정됨
    chroma_db_dir = os.path.abspath(os.path.join(current_dir, 'chroma_db')) # ChromaDB 저장 폴더 이름 변경

    print("\n--- ChromaDB 컬렉션 생성/로드 프로세스 시작 ---")

    # 먼저 문서 로드를 시도합니다. (컬렉션 유무와 상관없이)
    print("문서를 로드합니다...")
    all_tourism_docs = load_tourism_documents(data_file_path)

    if not all_tourism_docs:
        print("로드할 문서가 없습니다. ChromaDB 작업을 진행할 수 없습니다.")
    else:
        # VectorStoreManager를 초기화하고, 컬렉션이 없으면 이 단계에서 문서를 사용하여 생성합니다.
        # 컬렉션이 이미 있다면, 기존 컬렉션을 로드하고 문서를 추가하지 않습니다.
        # _load_or_create_vectorstore 메서드 내부에서 로드된 문서 수에 따라 적절히 처리됩니다.
        manager = VectorStoreManager(documents=all_tourism_docs, chroma_db_path=chroma_db_dir)
        
        print(f"\n최종 ChromaDB 컬렉션에 저장된 문서 수: {manager.get_document_count()}")
        
        # 2. 리트리버 테스트 (옵션)
        # 리트리버 테스트는 문서가 ChromaDB에 성공적으로 적재된 후에 실행됩니다.
        if manager.get_document_count() > 0:
            retriever = manager.get_retriever(k=3)
            query = "강원도 춘천의 분위기 좋은 카페 추천해줘"
            print(f"\n쿼리 '{query}'에 대한 리트리버 검색 결과:")
            retrieved_docs = retriever.invoke(query)
            for i, doc in enumerate(retrieved_docs):
                print(f"--- 문서 {i+1} ---")
                print(f"제목: {doc.metadata.get('title', 'N/A')}")
                print(f"카테고리: {doc.metadata.get('contentTypeName', 'N/A')}")
                print(f"주소: {doc.metadata.get('addr1', 'N/A')}")
                print(f"내용 일부: {doc.page_content[:100]}...")
                print("-" * 20)
        else:
            print("ChromaDB에 문서가 없어 리트리버 테스트를 건너뜝니다.")