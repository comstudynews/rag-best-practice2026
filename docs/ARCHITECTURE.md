# RAG Architecture

## Baseline

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

## Improved

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

## 설계 원칙

- Baseline과 Improved의 문서·Chunk·Embedding 조건은 동일하게 유지합니다.
- 개선 전략 외의 변수를 가능한 한 고정합니다.
- Retrieval과 Generation을 분리하여 평가합니다.
- 질문별 검색 결과를 기록하여 평균 지표만으로 판단하지 않습니다.
