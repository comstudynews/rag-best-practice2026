# RAG Architecture

## 1. Baseline

```text
Knowledge Documents
        ↓
TextLoader
        ↓
RecursiveCharacterTextSplitter
        ↓
OpenAIEmbeddings
        ↓
FAISS
        ↓
Similarity Retriever (k=3)
        ↓
Grounded Prompt
        ↓
ChatOpenAI
        ↓
Answer + Source IDs
```

## 2. Improved Reference

```text
                          ┌─ Dense Retriever ─┐
Question ─────────────────┤                   ├─ EnsembleRetriever ─┐
                          └─ BM25 Retriever ──┘                    │
                                                                   ↓
                                                            Grounded Prompt
                                                                   ↓
                                                               ChatOpenAI
                                                                   ↓
                                                           Answer + Source IDs
```

## 3. 비교 원칙

- Baseline과 Improved의 문서·Chunk·Embedding·Top-K 조건을 동일하게 유지합니다.
- 개선 전략 외의 변수를 가능한 한 고정합니다.
- Baseline 결과를 먼저 확인한 후 문제를 진단합니다.
- 동일한 Gold Set으로 재평가합니다.
- Retrieval과 Generation을 분리하여 분석합니다.
- 평균 지표뿐 아니라 질문별 결과도 확인합니다.
- 개선되지 않은 결과와 Trade-off를 숨기지 않습니다.
