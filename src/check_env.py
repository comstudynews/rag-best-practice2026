import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from src.config import ROOT, KNOWLEDGE_DIR, EVAL_DIR

load_dotenv(ROOT / ".env")


def main():
    print("=== RAG Best Practice 환경 점검 ===")
    print("Python:", sys.version.split()[0])
    print("Project:", ROOT)
    print("Knowledge documents:", len(list(KNOWLEDGE_DIR.glob("*.md"))))
    print("Gold dataset:", EVAL_DIR / "questions_gold.jsonl")

    if sys.version_info[:2] != (3, 11):
        print("[WARN] Python 3.11 사용을 권장합니다.")
    else:
        print("[OK] Python 3.11")

    if os.getenv("OPENAI_API_KEY"):
        print("[OK] OPENAI_API_KEY")
    else:
        print("[WARN] OPENAI_API_KEY가 설정되지 않았습니다.")

    if not KNOWLEDGE_DIR.exists():
        raise SystemExit("[FAIL] knowledge directory 없음")

    if not (EVAL_DIR / "questions_gold.jsonl").exists():
        raise SystemExit("[FAIL] Gold dataset 없음")

    print("[OK] 기본 파일 구조 확인 완료")


if __name__ == "__main__":
    main()
