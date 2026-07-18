#!/usr/bin/env python3

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from scripts.lib.fusion.engine import FusionEngine


def main() -> None:
    source_path, output_path = sys.argv[1:3]
    payload = json.load(open(source_path, encoding="utf-8"))
    engine = FusionEngine(enable_rewind=True)
    results = []
    for fixture in payload:
        started = time.perf_counter()
        result = engine.compress(text=fixture["text"])
        compressed = result.get("compressed", result.get("content", ""))
        text_latency_ms = round((time.perf_counter() - started) * 1000, 2)
        text = fixture["text"]
        system_text, user_text = text.split("\n[USER] ", 1)
        messages = [
            {"role": "system", "content": system_text.removeprefix("[SYSTEM] ")},
            {"role": "user", "content": user_text},
        ]
        messages_started = time.perf_counter()
        message_result = engine.compress_messages(messages)
        message_text = "\n".join(
            f"[{message['role'].upper()}] {message['content']}" for message in message_result["messages"]
        )
        results.append(
            {
                "fixture": fixture["name"],
                "text": compressed,
                "latency_ms": text_latency_ms,
                "stats": result.get("stats", {}),
                "markers": result.get("markers", []),
                "message_text": message_text,
                "message_latency_ms": round((time.perf_counter() - messages_started) * 1000, 2),
                "message_stats": message_result.get("stats", {}),
                "message_markers": message_result.get("markers", []),
                "message_warnings": message_result.get("warnings", []),
            }
        )
    json.dump({"results": results}, open(output_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
