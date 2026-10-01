# 종합실습 평가 결과

> 현재 파일은 **실행 전 안내 템플릿**입니다.  
> `uv run --locked python src/capstone_compare.py`를 실행하면 실제 Baseline / Improved 결과로 이 파일이 갱신됩니다.

## 실행 후 포함되는 내용

- 비교 조건
- Baseline Hit Rate@3 / MRR@3
- Baseline 문제 진단
- Hybrid Search 적용의 타당성 판단
- 질문 유형별 Retrieval 지표
- 20개 질문별 Baseline / Improved Rank
- Keyword Coverage
- Baseline / Improved 최종 답변
- Generation 자동 보조 체크
- 사람 검토 체크리스트
- 개선 / 동일 / 악화 결과 구분
- Trade-off
- 남은 한계
- 추가 개선 방향

## 해석 원칙

실제 실행 결과가 우선입니다.

Hybrid Search를 적용했다고 결과가 자동으로 개선되는 것은 아닙니다. Baseline에서 문제를 확인하고, 같은 질문으로 다시 평가한 결과를 근거로 개선 여부를 판단합니다.
