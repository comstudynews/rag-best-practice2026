# 평가 데이터셋 및 RAG 평가 가이드

## 1. 평가 질문 수

종합실습에서는 **8~10개의 질문**으로 평가 과정을 학습합니다.

실제 프로젝트에서는 질문 수 자체보다 다음이 중요합니다.

- 실제 사용 질문을 대표하는가?
- 질문 유형이 다양한가?
- 정답 또는 정답 문서가 명확한가?
- 문서에 답이 없는 질문이 포함되어 있는가?
- 실제 실패 사례가 포함되어 있는가?

이 Best Practice는 확장된 평가 예제로 20개를 사용합니다.

## 2. AI를 이용한 평가셋 확장

AI를 이용해 평가 질문 후보를 만들 수 있습니다.

```text
Human Seed
   ↓
AI Paraphrase / Variation
   ↓
Human Review
   ↓
Deduplication
   ↓
Gold Test Set
```

검수 항목:

- 원래 질문의 의미와 정답 범위를 유지하는가?
- 정답 문서 라벨이 여전히 유효한가?
- 질문에 정답을 노출하지 않는가?
- 사실상 동일한 중복 질문은 아닌가?
- 지나치게 쉬운 표현으로 변형되지 않았는가?

## 3. Gold Document 정책

`gold_doc_ids`가 여러 개인 경우 `gold_doc_policy`를 사용합니다.

- `any`: 하나 이상의 Gold Document가 Top-K에 있으면 Hit
- `all`: 모든 Gold Document가 Top-K에 있어야 Hit

복합 질문처럼 여러 문서를 모두 요구하는 평가에서는 `all`을 사용할 수 있습니다.

## 4. Retrieval 평가

### Hit Rate@K

Gold Document가 Top-K에 포함되는지 평가합니다.

### MRR@K

Gold Document가 상위에 검색될수록 높은 점수를 부여합니다.

```text
rank 1 → 1.0
rank 2 → 0.5
rank 3 → 0.333...
MISS   → 0
```

`gold_doc_policy=all`인 경우 모든 Gold Document가 검색되었을 때 가장 낮은 순위의 Gold Document를 기준으로 Rank를 계산합니다.

### Keyword Coverage

정답 판단에 필요한 핵심 키워드가 검색 Context에 포함되는지 보조적으로 확인합니다.

## 5. Generation 평가

Generation은 자동 체크와 사람 검토를 함께 사용합니다.

자동 체크 예:

- Gold Keyword Coverage
- 근거 문서 ID 표시 여부
- Unanswerable 질문의 Abstention 문구 여부

사람 검토:

- 검색된 Context와 답변이 실제로 일치하는가?
- 질문에 직접 답하는가?
- 근거 없는 내용을 만들지 않는가?
- 중요한 조건이나 예외를 누락하지 않았는가?

자동 체크는 최종 정답 판정을 대신하지 않습니다.

## 6. 결과 해석

개선 전략을 적용해도 모든 질문이 좋아질 필요는 없습니다.

다음 네 가지로 구분합니다.

- 개선
- 동일
- 악화
- 판단 불가

Baseline에서 확인한 문제 유형이 실제로 개선되었는지를 우선 확인하고, 다른 유형에서 발생한 성능 저하는 Trade-off로 기록합니다.
