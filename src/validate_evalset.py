import json
from collections import Counter

from src.config import EVAL_DIR


REQUIRED = {"id", "question", "category", "gold_doc_ids", "gold_keywords", "answerable"}


def main():
    path = EVAL_DIR / "questions_gold.jsonl"
    rows = []

    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue

        row = json.loads(line)
        missing = REQUIRED - row.keys()
        if missing:
            raise SystemExit(f"line {lineno}: missing fields {sorted(missing)}")
        rows.append(row)

    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("중복 ID가 있습니다.")

    categories = Counter(r["category"] for r in rows)
    answerable = Counter(r["answerable"] for r in rows)

    print("총 질문 수:", len(rows))
    print("질문 유형:", dict(categories))
    print("answerable 분포:", dict(answerable))

    if len(rows) < 10:
        print("[WARN] 종합실습 평가셋은 10개 이상을 권장합니다.")

    if not any(not r["answerable"] for r in rows):
        print("[WARN] 문서에 없는 질문이 없습니다.")
    else:
        print("[OK] 문서에 없는 질문 포함")

    print("[OK] 평가셋 기본 검증 완료")


if __name__ == "__main__":
    main()
