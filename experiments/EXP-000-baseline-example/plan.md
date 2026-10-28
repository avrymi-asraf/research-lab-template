---
exp_id: EXP-000-baseline-example
title: "Establish baseline metrics and failure taxonomy on example-agent-repo"
date: 2026-10-28
target_repo: example-agent-repo
base_branch: main
exp_branch: exp/EXP-000-baseline-example
linked_gaps:
  - G1
inspired_by: []
editable_scope:
  - "src/agents/**"
forbidden_scope:
  - "eval/**"
  - "tests/**"
guard_cmd: "pytest tests/unit -q"
verify_cmd: "python3 eval/run_bench.py --output-json"
primary_metric: "pass_at_1"
metric_direction: "maximize"
timeout_sec: 600
status: COMPLETED
---
# Experiment Plan: `EXP-000-baseline-example`

## 1. Context & Motivation
Before modifying prompts or routing code in `example-agent-repo`, we need a clean, reproducible baseline measurement and a breakdown of failure categories.

## 2. Testable Hypothesis
Running the unmodified `main` branch through the guard and evaluation suites will establish our anchor metrics (`Pass@1` and `P95 latency`) and reveal the primary failure bottleneck.
