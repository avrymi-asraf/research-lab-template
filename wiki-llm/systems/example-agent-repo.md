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

## 1b. Experiment Language (Must Stay Consistent)
> Every experiment on this repo is expressed in this shared language: the same concepts, the same structure, the same mental model. Anyone who understood one experiment should immediately understand the next. Change this frame only when the frame itself is the hypothesis, and update this section when such an experiment is promoted.
* **Mental Model:** An episode = one task → `AgentRunner` loop → (select tools → prompt → model call → tool execution)* → final answer scored by the bench. An experiment changes *one* stage of this loop and leaves the rest fixed.
* **Core Concepts & Vocabulary:** *episode*, *tool schema*, *tool selector*, *system prompt variant*, *trace*. Use these terms in code, plans, and postmortems. Do not coin synonyms.
* **Structure:** New behavior is a pluggable component in `src/agents/` (e.g., a new `ToolSelector` subclass) or a new prompt file `src/prompts/system_vN.md`, selected through `configs/*.yaml`, never via a parallel runner or hard-coded flags.
* **Tooling:** Python 3.11, `uv`, `pydantic` tool schemas, OpenAI-compatible client (or local vLLM), `pytest`.

## 2. Evaluation & Guard Harness
* **Guard Command (`guard_cmd`):** `pytest tests/unit -q` (runs in ~4s, verifies parser, memory, and schema validators).
* **Verify Command (`verify_cmd`):** `python3 eval/run_bench.py --output-json` (runs 50 multi-step scenarios; outputs `{"pass_at_1": float, "p95_latency_sec": float}`).
* **Forbidden Paths:** Never edit `eval/**` or `tests/**` during an optimization experiment.

## 3. Known quirks & Environment Notes
* Requires `OPENAI_API_KEY` or local vLLM endpoint configured in `.env`.
* Large evaluation traces are written to `/tmp/agent-eval-traces/` so they do not bloat the git working tree.
