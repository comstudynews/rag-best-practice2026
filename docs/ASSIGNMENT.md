# 종합실습 과제 안내

## 1. 과제 목표

RAG Pipeline을 구현한 뒤 실제 테스트 결과를 분석하여 문제를 진단하고, **문제에 적합한 개선 전략을 1개 이상 적용한 후 동일한 질문으로 전·후 결과를 비교**합니다.

핵심 흐름:

```text
문제 정의
→ Baseline RAG 구현
→ 테스트 질문 구성
→ Baseline 결과 평가
→ 문제 진단
→ 개선 전략 적용
→ 동일 질문 재평가
→ 결과 및 한계 정리
```

## 2. 필수 수행 항목

### A. 문제 및 문서 범위 정의

다음을 정리합니다.

- 대상 사용자
- 검색 대상 문서
- 답변할 질문 범위
- 문서에 근거가 없을 때의 응답 방식

### B. Baseline RAG 구현

```text
Loader
→ Text Splitter
→ Embedding
→ Vector Store
→ Retriever
→ Prompt
→ LLM
```

### C. 테스트 질문 구성

**교재 기준 8~10개**의 질문을 준비합니다.

다음 유형을 포함합니다.

- 정답이 명확한 질문
- 표현이 다른 질문
- 키워드·코드 중심 질문
- 복합 질문
- 문서에 없는 질문

이 Best Practice는 평가셋 확장 사례를 보여주기 위해 20개를 사용합니다. 학생 과제의 필수 개수가 20개라는 의미는 아닙니다.

### D. Baseline 결과 기록

개선 전략을 적용하기 전에 다음을 먼저 기록합니다.

- Top-K 검색 문서
- 정답 문서 포함 여부
- 정답 문서 순위
- 최종 답변
- 문서 근거 여부
- 발견한 문제

### E. 문제 진단

예:

| Baseline에서 확인한 문제 | 검토할 개선 방법 |
|---|---|
| 비슷한 Chunk가 반복 검색됨 | MMR |
| 정확한 코드·약어·제품명이 약함 | BM25 / Hybrid / Ensemble |
| 문맥이 부족함 | ParentDocumentRetriever |
| 질문 표현에 따라 결과 편차가 큼 | MultiQuery / Query Rewrite |
| 관련 문서는 찾지만 순위가 좋지 않음 | Reranker |
| 긴 Context에서 핵심 정보가 묻힘 | LongContextReorder |
| 검색 실패 시 재작성·재검색 필요 | Agentic RAG |

개선 전략은 **Baseline에서 실제로 관찰한 문제와 연결**해야 합니다.

### F. 개선 전략 적용

최소 1개 이상의 개선 전략을 적용합니다.

이 Best Practice의 비교 전략은 Hybrid Search입니다. 다만 실행 결과에서 키워드 검색 약점이 뚜렷하지 않다면 "Hybrid가 필수였다"고 결론내리지 않습니다.

### G. 동일 조건 재평가

Baseline에서 사용한 **동일한 질문**으로 Improved Pipeline을 다시 실행합니다.

Retrieval:

- 정답 문서가 Top-K에 포함되는가?
- 정답 문서의 순위는 어떻게 변했는가?
- 중복·무관 문서는 줄었는가?

Generation:

- 검색 Context와 답변이 일치하는가?
- 질문에 직접 답하는가?
- 근거가 없을 때 임의의 내용을 만들지 않는가?

### H. 결과 및 한계 정리

다음을 기록합니다.

- Baseline에서 확인한 문제
- 개선 전략과 선택 이유
- 개선된 결과
- 동일하거나 악화된 결과
- Trade-off
- 남은 한계
- 추가 개선 방향

## 3. 평가 데이터셋 구성 원칙

AI를 이용해 질문을 확장할 수 있습니다.

```text
사람이 Seed 질문·정답 기준 정의
→ AI로 표현 변형 후보 생성
→ 사람 검수
→ 중복·오류 제거
→ Gold Set 반영
```

AI 생성 결과를 검수 없이 Gold Set으로 사용하지 않습니다.

## 4. 제출물

교재 기준 실제 제출 구조:

```text
final_capstone/practice/
├── src/
│   └── capstone_compare.py
└── results/
    ├── design.md
    └── evaluation.md
```

이 Best Practice 저장소는 별도 Repository이므로 저장소 루트가 `final_capstone/practice/`에 해당합니다. 코드의 유지보수성을 위해 내부 구현을 여러 파일로 분리했지만, `src/capstone_compare.py`를 전체 실행 진입점으로 유지합니다.

## 5. 진행 안내

- 종합실습: 1교시 시작
- 구현 및 테스트: 가급적 16:00 이전 마무리
- Wrap-up Quiz: 16:00 오픈, 별도 안내
- 제출 마감: 16:30
- 별도 발표 없음

## 6. 최종 확인

- [ ] Baseline RAG가 정상 실행된다.
- [ ] 테스트 질문 8~10개를 준비했다.
- [ ] Baseline 결과를 먼저 기록했다.
- [ ] 문제를 확인한 뒤 개선 전략을 선택했다.
- [ ] 개선 전략을 1개 이상 적용했다.
- [ ] 동일한 질문으로 전·후를 비교했다.
- [ ] Retrieval과 Generation을 나누어 확인했다.
- [ ] 개선되지 않은 결과도 원인과 한계를 기록했다.
- [ ] 문서에 없는 질문의 응답을 확인했다.
- [ ] API Key와 민감정보가 소스에 포함되지 않았다.
