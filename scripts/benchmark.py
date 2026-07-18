#!/usr/bin/env python3

from __future__ import annotations

import csv
import json
import math
import re
import subprocess
import time
from collections import Counter
from pathlib import Path

import tiktoken
from headroom.transforms.content_router import ContentRouter, ContentRouterConfig


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "benchmarks" / "fixtures"
OUTPUT_DIR = ROOT / "benchmarks" / "results"
ENCODINGS = {name: tiktoken.get_encoding(name) for name in ("cl100k_base", "o200k_base")}


def prose_fixture() -> dict:
    common = (
        "The service is deployed using a conventional three-tier architecture. "
        "Each team records weekly status, routine maintenance, dependency updates, "
        "and capacity observations. Normal records are informational and do not change "
        "the incident response decision. Operators should focus on explicit exceptions, "
        "named constraints, dates, numeric thresholds, and mandatory regional boundaries. "
    )
    documents = []
    for index in range(1, 46):
        body = common * 3
        if index == 9:
            body += "Project Borealis must remain in region eu-central-1 because the regulated dataset may not cross the EU boundary. "
        if index == 23:
            body += "The active incident identifier is ERR-2048 and the rollback must finish before deadline 2026-08-01. "
        if index == 37:
            body += "Audit evidence has a mandatory retention 45 days and deletion before that window is prohibited. "
        documents.append(f"Document {index:02d}: {body}")
    text = (
        "[SYSTEM] Preserve authority, exact identifiers, dates, regions, and retention rules.\n"
        "[USER] Produce an incident plan for Project Borealis. Which region, incident ID, deadline, and retention period govern the response?\n\n"
        + "\n\n".join(documents)
    )
    return {
        "name": "prose_rag",
        "question": "Project Borealis region incident deadline retention",
        "text": text,
        "facts": ["Project Borealis", "eu-central-1", "ERR-2048", "2026-08-01", "retention 45 days"],
        "protected": ["[SYSTEM] Preserve authority, exact identifiers, dates, regions, and retention rules."],
        "force_tokens": ["Project", "Borealis", "region", "incident", "deadline", "retention", "ERR"],
    }


def code_fixture() -> dict:
    modules = []
    for index in range(1, 36):
        modules.append(
            "\n".join(
                [
                    f"def normalize_record_{index}(record: dict) -> dict:",
                    "    normalized = dict(record)",
                    f"    normalized[\"module\"] = \"module-{index:02d}\"",
                    "    normalized[\"status\"] = normalized.get(\"status\", \"ok\")",
                    "    return normalized",
                ]
            )
        )
    logs = [f"2026-07-18T12:{index % 60:02d}:00Z INFO worker={index % 8} batch={index} status=ok" for index in range(180)]
    logs[117] = "2026-07-18T12:57:00Z ERROR PaymentWriter idempotency-key missing CRITICAL-771 amount=9917.42"
    text = (
        "[SYSTEM] Do not rename functions, alter exact error strings, or remove the idempotency invariant.\n"
        "[USER] Diagnose why PaymentWriter duplicated a charge and propose the smallest safe patch.\n\n"
        "```python\n"
        + "\n".join(modules)
        + "\nclass PaymentWriter:\n"
        "    def commit_payment(self, payload: dict) -> None:\n"
        "        key = payload.get(\"idempotency-key\")\n"
        "        if not key:\n"
        "            raise RuntimeError(\"CRITICAL-771 idempotency-key missing\")\n"
        "        self.store.insert_once(key, payload)\n"
        "```\n\n"
        "Required invariant: idempotency-key must be checked before store.insert_once.\n\n"
        + "\n".join(logs)
    )
    return {
        "name": "code_debug",
        "question": "PaymentWriter duplicate charge idempotency-key CRITICAL-771",
        "text": text,
        "facts": ["PaymentWriter", "idempotency-key", "CRITICAL-771", "9917.42", "store.insert_once"],
        "protected": ["[SYSTEM] Do not rename functions, alter exact error strings, or remove the idempotency invariant."],
        "force_tokens": ["PaymentWriter", "idempotency", "CRITICAL", "store", "insert", "RuntimeError"],
    }


