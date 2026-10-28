---
name: experiment-lab-loop
description: Manage an epistemic ML, NLP, and AI Agent experimentation control repository (wiki-llm, JOURNAL.md, and per-experiment folders) that orchestrates isolated git worktrees across external target repositories. Use whenever the user asks to plan, run, evaluate, document, or distill experiments, update the research wiki or lab journal, check code drift against wiki pages, or iterate on external codebases using the Evaluate -> Plan -> Implement -> Distill loop.
---
# Experiment Lab Loop (`wiki-llm` + `JOURNAL` + `experiments/`)

Run a disciplined, compounding research loop across external codebases without polluting target repositories or losing lessons between sessions.

## When to Use

- Initializing or operating an out-of-tree experimentation repository (`research-lab`).
- Reviewing accumulated knowledge in `wiki-llm/` and `JOURNAL.md` to propose the next high-leverage ML, NLP, or Agent experiment.
- Spawning isolated `git worktree` sandboxes for external repositories, implementing atomic hypotheses, and enforcing `Guard` (regression test) and `Verify` (benchmark metric) gates.
- Distilling experiment outcomes (`postmortem.md`, `Spark` follow-ups, `Anti-Repeat Banlist`, and `wiki-llm/findings/` synthesis).

## Core Architecture

1. **`wiki-llm/` (Compiled Semantic Memory):**
   - `index.md`: One-line-per-page catalog read first in every session.
   - `purpose.md` & `gap_map.md`: Objectives and open bottlenecks (`G1`, `G2`, ...).
   - `systems/*.md`: Target codebase architecture anchored with `> Repo: <name> | Fingerprint: git:<sha>` and `> Monitored: <paths>`.
   - `findings/*.md`: Synthesized empirical knowledge. Never overwrite history silently; mark overturned claims with `Status: Superseded by [[EXP-XXX]]`.
   - `log.md` & `query_pack.md`: Append-only timeline and 8,000-character pre-planning summary.
2. **`JOURNAL.md` (Lab Journal & Experiment Index):**
   - Tracks the **Current Frontier** (best verified baseline per repo), **Active Sparks Queue** (next ideas captured while context is hot), **Master Experiment Matrix**, and **Anti-Repeat Banlist** (refuted ideas that must not be re-run under identical conditions).
3. **`experiments/EXP-XXX-<slug>/` (Immutable Evidence Folders):**
   - Contains `plan.md`, `execution.md`, `results.json`, `postmortem.md`, and `patch.diff`.
4. **`.targets/` (Git-Ignored Execution Sandboxes):**
   - Base clones live in `.targets/repos/<repo>`.
   - Active experiments run in isolated worktrees at `.targets/worktrees/EXP-XXX-<slug>/` on branch `exp/EXP-XXX-<slug>`.

## Step-by-Step Cyclic Workflow

### Step 1: Evaluate & Orient (Architect Role)

1. Run drift detection and build the pre-planning context pack:
   ```bash
   python3 scripts/lab.py check-drift
   python3 scripts/lab.py context-pack
   ```
2. If `check-drift` flags any `wiki-llm/systems/*.md` page as `DRIFTED!`, inspect `git diff` in `.targets/repos/<repo>`, update the system page, and bump its `Fingerprint: git:<new_sha>`.
3. Read `wiki-llm/query_pack.md` (or `JOURNAL.md` + `wiki-llm/index.md` + `wiki-llm/gap_map.md`) to identify the highest-priority open gap (`G*`) or `Spark` (`SPARK-*`).

### Step 2: Ideate & Plan (Architect Role)

1. Cross-check your candidate hypothesis against Section 4 of `JOURNAL.md` (`Anti-Repeat Banlist`) so you never repeat a refuted experiment.
2. Scaffold the experiment directory and its isolated `git worktree`:
   ```bash
   python3 scripts/lab.py new-exp --id EXP-XXX --repo <target-repo> --title "<short-slug>"
   ```
3. Edit `experiments/EXP-XXX-<short-slug>/plan.md` to specify:
   - The exact mechanistic hypothesis and linked gap (`G1`, `SPARK-01`).
   - `editable_scope` (files the Technician is allowed to edit) and `forbidden_scope` (evaluation scripts and test suites that must remain untouched).
   - `guard_cmd` (fast regression tests) and `verify_cmd` (benchmark command emitting JSON metrics).

### Step 3: Implement & Verify (Technician Role)

1. Work strictly inside `.targets/worktrees/EXP-XXX-<short-slug>/` following `plan.md`. Do not load unrelated wiki files into context during coding.
2. Apply one focused, atomic experimental change and commit it to the `exp/EXP-XXX-<short-slug>` branch.
3. Execute the mechanical verification harness:
   ```bash
   python3 scripts/lab.py evaluate --exp EXP-XXX
   ```
   This verifies that no `forbidden_scope` files were touched, runs `guard_cmd`, runs `verify_cmd`, exports `patch.diff`, and updates `results.json`.
4. If the run fails due to an environment or syntax issue, fix and retry up to 3 times before marking `INFRA_INCONCLUSIVE`.

### Step 4: Distill & Compound (Wiki Maintainer Role)

1. Complete `experiments/EXP-XXX-<short-slug>/postmortem.md`:
   - Classify the outcome strictly into:
     - `HYPOTHESIS_SUPPORTED` (metric improved AND `guard_cmd` passed)
     - `HYPOTHESIS_REFUTED` (code ran cleanly and `guard_cmd` passed, but metric did not improve)
     - `INFRA_INCONCLUSIVE` (environment/setup blocker prevented a valid test)
   - Fill out the mandatory **`Spark`** section proposing 1-2 concrete follow-up hypotheses based on the error analysis.
2. Record the verdict into `JOURNAL.md`, `results.json`, and `wiki-llm/log.md`:
   ```bash
   python3 scripts/lab.py record-verdict --exp EXP-XXX --verdict <VERDICT> --metric-delta "<delta>" --summary "<one-line-lesson>"
   ```
3. Update `wiki-llm/`:
   - Weave the new empirical finding into `wiki-llm/findings/<topic>.md` and update `wiki-llm/gap_map.md` and `wiki-llm/index.md`.
   - If `HYPOTHESIS_REFUTED`, add the refuted pattern and boundary conditions to `JOURNAL.md` (`Anti-Repeat Banlist`).
4. Clean up the temporary worktree once `patch.diff` is saved:
   ```bash
   python3 scripts/lab.py cleanup-worktree --exp EXP-XXX
   ```

## Gotchas

- **Anti-Self-Poisoning:** Never log an infrastructure crash, OOM, or typo as a scientific refutation in `wiki-llm/findings/` or the `Anti-Repeat Banlist`. Only clean executions can refute a hypothesis.
- **Reward Hacking Prevention:** Never modify files in `forbidden_scope` (such as evaluation harnesses or ground-truth test labels) to make a metric go up.
- **Simplicity Bias:** If an experiment adds 150 lines of complex code for a negligible metric gain within noise, discard it and document the complexity trade-off in `postmortem.md`.
