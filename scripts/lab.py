#!/usr/bin/env python3
"""lab.py — Zero-dependency CLI controller for the Epistemic Research Lab.

Manages external target repositories, isolated Git worktrees, 0-token code drift
detection, context-pack compilation, experiment folder scaffolding, scope/guard
verification, and journal logging using only Python 3 standard library.
"""

import argparse
import datetime as dt
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parent.parent
TARGETS_DIR = LAB_ROOT / ".targets"
REPOS_DIR = TARGETS_DIR / "repos"
WORKTREES_DIR = TARGETS_DIR / "worktrees"
WIKI_DIR = LAB_ROOT / "wiki-llm"
EXPS_DIR = LAB_ROOT / "experiments"
JOURNAL_PATH = LAB_ROOT / "JOURNAL.md"
REPOS_YAML_PATH = LAB_ROOT / "repos.yaml"


def now_iso() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def append_wiki_log(operation: str, target: str, summary: str) -> None:
    log_path = WIKI_DIR / "log.md"
    if not log_path.exists():
        return
    entry = f"## [{now_iso()}] {operation} | {target} — {summary}\n"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)


def parse_simple_repos_yaml(path: Path) -> dict:
    """Lightweight parser for repos.yaml using Python stdlib only."""
    if not path.exists():
        return {}
    repos = {}
    current = None
    current_list_key = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if stripped.startswith("- name:"):
            name = stripped.split(":", 1)[1].strip().strip('"')
            current = {
                "name": name,
                "url": "",
                "default_branch": "main",
                "setup_cmd": "",
                "guard_cmd": "",
                "verify_cmd": "",
                "editable_scope": [],
                "forbidden_scope": [],
            }
            repos[name] = current
            current_list_key = None
        elif current is not None and indent >= 4:
            if stripped.startswith("- ") and current_list_key:
                val = stripped[2:].strip().strip('"')
                current[current_list_key].append(val)
            elif ":" in stripped:
                k, v = stripped.split(":", 1)
                k = k.strip()
                v = v.strip().strip('"')
                if not v and k in ("editable_scope", "forbidden_scope"):
                    current_list_key = k
                else:
                    current[k] = v
                    current_list_key = None
    return repos


def parse_frontmatter(md_path: Path) -> dict:
    """Extract simple YAML frontmatter key-values and lists from a Markdown file."""
    if not md_path.exists():
        return {}
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm = {}
    current_list = None
    for line in parts[1].splitlines():
        raw = line.split("#", 1)[0].rstrip()
        if not raw.strip():
            continue
        s = raw.lstrip()
        if s.startswith("- ") and current_list is not None:
            fm[current_list].append(s[2:].strip().strip('"'))
        elif ":" in s:
            k, v = s.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"')
            if v == "":
                fm[k] = []
                current_list = k
            elif v == "[]":
                fm[k] = []
                current_list = None
            else:
                fm[k] = v
                current_list = None
    return fm


def cmd_init(_args: argparse.Namespace) -> None:
    REPOS_DIR.mkdir(parents=True, exist_ok=True)
    WORKTREES_DIR.mkdir(parents=True, exist_ok=True)
    (WIKI_DIR / "systems").mkdir(parents=True, exist_ok=True)
    (WIKI_DIR / "findings").mkdir(parents=True, exist_ok=True)
    (WIKI_DIR / "literature").mkdir(parents=True, exist_ok=True)
    EXPS_DIR.mkdir(parents=True, exist_ok=True)
    append_wiki_log("init", "workspace", "Verified .targets/repos, .targets/worktrees, wiki-llm, and experiments directories")
    print(f"[OK] Lab workspace initialized at: {LAB_ROOT}")
    print(f"     Target clones dir : {REPOS_DIR}")
    print(f"     Worktrees dir     : {WORKTREES_DIR}")


