#!/usr/bin/env python3
"""Detect a Hugo repository's setup so doc lookups target the right version.

Scans a Hugo project root and reports: the config file + format, the declared/pinned
Hugo version (from config `module.hugoVersion`, or `HUGO_VERSION` in netlify.toml / CI),
whether Hugo Modules are used (go.mod), an extended-vs-standard hint, configured
theme(s), and whether this looks like a brand-new/empty repo.

The `hugo-expert` skill uses this to pin Context7/find-docs lookups to the repo's
actual version (and to fall back to "latest" for a new repo).

Dependency-free (stdlib only).

    detect_hugo.py [PROJECT_DIR]      # defaults to .
    detect_hugo.py --json
    detect_hugo.py --self-check
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile

CONFIG_NAMES = ["hugo.toml", "hugo.yaml", "hugo.yml", "hugo.json",
                "config.toml", "config.yaml", "config.yml", "config.json"]
VERSION_RE = re.compile(r'(\d+\.\d+(?:\.\d+)?)')


def _read(path: str) -> str:
    try:
        return open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def find_config(root: str):
    for name in CONFIG_NAMES:
        p = os.path.join(root, name)
        if os.path.isfile(p):
            fmt = name.rsplit(".", 1)[1].replace("yml", "yaml")
            return name, fmt
    # config/ directory (Hugo supports split config)
    cfg_dir = os.path.join(root, "config")
    if os.path.isdir(cfg_dir):
        return "config/", "dir"
    return None, None


def declared_version(root: str, config_name: str | None) -> str | None:
    """Look for a pinned Hugo version in config or common CI/deploy files."""
    texts = []
    if config_name and config_name != "config/":
        texts.append(_read(os.path.join(root, config_name)))
    cfg_dir = os.path.join(root, "config")
    if os.path.isdir(cfg_dir):
        for dirpath, _d, files in os.walk(cfg_dir):
            for f in files:
                texts.append(_read(os.path.join(dirpath, f)))
    for text in texts:
        # inline form: hugoVersion = "0.140.0" / hugoVersion.min = "0.140.0"
        m = re.search(r'hugo[_-]?[Vv]ersion(?:\.min)?\s*[:=]\s*["\']?v?' + VERSION_RE.pattern,
                      text)
        if m:
            return m.group(1)
        # split-TOML/YAML block: a `hugoVersion` header/key, then a nearby `min` version
        h = re.search(r'hugo[_-]?[Vv]ersion', text)
        if h:
            nearby = text[h.end():h.end() + 200]
            mm = re.search(r'min\s*[:=]\s*["\']?v?' + VERSION_RE.pattern, nearby)
            if mm:
                return mm.group(1)

    # Deploy/CI pins: HUGO_VERSION
    for rel in ["netlify.toml", "vercel.json", ".github/workflows"]:
        p = os.path.join(root, rel)
        if os.path.isfile(p):
            m = re.search(r'HUGO_VERSION["\']?\s*[:=]\s*["\']?v?' + VERSION_RE.pattern, _read(p))
            if m:
                return m.group(1)
        elif os.path.isdir(p):
            for f in os.listdir(p):
                m = re.search(r'HUGO_VERSION["\']?\s*[:=]\s*["\']?v?' + VERSION_RE.pattern,
                              _read(os.path.join(p, f)))
                if m:
                    return m.group(1)
    return None


def uses_modules(root: str) -> bool:
    gomod = os.path.join(root, "go.mod")
    if not os.path.isfile(gomod):
        return False
    text = _read(gomod)
    return "hugo" in text.lower() or "module " in text


def extended_hint(root: str, config_name: str | None) -> bool | None:
    """True if the project likely needs Hugo Extended (Sass/SCSS present)."""
    for dirpath, dirs, files in os.walk(root):
        # skip vendored/build dirs
        dirs[:] = [d for d in dirs if d not in
                   ("node_modules", ".git", "public", "resources", "dist")]
        for f in files:
            if f.endswith((".scss", ".sass")):
                return True
    return None


def find_themes(root: str, config_name: str | None) -> list[str]:
    themes: list[str] = []
    if config_name and config_name != "config/":
        text = _read(os.path.join(root, config_name))
        m = re.search(r'theme\s*[:=]\s*(.+)', text)
        if m:
            raw = m.group(1).strip()
            for t in re.findall(r'["\']([^"\']+)["\']', raw) or [raw]:
                t = t.strip().strip("[]").strip()
                if t and t not in themes:
                    themes.append(t)
    themes_dir = os.path.join(root, "themes")
    if os.path.isdir(themes_dir):
        for t in sorted(os.listdir(themes_dir)):
            if not t.startswith(".") and t not in themes:
                themes.append(t)
    return themes


def detect(root: str) -> dict:
    config_name, config_format = find_config(root)
    has_content = os.path.isdir(os.path.join(root, "content")) and any(
        f.endswith(".md")
        for _r, _d, fs in os.walk(os.path.join(root, "content"))
        for f in fs
    ) if os.path.isdir(os.path.join(root, "content")) else False
    is_new_repo = config_name is None and not has_content
    return {
        "project_dir": os.path.abspath(root),
        "config_file": config_name,
        "config_format": config_format,
        "declared_version": declared_version(root, config_name),
        "uses_modules": uses_modules(root),
        "needs_extended_hint": extended_hint(root, config_name),
        "themes": find_themes(root, config_name),
        "has_content": has_content,
        "is_new_repo": is_new_repo,
    }


def self_check() -> None:
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "content"))
        open(os.path.join(d, "content", "post.md"), "w").write("---\ntitle: x\n---\nhi\n")
        open(os.path.join(d, "hugo.toml"), "w").write(
            'baseURL = "https://example.com"\ntheme = "papermod"\n'
            '[module]\n[module.hugoVersion]\nmin = "0.140.0"\n'
        )
        open(os.path.join(d, "netlify.toml"), "w").write(
            '[build.environment]\nHUGO_VERSION = "0.164.0"\n'
        )
        os.makedirs(os.path.join(d, "assets"))
        open(os.path.join(d, "assets", "main.scss"), "w").write("$c: red;\n")

        r = detect(d)
        assert r["config_file"] == "hugo.toml", r["config_file"]
        assert r["config_format"] == "toml", r["config_format"]
        assert r["declared_version"] == "0.140.0", r["declared_version"]
        assert r["needs_extended_hint"] is True, r["needs_extended_hint"]
        assert "papermod" in r["themes"], r["themes"]
        assert r["has_content"] is True and r["is_new_repo"] is False, r

    # empty repo -> is_new_repo True, falls back to latest
    with tempfile.TemporaryDirectory() as d2:
        r2 = detect(d2)
        assert r2["is_new_repo"] is True, r2
        assert r2["config_file"] is None, r2
    print("self-check passed")


def main() -> int:
    ap = argparse.ArgumentParser(description="Detect a Hugo repo's version and setup.")
    ap.add_argument("project_dir", nargs="?", default=".", help="Hugo project root (default: .)")
    ap.add_argument("--json", action="store_true", help="emit raw JSON only")
    ap.add_argument("--self-check", action="store_true", help="run the built-in test and exit")
    args = ap.parse_args()

    if args.self_check:
        self_check()
        return 0

    if not os.path.isdir(args.project_dir):
        print(f"error: not a directory: {args.project_dir}", file=sys.stderr)
        return 1

    r = detect(args.project_dir)
    if args.json:
        print(json.dumps(r, indent=2))
        return 0

    print(f"# Hugo setup for {r['project_dir']}")
    if r["is_new_repo"]:
        print("brand-new repo   : yes — no config/content found; use the LATEST Hugo version")
        return 0
    print(f"config           : {r['config_file']} ({r['config_format']})")
    print(f"declared version : {r['declared_version'] or 'none pinned — detect from `hugo version` or use latest'}")
    print(f"Hugo Modules     : {'yes (go.mod)' if r['uses_modules'] else 'no (classic)'}")
    print(f"needs extended   : {'likely (Sass/SCSS present)' if r['needs_extended_hint'] else 'unknown'}")
    print(f"themes           : {', '.join(r['themes']) or '(none)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
