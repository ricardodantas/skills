#!/usr/bin/env python3
"""Discover documentation files in a repo and report a doc drift map plus a link graph.

Classifies docs into `agent` (AGENTS.md, CLAUDE.md, .claude/, skill files), `changelog`, and
`human` (README, docs/, guides, ...). Inside a git repo, reports the files changed since a
baseline — a `--since` ref if given, else the most recent release tag — plus uncommitted work,
so the caller knows where reality drifted from the docs.

Also walks every doc's links (inline, reference-style, and HTML href/src, ignoring fenced code)
to report how the docs connect: inbound/outbound edges per doc, links pointing at paths that
don't exist, and orphans — docs nothing links to.

Usage:
    scan_docs.py [repo_root]              # default: cwd; baseline = last release tag
    scan_docs.py [repo_root] --since REF  # baseline = REF (e.g. a merge-base for a PR)
    scan_docs.py --self-check             # run assertions and exit
"""
from __future__ import annotations

import json
import os
import re
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


# Link syntaxes worth following: inline [t](target), reference defs [id]: target, HTML href/src.
FENCE_RE = re.compile(r"^\s{0,3}(```+|~~~+)")
INLINE_LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+[\"'][^\"']*[\"'])?\s*\)")
REF_DEF_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?([^\s>]+)>?", re.MULTILINE)
HTML_ATTR_RE = re.compile(r"(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)

EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:", "ftp://", "//")
# A target holding one of these is a template/placeholder, not a real path.
PLACEHOLDER_CHARS = set("<>{}$*")
# Docs an agent or reader reaches directly, so nothing has to link to them.
ENTRY_STEMS = {
    "readme", "index", "agents", "claude", "changelog", "contributing",
    "security", "code_of_conduct", "license", "skill",
}


def _strip_code(text: str) -> str:
    """Drop fenced blocks and inline code — links in them are samples, not navigation."""
    kept: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        m = FENCE_RE.match(line)
        if m:
            token = m.group(1)
            if fence is None:
                fence = token[0] * 3
            elif line.strip().startswith(fence):
                fence = None
            continue
        if fence is None:
            kept.append(re.sub(r"`[^`]*`", "", line))
    return "\n".join(kept)


def extract_links(path: Path) -> list[str]:
    """Raw link targets found in a doc, in source order."""
    try:
        body = _strip_code(path.read_text(encoding="utf-8", errors="replace"))
    except OSError:
        return []
    targets = [m.group(1) for m in INLINE_LINK_RE.finditer(body)]
    targets += REF_DEF_RE.findall(body)
    targets += HTML_ATTR_RE.findall(body)
    return targets


def _resolve(root: Path, rel: Path, target: str) -> tuple[str, str | None]:
    """Classify a link target; for `internal`, return its repo-relative path."""
    t = target.strip()
    if not t or t.startswith("#"):
        return "anchor", None
    if t.lower().startswith(EXTERNAL_PREFIXES):
        return "external", None
    if any(c in PLACEHOLDER_CHARS for c in t):
        return "placeholder", None
    t = t.split("#", 1)[0].split("?", 1)[0]
    if not t:
        return "anchor", None
    base = root if t.startswith("/") else (root / rel).parent
    dest = (base / t.lstrip("/")).resolve()
    try:
        return "internal", str(dest.relative_to(root.resolve()))
    except ValueError:
        return "outside", None


def _is_entry_point(rel: Path) -> bool:
    return rel.stem.lower() in ENTRY_STEMS or _is_agent_doc(rel)


def link_graph(root: Path, docs: list[dict]) -> dict:
    """How the docs connect: edges per doc, dead targets, and unlinked docs."""
    doc_paths = {d["path"] for d in docs}
    inbound: dict[str, set[str]] = {p: set() for p in doc_paths}
    graph: dict[str, dict] = {}
    broken: list[dict] = []
    for d in docs:
        rel = Path(d["path"])
        outs: set[str] = set()
        external = 0
        for target in extract_links(root / rel):
            kind, dest = _resolve(root, rel, target)
            if kind == "external":
                external += 1
                continue
            if kind != "internal" or dest is None:
                continue
            if not (root / dest).exists():
                broken.append({"from": d["path"], "target": target})
                continue
            if dest in doc_paths and dest != d["path"]:
                outs.add(dest)
                inbound[dest].add(d["path"])
        graph[d["path"]] = {"out": sorted(outs), "external": external}
    for path, srcs in inbound.items():
        graph[path]["in"] = sorted(srcs)
    orphans = sorted(p for p in doc_paths if not inbound[p] and not _is_entry_point(Path(p)))
    return {"graph": dict(sorted(graph.items())), "broken_links": broken, "orphans": orphans}


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


def _working_tree_changes(root: Path) -> list[str]:
    """Paths with staged/unstaged/untracked changes (`git status --porcelain`)."""
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain"], cwd=root,
            capture_output=True, text=True, check=True,
        ).stdout  # raw — porcelain columns are position-sensitive, don't strip
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    files = []
    for line in out.splitlines():
        if not line.strip():
            continue
        entry = line[3:]  # 'XY ' status prefix is always 3 chars in porcelain v1
        if " -> " in entry:  # rename/copy — keep the destination
            entry = entry.split(" -> ", 1)[1]
        files.append(entry.strip().strip('"'))
    return files


