#!/usr/bin/env python3
"""Analyze a Hugo site's existing posts to recover the author's writing conventions.

Scans a Hugo `content` directory, parses each post's front matter (TOML/YAML/JSON),
and reports the mechanical style profile the `hugo-write-post` skill uses to match
the author: front-matter format + keys, sections, filename pattern, length/heading/
list/code stats, tag & category vocabulary, and the most-recent posts to read for voice.

Dependency-free (stdlib only), matching this repo's other scanners.

    analyze_style.py [CONTENT_DIR] [--recent N] [--json]
    analyze_style.py --self-check
"""
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import sys
import tempfile

KEY_RE = re.compile(r'^\s*["\']?([A-Za-z_][\w-]*)["\']?\s*[:=]')
LIST_ITEM_RE = re.compile(r'^\s*-\s+(.*\S)\s*$')
INLINE_LIST_RE = re.compile(r'\[(.*?)\]')
TOKEN_RE = re.compile(r'["\']?([^,"\'\[\]]+?)["\']?(?:,|$)')


def parse_front_matter(text: str):
    """Return (format, front_matter_lines, keys, values_by_key, body)."""
    lines = text.splitlines()
    if not lines:
        return None, [], [], {}, text
    first = lines[0].strip()
    if first == "+++":
        fmt, closer = "toml", "+++"
    elif first == "---":
        fmt, closer = "yaml", "---"
    elif first == "{":
        fmt, closer = "json", "}"
    else:
        return None, [], [], {}, text  # no front matter

    fm_lines: list[str] = []
    end = None
    for i in range(1, len(lines)):
        if fmt == "json":
            fm_lines.append(lines[i])
            if lines[i].strip() == closer:
                end = i
                break
        elif lines[i].strip() == closer:
            end = i
            break
        else:
            fm_lines.append(lines[i])
    body = "\n".join(lines[(end + 1):]) if end is not None else ""

    keys: list[str] = []
    values: dict[str, list[str]] = {}
    if fmt == "json":
        try:
            obj = json.loads("{\n" + "\n".join(fm_lines))
            keys = list(obj.keys())
            for k, v in obj.items():
                if isinstance(v, list):
                    values[k] = [str(x) for x in v]
        except Exception:
            pass
    else:
        current_list_key = None
        for ln in fm_lines:
            item = LIST_ITEM_RE.match(ln)
            if item and current_list_key:
                values.setdefault(current_list_key, []).append(item.group(1).strip('"\''))
                continue
            m = KEY_RE.match(ln)
            if not m:
                continue
            key = m.group(1)
            if key not in keys:
                keys.append(key)
            inline = INLINE_LIST_RE.search(ln)
            if inline:
                toks = [t.strip().strip('"\'') for t in inline.group(1).split(",")]
                vals = [t for t in toks if t]
                if vals:
                    values.setdefault(key, []).extend(vals)
                current_list_key = None
            else:
                rhs = ln[m.end():].strip().strip('"\'')
                if rhs:
                    values.setdefault(key, [rhs])  # scalar value, e.g. date/title
                    current_list_key = None
                else:
                    current_list_key = key  # a YAML block list may follow
    return fmt, fm_lines, keys, values, body


def body_stats(body: str) -> dict:
    words = len(re.findall(r"\S+", body))
    headings = len([ln for ln in body.splitlines() if re.match(r"^#{1,6}\s", ln)])
    lists = len([ln for ln in body.splitlines() if re.match(r"^\s*([-*+]|\d+\.)\s", ln)])
    code_fences = body.count("```") // 2
    images = len(re.findall(r"!\[[^\]]*\]\(", body))
    return {"words": words, "headings": headings, "list_items": lists,
            "code_blocks": code_fences, "images": images}


def find_posts(content_dir: str) -> list[str]:
    posts = []
    for root, _dirs, files in os.walk(content_dir):
        for f in files:
            if f.endswith(".md") and not f.startswith("_index"):
                posts.append(os.path.join(root, f))
    return posts


def filename_pattern(names: list[str]) -> str:
    dated = sum(1 for n in names if re.match(r"^\d{4}-\d{2}-\d{2}-", n))
    if names and dated == len(names):
        return "YYYY-MM-DD-<slug>.md"
    if dated:
        return "mixed (some date-prefixed)"
    return "<slug>.md"


