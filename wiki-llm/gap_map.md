# System Bottlenecks & Knowledge Gaps (`gap_map.md`)

> Each gap has a stable ID (`G1`, `G2`, ...) referenced by experiments (`plan.md`) and findings (`wiki-llm/findings/`).

## Open Gaps

### `G1` — Tool Selection Degradation Under High Schema Count
* **System:** `example-agent-repo`
* **Status:** `OPEN` (Priority: High)
* **Observation:** Baseline profiling in `[[EXP-000-baseline-example]]` revealed that agent tool-argument accuracy drops sharply when the prompt includes >12 MCP tool definitions.
* **Linked Experiments:** `[[EXP-000-baseline-example]]`
* **Candidate Directions:** Dynamic top-K tool retrieval; compact one-line tool stubs with on-demand schema expansion (`SPARK-01`).

### `G2` — Temporal Blindness in Chunk Retrieval
* **System:** `example-nlp-pipeline`
* **Status:** `OPEN` (Priority: Medium)
* **Observation:** Standard dense retrieval ignores document publication timestamps when chunks are sliced without header injection.
* **Linked Experiments:** None yet
* **Candidate Directions:** Prepend document metadata header to every chunk (`SPARK-02`).

## Resolved Gaps
* *(Move gaps here once an experiment verified and merged a durable fix).*
