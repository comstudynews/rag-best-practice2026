# 종합실습 평가 결과 작성 예시

> 이 문서는 결과 해석의 Best Practice 예시입니다.  
> 실제 수치는 `src/run_compare.py` 실행 후 생성되는 `runtime_comparison.md`를 기준으로 작성합니다.

## 1. 비교 조건

| 항목 | Baseline | Improved |
|---|---|---|
| Knowledge | 동일 | 동일 |
| Chunk Size | 420 | 420 |
| Chunk Overlap | 80 | 80 |
| Embedding | text-embedding-3-small | 동일 |
| Vector Store | FAISS | 동일 |
| Top-K | 3 | 3 |
| Dense | Similarity | Similarity |
| Sparse | 없음 | BM25 |
| Fusion | 없음 | Ensemble 0.6/0.4 |

## 2. Baseline 문제

다음 질문 유형에서 검색 결과를 중점적으로 확인한다.

- 정확한 오류 코드
- 파일 경로
- 포트 번호
- 제품 식별자

예:

```text
ERR-NET-403 오류의 원인과 우선 점검 순서를 알려 주세요.
AsterDesk-ENT는 무엇을 의미하나요?
Linux 서버의 기본 백업 디렉터리는 어디인가요?
```

## 3. 개선 전략 선택 이유

Dense Search는 의미적 유사성에 강하고 BM25는 정확 키워드에 강하다.

따라서 기술 문서의 자연어 질문과 코드·경로 질문을 함께 처리하기 위해 Hybrid Search를 선택했다.

## 4. 개선 전·후 비교

`runtime_comparison.md`를 바탕으로 아래를 작성한다.

- Hit Rate@3:
- MRR@3:
- 순위가 개선된 질문:
- 변화가 없는 질문:
- 순위가 하락한 질문:

## 5. Generation 비교

확인 항목:

- 검색 Context와 최종 답변이 일치하는가?
- 문서에 없는 가격·전화번호를 추측하지 않는가?
- 근거 문서 ID가 포함되는가?

## 6. 결과 해석

좋은 분석은 "Hybrid Search가 더 좋았다"로 끝나지 않는다.

다음 수준까지 설명한다.

- 어떤 질문 유형에서 개선되었는가?
- 왜 그 유형에서 개선되었는가?
- 어떤 질문에서는 차이가 없었는가?
- 어떤 Trade-off가 발생했는가?

## 7. 한계

- 문서와 평가셋 규모가 실제 서비스보다 작음
- BM25/Dense 가중치가 고정값임
- 실제 사용자 로그가 포함되지 않음
- Generation 평가는 일부 사람 검토가 필요함

## 8. 추가 개선

- MMR
- Reranker
- Query Rewrite
- MultiQuery
- Metadata Filter
- Chunk 전략 비교
- 실제 사용자 실패 질문 추가
