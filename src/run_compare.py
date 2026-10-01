import argparse

from dotenv import load_dotenv

from src.config import ROOT, RESULTS_DIR, TOP_K
from src.evaluation import (
    load_gold_set,
    evaluate_retriever,
    format_doc_ids,
)
from src.generation import answer_question
from src.loaders import load_knowledge, split_knowledge
from src.retrievers import build_retrievers

load_dotenv(ROOT / ".env")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--with-generation",
        action="store_true",
        help="Retrieval 비교에 더해 Baseline/Improved 답변도 생성합니다.",
    )
    return parser.parse_args()


def row_map(result):
    return {row["case"].id: row for row in result["rows"]}


def main():
    args = parse_args()

    docs = load_knowledge()
    chunks = split_knowledge(docs)
    baseline, improved = build_retrievers(chunks)
    cases = load_gold_set()

    base_result = evaluate_retriever("Baseline Similarity", baseline, cases)
    imp_result = evaluate_retriever("Improved Hybrid", improved, cases)

    print("=== Retrieval Comparison ===")
    print(
        f"Hit Rate@{TOP_K}: "
        f"{base_result['hit_rate']:.3f} → {imp_result['hit_rate']:.3f}"
    )
    print(
        f"MRR@{TOP_K}: "
        f"{base_result['mrr']:.3f} → {imp_result['mrr']:.3f}"
    )

    base_map = row_map(base_result)
    imp_map = row_map(imp_result)

    lines = [
        "# Runtime Comparison",
        "",
        "이 파일은 실제 실행 결과입니다.",
        "",
        "## Retrieval Metrics",
        "",
        f"- Baseline Hit Rate@{TOP_K}: **{base_result['hit_rate']:.3f}**",
        f"- Improved Hit Rate@{TOP_K}: **{imp_result['hit_rate']:.3f}**",
        f"- Baseline MRR@{TOP_K}: **{base_result['mrr']:.3f}**",
        f"- Improved MRR@{TOP_K}: **{imp_result['mrr']:.3f}**",
        "",
        "## 질문별 결과",
        "",
    ]

    for case in cases:
        b = base_map[case.id]
        i = imp_map[case.id]

        lines.extend(
            [
                f"### {case.id}. {case.question}",
                "",
                f"- 유형: {case.category}",
                f"- Answerable: {case.answerable}",
                f"- Gold Docs: {', '.join(case.gold_doc_ids) if case.gold_doc_ids else '없음'}",
                f"- Baseline Rank: {b['rank'] if b['rank'] is not None else '-'}",
                f"- Improved Rank: {i['rank'] if i['rank'] is not None else '-'}",
                f"- Baseline Top-{TOP_K}: {format_doc_ids(b['docs'])}",
                f"- Improved Top-{TOP_K}: {format_doc_ids(i['docs'])}",
                "",
            ]
        )

        if args.with_generation:
            base_answer, _ = answer_question(baseline, case.question)
            imp_answer, _ = answer_question(improved, case.question)
            lines.extend(
                [
                    "**Baseline Answer**",
                    "",
                    base_answer,
                    "",
                    "**Improved Answer**",
                    "",
                    imp_answer,
                    "",
                ]
            )

    lines.extend(
        [
            "## 분석",
            "",
            "- Baseline에서 발견한 문제:",
            "- 개선 전략 선택 이유:",
            "- 실제로 개선된 질문:",
            "- 동일하거나 악화된 질문:",
            "- Trade-off:",
            "- 남은 한계:",
            "- 추가 개선 방향:",
            "",
        ]
    )

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = RESULTS_DIR / "runtime_comparison.md"
    path.write_text("\n".join(lines), encoding="utf-8")

    print("결과 저장:", path)


if __name__ == "__main__":
    main()
