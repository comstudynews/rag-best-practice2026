import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.run_compare import run_comparison


def parse_args():
    parser = argparse.ArgumentParser(
        description="RAG 종합실습 Baseline / Improved 비교 실행"
    )
    parser.add_argument(
        "--retrieval-only",
        action="store_true",
        help="Generation 호출을 생략하고 Retrieval 비교만 수행합니다.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    run_comparison(
        with_generation=not args.retrieval_only,
    )


if __name__ == "__main__":
    main()
