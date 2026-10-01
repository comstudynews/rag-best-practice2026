from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DIR = ROOT / "data" / "knowledge"
EVAL_DIR = ROOT / "data" / "eval"
RESULTS_DIR = ROOT / "results"

CHUNK_SIZE = 420
CHUNK_OVERLAP = 80
TOP_K = 3

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"
