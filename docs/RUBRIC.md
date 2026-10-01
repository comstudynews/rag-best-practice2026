# 종합실습 평가 중점사항

Best Practice는 다음 네 가지 관점에서 확인할 수 있도록 구성합니다.

## 1. 기본 RAG Pipeline 구현

확인 내용:

- Loader
- Text Splitter
- Embedding
- Vector Store
- Retriever
- Prompt
- LLM
- End-to-End 실행
- 검색된 문서 직접 확인

## 2. Baseline 평가 및 문제 진단

확인 내용:

- 다양한 유형의 테스트 질문
- Baseline 결과를 먼저 기록
- Top-K 검색 결과 확인
- 정답 문서 포함 여부와 순위 확인
- Retrieval / Generation 문제 구분
- 실제 실패 사례에 근거한 진단

## 3. 검색 품질 개선 전략 적용

확인 내용:

- Baseline 문제와 개선 전략의 논리적 연결
- 개선 전략을 선택한 이유
- 개선 코드 정상 실행
- 단순 기능 추가가 아닌 문제 해결 목적의 구현

## 4. 개선 전·후 비교 및 결과 설명

확인 내용:

- 동일 질문셋 사용
- Retrieval 비교
- Generation 비교
- 개선·동일·악화 결과 구분
- 판단 근거
- 남은 한계 및 추가 개선 방향

> 이 문서는 학생이 확인할 평가 관점을 설명하기 위한 자료입니다. 실제 점수와 세부 채점은 공식 평가 기준을 따릅니다.
