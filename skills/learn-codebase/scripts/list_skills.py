#!/usr/bin/env python3
"""
List available agent skills as `name: description` pairs.

The agent's injected <available_skills> list is often truncated, so this scans
skill directories on disk and parses each SKILL.md frontmatter to recover the
FULL descriptions needed for accurate skill selection.

Usage:
    list_skills.py [extra_dir ...]        # scan defaults (+ any extra dirs)
    list_skills.py --self-check           # run the built-in parser check

Default scan locations (first existing wins per skill name):
    ~/.agents/skills, ~/.claude/skills, ./.claude/skills, ./skills
"""

import os
import sys
from pathlib import Path

DEFAULT_DIRS = [
    "~/.agents/skills",
    "~/.claude/skills",
    "./.claude/skills",
    "./skills",
]


def parse_frontmatter(text):
    """Return {name, description} from a SKILL.md's YAML frontmatter.

    Intentionally dependency-free (no PyYAML). Handles single-line values and
    block/folded scalars (`|`, `>`) spanning multiple indented lines.
    """
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    body = text[text.find("\n", 3) + 1 : end]

    out = {}
    key = None
    buf = []
    block = False
    for line in body.splitlines():
        stripped = line.strip()
        is_top = line[:1] not in (" ", "\t") and ":" in line
        if is_top:
            if key is not None:
                out[key] = " ".join(b for b in buf if b).strip()
            raw_key, _, rest = line.partition(":")
            key = raw_key.strip()
            rest = rest.strip()
            block = rest in ("|", ">", "|-", ">-", "|+", ">+")
            buf = [] if block else [rest.strip("'\"")]
        elif key is not None and (block or stripped):
            buf.append(stripped)
    if key is not None:
        out[key] = " ".join(b for b in buf if b).strip()
    return {k: out[k] for k in ("name", "description") if k in out}


def collect(dirs):
    """Map skill name -> description across dirs (first occurrence wins)."""
    skills = {}
    for d in dirs:
        base = Path(os.path.expanduser(d))
        if not base.is_dir():
            continue
        for skill_md in sorted(base.glob("*/SKILL.md")):
            fm = parse_frontmatter(skill_md.read_text(encoding="utf-8", errors="replace"))
            name = fm.get("name") or skill_md.parent.name
            if name not in skills:
                skills[name] = fm.get("description", "").strip()
    return skills


def self_check():
    sample = (
        "---\n"
        "name: demo-skill\n"
        "description: >\n"
        "  First line of desc.\n"
        "  Second line continues.\n"
        "---\n\n# Body\n"
    )
    fm = parse_frontmatter(sample)
    assert fm["name"] == "demo-skill", fm
    assert fm["description"] == "First line of desc. Second line continues.", fm

    inline = "---\nname: x\ndescription: 'quoted, one line'\n---\n"
    fm2 = parse_frontmatter(inline)
    assert fm2 == {"name": "x", "description": "quoted, one line"}, fm2

    assert parse_frontmatter("no frontmatter here") == {}
    print("self-check OK")


def main(argv):
    if "--self-check" in argv:
        self_check()
        return 0
    dirs = DEFAULT_DIRS + [a for a in argv if not a.startswith("-")]
    skills = collect(dirs)
    if not skills:
        print("No skills found. Pass a skills directory as an argument.", file=sys.stderr)
        return 1
    for name in sorted(skills):
        print(f"{name}: {skills[name]}")
    print(f"\n({len(skills)} skills)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