def git_changes(root: Path, since: str | None = None) -> dict:
    """Drift map: files changed since a baseline plus uncommitted work.

    Baseline is `since` if given, else the most recent release tag. With no baseline the
    map is only uncommitted work and `has_baseline` is False — the caller should then
    reconcile the whole doc set against the repo model rather than trust a diff.
    """
    if _git(root, "rev-parse", "--is-inside-work-tree") != "true":
        return {"is_git": False}
    baseline = since or _git(root, "describe", "--tags", "--abbrev=0")
    baseline_kind = "since" if since else ("tag" if baseline else None)
    committed: list[str] = []
    if baseline:
        diff = _git(root, "diff", "--name-only", f"{baseline}..HEAD")
        committed = [f for f in (diff or "").splitlines() if f]
    changed = sorted(set(committed) | set(_working_tree_changes(root)))
    return {
        "is_git": True,
        "baseline": baseline,
        "baseline_kind": baseline_kind,
        "has_baseline": bool(baseline),
        "changed_files": changed,
    }


def scan(root: Path, since: str | None = None) -> dict:
    docs = find_docs(root)
    counts: dict[str, int] = {}
    for d in docs:
        counts[d["type"]] = counts.get(d["type"], 0) + 1
    return {
        "root": str(root),
        "docs": docs,
        "counts": counts,
        "git": git_changes(root, since),
        "links": link_graph(root, docs),
    }


def self_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "README.md").write_text(
            "# hi\n"
            "[guide](docs/guide.md) [site](https://example.com) [gone](docs/missing.md)\n"
            "```\n[fenced](docs/never.md)\n```\n"
        )
        (root / "AGENTS.md").write_text("agents")
        (root / "CHANGELOG.md").write_text("changes")
        (root / ".claude").mkdir()
        (root / ".claude" / "notes.md").write_text("agent notes")
        (root / "docs").mkdir()
        (root / "docs" / "guide.md").write_text("guide — back to [README](../README.md)")
        (root / "docs" / "lonely.md").write_text("nothing links here")
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
        assert by[str(Path("docs") / "lonely.md")] == "human", by
        assert all("node_modules" not in p for p in by), "skip dirs leaked"
        assert "app.py" not in by, "non-doc picked up"
        assert result["git"]["is_git"] is False, "temp dir is not a git repo"

        links = result["links"]
        graph = links["graph"]
        guide = str(Path("docs") / "guide.md")
        assert graph["README.md"]["out"] == [guide], graph["README.md"]
        assert graph["README.md"]["external"] == 1, graph["README.md"]
        assert graph[guide]["in"] == ["README.md"], graph[guide]
        assert links["broken_links"] == [
            {"from": "README.md", "target": "docs/missing.md"}
        ], links["broken_links"]
        assert all(b["target"] != "docs/never.md" for b in links["broken_links"]), "fenced link followed"
        assert links["orphans"] == [str(Path("docs") / "lonely.md")], links["orphans"]

    import shutil
    if shutil.which("git"):
        with tempfile.TemporaryDirectory() as g:
            groot = Path(g)

            def run(*a: str) -> None:
                subprocess.run(["git", *a], cwd=groot, check=True, capture_output=True)

            run("init", "-q")
            run("config", "user.email", "t@t.t")
            run("config", "user.name", "t")
            (groot / "README.md").write_text("v1")
            run("add", "-A")
            run("commit", "-qm", "init")
            run("tag", "v1")
            (groot / "README.md").write_text("v1 changed")  # unstaged change
            (groot / "new.md").write_text("untracked doc")  # untracked
            gc = git_changes(groot)
            assert gc["baseline"] == "v1" and gc["baseline_kind"] == "tag", gc
            assert "README.md" in gc["changed_files"] and "new.md" in gc["changed_files"], gc
            run("add", "-A")
            run("commit", "-qm", "work")
            gc2 = git_changes(groot)  # now committed since the tag
            assert "README.md" in gc2["changed_files"], gc2
            gc3 = git_changes(groot, since="HEAD")  # --since overrides the tag
            assert gc3["baseline"] == "HEAD" and gc3["baseline_kind"] == "since", gc3
        print("git self-check OK")
    print("self-check OK")


def main(argv: list[str]) -> int:
    if "--self-check" in argv:
        self_check()
        return 0
    since: str | None = None
    positional: list[str] = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--since":
            since = argv[i + 1] if i + 1 < len(argv) else None
            i += 2
        elif a.startswith("--since="):
            since = a.split("=", 1)[1]
            i += 1
        elif a.startswith("--"):
            i += 1
        else:
            positional.append(a)
            i += 1
    root = Path(positional[0]).resolve() if positional else Path.cwd()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 1
    print(json.dumps(scan(root, since), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
