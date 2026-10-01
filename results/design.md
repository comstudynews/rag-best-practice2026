# RAG 시스템 설계 문서

## 1. 문제 정의

제품 매뉴얼 문서를 기반으로 사용자의 기술 문의에 답변하는 RAG 시스템을 구축한다.

## 2. 대상 사용자

제품 사용자가 설치, 설정, 오류 해결 관련 질문을 입력한다.

## 3. Baseline RAG 구조

```text
PDF Document
 → Loader
 → Chunking
 → Embedding
 → FAISS Vector Store
 → Retriever
 → LLM Answer
```

## 4. 평가 목적

Baseline RAG에서 발생하는 검색 실패와 답변 오류를 확인하고 개선한다.

## 5. 개선 전략

선택: Hybrid Search

선택 이유:

- Vector Search는 의미 기반 검색에 강점이 있다.
- 제품명, 코드명, 오류번호 같은 정확한 키워드 검색에는 한계가 있다.
- BM25와 Vector Search를 결합하여 검색 정확도를 개선한다.

## 6. 평가 방법

동일한 테스트 질문으로 Baseline과 개선 버전을 비교한다.

평가 항목:

- Retrieval: 관련 문서 검색 여부
- Generation: 검색 근거 기반 답변 여부
- Hallucination 발생 여부