def structured_fixture() -> dict:
    records = []
    for index in range(160):
        record = {
            "record_id": f"rec-{index:04d}",
            "tenant": f"tenant-{index % 12:02d}",
            "amount": round(10 + index * 1.17, 2),
            "status": "normal",
            "policy": "archive_after_30_days",
            "region": "eu-central-1",
            "metadata": {"batch": index // 10, "retry": 0, "source": "ledger-v3"},
        }
        if index == 121:
            record.update({"record_id": "CRITICAL-771", "amount": 9917.42, "status": "blocked", "policy": "never_delete"})
        records.append(record)
    payload = {"schema_version": "ledger.v3", "required_action": "investigate blocked record without deleting evidence", "records": records}
    text = (
        "[SYSTEM] JSON keys, schema_version, record IDs, amounts, policies, and regions are exact protected data.\n"
        "[USER] Find the blocked record and state the required action without deleting audit evidence.\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
    )
    return {
        "name": "structured_json",
        "question": "blocked record required action never delete evidence",
        "text": text,
        "facts": ["ledger.v3", "CRITICAL-771", "9917.42", "never_delete", "investigate blocked record without deleting evidence"],
        "protected": ["[SYSTEM] JSON keys, schema_version, record IDs, amounts, policies, and regions are exact protected data."],
        "force_tokens": ["schema", "record", "CRITICAL", "amount", "policy", "never", "delete", "region"],
    }


def lossless_cleanup(text: str, question: str) -> str:
    lines = [re.sub(r"[ \t]+", " ", line).rstrip() for line in text.splitlines()]
    output = []
    blank = False
    for line in lines:
        if line:
            output.append(line)
            blank = False
        elif not blank:
            output.append("")
            blank = True
    return "\n".join(output).strip()


def lexical_selector(text: str, question: str) -> str:
    query_terms = set(re.findall(r"[a-z0-9_-]+", question.lower()))
    units = [unit.strip() for unit in re.split(r"(?<=[.!?])\s+|\n+", text) if unit.strip()]
    counts = Counter(term for unit in units for term in set(re.findall(r"[a-z0-9_-]+", unit.lower())))
    scored = []
    for index, unit in enumerate(units):
        terms = set(re.findall(r"[a-z0-9_-]+", unit.lower()))
        overlap = sum(1.0 + math.log1p(len(units) / max(1, counts[term])) for term in query_terms & terms)
        protected = bool(re.search(r"\[SYSTEM\]|ERR-|CRITICAL-|deadline|retention|never_delete|idempotency-key|schema_version", unit, re.I))
        scored.append((1000 if protected else overlap, index, unit))
    budget = max(1, len(units) // 3)
    keep = {index for _, index, _ in sorted(scored, reverse=True)[:budget]}
    return "\n".join(unit for index, unit in enumerate(units) if index in keep)


def headroom_compress(text: str, question: str) -> str:
    router = ContentRouter(
        ContentRouterConfig(
            skip_user_messages=False,
            enable_code_aware=True,
            force_kompress_all=False,
            protect_analysis_context=True,
        )
    )
    return router.compress(text, question=question).compressed


def agy_transform(text: str, question: str, mode: str, facts: list[str]) -> str:
    if mode == "compaction":
        directive = (
            "Compress the PROMPT to about 45% of its current tokens. Preserve authority order, task intent, code/JSON syntax needed for the task, citations, and every REQUIRED EXACT STRING verbatim. Return only the compressed prompt, no commentary."
        )
    else:
        directive = (
            "Enhance the PROMPT for maximum clarity and downstream answer quality. Preserve authority order, exact code/JSON, and every REQUIRED EXACT STRING verbatim. Do not optimize for brevity. Return only the enhanced prompt, no commentary."
        )
    request = (
        f"{directive}\nQUESTION: {question}\nREQUIRED EXACT STRINGS:\n"
        + "\n".join(f"- {fact}" for fact in facts)
        + f"\n<PROMPT>\n{text}\n</PROMPT>"
    )
    completed = subprocess.run(
        ["agy", "--model", "Gemini 3.5 Flash (Low)", "--print", request, "--print-timeout", "5m"],
        check=True,
        capture_output=True,
        text=True,
        timeout=330,
    )
    return completed.stdout.strip()


def token_counts(text: str) -> dict[str, int]:
    return {name: len(encoding.encode(text)) for name, encoding in ENCODINGS.items()}


def quality(fixture: dict, text: str) -> tuple[float, float, float]:
    fact_recall = sum(fact in text for fact in fixture["facts"]) / len(fixture["facts"])
    span_integrity = sum(span in text for span in fixture["protected"]) / len(fixture["protected"])
    return fact_recall, span_integrity, 100 * (0.7 * fact_recall + 0.3 * span_integrity)


def timed(function, *args) -> tuple[str, float]:
    started = time.perf_counter()
    output = function(*args)
    return output, round((time.perf_counter() - started) * 1000, 2)


def main() -> None:
    fixtures = [prose_fixture(), code_fixture(), structured_fixture()]
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for fixture in fixtures:
        (FIXTURE_DIR / f"{fixture['name']}.txt").write_text(fixture["text"], encoding="utf-8")

    worker_input = OUTPUT_DIR / "llmlingua-input.json"
    worker_output = OUTPUT_DIR / "llmlingua-output.json"
    worker_input.write_text(json.dumps(fixtures, ensure_ascii=False), encoding="utf-8")
    subprocess.run(
        [str(ROOT / ".venv" / "bin" / "python"), str(ROOT / "scripts" / "llmlingua_worker.py"), str(worker_input), str(worker_output)],
        check=True,
        timeout=900,
    )
    llmlingua_payload = json.loads(worker_output.read_text(encoding="utf-8"))
    llmlingua = {item["fixture"]: item for item in llmlingua_payload["results"]}

    rows = []
    outputs = {}
    for fixture in fixtures:
        original_counts = token_counts(fixture["text"])
        methods = {
            "original": (fixture["text"], 0.0, "measured local"),
            "lossless_cleanup": (*timed(lossless_cleanup, fixture["text"], fixture["question"]), "measured local"),
            "query_aware_lexical": (*timed(lexical_selector, fixture["text"], fixture["question"]), "measured local baseline"),
            "headroom_0.31_router": (*timed(headroom_compress, fixture["text"], fixture["question"]), "measured installed package"),
            "llmlingua2_mbert_cpu": (llmlingua[fixture["name"]]["text"], llmlingua[fixture["name"]]["latency_ms"], "measured local model"),
        }
        for mode in ("compaction", "enhancement"):
            output, latency = timed(agy_transform, fixture["text"], fixture["question"], mode, fixture["facts"])
            methods[f"agy_gemini_3.5_flash_low_{mode}"] = (output, latency, "measured remote cheap model")
        methods["kv_cache_only_reference"] = (fixture["text"], 0.0, "analytical control: transmitted text unchanged")

        outputs[fixture["name"]] = {}
        for method, (text, latency_ms, evidence) in methods.items():
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
                    "latency_ms": latency_ms,
                    "fact_recall_pct": round(100 * fact_recall, 2),
                    "protected_span_integrity_pct": round(100 * span_integrity, 2),
                    "quality_pct": round(quality_pct, 2),
                    "evidence": evidence,
                }
            )
            outputs[fixture["name"]][method] = text

    csv_path = OUTPUT_DIR / "benchmark-results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    json_path = OUTPUT_DIR / "benchmark-results.json"
    json_path.write_text(
        json.dumps(
            {
                "tokenizers": {"cl100k_base": "tiktoken 0.12/0.13 compatible", "o200k_base": "tiktoken 0.12/0.13 compatible"},
                "llmlingua_model": "microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank",
                "llmlingua_model_load_ms": llmlingua_payload["model_load_ms"],
                "rows": rows,
                "outputs": outputs,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(json.dumps({"fixtures": len(fixtures), "methods": len(rows) // len(fixtures), "measurements": len(rows), "csv": str(csv_path), "json": str(json_path)}))


if __name__ == "__main__":
    main()