def analyze(content_dir: str, recent: int = 5) -> dict:
    paths = find_posts(content_dir)
    records = []
    fmt_counts: dict[str, int] = {}
    key_counts: dict[str, int] = {}
    sections: dict[str, int] = {}
    tags: dict[str, int] = {}
    categories: dict[str, int] = {}
    for p in paths:
        try:
            text = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        fmt, _fm, keys, values, body = parse_front_matter(text)
        fmt_counts[fmt or "none"] = fmt_counts.get(fmt or "none", 0) + 1
        for k in keys:
            key_counts[k] = key_counts.get(k, 0) + 1
        rel = os.path.relpath(p, content_dir)
        section = rel.split(os.sep)[0] if os.sep in rel else "(root)"
        sections[section] = sections.get(section, 0) + 1
        for t in values.get("tags", []):
            tags[t] = tags.get(t, 0) + 1
        for c in values.get("categories", []):
            categories[c] = categories.get(c, 0) + 1
        stats = body_stats(body)
        date = (values.get("date", [None])[0] if isinstance(values.get("date"), list) else None)
        records.append({"path": rel, "name": os.path.basename(p), "format": fmt,
                        "date": date, "mtime": os.path.getmtime(p), **stats})

    def sort_key(r):
        return (r["date"] or "", r["mtime"])

    recent_posts = sorted(records, key=sort_key, reverse=True)[:recent]
    wordcounts = [r["words"] for r in records] or [0]
    headingcounts = [r["headings"] for r in records] or [0]

    def top(d, n=15):
        return [k for k, _ in sorted(d.items(), key=lambda kv: kv[1], reverse=True)[:n]]

    return {
        "content_dir": content_dir,
        "post_count": len(records),
        "front_matter_format": (max(fmt_counts, key=fmt_counts.get) if fmt_counts else None),
        "front_matter_format_counts": fmt_counts,
        "front_matter_keys": top(key_counts, 30),
        "sections": sections,
        "filename_pattern": filename_pattern([r["name"] for r in records]),
        "words_avg": round(statistics.mean(wordcounts)),
        "words_median": round(statistics.median(wordcounts)),
        "headings_avg": round(statistics.mean(headingcounts), 1),
        "tag_vocabulary": top(tags),
        "category_vocabulary": top(categories),
        "recent_posts": [{"path": r["path"], "words": r["words"], "date": r["date"]}
                         for r in recent_posts],
    }


def self_check() -> None:
    yaml_post = (
        "---\n"
        "title: \"First Post\"\n"
        "date: 2026-08-01\n"
        "draft: false\n"
        "tags: [\"hugo\", \"writing\"]\n"
        "categories: [\"blog\"]\n"
        "---\n"
        "# Hello\n\nSome words here across a couple of lines.\n\n- one\n- two\n"
    )
    toml_post = (
        "+++\n"
        "title = \"Second Post\"\n"
        "date = 2026-08-05\n"
        "tags = [\"hugo\", \"go\"]\n"
        "+++\n"
        "## Heading\n\nMore content with ```code``` inline and words.\n"
    )
    with tempfile.TemporaryDirectory() as d:
        posts = os.path.join(d, "posts")
        os.makedirs(posts)
        open(os.path.join(posts, "2026-08-01-first.md"), "w").write(yaml_post)
        open(os.path.join(posts, "2026-08-05-second.md"), "w").write(toml_post)

        fmt, _fm, keys, values, body = parse_front_matter(yaml_post)
        assert fmt == "yaml", fmt
        assert "title" in keys and "tags" in keys, keys
        assert values.get("tags") == ["hugo", "writing"], values.get("tags")
        assert "Hello" in body, "body should exclude front matter but keep content"

        fmt2, _f2, keys2, values2, _b2 = parse_front_matter(toml_post)
        assert fmt2 == "toml", fmt2
        assert values2.get("tags") == ["hugo", "go"], values2.get("tags")
        assert values2.get("date") == ["2026-08-05"], values2.get("date")

        result = analyze(d, recent=5)
        assert result["post_count"] == 2, result["post_count"]
        assert result["front_matter_format"] in ("yaml", "toml"), result
        assert "title" in result["front_matter_keys"], result["front_matter_keys"]
        assert "hugo" in result["tag_vocabulary"], result["tag_vocabulary"]
        assert result["filename_pattern"] == "YYYY-MM-DD-<slug>.md", result["filename_pattern"]
        # most-recent first, ordered by the post's own date
        assert result["recent_posts"][0]["path"].endswith("second.md"), result["recent_posts"]
        assert result["recent_posts"][0]["date"] == "2026-08-05", result["recent_posts"]
    print("self-check passed")


def main() -> int:
    ap = argparse.ArgumentParser(description="Analyze a Hugo site's writing conventions.")
    ap.add_argument("content_dir", nargs="?", default="content",
                    help="Hugo content directory (default: content)")
    ap.add_argument("--recent", type=int, default=5, help="how many recent posts to list")
    ap.add_argument("--json", action="store_true", help="emit raw JSON only")
    ap.add_argument("--self-check", action="store_true", help="run the built-in test and exit")
    args = ap.parse_args()

    if args.self_check:
        self_check()
        return 0

    if not os.path.isdir(args.content_dir):
        print(f"error: content dir not found: {args.content_dir}", file=sys.stderr)
        return 1

    result = analyze(args.content_dir, recent=args.recent)
    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print(f"# Style profile for {result['content_dir']} ({result['post_count']} posts)")
    print(f"front-matter format : {result['front_matter_format']} {result['front_matter_format_counts']}")
    print(f"front-matter keys   : {', '.join(result['front_matter_keys'])}")
    print(f"sections            : {result['sections']}")
    print(f"filename pattern    : {result['filename_pattern']}")
    print(f"length (words)      : avg {result['words_avg']}, median {result['words_median']}")
    print(f"headings per post   : avg {result['headings_avg']}")
    print(f"tags                : {', '.join(result['tag_vocabulary']) or '(none)'}")
    print(f"categories          : {', '.join(result['category_vocabulary']) or '(none)'}")
    print("recent posts (read these for voice):")
    for r in result["recent_posts"]:
        print(f"  - {r['path']}  ({r['words']} words, date {r['date']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
