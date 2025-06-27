#!/usr/bin/env python3
"""Summarize repeated errors from plain-text application logs."""
from __future__ import annotations
import argparse, json, re
from collections import Counter
from pathlib import Path

ERROR_RE = re.compile(r"(ERROR|CRITICAL|Exception|Traceback|failed|timeout)", re.I)

def summarize(path: Path, top: int = 10) -> dict:
    counts: Counter[str] = Counter()
    samples: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not ERROR_RE.search(line):
            continue
        key = re.sub(r"\d+", "#", line.strip())
        key = re.sub(r"\s+", " ", key)[:160]
        counts[key] += 1
        samples.setdefault(key, line.strip())
    top_errors = [
        {"pattern": pattern, "count": count, "sample": samples[pattern]}
        for pattern, count in counts.most_common(top)
    ]
    return {"total_error_lines": sum(counts.values()), "unique_patterns": len(counts), "top_errors": top_errors}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--out", default="samples/error_summary.json")
    args = parser.parse_args()
    report = summarize(Path(args.input), args.top)
    Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"errors={report['total_error_lines']} unique={report['unique_patterns']}")

if __name__ == "__main__":
    main()
