import json
import unittest
from pathlib import Path


class GoldDatasetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path("data/eval/questions_gold.jsonl")
        cls.rows = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def test_has_at_least_course_minimum_cases(self):
        self.assertGreaterEqual(len(self.rows), 8)

    def test_has_unanswerable_case(self):
        self.assertTrue(any(row["answerable"] is False for row in self.rows))

    def test_ids_are_unique(self):
        ids = [row["id"] for row in self.rows]
        self.assertEqual(len(ids), len(set(ids)))

    def test_has_multiple_categories(self):
        categories = {row["category"] for row in self.rows}
        self.assertGreaterEqual(len(categories), 5)

    def test_gold_doc_policy_is_valid(self):
        for row in self.rows:
            self.assertIn(row["gold_doc_policy"], {"any", "all"})

    def test_unanswerable_has_no_gold_docs(self):
        for row in self.rows:
            if row["answerable"] is False:
                self.assertEqual(row["gold_doc_ids"], [])


if __name__ == "__main__":
    unittest.main()
