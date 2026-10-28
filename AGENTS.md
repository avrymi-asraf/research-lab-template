# Operational Schema: Epistemic Research Lab (`AGENTS.md`)

You operate inside a dedicated **Research & Experimentation Control Repository**.
Your mission is to systematically discover, plan, implement, verify, and document improvements across external target repositories (ML, NLP, and AI Agent systems) while compounding institutional knowledge in `wiki-llm/` and `JOURNAL.md`.

## 1. Architectural Invariants (Read First)

1. **Three-Layer Memory Discipline:**
   - `experiments/EXP-*/` is the **Immutable Evidence Layer** (raw plans, execution logs, quantitative `results.json`, `patch.diff`, and `postmortem.md`). Never rewrite past experiment results.
   - `JOURNAL.md` is the **Episodic & Routing Layer** (current baselines, active `Sparks`, master index of experiments, and the `Anti-Repeat Banlist`).
   - `wiki-llm/` is the **Compiled Semantic Layer** (`index.md`, `purpose.md`, `gap_map.md`, `systems/`, `findings/`, `literature/`). Compile new lessons into existing wiki pages rather than dumping raw logs.
2. **External Code Isolation (`.targets/`):**
   - Never modify code directly inside `.targets/repos/<repo>` (the base clone).
   - Every experiment MUST execute inside its own isolated Git worktree at `.targets/worktrees/<EXP-ID>/` on branch `exp/<EXP-ID>`, created via `python3 scripts/lab.py new-exp`.
3. **Anti-Reward-Hacking & Guard Rail:**
   - Never modify evaluation scripts, benchmark datasets, or unit tests listed in `forbidden_scope`.
   - Every experiment requires TWO mechanical checks: `guard_cmd` (regression suite that must stay green) and `verify_cmd` (benchmark/metric script).
4. **Capture Hygiene (Anti-Self-Poisoning):**
   - Strictly separate **infrastructure/setup bugs** (`INFRA_INCONCLUSIVE`) from **scientific refutations** (`HYPOTHESIS_REFUTED`).
   - If a run crashes due to OOM, missing credentials, or a typo, fix the bug or log a technical note in `wiki-llm/systems/`, but NEVER record in `wiki-llm/findings/` or the `Anti-Repeat Banlist` that the scientific idea failed until it has actually run cleanly.

## 2. The 4-Phase Closed Experiment Loop

Whenever asked to run an experiment cycle or explore a new direction, execute these four phases in order:

### Phase 1: Evaluate & Orient (Architect Role)
1. Run `python3 scripts/lab.py check-drift` to check if any external target repository changed since `wiki-llm/systems/*.md` was last updated. If a page is flagged `DRIFTED`, inspect the git diff in `.targets/repos/<repo>` and update the system wiki page and its `Fingerprint: git:<sha>`.
2. Run `python3 scripts/lab.py context-pack` and read `wiki-llm/query_pack.md` (which compiles `purpose.md`, `gap_map.md`, and `JOURNAL.md`).
3. Drill into specific pages in `wiki-llm/findings/` and `wiki-llm/systems/` listed in `wiki-llm/index.md` that relate to the current bottleneck.

### Phase 2: Ideate & Plan (Architect Role)
1. Formulate a testable hypothesis that addresses an open gap in `wiki-llm/gap_map.md` or follows a high-priority `Spark` in `JOURNAL.md`.
2. **Banlist Check:** Verify that the proposed idea does not repeat a refuted approach in `JOURNAL.md` (`Anti-Repeat Banlist`) unless testing a specific new condition noted there.
3. Scaffold the experiment:
   ```bash
   python3 scripts/lab.py new-exp --id EXP-XXX --repo <target-repo> --title "<short-slug>"
   ```
4. Complete `experiments/EXP-XXX-<short-slug>/plan.md` with exact `editable_scope`, `guard_cmd`, `verify_cmd`, expected metric direction, and falsification criteria.
   *(If operating in human-in-the-loop mode, pause here for user approval of `plan.md` before Phase 3).*

### Phase 3: Implement & Verify (Technician Role)
1. Switch focus strictly to `experiments/EXP-XXX-<short-slug>/plan.md` and the isolated worktree `.targets/worktrees/EXP-XXX-<short-slug>/`.
2. **Baseline Check:** If no baseline metric is recorded for the current base commit, run `python3 scripts/lab.py evaluate --exp EXP-XXX --baseline` first.
3. Make the minimal, atomic code or configuration changes required by `plan.md` inside the worktree and commit them to the `exp/EXP-XXX-<short-slug>` branch.
4. Run mechanical verification:
   ```bash
   python3 scripts/lab.py evaluate --exp EXP-XXX
   ```
   This verifies `editable_scope`, runs `guard_cmd`, runs `verify_cmd`, saves `patch.diff`, and writes `results.json`.
5. If `execution.md` encounters a syntax/setup error, debug and retry (up to 3 attempts) before declaring `INFRA_INCONCLUSIVE`.

### Phase 4: Distill & Compound (Wiki Maintainer Role)
1. Write `experiments/EXP-XXX-<short-slug>/postmortem.md`:
   - State the verdict (`HYPOTHESIS_SUPPORTED`, `HYPOTHESIS_REFUTED`, or `INFRA_INCONCLUSIVE`).
   - Analyze *why* the metric moved (or failed to move), citing specific error cases or traces.
   - **Mandatory `Spark` Section:** While execution context is fresh, write 1–2 concrete follow-up hypotheses sparked by what you just observed.
2. Update `JOURNAL.md` via `python3 scripts/lab.py record-verdict` (or direct edit):
   - Add the row to the Experiment Matrix.
   - Update `Current Frontier` if a new best score was achieved, or add to `Anti-Repeat Banlist` if refuted.
   - Copy the new `Spark` into the `Active Sparks Queue`.
3. Update `wiki-llm/`:
   - Integrate the empirical lesson into the relevant page under `wiki-llm/findings/` (use `Status: Superseded by [[EXP-XXX]]` if overturning an older claim—never silently delete history).
   - Update `wiki-llm/gap_map.md` if a gap was resolved or a new bottleneck emerged.
   - Update `wiki-llm/index.md` and append a parseable line to `wiki-llm/log.md`.
4. Optional cleanup: run `python3 scripts/lab.py cleanup-worktree --exp EXP-XXX` (the `patch.diff` and `results.json` remain safely in `experiments/EXP-XXX/`).
