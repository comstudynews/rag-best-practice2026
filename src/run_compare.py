from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from src.config import ROOT, RESULTS_DIR, TOP_K
from src.evaluation import (
    category_metrics,
    compare_rank,
    evaluate_retriever,
    format_doc_ids,
    generation_auto_checks,
    load_gold_set,
)
from src.generation import answer_question, build_llm
from src.loaders import load_knowledge, split_knowledge
from src.retrievers import build_retrievers

load_dotenv(ROOT / ".env")


def row_map(result):
    return {row["case"].id: row for row in result["rows"]}


def fmt(value):
    return "-" if value is None else f"{value:.3f}"


def bool_text(value):
    if value is None:
        return "-"
    return "Yes" if value else "No"


def diagnose_baseline(result):
    keyword_rows = [
        row
        for row in result["rows"]
        if row["case"].answerable and row["case"].category == "keyword"
    ]

    if not keyword_rows:
        return (
            False,
            "keyword 유형 질문이 없어 Hybrid Search 필요성을 판단하기 어렵습니다.",
        )

    weak_rows = [
        row for row in keyword_rows
        if row["rank"] is None or row["rank"] > 1
    ]

    if weak_rows:
        ids = ", ".join(row["case"].id for row in weak_rows)
        return (
            True,
            f"키워드 유형에서 Top-1 실패 또는 MISS가 확인되었습니다: {ids}",
        )

    return (
        False,
        "키워드 유형에서 뚜렷한 Baseline 약점이 확인되지 않았습니다. "
        "Hybrid Search는 비교 실험으로 평가합니다.",
    )


def build_report(
    docs,
    chunks,
    cases,
    base_result,
    improved_result,
    with_generation,
    generation_rows,
):
    base_map = row_map(base_result)
    improved_map = row_map(improved_result)
    base_categories = category_metrics(base_result)
    improved_categories = category_metrics(improved_result)

    keyword_issue, diagnosis = diagnose_baseline(base_result)

    rank_changes = {"개선": 0, "동일": 0, "악화": 0}
    for case in cases:
        if not case.answerable:
            continue
        status = compare_rank(
            base_map[case.id]["rank"],
            improved_map[case.id]["rank"],
        )
        rank_changes[status] += 1

    lines = [
        "# 종합실습 평가 결과",
        "",
        "> 이 파일은 실제 실행 결과를 바탕으로 생성됩니다. "
        "자동 지표는 보조 자료이며, Generation 품질은 사람 검토가 필요합니다.",
        "",
        "## 1. 비교 조건",
        "",
        f"- Knowledge Documents: {len(docs)}",
        f"- Chunks: {len(chunks)}",
        f"- Top-K: {TOP_K}",
        "- Baseline: Dense Similarity Search",
        "- Improved: Dense + BM25 EnsembleRetriever",
        "- 질문셋: Baseline과 Improved에 동일한 Gold Set 사용",
        "",
        "## 2. Baseline 결과 및 문제 진단",
        "",
        f"- Hit Rate@{TOP_K}: **{base_result['hit_rate']:.3f}**",
        f"- MRR@{TOP_K}: **{base_result['mrr']:.3f}**",
        f"- 진단: {diagnosis}",
        "",
    ]

    if keyword_issue:
        lines.append(
            "- 개선 전략 판단: 정확 키워드 유형의 검색 약점을 보완하기 위해 "
            "BM25를 결합한 Hybrid Search를 적용하는 것이 논리적으로 연결됩니다."
        )
    else:
        lines.append(
            "- 개선 전략 판단: 뚜렷한 키워드 약점이 관찰되지 않았으므로 "
            "Hybrid Search를 필수 개선으로 단정하지 않고 비교 실험으로 해석합니다."
        )

    lines.extend(
        [
            "",
            "## 3. Retrieval 전체 지표",
            "",
            "| 지표 | Baseline | Improved |",
            "|---|---:|---:|",
            f"| Hit Rate@{TOP_K} | {base_result['hit_rate']:.3f} | {improved_result['hit_rate']:.3f} |",
            f"| MRR@{TOP_K} | {base_result['mrr']:.3f} | {improved_result['mrr']:.3f} |",
            "",
            f"- Rank 개선: {rank_changes['개선']}건",
            f"- Rank 동일: {rank_changes['동일']}건",
            f"- Rank 악화: {rank_changes['악화']}건",
            "",
            "## 4. 질문 유형별 Retrieval 지표",
            "",
            "| Category | Baseline Hit | Baseline MRR | Improved Hit | Improved MRR |",
            "|---|---:|---:|---:|---:|",
        ]
    )

    categories = sorted(set(base_categories) | set(improved_categories))
    for category in categories:
        base = base_categories.get(category, {})
        improved = improved_categories.get(category, {})
        lines.append(
            f"| {category} | {base.get('hit_rate', 0):.3f} | "
            f"{base.get('mrr', 0):.3f} | "
            f"{improved.get('hit_rate', 0):.3f} | "
            f"{improved.get('mrr', 0):.3f} |"
        )

    lines.extend(["", "## 5. 질문별 개선 전·후 비교", ""])

    for case in cases:
        base = base_map[case.id]
        improved = improved_map[case.id]
        status = (
            compare_rank(base["rank"], improved["rank"])
            if case.answerable
            else "Retrieval 지표 제외"
        )

        lines.extend(
            [
                f"### {case.id}. {case.question}",
                "",
                f"- 유형: {case.category}",
                f"- Answerable: {case.answerable}",
                f"- Gold Document Policy: {case.gold_doc_policy}",
                f"- Gold Docs: {', '.join(case.gold_doc_ids) if case.gold_doc_ids else '없음'}",
                f"- Baseline Rank: {base['rank'] if base['rank'] is not None else '-'}",
                f"- Improved Rank: {improved['rank'] if improved['rank'] is not None else '-'}",
                f"- Retrieval 판단: **{status}**",
                f"- Baseline Keyword Coverage: {fmt(base['keyword_coverage'])}",
                f"- Improved Keyword Coverage: {fmt(improved['keyword_coverage'])}",
                f"- Baseline Top-{TOP_K}: {format_doc_ids(base['docs'])}",
                f"- Improved Top-{TOP_K}: {format_doc_ids(improved['docs'])}",
                "",
            ]
        )

        if with_generation:
            generation = generation_rows[case.id]
            lines.extend(
                [
                    "**Baseline Answer**",
                    "",
                    generation["baseline_answer"],
                    "",
                    "**Improved Answer**",
                    "",
                    generation["improved_answer"],
                    "",
                    "**Generation 자동 체크 — 참고용**",
                    "",
                    "| 항목 | Baseline | Improved |",
                    "|---|---:|---:|",
                    f"| Gold Keyword Coverage | {fmt(generation['baseline_checks']['keyword_coverage'])} | {fmt(generation['improved_checks']['keyword_coverage'])} |",
                    f"| Gold Source Citation | {bool_text(generation['baseline_checks']['source_citation_ok'])} | {bool_text(generation['improved_checks']['source_citation_ok'])} |",
                    f"| Unanswerable Abstention | {bool_text(generation['baseline_checks']['abstention_ok'])} | {bool_text(generation['improved_checks']['abstention_ok'])} |",
                    "",
                    "**사람 검토**",
                    "",
                    "- [ ] 검색된 Context와 답변이 일치한다.",
                    "- [ ] 질문에 직접 답한다.",
                    "- [ ] 근거 없는 내용을 생성하지 않는다.",
                    "- [ ] 중요한 조건이나 예외를 누락하지 않는다.",
                    "",
                ]
            )

    lines.extend(
        [
            "## 6. 최종 해석",
            "",
            "실행 결과를 바탕으로 아래 항목을 작성합니다.",
            "",
            "- Baseline에서 실제로 확인한 문제:",
            "- 개선 전략 선택 이유:",
            "- 개선된 질문:",
            "- 동일한 질문:",
            "- 악화된 질문:",
            "- Trade-off:",
            "- 남은 한계:",
            "- 추가 개선 방향:",
            "",
            "## 7. 해석 원칙",
            "",
            "- 개선 전략을 적용했다고 모든 결과가 좋아질 필요는 없습니다.",
            "- Baseline 문제와 개선 전략의 연결이 우선입니다.",
            "- 평균 지표와 질문별 결과를 함께 확인합니다.",
            "- 자동 Generation 체크는 최종 정답 판정을 대신하지 않습니다.",
            "- 문서에 없는 질문은 Retrieval Hit Rate에서 제외하고 Generation의 Abstention을 확인합니다.",
            "",
        ]
    )

    return "\n".join(lines)


