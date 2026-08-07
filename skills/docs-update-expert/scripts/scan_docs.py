#!/usr/bin/env python3
"""Discover documentation files in a repo and report what changed since the last release.

Classifies docs into `agent` (AGENTS.md, CLAUDE.md, .claude/, skill files) vs `human`
(README, docs/, guides, changelog, etc.), and — inside a git repo — lists files changed
since the most recent release tag so the agent knows where reality drifted from the docs.

Usage:
    scan_docs.py [repo_root]          # default: cwd
    scan_docs.py --self-check         # run assertions and exit
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# Directories that never contain source-of-truth docs worth reconciling.
SKIP_DIRS = {
    ".git", "node_modules", "dist", "build", "target", "vendor", ".venv",
    "venv", "__pycache__", ".next", ".turbo", ".cache", "coverage", ".idea",
}

DOC_EXTS = {".md", ".mdx", ".markdown", ".rst", ".adoc", ".txt"}

# Docs written for an AI agent — route these through the writing-for-agents skill.
AGENT_NAMES = {"agents.md", "claude.md", "cursor.md", "copilot-instructions.md", "skill.md"}


def _is_agent_doc(rel: Path) -> bool:
    name = rel.name.lower()
    if name in AGENT_NAMES:
        return True
    parts = {p.lower() for p in rel.parts}
    return ".claude" in parts or ".cursor" in parts


def _classify(rel: Path) -> str:
    if _is_agent_doc(rel):
        return "agent"
    if rel.name.upper().startswith("CHANGELOG"):
        return "changelog"
    return "human"


def find_docs(root: Path) -> list[dict]:
    docs: list[dict] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            p = Path(dirpath) / fn
            rel = p.relative_to(root)
            if p.suffix.lower() in DOC_EXTS or fn.lower() in AGENT_NAMES:
                docs.append({"path": str(rel), "type": _classify(rel)})
    docs.sort(key=lambda d: d["path"])
    return docs


def _git(root: Path, *args: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", *args], cwd=root, capture_output=True, text=True, check=True
        )
        return out.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def git_changes(root: Path) -> dict:
    """Files changed since the most recent release tag (or the whole history if untagged)."""
    if _git(root, "rev-parse", "--is-inside-work-tree") != "true":
        return {"is_git": False}
    last_tag = _git(root, "describe", "--tags", "--abbrev=0")
    rng = f"{last_tag}..HEAD" if last_tag else None
    changed = _git(root, "diff", "--name-only", rng) if rng else _git(root, "ls-files")
    files = [f for f in (changed or "").splitlines() if f]
    return {"is_git": True, "last_tag": last_tag, "changed_files": files}


def scan(root: Path) -> dict:
    docs = find_docs(root)
    counts: dict[str, int] = {}
    for d in docs:
        counts[d["type"]] = counts.get(d["type"], 0) + 1
    return {"root": str(root), "docs": docs, "counts": counts, "git": git_changes(root)}


def self_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "README.md").write_text("# hi")
        (root / "AGENTS.md").write_text("agents")
        (root / "CHANGELOG.md").write_text("changes")
        (root / ".claude").mkdir()
        (root / ".claude" / "notes.md").write_text("agent notes")
        (root / "docs").mkdir()
        (root / "docs" / "guide.md").write_text("guide")
        skill = root / "skills" / "x"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("skill")
        (root / "node_modules").mkdir()
        (root / "node_modules" / "junk.md").write_text("ignore me")
        (root / "app.py").write_text("print(1)")  # non-doc

        result = scan(root)
        by = {d["path"]: d["type"] for d in result["docs"]}
        assert "README.md" in by and by["README.md"] == "human", by
        assert by["AGENTS.md"] == "agent", by
        assert by["CHANGELOG.md"] == "changelog", by
        assert by[str(Path(".claude") / "notes.md")] == "agent", by
        assert by[str(Path("skills") / "x" / "SKILL.md")] == "agent", by
        assert by[str(Path("docs") / "guide.md")] == "human", by
        assert all("node_modules" not in p for p in by), "skip dirs leaked"
        assert "app.py" not in by, "non-doc picked up"
        assert result["git"]["is_git"] is False, "temp dir is not a git repo"
    print("self-check OK")


def main(argv: list[str]) -> int:
    if "--self-check" in argv:
        self_check()
        return 0
    args = [a for a in argv if not a.startswith("--")]
    root = Path(args[0]).resolve() if args else Path.cwd()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 1
    print(json.dumps(scan(root), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
