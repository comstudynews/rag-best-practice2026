import json
from pathlib import Path


def test_gold_dataset_has_minimum_cases():
    path = Path("data/eval/questions_gold.jsonl")
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert len(rows) >= 10


def test_gold_dataset_has_unanswerable_case():
    path = Path("data/eval/questions_gold.jsonl")
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert any(row["answerable"] is False for row in rows)


def test_gold_dataset_ids_are_unique():
    path = Path("data/eval/questions_gold.jsonl")
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    ids = [row["id"] for row in rows]
    assert len(ids) == len(set(ids))
