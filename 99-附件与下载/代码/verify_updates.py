"""
verify_updates.py -- 校验知识库的完整性 + 确认关键更正已落盘

用法: python verify_updates.py [vault根目录]
退出码: 0 = 全部通过
"""

import os
import re
import sys
import unicodedata

VAULT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
EXCLUDE = ("_调研原始缓存", "深度调研报告", os.path.join("99-附件与下载", "代码"))
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")

# 关键更正清单: (说明, 文件, 必须包含的字符串)
MUST_HAVE = [
    ("标准编号 LasIA LIA202001", "01-协议篇/01-XY2-100协议总览.md", "LIA202001"),
    ("CLK/SYNC 互换陷阱", "01-协议篇/08-物理层与连接器.md", "CLK/SYNC"),
    ("CLK/SYNC 互换陷阱", "🏠 开始这里.md", "CLK/SYNC"),
    ("CLK/SYNC 互换陷阱", "03-调试与排错篇/03-常见故障速查.md", "CLK/SYNC"),
    ("CLK/SYNC 互换陷阱", "05-速查卡/02-引脚接线速查.md", "CLK/SYNC"),
    ("CLK/SYNC 互换陷阱", "02-硬件实现篇/04-差分驱动电路.md", "CLK/SYNC"),
    ("终端电阻规定差异", "02-硬件实现篇/04-差分驱动电路.md", "必须加"),
    ("模拟标度因子更正", "01-协议篇/07-协议家族横向对比.md", "标度因子"),
    ("SL2-100 官方定义", "01-协议篇/07-协议家族横向对比.md", "192"),
    ("XY3-100 官方标准", "01-协议篇/07-协议家族横向对比.md", "LIA202307"),
    ("撤 SCANLAB 制定者说法", "01-协议篇/01-XY2-100协议总览.md", "没有一手证据"),
    ("撤 SCANLAB 制定者说法", "04-资源库/04-论文书籍.md", "不是"),
    ("误区补充", "00-入门篇/04-常见误区.md", "标度因子"),
]


def collect(vault):
    out = []
    for dp, dn, fn in os.walk(vault):
        if any(e in dp for e in EXCLUDE):
            continue
        dn[:] = [d for d in dn if d != ".obsidian"]
        for f in fn:
            if f.endswith(".md"):
                out.append(os.path.join(dp, f))
    return out


def main():
    os.chdir(VAULT)
    notes = collect(VAULT)
    rc = 0

    # ---- 1) wikilink 完整性 ----
    paths, bases = set(), set()
    for n in notes:
        rel = os.path.relpath(n, VAULT).replace("\\", "/")
        paths.add(rel[:-3] if rel.endswith(".md") else rel)
        bases.add(os.path.splitext(os.path.basename(n))[0])

    bad, total = [], 0
    for n in notes:
        with open(n, encoding="utf-8") as f:
            for m in LINK_RE.finditer(f.read()):
                t = m.group(1).split("|")[0].split("#")[0].strip().replace("\\", "")
                if not t:
                    continue
                total += 1
                if t not in paths and t not in bases:
                    bad.append(f"{os.path.basename(n)} -> [[{t}]]")

    print(f"[1] wikilink: 检查 {len(notes)} 篇, {total} 个链接")
    if bad:
        print(f"    ❌ {len(bad)} 个失效:")
        for b in sorted(set(bad)):
            print(f"       {b}")
        rc = 1
    else:
        print("    ✅ 全部可解析")

    # ---- 2) 编码损坏检查 ----
    fffd = []
    for n in notes:
        with open(n, encoding="utf-8", errors="replace") as f:
            c = f.read().count("\ufffd")
        if c:
            fffd.append((os.path.relpath(n, VAULT), c))
    print(f"\n[2] 编码损坏 (U+FFFD): {len(fffd)} 处")
    if fffd:
        for p, c in fffd:
            print(f"    ❌ {p}: {c}")
        rc = 1
    else:
        print("    ✅ 无损坏")

    # ---- 3) 代码块闭合 ----
    odd = []
    for n in notes:
        with open(n, encoding="utf-8") as f:
            c = len(re.findall(r"(?m)^```", f.read()))
        if c % 2:
            odd.append(f"{os.path.relpath(n, VAULT)} ({c})")
    print(f"\n[3] 代码块闭合: {'✅ 正常' if not odd else '❌ ' + ', '.join(odd)}")
    if odd:
        rc = 1

    # ---- 4) 关键更正落盘确认 ----
    print("\n[4] 关键更正是否落盘:")
    for desc, rel, needle in MUST_HAVE:
        p = os.path.join(VAULT, rel)
        if not os.path.exists(p):
            print(f"    ❌ 文件缺失: {rel}")
            rc = 1
            continue
        with open(p, encoding="utf-8") as f:
            ok = needle in f.read()
        print(f"    {'✅' if ok else '❌'} {desc:<24} {rel}" + ("" if ok else f"  (未找到「{needle}」)"))
        if not ok:
            rc = 1

    # ---- 5) 遗留的错误断言扫描 ----
    # 注意: 只报"正面断言", 排除否定/纠正语境 (否则会误报我们自己的纠错说明)
    print("\n[5] 遗留错误断言扫描:")
    NEG = re.compile(r"不是|别说|并非|未找到|没有一手证据|无一手证据|不成立|错误|❌|⚠️")
    stale = [
        ("断言 SCANLAB 是协议制定者", re.compile(r"协议制定者|协议的制定者")),
        ("断言 XY3-100 与 XY2-100 引脚完全兼容",
         re.compile(r"引脚完全兼容|Same pinout as XY2-100\(E\)[^。]*无需")),
    ]
    found = False
    for desc, pat in stale:
        hits = []
        for n in notes:
            with open(n, encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    if pat.search(line) and not NEG.search(line):
                        hits.append(f"{os.path.relpath(n, VAULT)}:{i}")
        if hits:
            found = True
            print(f"    ⚠️ {desc}:")
            for h in hits:
                print(f"       {h}")
    if not found:
        print("    ✅ 未发现遗留错误断言 (已排除纠错性表述)")

    print("\n" + "=" * 60)
    print(" 全部检查通过 (PASS)" if rc == 0 else " 存在问题 (FAIL)")
    print("=" * 60)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
