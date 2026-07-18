#!/usr/bin/env python3

import csv
import json
import subprocess

from benchmark import OUTPUT_DIR, ROOT, code_fixture, prose_fixture, quality, structured_fixture, token_counts


def main() -> None:
    fixtures = [prose_fixture(), code_fixture(), structured_fixture()]
    worker_input = OUTPUT_DIR / "claw-input.json"
    worker_output = OUTPUT_DIR / "claw-output.json"
    worker_input.write_text(json.dumps(fixtures, ensure_ascii=False), encoding="utf-8")
    clone = ROOT / "research" / "models" / "claw-compactor"
    subprocess.run(
        [str(ROOT / ".venv" / "bin" / "python"), str(ROOT / "scripts" / "claw_worker.py"), str(worker_input), str(worker_output)],
        cwd=clone,
        check=True,
        timeout=300,
    )
    claw = {item["fixture"]: item for item in json.loads(worker_output.read_text(encoding="utf-8"))["results"]}
    json_path = OUTPUT_DIR / "benchmark-results.json"
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    claw_methods = {"claw_compactor_7.0_text", "claw_compactor_7.1_messages", "claw_compactor_7.0"}
    rows = [row for row in payload["rows"] if row["method"] not in claw_methods]
    for fixture in fixtures:
        original_counts = token_counts(fixture["text"])
        for method, text_key, latency_key in (
            ("claw_compactor_7.0_text", "text", "latency_ms"),
            ("claw_compactor_7.1_messages", "message_text", "message_latency_ms"),
        ):
            text = claw[fixture["name"]][text_key]
            counts = token_counts(text)
            fact_recall, span_integrity, quality_pct = quality(fixture, text)
            rows.append(
                {
                    "fixture": fixture["name"],
                    "method": method,
                    "before_cl100k": original_counts["cl100k_base"],
                    "after_cl100k": counts["cl100k_base"],
                    "saved_cl100k": original_counts["cl100k_base"] - counts["cl100k_base"],
                    "savings_pct_cl100k": round(100 * (1 - counts["cl100k_base"] / original_counts["cl100k_base"]), 2),
                    "before_o200k": original_counts["o200k_base"],
                    "after_o200k": counts["o200k_base"],
                    "savings_pct_o200k": round(100 * (1 - counts["o200k_base"] / original_counts["o200k_base"]), 2),
                    "latency_ms": claw[fixture["name"]][latency_key],
                    "fact_recall_pct": round(100 * fact_recall, 2),
                    "protected_span_integrity_pct": round(100 * span_integrity, 2),
                    "quality_pct": round(quality_pct, 2),
                    "evidence": "measured pinned Git clone c1b936d40b1145c7a257bd6e34a17994f467495f",
                }
            )
            payload["outputs"][fixture["name"]][method] = text
    payload["rows"] = rows
    payload["claw_compactor_commit"] = "c1b936d40b1145c7a257bd6e34a17994f467495f"
    payload["claw_details"] = claw
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    with (OUTPUT_DIR / "benchmark-results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"measurements": len(rows), "claw_commit": payload["claw_compactor_commit"]}))


if __name__ == "__main__":
    main()
