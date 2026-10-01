from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from src.config import EVAL_DIR, TOP_K


@dataclass(frozen=True)
class EvalCase:
    id: str
    question: str
    category: str
    gold_doc_ids: tuple[str, ...]
    gold_keywords: tuple[str, ...]
    answerable: bool


def load_gold_set(path: Path | None = None) -> list[EvalCase]:
    path = path or (EVAL_DIR / "questions_gold.jsonl")
    cases: list[EvalCase] = []

    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        cases.append(
            EvalCase(
                id=row["id"],
                question=row["question"],
                category=row["category"],
                gold_doc_ids=tuple(row.get("gold_doc_ids", [])),
                gold_keywords=tuple(row.get("gold_keywords", [])),
                answerable=bool(row["answerable"]),
            )
        )
    return cases


def top_k_docs(retriever, question):
    return list(retriever.invoke(question))[:TOP_K]


def first_gold_rank(docs, gold_doc_ids):
    if not gold_doc_ids:
        return None

    gold = set(gold_doc_ids)
    for rank, doc in enumerate(docs, start=1):
        if doc.metadata.get("doc_id") in gold:
            return rank
    return None


def keyword_coverage(docs, gold_keywords):
    if not gold_keywords:
        return None

    text = "\n".join(doc.page_content for doc in docs)
    hits = sum(1 for keyword in gold_keywords if keyword in text)
    return hits / len(gold_keywords)


def evaluate_retriever(name, retriever, cases):
    rows = []

    for case in cases:
        docs = top_k_docs(retriever, case.question)
        rank = first_gold_rank(docs, case.gold_doc_ids)
        coverage = keyword_coverage(docs, case.gold_keywords)

        rows.append(
            {
                "case": case,
                "docs": docs,
                "rank": rank,
                "keyword_coverage": coverage,
            }
        )

    evaluable = [r for r in rows if r["case"].answerable]

    hit_rate = (
        sum(1 for r in evaluable if r["rank"] is not None) / len(evaluable)
        if evaluable else 0.0
    )

    mrr = (
        sum(0.0 if r["rank"] is None else 1.0 / r["rank"] for r in evaluable)
        / len(evaluable)
        if evaluable else 0.0
    )

    return {
        "name": name,
        "rows": rows,
        "hit_rate": hit_rate,
        "mrr": mrr,
        "count": len(evaluable),
    }


def format_doc_ids(docs):
    return ", ".join(doc.metadata.get("doc_id", "unknown") for doc in docs)
