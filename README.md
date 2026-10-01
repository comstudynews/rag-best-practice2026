# RAG Pipeline 종합실습 Best Practice

이 저장소는 RAG Pipeline 종합실습의 모범 구현 예제입니다.

## 실습 목표

단순히 RAG 기능을 구현하는 것이 아니라 다음 과정을 수행합니다.

1. 문제 정의
2. Baseline RAG 구현
3. 평가 데이터셋 구성
4. 검색 결과 분석
5. 개선 전략 적용
6. 개선 전·후 비교 평가

## 프로젝트 구조

```text
rag-best-practice2026/
├── data/
│   └── documents/
├── src/
│   ├── baseline_rag.py
│   ├── improved_rag.py
│   └── evaluate.py
├── results/
│   ├── design.md
│   └── evaluation.md
└── requirements.txt
```

## 핵심 구현 흐름

```text
Document
   ↓
Loader
   ↓
Text Splitter
   ↓
Embedding
   ↓
Vector Store
   ↓
Retriever
   ↓
Prompt
   ↓
LLM
   ↓
Evaluation
```

## Best Practice 원칙

- Baseline 결과를 먼저 측정합니다.
- 문제 원인을 Retrieval과 Generation으로 구분합니다.
- 개선 기법은 문제 해결 목적에 맞게 선택합니다.
- 동일한 테스트 질문으로 개선 전·후를 비교합니다.

## 평가 데이터셋 구성

실무에서는 사람이 핵심 질문과 정답 기준을 정의하고, AI는 표현 변형과 데이터 확장에 활용합니다.

AI가 생성한 질문은 그대로 평가 기준으로 사용하지 않고 사람이 검증합니다.
