# RAG Pipeline 종합실습 Best Practice

이 저장소는 **RAG Pipeline 설계·개발·평가 종합실습의 완성형 참조 구현**입니다.

주제는 가상의 제품 **DEMO-RAG-2026** 기술지원으로 구성했습니다. 문서·제품명·오류 코드는 모두 교육용 예시이며 실제 기업·서비스 정보가 아닙니다.

종합실습의 핵심은 다음 흐름을 끝까지 수행하는 것입니다.

> 문제 정의 → Baseline 구현 → 평가 데이터셋 구성 → Baseline 평가 → 문제 진단 → 개선 전략 적용 → 동일 조건 재평가 → 결과 및 한계 정리

## 1. 교재 기준과 이 샘플의 범위

- 종합실습 교재 기준 테스트 질문: **8~10개**
- 이 Best Practice의 Gold Set: **20개**

20개를 사용한 이유는 평가 질문의 유형을 넓히고, 실제 프로젝트에서 평가셋을 확장하는 방법까지 보여주기 위해서입니다. 질문 수가 많다고 더 좋은 평가가 되는 것은 아니며, **대표성·정답 신뢰성·실패 사례 포함 여부**가 더 중요합니다.

## 2. 프로젝트 시나리오

DEMO-RAG-2026 제품의 설치·계정·네트워크·백업·보안·라이선스·오류 코드 문서를 대상으로 기술지원 RAG를 구축합니다.

예시 질문:

- Windows 설치 절차는?
- ERR-NET-403 오류의 원인은?
- 계정 잠금은 몇 분 후 해제되는가?
- Linux 백업 경로는?
- DEMO-RAG-ENT는 무엇인가?
- 문서에 없는 가격이나 전화번호를 물으면 어떻게 답해야 하는가?

## 3. 종합실습 수행 흐름

### 3.1 문제 및 문서 범위 정의

`results/design.md`에 다음을 정리합니다.

- 대상 사용자
- 사용할 문서
- 답변 가능한 질문 범위
- 문서에 근거가 없을 때의 응답 원칙
- Baseline 구조
- 평가 방법
- 개선 전략을 선택하기 위한 판단 기준

### 3.2 Baseline RAG 구현

```text
Documents
  ↓
Loader
  ↓
Text Splitter
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

### 3.3 평가 데이터셋 구성

이 샘플은 20개의 Gold 질문을 제공합니다.

질문 유형:

- fact
- paraphrase
- keyword
- compound
- security
- unanswerable

### 3.4 Baseline 평가 및 문제 진단

먼저 Baseline을 실행하고 다음을 확인합니다.

- Top-K 검색 문서
- 정답 문서 포함 여부
- 정답 문서 순위
- Keyword Coverage
- 최종 답변의 문서 근거 여부
- 문서에 없는 질문의 응답

**개선 전략은 Baseline 결과를 본 뒤 선택해야 합니다.**

이 샘플은 코드·오류번호·경로·제품 식별자 질문에서 Sparse Retrieval이 도움이 될 수 있다는 가설을 두고 **Hybrid Search**를 비교 전략으로 구현했습니다.

실행 결과에서 키워드 유형의 약점이 실제로 확인되지 않으면, "Hybrid가 반드시 더 좋다"고 결론내리지 않습니다. 동일·악화 결과와 Trade-off를 그대로 기록합니다.

### 3.5 개선 전략 적용

참조 구현:

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

### 3.6 동일 조건 재평가

Baseline과 Improved Pipeline에 **동일한 Gold Set**을 사용합니다.

Retrieval:

- Hit Rate@3
- MRR@3
- Gold Document Rank
- Keyword Coverage

Generation:

- Gold Keyword Coverage
- 근거 문서 ID 표시
- 문서에 없는 질문의 Abstention
- 사람 검토: 근거 일치 / 직접성 / 근거 없는 생성 여부

자동 체크는 보조 지표이며, Generation의 최종 판단은 사람이 결과를 확인합니다.

## 4. 프로젝트 구조

```text
rag-best-practice2026/
├── README.md
├── .env.example
├── .gitignore
├── .python-version
├── pyproject.toml
├── requirements.txt
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
│   ├── capstone_compare.py
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

교재의 단일 제출 파일 `src/capstone_compare.py`에 대응하는 진입점을 유지하되, Best Practice에서는 유지보수성을 위해 내부 기능을 여러 모듈로 분리했습니다.

> **경로 안내**  
> 이 저장소는 별도의 Best Practice 저장소이므로 프로젝트 루트가 교재의 `final_capstone/practice/`에 해당합니다.  
> 실제 종합실습 제출 시에는 교재 안내에 따라 `final_capstone/practice/src/capstone_compare.py`, `final_capstone/practice/results/design.md`, `final_capstone/practice/results/evaluation.md` 구조를 따릅니다.

## 5. 실행

### 5.1 환경 구성

macOS / Linux:

```bash
cp .env.example .env
uv sync
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
uv sync
```

`.env`:

```env
OPENAI_API_KEY=...
```

### 5.2 환경 점검

```bash
uv run --locked python -m src.check_env
```

### 5.3 평가셋 검증

```bash
uv run --locked python -m src.validate_evalset
```

### 5.4 Baseline만 확인

```bash
uv run --locked python -m src.run_baseline
```

### 5.5 종합실습 전체 비교

Retrieval + Generation:

```bash
uv run --locked python src/capstone_compare.py
```

Retrieval만 빠르게 확인:

```bash
uv run --locked python src/capstone_compare.py --retrieval-only
```

실행 후 실제 결과는 `results/evaluation.md`에 저장됩니다.

### 5.6 평가셋 AI 확장 예제

```bash
uv run --locked python -m src.augment_evalset
```

AI 생성 질문은 `review_status=pending` 상태로 저장됩니다. 사람이 검수한 뒤에만 Gold Set에 반영합니다.

### 5.7 데이터셋 단위 테스트

```bash
uv run --locked python -m unittest discover -s tests
```

## 6. Gold Set의 의미

`questions_gold.jsonl`은 **Gold Set 형식의 Best Practice 예시**입니다.

`gold_doc_ids`가 여러 개인 경우 `gold_doc_policy`로 의미를 명확히 합니다.

- `"any"`: 목록 중 하나 이상이 검색되면 정답 문서 Hit
- `"all"`: 목록의 모든 문서가 Top-K에 포함되어야 Hit

현재 샘플의 다중 문서 문항은 모두 `"any"`를 사용합니다.

## 7. 결과 해석 원칙

개선 기법을 적용했다고 모든 질문이 좋아질 필요는 없습니다.

반드시 다음을 구분해 기록합니다.

- 개선됨
- 동일함
- 악화됨
- 판단 불가

Best Practice의 핵심은 특정 기법 자체가 아니라 다음 연결입니다.

> **Baseline 결과 → 문제 진단 → 개선 전략 선택 이유 → 동일 조건 재평가 → 근거와 한계 설명**
