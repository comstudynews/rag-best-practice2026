from dotenv import load_dotenv

from src.config import ROOT
from src.evaluation import load_gold_set, evaluate_retriever, format_doc_ids
from src.loaders import load_knowledge, split_knowledge
from src.retrievers import build_retrievers

load_dotenv(ROOT / ".env")


def main():
    docs = load_knowledge()
    chunks = split_knowledge(docs)
    baseline, _ = build_retrievers(chunks)
    cases = load_gold_set()

    result = evaluate_retriever("Baseline Similarity", baseline, cases)

    print("=== Baseline Retrieval Evaluation ===")
    print(f"Hit Rate@3: {result['hit_rate']:.3f}")
    print(f"MRR@3: {result['mrr']:.3f}")

    for row in result["rows"]:
        case = row["case"]
        rank = row["rank"] if row["rank"] is not None else "-"
        print(f"{case.id} | rank={rank} | {format_doc_ids(row['docs'])}")


if __name__ == "__main__":
    main()
