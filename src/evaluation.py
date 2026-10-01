from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from src.config import EVAL_DIR, TOP_K
from src.prompts import FALLBACK_ANSWER


@dataclass(frozen=True)
class EvalCase:
    id: str
    question: str
    category: str
    gold_doc_ids: tuple[str, ...]
    gold_doc_policy: str
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
                gold_doc_policy=row.get("gold_doc_policy", "any"),
                gold_keywords=tuple(row.get("gold_keywords", [])),
                answerable=bool(row["answerable"]),
            )
        )
    return cases


def top_k_docs(retriever, question):
    return list(retriever.invoke(question))[:TOP_K]


def gold_rank(docs, gold_doc_ids, policy="any"):
    if not gold_doc_ids:
        return None

    positions = {}
    gold = set(gold_doc_ids)

    for rank, doc in enumerate(docs, start=1):
        doc_id = doc.metadata.get("doc_id")
        if doc_id in gold and doc_id not in positions:
            positions[doc_id] = rank

    if policy == "all":
        if not gold.issubset(positions):
            return None
        return max(positions.values())

    found = [positions[doc_id] for doc_id in gold if doc_id in positions]
    return min(found) if found else None


def keyword_coverage(text, gold_keywords):
    if not gold_keywords:
        return None

    hits = sum(1 for keyword in gold_keywords if keyword in text)
    return hits / len(gold_keywords)


def retrieval_keyword_coverage(docs, gold_keywords):
    text = "\n".join(doc.page_content for doc in docs)
    return keyword_coverage(text, gold_keywords)


def evaluate_retriever(name, retriever, cases):
    rows = []

    for case in cases:
        docs = top_k_docs(retriever, case.question)
        rank = gold_rank(docs, case.gold_doc_ids, case.gold_doc_policy)
        coverage = retrieval_keyword_coverage(docs, case.gold_keywords)

        rows.append(
            {
                "case": case,
                "docs": docs,
                "rank": rank,
                "keyword_coverage": coverage,
            }
        )

    evaluable = [row for row in rows if row["case"].answerable]

    hit_rate = (
        sum(1 for row in evaluable if row["rank"] is not None) / len(evaluable)
        if evaluable
        else 0.0
    )

    mrr = (
        sum(0.0 if row["rank"] is None else 1.0 / row["rank"] for row in evaluable)
        / len(evaluable)
        if evaluable
        else 0.0
    )

    return {
        "name": name,
        "rows": rows,
        "hit_rate": hit_rate,
        "mrr": mrr,
        "count": len(evaluable),
    }


def category_metrics(result):
    grouped = defaultdict(list)

    for row in result["rows"]:
        if row["case"].answerable:
            grouped[row["case"].category].append(row)

    summary = {}
    for category, rows in grouped.items():
        summary[category] = {
            "count": len(rows),
            "hit_rate": sum(1 for row in rows if row["rank"] is not None) / len(rows),
            "mrr": sum(
                0.0 if row["rank"] is None else 1.0 / row["rank"]
                for row in rows
            ) / len(rows),
        }
    return summary


def generation_auto_checks(case, answer):
    coverage = keyword_coverage(answer, case.gold_keywords)

    if case.answerable:
        cited = {doc_id for doc_id in case.gold_doc_ids if doc_id in answer}
        if case.gold_doc_policy == "all":
            source_citation_ok = set(case.gold_doc_ids).issubset(cited)
        else:
            source_citation_ok = bool(cited)
        abstention_ok = None
    else:
        source_citation_ok = None
        abstention_ok = answer.strip().startswith(FALLBACK_ANSWER)

    return {
        "keyword_coverage": coverage,
        "source_citation_ok": source_citation_ok,
        "abstention_ok": abstention_ok,
    }


def format_doc_ids(docs):
    return ", ".join(doc.metadata.get("doc_id", "unknown") for doc in docs)


def format_docs_markdown(docs, max_chars=220):
    lines = []
    for rank, doc in enumerate(docs, start=1):
        doc_id = doc.metadata.get("doc_id", "unknown")
        excerpt = " ".join(doc.page_content.split())
        if len(excerpt) > max_chars:
            excerpt = excerpt[: max_chars - 3] + "..."
        lines.append(f"{rank}. `{doc_id}` — {excerpt}")
    return "\n".join(lines) if lines else "- 검색 결과 없음"


def compare_rank(base_rank, improved_rank):
    if base_rank is None and improved_rank is None:
        return "동일"
    if base_rank is None and improved_rank is not None:
        return "개선"
    if base_rank is not None and improved_rank is None:
        return "악화"
    if improved_rank < base_rank:
        return "개선"
    if improved_rank > base_rank:
        return "악화"
    return "동일"
