---
type: system
repo: example-agent-repo
status: fresh
updated: 2026-10-28
---
# System Profile: `example-agent-repo`

> Repo: example-agent-repo | Fingerprint: git:HEAD
> Monitored: src/agents/runner.py, src/agents/tool_selector.py, eval/run_bench.py

## 1. Overview & Architecture
`example-agent-repo` implements our tool-augmented LLM agent runtime.
* **Entry Point:** `src/agents/runner.py` (`AgentRunner.run_episode()`)
* **Tool Routing:** `src/agents/tool_selector.py` injects tool JSON schemas into the system prompt.
* **Prompt Templates:** `src/prompts/system_v2.md`

## 2. Evaluation & Guard Harness
* **Guard Command (`guard_cmd`):** `pytest tests/unit -q` (runs in ~4s, verifies parser, memory, and schema validators).
* **Verify Command (`verify_cmd`):** `python3 eval/run_bench.py --output-json` (runs 50 multi-step scenarios; outputs `{"pass_at_1": float, "p95_latency_sec": float}`).
* **Forbidden Paths:** Never edit `eval/**` or `tests/**` during an optimization experiment.

## 3. Known quirks & Environment Notes
* Requires `OPENAI_API_KEY` or local vLLM endpoint configured in `.env`.
* Large evaluation traces are written to `/tmp/agent-eval-traces/` so they do not bloat the git working tree.
