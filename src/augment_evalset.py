import json

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from src.config import ROOT, EVAL_DIR, CHAT_MODEL

load_dotenv(ROOT / ".env")


SYSTEM = """당신은 RAG 평가 질문 데이터셋 작성 보조 도구입니다.
주어진 질문의 의미와 정답 범위를 유지하면서 표현만 다른 한국어 질문 3개를 만드세요.
정답을 질문에 노출하지 마세요.
JSON 배열만 출력하세요.
"""


def main():
    seed_path = EVAL_DIR / "questions_seed.jsonl"
    out_path = EVAL_DIR / "augmented_candidates.jsonl"
    llm = ChatOpenAI(model=CHAT_MODEL, temperature=0.3)

    candidates = []

    for line in seed_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue

        seed = json.loads(line)
        prompt = (
            SYSTEM
            + "\n\n원본 질문: "
            + seed["question"]
            + "\n카테고리: "
            + seed["category"]
        )

        response = llm.invoke(prompt).content.strip()

        try:
            variants = json.loads(response)
        except json.JSONDecodeError:
            print(f"[WARN] JSON 파싱 실패: {seed['id']}")
            continue

        for idx, question in enumerate(variants, start=1):
            candidates.append(
                {
                    "source_id": seed["id"],
                    "candidate_id": f"{seed['id']}-A{idx}",
                    "question": question,
                    "category": seed["category"],
                    "gold_doc_ids": seed["gold_doc_ids"],
                    "answerable": seed["answerable"],
                    "review_status": "pending",
                }
            )

    with out_path.open("w", encoding="utf-8") as f:
        for row in candidates:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"생성 후보: {len(candidates)}")
    print(f"저장 위치: {out_path}")
    print("주의: review_status=pending 상태입니다. 사람이 검수한 뒤 Gold Set에 반영하세요.")


if __name__ == "__main__":
    main()
