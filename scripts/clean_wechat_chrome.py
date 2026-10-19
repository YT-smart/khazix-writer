"""Remove WeChat reader chrome that was appended after article text.

This intentionally keeps the article body, Markdown images, author footer and
any user-written mentions before the first reader UI marker. It rewrites the
active normalized raw copies and refreshes manifest/catalog fingerprints.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

MARKER = "\n预览时标签不可点\n"

def clean_articles(root: Path) -> dict:
    raw = root / "raw" / "articles"
    removed = []
    for path in sorted(raw.glob("S*.md")):
        text = path.read_text(encoding="utf-8-sig")
        if MARKER not in text:
            continue
        body = text.split(MARKER, 1)[0].rstrip() + "\n"
        path.write_text(body, encoding="utf-8")
        removed.append({"id": path.stem, "removed_chars": len(text) - len(body), "chars": len(body)})

    manifest_path = root / "raw" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_id = {row["id"]: row for row in manifest}
    for path in sorted(raw.glob("S*.md")):
        data = path.read_bytes()
        row = by_id[path.stem]
        row["sha256"] = hashlib.sha256(data).hexdigest()
        row["chars"] = len(data.decode("utf-8-sig"))
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    catalog = root / "references" / "corpus-catalog.md"
    if catalog.exists():
        lines = ["# 原文目录", "", "| ID | 日期 | 字符数 | 状态 | 原文 |", "|---|---|---:|---|---|"]
        for row in manifest:
            lines.append(f"| {row['id']} | {row['date'] or '未知'} | {row['chars']} | {row['status']} | [{row['title']}](../{row['raw']}) |")
        catalog.write_text("\n".join(lines) + "\n", encoding="utf-8")

    log = root / "wiki" / "log.md"
    with log.open("a", encoding="utf-8") as handle:
        handle.write("\n## [2026-10-19] normalize | remove WeChat reader chrome\n\nRemoved the appended reader UI after `预览时标签不可点` from active raw article copies. Preserved article text, images, authorship/footer text before the marker, and refreshed SHA256/character counts. Original exported files remain outside the active knowledge base; this cleanup is normalization, not a claim that the source export was byte-identical.\n")
    return {"root": str(root), "cleaned": len(removed), "removed_chars": sum(x["removed_chars"] for x in removed), "items": removed}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    print(json.dumps(clean_articles(args.root.resolve()), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
