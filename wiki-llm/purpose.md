# Research Purpose & Evaluation Philosophy (`purpose.md`)

## 1. Mission Statement
This lab systematically improves the accuracy, reliability, and latency of our Machine Learning, NLP, and AI Agent codebases through controlled, reproducible experiments on external repositories.

## 2. Core Evaluation Rules
1. **Simplicity Criterion:** All else being equal, simpler code and shorter prompts win. A +0.3% metric gain that adds 200 lines of brittle heuristics should be rejected (`discard`). Removing code while maintaining or improving metrics is an automatic win (`keep`).
2. **Guard First, Metric Second:** An experiment that improves the primary NLP/Agent metric but breaks existing unit/integration tests (`guard_cmd`) is invalid until repaired.
3. **Explain the Mechanism:** Every experiment must seek to explain *why* a change worked or failed, updating `wiki-llm/findings/` so our mental model of the system sharpens over time.
