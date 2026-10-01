import json
from collections import Counter

from src.config import EVAL_DIR, KNOWLEDGE_DIR


REQUIRED = {
    "id",
    "question",
    "category",
    "gold_doc_ids",
    "gold_doc_policy",
    "gold_keywords",
    "answerable",
}
VALID_POLICIES = {"any", "all"}


def main():
    path = EVAL_DIR / "questions_gold.jsonl"
    rows = []

    known_doc_ids = {path.stem for path in KNOWLEDGE_DIR.glob("*.md")}

    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue

        row = json.loads(line)
        missing = REQUIRED - row.keys()
        if missing:
            raise SystemExit(f"line {lineno}: missing fields {sorted(missing)}")

        if row["gold_doc_policy"] not in VALID_POLICIES:
            raise SystemExit(
                f"line {lineno}: invalid gold_doc_policy={row['gold_doc_policy']}"
            )

        unknown = set(row["gold_doc_ids"]) - known_doc_ids
        if unknown:
            raise SystemExit(f"line {lineno}: unknown gold_doc_ids={sorted(unknown)}")

        if row["answerable"] and not row["gold_doc_ids"]:
            raise SystemExit(f"line {lineno}: answerable=true인데 gold_doc_ids가 없습니다.")

        if not row["answerable"] and row["gold_doc_ids"]:
            raise SystemExit(
                f"line {lineno}: answerable=false인데 gold_doc_ids가 지정되어 있습니다."
            )

        rows.append(row)

    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("중복 ID가 있습니다.")

    categories = Counter(row["category"] for row in rows)
    answerable = Counter(row["answerable"] for row in rows)

    print("총 질문 수:", len(rows))
    print("질문 유형:", dict(categories))
    print("answerable 분포:", dict(answerable))

    if len(rows) < 8:
        print("[WARN] 교재 기준 테스트 질문 8개 미만입니다.")
    else:
        print("[OK] 교재 기준 8개 이상")

    if not any(not row["answerable"] for row in rows):
        print("[WARN] 문서에 없는 질문이 없습니다.")
    else:
        print("[OK] 문서에 없는 질문 포함")

    print("[OK] 평가셋 기본 검증 완료")


if __name__ == "__main__":
    main()
