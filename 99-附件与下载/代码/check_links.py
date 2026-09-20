"""
check_links.py -- 检查 Obsidian 知识库内的 wikilink 完整性

用法: python check_links.py [vault根目录]
退出码: 0 = 全部有效, 1 = 有失效链接
"""

import os
import re
import sys

VAULT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))

# 排除的目录（第三方代码 / 原始缓存 / 调研报告）
EXCLUDE = ("_调研原始缓存", "深度调研报告", os.path.join("99-附件与下载", "代码"))

LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def collect_notes(vault):
    notes = []
    for dirpath, dirnames, filenames in os.walk(vault):
        if any(e in dirpath for e in EXCLUDE):
            continue
        dirnames[:] = [d for d in dirnames if d != ".obsidian"]
        for fn in filenames:
            if fn.endswith(".md"):
                notes.append(os.path.join(dirpath, fn))
    return notes


def main():
    notes = collect_notes(VAULT)
    paths, bases = set(), set()
    for n in notes:
        rel = os.path.relpath(n, VAULT).replace("\\", "/")
        paths.add(rel[:-3] if rel.endswith(".md") else rel)   # 去掉 .md
        bases.add(os.path.splitext(os.path.basename(n))[0])

    bad, total = [], 0
    for n in notes:
        with open(n, encoding="utf-8") as f:
            txt = f.read()
        for m in LINK_RE.finditer(txt):
            raw = m.group(1)
            target = raw.split("|")[0].split("#")[0].strip()
            target = target.replace("\\", "")          # Obsidian 表格中的转义
            if not target:
                continue
            total += 1
            if target not in paths and target not in bases:
                bad.append((os.path.basename(n), target))

    print(f"检查了 {len(notes)} 篇笔记, {total} 个 wikilink")
    if not bad:
        print("✅ 全部 wikilink 均能正确解析")
        return 0

    print(f"⚠️ 发现 {len(bad)} 个无法解析的链接:")
    seen = set()
    for src, tgt in bad:
        key = (src, tgt)
        if key in seen:
            continue
        seen.add(key)
        print(f"   {src}  ->  [[{tgt}]]")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
