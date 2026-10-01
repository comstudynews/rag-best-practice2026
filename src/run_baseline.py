import os

from dotenv import load_dotenv

from src.config import ROOT, TOP_K
from src.evaluation import (
    category_metrics,
    evaluate_retriever,
    format_doc_ids,
    load_gold_set,
)
from src.loaders import load_knowledge, split_knowledge
from src.retrievers import build_retrievers

load_dotenv(ROOT / ".env")


def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY가 없습니다.")

    docs = load_knowledge()
    chunks = split_knowledge(docs)
    baseline, _ = build_retrievers(chunks)
    cases = load_gold_set()

    result = evaluate_retriever("Baseline Similarity", baseline, cases)

    print("=== Baseline Retrieval Evaluation ===")
    print(f"문서 수: {len(docs)}")
    print(f"Chunk 수: {len(chunks)}")
    print(f"Hit Rate@{TOP_K}: {result['hit_rate']:.3f}")
    print(f"MRR@{TOP_K}: {result['mrr']:.3f}")

    print("\n=== Category Metrics ===")
    for category, metrics in sorted(category_metrics(result).items()):
        print(
            f"{category}: count={metrics['count']} "
            f"hit={metrics['hit_rate']:.3f} mrr={metrics['mrr']:.3f}"
        )

    print("\n=== Question Results ===")
    for row in result["rows"]:
        case = row["case"]
        rank = row["rank"] if row["rank"] is not None else "-"
        coverage = (
            "-"
            if row["keyword_coverage"] is None
            else f"{row['keyword_coverage']:.2f}"
        )
        print(
            f"{case.id} | category={case.category} | rank={rank} "
            f"| keyword={coverage} | {format_doc_ids(row['docs'])}"
        )


if __name__ == "__main__":
    main()
