#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "candidates.csv"
RAW = ROOT / "research" / "github-metadata.json"
OUTPUT = ROOT / "data" / "repository-matrix.csv"
BENCHMARK_STATUS = {
    "microsoft/LLMLingua": "measured: LLMLingua-2 mBERT CPU, 3 fixtures",
    "open-compress/claw-compactor": "measured: pinned commit, text and messages APIs, 3 fixtures",
    "rtk-ai/rtk": "installed/live metrics; not a general prompt compressor",
}

CAPABILITY_COLUMNS = [
    "prompt_tokens_reduced",
    "target_model_agnostic",
    "query_aware",
    "extractive",
    "abstractive",
    "token_pruning",
    "sentence_pruning",
    "reranking",
    "local_execution",
    "cpu_viable",
    "gpu_optional",
    "cheap_model_supported",
    "model_free",
    "streaming_safe",
    "structured_data_safe",
    "code_safe",
    "citation_safe",
    "instruction_hierarchy_safe",
    "reversible",
    "fallback_capable",
    "proxy_integration",
    "openai_compatible",
    "python_api",
    "cli",
    "batch",
    "quality_evaluation",
    "latency_measurement",
    "long_context_focus",
    "kv_cache_only",
]

CAP_MAP = {
    "prompt_tokens": "prompt_tokens_reduced",
    "query_aware": "query_aware",
    "extractive": "extractive",
    "abstractive": "abstractive",
    "token_pruning": "token_pruning",
    "sentence_pruning": "sentence_pruning",
    "reranking": "reranking",
    "local": "local_execution",
    "cpu": "cpu_viable",
    "gpu_optional": "gpu_optional",
    "cheap_model": "cheap_model_supported",
    "model_free": "model_free",
    "streaming": "streaming_safe",
    "structured_safe": "structured_data_safe",
    "code_safe": "code_safe",
    "citation_safe": "citation_safe",
    "hierarchy_safe": "instruction_hierarchy_safe",
    "reversible": "reversible",
    "fallback": "fallback_capable",
    "proxy": "proxy_integration",
    "openai_compatible": "openai_compatible",
    "python_api": "python_api",
    "cli": "cli",
    "batch": "batch",
    "quality_eval": "quality_evaluation",
    "latency_eval": "latency_measurement",
    "long_context": "long_context_focus",
    "kv_only": "kv_cache_only",
}


def gh_repo(repo: str) -> dict:
    result = subprocess.run(
        ["gh", "api", f"repos/{repo}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def popularity(stars: int) -> float:
    if stars >= 50_000:
        return 5.0
    if stars >= 10_000:
        return 4.5
    if stars >= 5_000:
        return 4.0
    if stars >= 1_000:
        return 3.5
    if stars >= 500:
        return 3.0
    if stars >= 100:
        return 2.5
    if stars >= 25:
        return 2.0
    if stars >= 5:
        return 1.0
    return 0.5


def yes_no(capabilities: set[str], column: str) -> str:
    if column == "target_model_agnostic":
        return "yes" if "kv_only" not in capabilities else "no"
    if column == "citation_safe":
        return "partial" if {"extractive", "reversible"} & capabilities else "no"
    if column == "instruction_hierarchy_safe":
        return "partial" if "reversible" in capabilities else "no"
    return "yes" if column in {CAP_MAP.get(cap) for cap in capabilities} else "no"


def main() -> None:
    captured_at = datetime.now(UTC).isoformat()
    with INPUT.open(newline="", encoding="utf-8") as handle:
        candidates = list(csv.DictReader(handle))
    if len(candidates) != 50:
        raise SystemExit(f"expected exactly 50 candidates, found {len(candidates)}")

    metadata = []
    rows = []
    for candidate in candidates:
        repo = candidate["repo"]
        data = gh_repo(repo)
        metadata.append(data)
        caps = set(filter(None, candidate["capabilities"].split("|")))
        pop = popularity(int(data["stargazers_count"]))
        spdx_id = (data.get("license") or {}).get("spdx_id")
        dimensions = {
            key: float(candidate[key])
            for key in (
                "savings",
                "quality",
                "latency",
                "local",
                "footprint",
                "integration",
                "safety",
                "maturity",
            )
        }
        total = round(sum(dimensions.values()) + pop, 1)
        row = {
            "repository": data["full_name"],
            "category": candidate["category"],
            "technique": candidate["technique"],
            "github_url": data["html_url"],
            "stars": data["stargazers_count"],
            "forks": data["forks_count"],
            "open_issues": data["open_issues_count"],
            "archived": data["archived"],
            "license": spdx_id if spdx_id and spdx_id != "NOASSERTION" else "[UNVERIFIZIERT] (NOASSERTION)",
            "last_push_utc": data["pushed_at"],
            "primary_language": data.get("language") or "unknown",
            "default_branch": data["default_branch"],
            "created_utc": data["created_at"],
            "updated_utc": data["updated_at"],
            "homepage": data.get("homepage") or "",
            "description": data.get("description") or "",
            "evidence_grade": "GitHub API + primary README + category inference",
            "local_benchmark_status": BENCHMARK_STATUS.get(repo, "not locally executed; primary-source assessment"),
            **{column: yes_no(caps, column) for column in CAPABILITY_COLUMNS},
            "savings_20": dimensions["savings"],
            "quality_20": dimensions["quality"],
            "latency_10": dimensions["latency"],
            "local_deploy_10": dimensions["local"],
            "model_footprint_8": dimensions["footprint"],
            "proxy_integration_12": dimensions["integration"],
            "safety_reversibility_8": dimensions["safety"],
            "maturity_7": dimensions["maturity"],
            "popularity_5": pop,
            "total_100": total,
            "crown": "",
            "notes": candidate["notes"],
            "captured_at_utc": captured_at,
        }
        rows.append(row)

    winner = max(rows, key=lambda row: row["total_100"])
    winner["crown"] = "CROWN"
    rows.sort(key=lambda row: -float(row["total_100"]))
    RAW.parent.mkdir(parents=True, exist_ok=True)
    RAW.write_text(json.dumps({"captured_at_utc": captured_at, "repositories": metadata}, indent=2), encoding="utf-8")
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"repositories": len(rows), "columns": len(rows[0]), "winner": winner["repository"], "winner_score": winner["total_100"], "captured_at_utc": captured_at}))


if __name__ == "__main__":
    main()
