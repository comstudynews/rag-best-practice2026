# 종합실습 설계 문서 — Best Practice

## 1. 문제 정의

DEMO-RAG-2026 기술지원 문서는 설치, 계정, 네트워크, 백업, 보안, 라이선스, 오류 코드 등 여러 문서로 나뉘어 있다.

사용자는 자연어 질문뿐 아니라 오류 코드, 포트 번호, 파일 경로, 제품 식별자처럼 정확한 문자열이 포함된 질문도 한다.

목표는 문서 기반 기술지원 RAG를 구현하고, Baseline 결과에서 실제 문제를 확인한 뒤 적합한 개선 전략을 적용하여 동일 질문으로 효과를 비교하는 것이다.

## 2. 대상 사용자

- 일반 사용자
- 조직 관리자
- 기술지원 담당자

## 3. 문서 및 답변 범위

답변 가능:

- 설치
- 계정 및 접근
- 네트워크
- 백업 및 복구
- 오류 코드
- 보안 운영
- 라이선스 기능
- 로그 경로

답변 제한:

- 문서에 없는 가격
- 문서에 없는 고객센터 연락처
- 문서에 없는 정책

근거가 없을 때는 다음과 같이 답한다.

```text
제공된 문서에서 확인할 수 없습니다.
```

## 4. Baseline 구조

```text
Markdown Documents
→ TextLoader
→ RecursiveCharacterTextSplitter
→ OpenAIEmbeddings
→ FAISS
→ Similarity Retriever
→ Grounded Prompt
→ ChatOpenAI
```

설정:

- Chunk Size: 420
- Chunk Overlap: 80
- Top-K: 3
- Embedding: text-embedding-3-small
- Chat Model: gpt-4o-mini

## 5. 평가 데이터셋

Best Practice에서는 20문항을 사용한다.

교재의 종합실습 기준은 8~10개이며, 이 샘플은 평가셋 확장 사례를 보여주기 위해 문항 수를 늘렸다.

질문 유형:

- fact
- paraphrase
- keyword
- compound
- security
- unanswerable

## 6. Baseline 평가 계획

다음 지표와 결과를 먼저 확인한다.

Retrieval:

- Hit Rate@3
- MRR@3
- Gold Document Rank
- Keyword Coverage
- 질문별 Top-3 문서

Generation:

- 검색 Context 근거 일치
- 질문에 대한 직접성
- Gold Keyword Coverage
- 근거 문서 ID 표시
- Unanswerable 질문의 Abstention

## 7. 개선 전략 선택 원칙

개선 기법은 Baseline 실행 전에 확정하지 않는다.

먼저 다음과 같은 실패 여부를 확인한다.

- 정확한 코드·약어·제품 식별자의 검색 순위가 낮은가?
- 관련 문서가 Top-K에 포함되지 않는가?
- 유사 문서가 반복 검색되는가?
- 질문 표현에 따라 검색 결과 편차가 큰가?
- 검색은 되었지만 답변에 필요한 문맥이 부족한가?

## 8. 이 Best Practice의 비교 전략

이 샘플은 기술지원 문서의 특성을 고려해 **Hybrid Search(Dense + BM25)** 를 비교 전략으로 구현한다.

가설:

- Dense Retrieval은 의미 기반 질문에 강하다.
- BM25는 오류 코드·경로·제품 식별자 같은 정확 문자열 검색을 보완할 수 있다.

단, 실제 Baseline에서 키워드 유형의 약점이 확인되지 않으면 Hybrid가 반드시 필요한 개선이라고 결론내리지 않는다.

## 9. 재평가 방법

Baseline과 Improved Pipeline에 동일한 20문항을 사용한다.

비교:

- Hit Rate@3
- MRR@3
- 질문별 Rank
- Keyword Coverage
- Generation 자동 보조 체크
- 사람의 근거성 검토

## 10. 예상 한계

- 문서와 평가셋 규모가 실제 서비스보다 작음
- BM25/Dense 가중치가 고정값임
- 실제 사용자 로그가 없음
- Generation 품질은 자동 지표만으로 완전히 판단할 수 없음
- 임베딩 모델 변경 시 결과가 달라질 수 있음

## 11. 추가 개선 방향

실제 Baseline 문제에 따라 다음을 검토할 수 있다.

- MMR
- Reranker
- Query Rewrite
- MultiQuery
- ParentDocumentRetriever
- LongContextReorder
- Agentic RAG
