import tempfile, unittest
from pathlib import Path
from src.summarizer import summarize

class SummarizerTests(unittest.TestCase):
    def test_groups_repeated_errors(self):
        content = "ERROR timeout 1\nINFO ok\nERROR timeout 2\nCRITICAL boom\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "app.log"
            path.write_text(content, encoding="utf-8")
            report = summarize(path, top=5)
            self.assertEqual(report["total_error_lines"], 3)
            self.assertGreaterEqual(report["unique_patterns"], 2)

if __name__ == "__main__":
    unittest.main()
