# 종합실습 과제 안내

## 1. 과제 목표

이번 종합실습에서는 기업용 기술지원 문서를 기반으로 RAG Pipeline을 구현하고, **Baseline의 검색·답변 품질을 평가한 뒤 문제에 맞는 개선 전략을 적용하고 동일 조건에서 효과를 검증**합니다.

완성 코드의 양보다 다음 흐름이 중요합니다.

```text
문제 정의
→ Baseline RAG
→ 평가 데이터셋
→ Baseline 평가
→ 문제 진단
→ 개선 전략
→ 동일 질문 재평가
→ 결과 및 한계 정리
```

## 2. 필수 수행 항목

### A. 문제 및 문서 범위 정의

- 대상 사용자 정의
- 문서 범위 정의
- 답변 가능한 질문 범위 정의
- 문서에 근거가 없을 때의 응답 원칙 정의

### B. Baseline RAG 구현

다음 구성요소를 연결합니다.

```text
Loader
→ Text Splitter
→ Embedding
→ Vector Store
→ Retriever
→ Prompt
→ LLM
```

Baseline은 Dense Similarity Search를 사용합니다.

### C. 평가 데이터셋 구축

최소 10개 이상을 권장합니다.

다음 유형을 포함합니다.

- 정답이 명확한 질문
- 표현이 다른 질문
- 정확 키워드·코드 질문
- 복합 질문
- 문서에 없는 질문

Gold Set에는 최소한 다음 정보가 필요합니다.

- question
- gold_doc_ids
- gold_keywords
- answerable
- category

### D. Baseline 평가

질문마다 다음을 기록합니다.

- Top-K 검색 문서
- 정답 문서 포함 여부
- 정답 문서 순위
- 최종 답변
- 근거 일치 여부
- 발견한 문제

### E. 문제 진단

예:

| 문제 | 후보 개선 방법 |
|---|---|
| 정확한 코드·약어 검색이 약함 | BM25 / Hybrid |
| 비슷한 문서가 반복 검색됨 | MMR |
| 관련 문서는 찾지만 순위가 좋지 않음 | Reranker |
| 질문 표현에 따라 결과 편차가 큼 | MultiQuery / Query Rewrite |
| 검색 Context가 너무 짧음 | ParentDocumentRetriever |

### F. 개선 전략 적용

최소 1개 이상의 개선을 적용합니다.

참조 구현에서는 **Hybrid Search(Dense + BM25)** 를 사용합니다.

### G. 동일 조건 재평가

Baseline과 동일한 Gold Set을 사용합니다.

비교 대상:

- Hit Rate@K
- MRR@K
- 질문별 정답 문서 순위
- 최종 답변의 근거성
- 문서에 없는 질문의 처리

### H. 결과 및 한계 정리

다음을 반드시 설명합니다.

- Baseline에서 발견한 문제
- 개선 전략을 선택한 이유
- 개선된 질문
- 동일하거나 악화된 질문
- Trade-off
- 남은 한계
- 추가 개선 방향

## 3. 권장 진행 시간

하루 종합실습 기준 예시입니다.

| 구간 | 수행 내용 |
|---|---|
| 1교시 | 문제 정의, 저장소 구조 확인, 환경 점검 |
| 2교시 | Baseline RAG 구현 |
| 3교시 | 테스트 질문·Gold Set 구성 |
| 4교시 | Baseline 실행 및 Retrieval 분석 |
| 오후 초반 | 문제 진단 및 개선 전략 적용 |
| 오후 중반 | 동일 질문셋 재평가 및 Generation 확인 |
| 15:00 이후 | 결과 문서 정리, 실행 재현성 점검 |
| 16:00 이후 | 최종 제출 확인 및 별도 Quiz 진행 |

## 4. 제출 결과

최소 다음 산출물이 확인되어야 합니다.

```text
src/
  RAG 구현 및 평가 코드

data/eval/
  평가 질문셋

results/design.md
  문제 정의·설계·개선 전략 선택 이유

results/evaluation.md
  Baseline 및 개선 전·후 결과와 한계
```

## 5. 평가 시 유의사항

- 개선 기법의 개수가 많다고 높은 평가를 받는 것은 아닙니다.
- Baseline 문제와 개선 전략이 연결되어야 합니다.
- 동일한 질문으로 전·후를 비교해야 합니다.
- 결과가 개선되지 않은 경우도 원인을 설명하면 의미 있는 결과입니다.
- AI를 이용해 평가 질문을 확장할 수 있으나, Gold Set은 사람이 검수해야 합니다.
