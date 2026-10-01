import json
import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from src.config import ROOT, EVAL_DIR, CHAT_MODEL

load_dotenv(ROOT / ".env")


class QuestionVariants(TypedDict):
    questions: list[str]


SYSTEM = """당신은 RAG 평가 질문 데이터셋 작성 보조 도구입니다.
주어진 질문의 의미와 정답 범위를 유지하면서 표현만 다른 한국어 질문 3개를 만드세요.
정답을 질문에 노출하지 마세요.
"""


def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY가 없습니다.")

    seed_path = EVAL_DIR / "questions_seed.jsonl"
    out_path = EVAL_DIR / "augmented_candidates.jsonl"

    llm = ChatOpenAI(model=CHAT_MODEL, temperature=0.3)
    structured_llm = llm.with_structured_output(QuestionVariants)

    candidates = []

    for line in seed_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue

        seed = json.loads(line)

        result = structured_llm.invoke(
            SYSTEM
            + "\n\n원본 질문: "
            + seed["question"]
            + "\n카테고리: "
            + seed["category"]
        )

        for idx, question in enumerate(result["questions"][:3], start=1):
            candidates.append(
                {
                    "source_id": seed["id"],
                    "candidate_id": f"{seed['id']}-A{idx}",
                    "question": question,
                    "category": seed["category"],
                    "gold_doc_ids": seed["gold_doc_ids"],
                    "gold_doc_policy": seed.get("gold_doc_policy", "any"),
                    "answerable": seed["answerable"],
                    "review_status": "pending",
                }
            )

    with out_path.open("w", encoding="utf-8") as file:
        for row in candidates:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"생성 후보: {len(candidates)}")
    print(f"저장 위치: {out_path}")
    print("review_status=pending 상태입니다. 사람 검수 후 Gold Set에 반영하세요.")


if __name__ == "__main__":
    main()