def cmd_sync_repos(args: argparse.Namespace) -> None:
    repos = parse_simple_repos_yaml(REPOS_YAML_PATH)
    if not repos:
        print("[WARN] No repositories found in repos.yaml")
        return
    REPOS_DIR.mkdir(parents=True, exist_ok=True)
    for name, cfg in repos.items():
        if args.repo and args.repo != name:
            continue
        target_path = REPOS_DIR / name
        url = cfg.get("url", "")
        if target_path.exists() and (target_path / ".git").exists():
            print(f"[SYNC] Fetching latest changes for {name}...")
            subprocess.run(["git", "-C", str(target_path), "fetch", "--all", "--prune"], check=False)
        else:
            if "your-org/" in url or not url:
                print(f"[SKIP] {name} has placeholder URL ({url}). Update repos.yaml or clone into {target_path}.")
                continue
            print(f"[CLONE] Cloning {name} from {url} -> {target_path}...")
            subprocess.run(["git", "clone", url, str(target_path)], check=False)
    append_wiki_log("sync-repos", args.repo or "all", "Synchronized target repositories")


def cmd_check_drift(_args: argparse.Namespace) -> None:
    """0-Token Code Drift Detection: checks Fingerprint & Monitored headers in wiki-llm/."""
    fp_pattern = re.compile(r"^>\s*Repo:\s*(\S+)\s*\|\s*Fingerprint:\s*git:(\S+)", re.MULTILINE)
    mon_pattern = re.compile(r"^>\s*Monitored:\s*(.+)$", re.MULTILINE)

    checked = 0
    drifted = 0
    print("=== 0-Token Wiki-to-Code Drift Check ===")
    for md_file in sorted(WIKI_DIR.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        fp_match = fp_pattern.search(content)
        if not fp_match:
            continue
        checked += 1
        repo_name, commit_sha = fp_match.group(1).strip(), fp_match.group(2).strip()
        mon_match = mon_pattern.search(content)
        monitored_paths = [p.strip() for p in mon_match.group(1).split(",")] if mon_match else []
        repo_path = REPOS_DIR / repo_name
        rel_md = md_file.relative_to(LAB_ROOT)

        if not (repo_path / ".git").exists():
            print(f"  [UNMOUNTED] {rel_md} -> Target repo '{repo_name}' not cloned yet in .targets/repos/{repo_name}")
            continue

        if commit_sha == "HEAD":
            head_proc = subprocess.run(
                ["git", "-C", str(repo_path), "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, check=False
            )
            print(f"  [UNPINNED]  {rel_md} -> Fingerprint is git:HEAD (current repo HEAD is {head_proc.stdout.strip()})")
            continue

        cmd = ["git", "-C", str(repo_path), "diff", "--name-only", commit_sha, "HEAD", "--"] + monitored_paths
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        changed_files = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
        if proc.returncode != 0:
            print(f"  [WARN]      {rel_md} -> Could not diff {commit_sha}..HEAD in {repo_name}")
        elif changed_files:
            drifted += 1
            print(f"  [DRIFTED!]  {rel_md} -> Monitored files changed since {commit_sha}: {', '.join(changed_files)}")
        else:
            print(f"  [FRESH]     {rel_md} -> 0 changes in monitored paths since {commit_sha}")

    print(f"Summary: {checked} fingerprinted wiki page(s) checked, {drifted} drifted.")


def cmd_context_pack(_args: argparse.Namespace) -> None:
    """Compile a compact (<8000 chars) query_pack.md for fast pre-planning orientation."""
    sections = []
    sections.append(f"# Compiled Pre-Planning Context Pack (`query_pack.md`)\n> Auto-generated on `{now_iso()}` by `scripts/lab.py context-pack`. Read this before planning a new experiment.\n")

    purpose_path = WIKI_DIR / "purpose.md"
    if purpose_path.exists():
        sections.append("## 1. Lab Purpose & Rules\n" + purpose_path.read_text(encoding="utf-8").strip()[:1200])

    gap_path = WIKI_DIR / "gap_map.md"
    if gap_path.exists():
        sections.append("## 2. Open System Gaps (`gap_map.md`)\n" + gap_path.read_text(encoding="utf-8").strip()[:2000])

    if JOURNAL_PATH.exists():
        j_text = JOURNAL_PATH.read_text(encoding="utf-8")
        sections.append("## 3. Journal Snapshot (Frontier, Active Sparks & Banlist)\n" + j_text.strip()[:3000])

    index_path = WIKI_DIR / "index.md"
    if index_path.exists():
        sections.append("## 4. Wiki Page Catalog (`index.md`)\n" + index_path.read_text(encoding="utf-8").strip()[:1500])

    out_text = "\n\n".join(sections)[:8000] + "\n"
    # Planning reminders are appended after truncation so they are always present.
    out_text += (
        "\n## Planning Reminders\n"
        "* **Ideate deeply:** use the `iterative-deep-researcher` skill and weigh at least 3 competing hypotheses before choosing one.\n"
        "* **Same experiment language:** reuse the concepts, structure, and mental model of previous experiments so the next reader instantly follows (`Experiment Language` in `wiki-llm/systems/<repo>.md`).\n"
        "* **Protect your attention:** delegate source gathering, implementation, and wiki ingestion to subagents, then review what they return.\n"
    )
    out_path = WIKI_DIR / "query_pack.md"
    out_path.write_text(out_text, encoding="utf-8")
    append_wiki_log("context-pack", "wiki-llm/query_pack.md", f"Compiled context pack ({len(out_text)} chars)")
    print(f"[OK] Compiled context pack written to: {out_path} ({len(out_text)} chars)")


def resolve_exp_dir(exp_id: str) -> Path:
    matches = sorted(EXPS_DIR.glob(f"{exp_id}*"))
    if not matches:
        raise FileNotFoundError(f"No experiment directory matching '{exp_id}*' found in {EXPS_DIR}")
    return matches[0]


def cmd_new_exp(args: argparse.Namespace) -> None:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", args.title.strip().lower()).strip("-")
    folder_name = f"{args.id}-{slug}" if not args.id.endswith(slug) else args.id
    exp_dir = EXPS_DIR / folder_name
    if exp_dir.exists():
        print(f"[ERROR] Experiment directory already exists: {exp_dir}", file=sys.stderr)
        sys.exit(1)

    template_dir = EXPS_DIR / "_TEMPLATE"
    shutil.copytree(template_dir, exp_dir)

    repos = parse_simple_repos_yaml(REPOS_YAML_PATH)
    repo_cfg = repos.get(args.repo, {})
    base_branch = args.base_branch or repo_cfg.get("default_branch", "main")
    exp_branch = f"exp/{folder_name}"
    guard_cmd = repo_cfg.get("guard_cmd", "pytest -q")
    verify_cmd = repo_cfg.get("verify_cmd", "python3 eval.py")

    # Populate plan.md template placeholders
    plan_path = exp_dir / "plan.md"
    plan_text = plan_path.read_text(encoding="utf-8")
    plan_text = (
        plan_text.replace("exp_id: EXP-XXX", f"exp_id: {folder_name}")
        .replace('title: "Short descriptive title"', f'title: "{args.title}"')
        .replace("date: YYYY-MM-DD", f"date: {dt.date.today().isoformat()}")
        .replace("target_repo: example-agent-repo", f"target_repo: {args.repo}")
        .replace("base_branch: main", f"base_branch: {base_branch}")
        .replace("exp_branch: exp/EXP-XXX", f"exp_branch: {exp_branch}")
        .replace("`EXP-XXX` — [Title]", f"`{folder_name}` — {args.title}")
        .replace('guard_cmd: "pytest tests/unit -q"', f'guard_cmd: "{guard_cmd}"')
        .replace('verify_cmd: "python3 eval/run_bench.py --output-json"', f'verify_cmd: "{verify_cmd}"')
    )
    plan_path.write_text(plan_text, encoding="utf-8")

    # Create git worktree if target repo exists in .targets/repos/
    repo_path = REPOS_DIR / args.repo
    wt_path = WORKTREES_DIR / folder_name
    base_sha = "unmounted-repo"
    if (repo_path / ".git").exists():
        WORKTREES_DIR.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "-C", str(repo_path), "worktree", "add", "-b", exp_branch, str(wt_path), base_branch],
            check=True,
        )
        sha_proc = subprocess.run(
            ["git", "-C", str(wt_path), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=False
        )
        base_sha = sha_proc.stdout.strip() or "unknown"
        print(f"[WORKTREE] Created isolated git worktree at: {wt_path} (branch: {exp_branch}, base: {base_sha})")
    else:
        print(f"[INFO] Target repo '{args.repo}' is not cloned in {repo_path} yet.")
        print(f"       Scaffolded experiment folder only. Clone repo into {repo_path} to spawn worktree.")

    # Update execution.md and results.json with metadata
    exec_path = exp_dir / "execution.md"
    exec_text = exec_path.read_text(encoding="utf-8")
    exec_text = (
        exec_text.replace("EXP-XXX", folder_name)
        .replace("example-agent-repo", args.repo)
        .replace("<auto-filled-by-lab.py>", base_sha)
        .replace("YYYY-MM-DD HH:MM", now_iso())
    )
    exec_path.write_text(exec_text, encoding="utf-8")

    res_path = exp_dir / "results.json"
    res_data = json.loads(res_path.read_text(encoding="utf-8"))
    res_data["exp_id"] = folder_name
    res_data["target_repo"] = args.repo
    res_data["base_commit"] = base_sha
    res_data["timestamp"] = now_iso()
    res_path.write_text(json.dumps(res_data, indent=2) + "\n", encoding="utf-8")

    post_path = exp_dir / "postmortem.md"
    post_path.write_text(post_path.read_text(encoding="utf-8").replace("EXP-XXX", folder_name), encoding="utf-8")

    append_wiki_log("new-exp", folder_name, f"Scaffolded experiment for {args.repo} ({args.title})")
    print(f"[OK] Experiment folder ready: {exp_dir}")


def check_scope_violations(changed_files: list, editable_scope: list, forbidden_scope: list) -> list:
    violations = []
    for fpath in changed_files:
        for pat in forbidden_scope:
            if fnmatch.fnmatch(fpath, pat) or fpath.startswith(pat.rstrip("/*")):
                violations.append(f"Forbidden file modified: {fpath} (matches {pat})")
        if editable_scope:
            allowed = any(
                fnmatch.fnmatch(fpath, pat) or fpath.startswith(pat.rstrip("/*"))
                for pat in editable_scope
            )
            if not allowed:
                violations.append(f"Out-of-scope file modified: {fpath}")
    return violations


def cmd_evaluate(args: argparse.Namespace) -> None:
    exp_dir = resolve_exp_dir(args.exp)
    fm = parse_frontmatter(exp_dir / "plan.md")
    folder_name = exp_dir.name
    wt_path = WORKTREES_DIR / folder_name

    if not wt_path.exists():
        print(f"[ERROR] Worktree not found at {wt_path}. Make sure the target repo is cloned and worktree is mounted.", file=sys.stderr)
        sys.exit(1)

    res_path = exp_dir / "results.json"
    res_data = json.loads(res_path.read_text(encoding="utf-8"))
    base_commit = res_data.get("base_commit") or "HEAD~1"

    # 1. Export patch.diff and check modified files against scope
    diff_proc = subprocess.run(["git", "-C", str(wt_path), "diff", base_commit], capture_output=True, text=True, check=False)
    (exp_dir / "patch.diff").write_text(diff_proc.stdout or "# No changes against base commit\n", encoding="utf-8")

    names_proc = subprocess.run(["git", "-C", str(wt_path), "diff", "--name-only", base_commit], capture_output=True, text=True, check=False)
    changed_files = [l.strip() for l in names_proc.stdout.splitlines() if l.strip()]

    violations = check_scope_violations(
        changed_files,
        fm.get("editable_scope", []),
        fm.get("forbidden_scope", []),
    )
    res_data["scope_check_passed"] = len(violations) == 0
    if violations:
        print("[FAIL] Scope / Anti-Reward-Hacking check failed:")
        for v in violations:
            print(f"  - {v}")
        res_path.write_text(json.dumps(res_data, indent=2) + "\n", encoding="utf-8")
        sys.exit(1)

    # 2. Run Guard command
    guard_cmd = fm.get("guard_cmd", "")
    timeout_sec = int(fm.get("timeout_sec", "600"))
    guard_ok = True
    if guard_cmd:
        print(f"[GUARD] Running guard_cmd in worktree: {guard_cmd}")
        g_proc = subprocess.run(guard_cmd, shell=True, cwd=str(wt_path), timeout=timeout_sec, capture_output=True, text=True, check=False)
        guard_ok = g_proc.returncode == 0
        print(f"        Guard status: {'PASS' if guard_ok else 'FAIL'}")
    res_data["guard_passed"] = guard_ok

    # 3. Run Verify command
    verify_cmd = fm.get("verify_cmd", "")
    if verify_cmd:
        print(f"[VERIFY] Running verify_cmd in worktree: {verify_cmd}")
        v_proc = subprocess.run(verify_cmd, shell=True, cwd=str(wt_path), timeout=timeout_sec, capture_output=True, text=True, check=False)
        stdout = v_proc.stdout.strip()
        print(f"         Verify exit code: {v_proc.returncode}")
        # Attempt to parse JSON metric dictionary from last line of stdout
        for line in reversed(stdout.splitlines()):
            line = line.strip()
            if line.startswith("{") and line.endswith("}"):
                try:
                    metrics = json.loads(line)
                    if args.baseline:
                        res_data["baseline_metrics"] = metrics
                    else:
                        res_data["candidate_metrics"] = metrics
                    break
                except json.JSONDecodeError:
                    pass

    head_proc = subprocess.run(["git", "-C", str(wt_path), "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=False)
    res_data["exp_commit"] = head_proc.stdout.strip()
    res_data["timestamp"] = now_iso()
    res_path.write_text(json.dumps(res_data, indent=2) + "\n", encoding="utf-8")
    append_wiki_log("evaluate", folder_name, f"Evaluated worktree (guard={guard_ok})")
    print(f"[OK] Saved patch.diff and updated {res_path}")


def cmd_record_verdict(args: argparse.Namespace) -> None:
    exp_dir = resolve_exp_dir(args.exp)
    folder_name = exp_dir.name
    fm = parse_frontmatter(exp_dir / "plan.md")
    res_path = exp_dir / "results.json"
    res_data = json.loads(res_path.read_text(encoding="utf-8"))
    res_data["verdict"] = args.verdict
    res_path.write_text(json.dumps(res_data, indent=2) + "\n", encoding="utf-8")

    # Append row to JOURNAL.md Section 3 table
    if JOURNAL_PATH.exists():
        j_text = JOURNAL_PATH.read_text(encoding="utf-8")
        guard_str = "✅ Pass" if res_data.get("guard_passed", True) else "❌ Fail"
        row = (
            f"| `[[{folder_name}]]` | {dt.date.today().isoformat()} | "
            f"`{fm.get('target_repo', 'repo')}` (`{fm.get('exp_branch', 'exp')}`) | "
            f"{fm.get('title', folder_name)} | `{args.metric_delta}` | {guard_str} | "
            f"**{args.verdict}** | {args.summary} |\n"
        )
        marker = "## 4. Anti-Repeat Banlist"
        if marker in j_text and f"[[{folder_name}]]" not in j_text:
            j_text = j_text.replace(marker, row + "\n" + marker, 1)
            JOURNAL_PATH.write_text(j_text, encoding="utf-8")

    append_wiki_log("verdict", folder_name, f"{args.verdict}: {args.summary} ({args.metric_delta})")
    print(f"[OK] Recorded verdict {args.verdict} for {folder_name} in JOURNAL.md and wiki-llm/log.md")


def cmd_cleanup_worktree(args: argparse.Namespace) -> None:
    exp_dir = resolve_exp_dir(args.exp)
    folder_name = exp_dir.name
    fm = parse_frontmatter(exp_dir / "plan.md")
    repo_path = REPOS_DIR / fm.get("target_repo", "")
    wt_path = WORKTREES_DIR / folder_name

    if wt_path.exists() and (repo_path / ".git").exists():
        subprocess.run(["git", "-C", str(repo_path), "worktree", "remove", "--force", str(wt_path)], check=False)
        append_wiki_log("cleanup-worktree", folder_name, "Removed temporary worktree after archiving patch.diff")
        print(f"[OK] Removed worktree {wt_path}. Experiment artifacts remain safely in {exp_dir}")
    else:
        print(f"[INFO] No active worktree found at {wt_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Epistemic Research Lab Controller (stdlib CLI)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="Initialize .targets/ and verify lab directory structure")

    p_sync = sub.add_parser("sync-repos", help="Clone or fetch external repositories from repos.yaml")
    p_sync.add_argument("--repo", help="Sync only a specific repository name")

    sub.add_parser("check-drift", help="0-token check for code drift on fingerprinted wiki-llm pages")
    sub.add_parser("context-pack", help="Compile compact wiki-llm/query_pack.md for experiment planning")

    p_new = sub.add_parser("new-exp", help="Scaffold a new experiment folder and spawn an isolated git worktree")
    p_new.add_argument("--id", required=True, help="Experiment ID prefix (e.g. EXP-001)")
    p_new.add_argument("--repo", required=True, help="Target repository name from repos.yaml")
    p_new.add_argument("--title", required=True, help="Short title or hypothesis slug")
    p_new.add_argument("--base-branch", help="Override default base branch")

    p_eval = sub.add_parser("evaluate", help="Check scope, run guard_cmd and verify_cmd in worktree, export patch.diff")
    p_eval.add_argument("--exp", required=True, help="Experiment ID (e.g. EXP-001)")
    p_eval.add_argument("--baseline", action="store_true", help="Record metrics as baseline_metrics")

    p_verdict = sub.add_parser("record-verdict", help="Record experiment verdict into results.json, JOURNAL.md, and log.md")
    p_verdict.add_argument("--exp", required=True, help="Experiment ID (e.g. EXP-001)")
    p_verdict.add_argument("--verdict", required=True, choices=["HYPOTHESIS_SUPPORTED", "HYPOTHESIS_REFUTED", "INFRA_INCONCLUSIVE", "BASELINE"])
    p_verdict.add_argument("--metric-delta", required=True, help="Short metric change string (e.g. '+4.2% F1')")
    p_verdict.add_argument("--summary", required=True, help="One-line takeaway for JOURNAL.md")

    p_clean = sub.add_parser("cleanup-worktree", help="Remove temporary git worktree after patch.diff is saved")
    p_clean.add_argument("--exp", required=True, help="Experiment ID (e.g. EXP-001)")

    args = parser.parse_args()
    dispatch = {
        "init": cmd_init,
        "sync-repos": cmd_sync_repos,
        "check-drift": cmd_check_drift,
        "context-pack": cmd_context_pack,
        "new-exp": cmd_new_exp,
        "evaluate": cmd_evaluate,
        "record-verdict": cmd_record_verdict,
        "cleanup-worktree": cmd_cleanup_worktree,
    }
    dispatch[args.cmd](args)


if __name__ == "__main__":
    main()
