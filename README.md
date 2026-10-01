# RAG Pipeline 종합실습 Best Practice

이 저장소는 **하루 종합실습 기준으로 설계한 RAG Pipeline Best Practice 참조 구현**입니다.

단순히 RAG를 한 번 실행하는 것이 아니라, 다음 과정을 끝까지 수행하도록 구성했습니다.

> 문제 정의 → Baseline 구현 → 평가 데이터셋 구성 → Baseline 평가 → 문제 진단 → 개선 전략 적용 → 동일 조건 재평가 → 결과·한계 정리

> **교수자 참고**  
> 이 저장소는 완성형 참조 구현입니다. 평가 과제로 사용할 경우 제출 마감 전 전체 해답을 그대로 공개하기보다 과제 지시서와 Starter 구조만 제공하고, 이 저장소는 채점·피드백·사후 복습용으로 사용하는 것을 권장합니다.

## 1. 프로젝트 시나리오

가상의 기업용 제품 **AsterDesk**의 설치·계정·네트워크·백업·보안·라이선스·오류 코드 문서를 기반으로 기술지원 RAG를 구축합니다.

사용자는 다음과 같은 질문을 할 수 있습니다.

- Windows 설치 방법은?
- ERR-NET-403 오류의 원인은?
- 계정 잠금은 몇 분 후 해제되는가?
- 백업 파일은 어디에 저장되는가?
- 문서에 없는 가격 정책을 물으면 어떻게 답해야 하는가?

## 2. 종합실습 핵심 과제

### Baseline

Dense Similarity Search 기반 RAG를 구현합니다.

```text
Documents
  ↓
Loader
  ↓
Chunking
  ↓
Embedding
  ↓
FAISS
  ↓
Similarity Retriever
  ↓
Prompt
  ↓
LLM
```

### 평가

Gold Test Set으로 다음을 확인합니다.

- Hit Rate@K
- MRR@K
- 정답 문서 순위
- 키워드 포함 여부
- 근거 기반 답변 여부
- 문서에 없는 질문의 Hallucination 억제

### 개선

Baseline에서 확인한 문제를 근거로 **Hybrid Search(Dense + BM25)** 를 적용합니다.

```text
Question
  ├─ Dense Retrieval
  └─ BM25 Retrieval
        ↓
EnsembleRetriever
        ↓
Prompt
        ↓
LLM
```

개선 후에는 **동일한 평가 질문**을 다시 사용하여 전·후 결과를 비교합니다.

## 3. 프로젝트 구조

```text
rag-best-practice2026/
├── README.md
├── .env.example
├── .gitignore
├── .python-version
├── pyproject.toml
├── docs/
│   ├── ASSIGNMENT.md
│   ├── ARCHITECTURE.md
│   ├── EVALUATION_GUIDE.md
│   ├── RUBRIC.md
│   └── BEST_PRACTICE_NOTES.md
├── data/
│   ├── knowledge/
│   │   ├── 01_installation.md
│   │   ├── 02_account_access.md
│   │   ├── 03_network.md
│   │   ├── 04_backup_restore.md
│   │   ├── 05_error_codes.md
│   │   ├── 06_security.md
│   │   ├── 07_license.md
│   │   └── 08_operations.md
│   └── eval/
│       ├── questions_seed.jsonl
│       └── questions_gold.jsonl
├── src/
│   ├── check_env.py
│   ├── config.py
│   ├── loaders.py
│   ├── retrievers.py
│   ├── prompts.py
│   ├── generation.py
│   ├── evaluation.py
│   ├── validate_evalset.py
│   ├── augment_evalset.py
│   ├── run_baseline.py
│   └── run_compare.py
├── results/
│   ├── design.md
│   └── evaluation.md
└── tests/
    └── test_evalset.py
```

## 4. 실행

### 4.1 환경 구성

```bash
cp .env.example .env
uv sync
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
uv sync
```

`.env`에 다음 값을 설정합니다.

```env
OPENAI_API_KEY=...
```

### 4.2 환경 점검

```bash
uv run --locked python -m src.check_env
```

### 4.3 평가셋 검증

```bash
uv run --locked python -m src.validate_evalset
```

### 4.4 Baseline 실행

```bash
uv run --locked python -m src.run_baseline
```

### 4.5 개선 전·후 비교

Retrieval만 비교:

```bash
uv run --locked python -m src.run_compare
```

Generation까지 포함:

```bash
uv run --locked python -m src.run_compare --with-generation
```

실행 결과는 `results/runtime_comparison.md`에 저장됩니다.

## 5. 평가 데이터셋

`questions_gold.jsonl`은 사람이 검수한 Gold Set 예시입니다.

각 레코드는 다음 정보를 포함합니다.

```json
{
  "id": "Q01",
  "question": "Windows에서 AsterDesk를 설치하는 기본 절차는?",
  "category": "fact",
  "gold_doc_ids": ["01_installation"],
  "gold_keywords": ["Windows", "설치"],
  "answerable": true
}
```

AI로 질문을 확장할 수 있지만, 자동 생성 결과를 바로 Gold Set에 넣지 않습니다.

```text
사람이 Seed 작성
→ AI로 표현 변형 후보 생성
→ 사람이 검수
→ 중복·오류 제거
→ Gold Set 반영
```

AI 확장 예제:

```bash
uv run --locked python -m src.augment_evalset
```

생성 결과는 `data/eval/augmented_candidates.jsonl`에 **review_status=pending** 상태로 저장됩니다.

## 6. 제출물 관점에서 확인할 사항

- 코드가 실행되는가?
- Baseline이 별도로 존재하는가?
- 평가 질문이 8~10개 이상이며 유형이 다양하게 구성되어 있는가?
- Baseline 문제를 실제 결과로 진단했는가?
- 개선 전략이 문제와 연결되는가?
- 동일 질문으로 전·후를 비교했는가?
- 개선되지 않은 결과와 Trade-off도 기록했는가?
- API Key가 저장소에 포함되지 않았는가?

세부 기준은 `docs/RUBRIC.md`를 확인합니다.
