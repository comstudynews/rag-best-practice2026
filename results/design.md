# 종합실습 설계 문서 — Best Practice 예시

## 1. 문제 정의

AsterDesk 기술지원 문서는 설치, 계정, 네트워크, 백업, 보안, 라이선스, 오류 코드 등으로 분리되어 있다.

사용자는 하나의 질문으로 필요한 정보를 찾고 싶어 하지만, 정확한 오류 코드·경로·포트처럼 **의미 검색만으로는 검색 순위가 불안정할 수 있는 정보**도 존재한다.

본 프로젝트의 목표는 문서 기반 기술지원 RAG를 구현하고, Baseline 검색 결과를 평가한 뒤 정확 키워드 검색 문제를 개선하는 것이다.

## 2. 대상 사용자

- AsterDesk 일반 사용자
- 조직 관리자
- 기술지원 담당자

## 3. 답변 범위

답변 가능:

- 설치
- 계정 및 접근
- 네트워크
- 백업 및 복구
- 오류 코드
- 보안 운영
- 라이선스 기능
- 로그 경로

답변하지 않음:

- 문서에 없는 가격
- 고객센터 전화번호
- 문서에 없는 정책

## 4. Baseline

```text
Markdown Documents
→ TextLoader
→ RecursiveCharacterTextSplitter
→ OpenAIEmbeddings
→ FAISS
→ Similarity Retriever
→ Prompt
→ ChatOpenAI
```

## 5. 평가 데이터셋

Gold Set 20문항.

질문 유형:

- fact
- paraphrase
- keyword
- compound
- security
- unanswerable

AI는 Seed 질문의 표현 변형 후보를 만드는 데 사용할 수 있으나, Gold Set은 사람이 검수한다.

## 6. Baseline 문제 가설

Dense Retrieval은 의미 기반 검색에는 적합하지만 다음 유형에서 약점이 있을 수 있다.

- ERR-NET-403
- ERR-AUTH-017
- AsterDesk-ENT
- TCP 443
- 파일 경로

## 7. 개선 전략

Hybrid Search를 적용한다.

- Dense Similarity Search: 의미 기반 검색
- BM25: 정확 키워드 검색
- EnsembleRetriever: 두 결과 통합

가중치:

```text
Dense 0.6
BM25  0.4
```

## 8. 평가 방법

Retrieval:

- Hit Rate@3
- MRR@3
- 질문별 Gold Document Rank
- Keyword Coverage

Generation:

- 문서 근거 일치
- 직접성
- Hallucination 억제
- Source ID 표시

## 9. 성공 기준

모든 질문의 점수가 상승하는 것을 성공으로 정의하지 않는다.

성공 여부는 다음을 종합해 판단한다.

- Baseline에서 진단한 문제 유형이 실제로 개선되었는가?
- 다른 질문 유형에서 큰 성능 저하가 발생하지 않았는가?
- 개선 전략의 Trade-off를 설명할 수 있는가?