def run_comparison(with_generation=False, output_path: Path | None = None):
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY가 없습니다.")

    docs = load_knowledge()
    chunks = split_knowledge(docs)
    baseline, improved = build_retrievers(chunks)
    cases = load_gold_set()

    base_result = evaluate_retriever("Baseline Similarity", baseline, cases)
    improved_result = evaluate_retriever("Improved Hybrid", improved, cases)

    print("=== Retrieval Comparison ===")
    print(
        f"Hit Rate@{TOP_K}: "
        f"{base_result['hit_rate']:.3f} → {improved_result['hit_rate']:.3f}"
    )
    print(
        f"MRR@{TOP_K}: "
        f"{base_result['mrr']:.3f} → {improved_result['mrr']:.3f}"
    )

    generation_rows = {}

    if with_generation:
        llm = build_llm()
        print("=== Generation Comparison ===")

        for case in cases:
            baseline_answer, _ = answer_question(
                baseline,
                case.question,
                llm=llm,
            )
            improved_answer, _ = answer_question(
                improved,
                case.question,
                llm=llm,
            )

            generation_rows[case.id] = {
                "baseline_answer": baseline_answer,
                "improved_answer": improved_answer,
                "baseline_checks": generation_auto_checks(
                    case,
                    baseline_answer,
                ),
                "improved_checks": generation_auto_checks(
                    case,
                    improved_answer,
                ),
            }

            print(f"{case.id} generation 완료")

    report = build_report(
        docs,
        chunks,
        cases,
        base_result,
        improved_result,
        with_generation,
        generation_rows,
    )

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = output_path or (RESULTS_DIR / "evaluation.md")
    output_path.write_text(report, encoding="utf-8")

    print("결과 저장:", output_path)
    return output_path


def main():
    run_comparison(with_generation=False)


if __name__ == "__main__":
    main()
