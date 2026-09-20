"""
xy2_encode.py -- XY2-100 帧编码器 / 解码器（参考实现 + 教学工具）

用途:
  1. 算出任意目标位置对应的 20 位帧（可直接和你代码的输出比对）
  2. 反解一个 20 位帧，验证校验位
  3. 打印完整位序波形，方便和示波器/逻辑分析仪对照

用法:
  python xy2_encode.py encode 0            # 编码单个值
  python xy2_encode.py encode -32768 0 32767   # 编码多个值
  python xy2_encode.py decode 0x30000      # 反解一个帧
  python xy2_encode.py table               # 打印常用值对照表
  python xy2_encode.py wave 0              # 打印 ASCII 波形
  python xy2_encode.py selftest            # 自检

校验位说明（关键）:
  偶校验覆盖【全部 19 个前导位】(控制字 001 + 16 位位置数据)，
  不是只覆盖 16 位数据位。
  因为控制字 001 含 1 个 '1'，只算数据位会得到【相反】的结果。
"""

import sys

# ---------------------------------------------------------------- 编码/解码

def encode(target: int) -> int:
    """有符号目标值 (-32768..32767) -> 20 位发送字（含偶校验）"""
    if not -32768 <= target <= 32767:
        raise ValueError(f"target 超出范围: {target}")
    wire = (target + 32768) & 0xFFFF          # 偏移二进制
    frame19 = (0b001 << 17) | (wire << 1)     # 控制字 bit19..17, 数据 bit16..1
    parity = bin(frame19).count("1") & 1      # 补成偶数
    return frame19 | parity                   # 校验位在 bit0


def decode(word: int):
    """20 位帧 -> (控制字, 位置发送值, 位置有符号值, 校验是否正确)"""
    word &= 0xFFFFF
    ctrl = (word >> 17) & 0b111
    wire = (word >> 1) & 0xFFFF
    target = wire - 32768
    ok = (bin(word).count("1") % 2 == 0)      # 偶校验: 1 的个数为偶数
    return ctrl, wire, target, ok


def bits20(word: int) -> str:
    return format(word & 0xFFFFF, "020b")


# ---------------------------------------------------------------- 输出

def cmd_encode(args):
    for a in args:
        t = int(a, 0)
        w = encode(t)
        ctrl, wire, _, _ = decode(w)
        print(f"target={t:7d}  wire=0x{wire:04X}  帧=0x{w:05X}  {bits20(w)}")
    print()
    print("位序: [19:17]=控制字  [16:1]=位置数据(MSB first)  [0]=偶校验")


def cmd_decode(args):
    for a in args:
        w = int(a, 0)
        ctrl, wire, target, ok = decode(w)
        print(f"帧=0x{w:05X}  {bits20(w)}")
        print(f"  控制字 = {ctrl:03b}" + ("  (001 = 位置帧 ✅)" if ctrl == 0b001 else "  ⚠️ 非标准位置帧"))
        print(f"  位置发送值 = 0x{wire:04X} = {wire}")
        print(f"  位置有符号值 = {target}")
        print(f"  偶校验 = {'✅ 正确' if ok else '❌ 错误 (整帧 1 的个数为奇数)'}")
        print()


def cmd_table(_args):
    print(f"{'target':>8} {'wire':>7} {'帧(hex)':>9}   20 位")
    print("-" * 52)
    for t in (-32768, -24576, -16384, -8192, -1, 0, 1, 8192, 16384, 24576, 32767):
        w = encode(t)
        _, wire, _, _ = decode(w)
        print(f"{t:8d}  0x{wire:04X}  0x{w:05X}   {bits20(w)}")


def cmd_wave(args):
    """打印 ASCII 波形, 方便和示波器对照"""
    t = int(args[0], 0) if args else 0
    w = encode(t)
    print(f"target={t}  帧=0x{w:05X}  {bits20(w)}")
    print()

    n = 20
    clk_hi = "‾" * 1
    # CLK: 每位 1 个周期 (这里用 2 字符表示半个周期)
    clk = "".join("┌─┐" for _ in range(n))
    data = "".join(f" {b} " for b in bits20(w))
    # SYNC: 前 19 位高, 第 20 位(校验位)低
    sync = "".join("‾‾‾" if i < 19 else "___" for i in range(n))

    print("位序:   " + "".join(f"{i+1:^3d}" for i in range(n)))
    print("内容:   " + "".join(f"{b:^3s}" for b in bits20(w)))
    print("       " + "   " * 3 + "└控制字┘" + "└────── 16 位位置数据 ──────┘" + "校验")
    print("CLK:    " + clk)
    print("SYNC:   " + sync + "   ← 前 19 位高, 校验位拉低")
    print("DATA:   " + "".join(f"{'‾' if b == '1' else '_'}" * 3 for b in bits20(w)))
    print()
    print("注: 实际数据在 CLK 上升沿变化、下降沿被采样; SYNC 高 19 位。")


def cmd_selftest(_args):
    """自检: 验证编码/解码/校验/中心值"""
    err = 0
    cases = [(-32768, 0x20001), (0, 0x30000), (1, 0x30003),
             (32767, 0x3FFFF), (-12345, 0x29F8F), (30000, 0x3EA61)]
    for t, expect in cases:
        got = encode(t)
        ok = got == expect
        if not ok:
            err += 1
        print(f"  encode({t:7d}) = 0x{got:05X}  (期望 0x{expect:05X})  "
              f"[{'PASS' if ok else 'FAIL'}]")

    # 往返一致性
    for t in range(-32768, 32768, 131):
        w = encode(t)
        _, _, back, okp = decode(w)
        if back != t or not okp:
            print(f"  [FAIL] 往返不一致: {t}")
            err += 1
    print(f"  往返测试 (500 个采样点): {'PASS' if err == 0 else '见上'}")

    # 中心值必须是 0x8000
    _, wire, _, _ = decode(encode(0))
    if wire != 0x8000:
        print(f"  [FAIL] 中心发送值应为 0x8000, 实际 0x{wire:04X}")
        err += 1
    else:
        print("  中心发送值 = 0x8000  [PASS]")

    # 每位都必须是偶数个 1
    bad = [t for t in range(-32768, 32768, 977) if bin(encode(t)).count("1") % 2]
    if bad:
        print(f"  [FAIL] {len(bad)} 个值的校验不是偶数")
        err += 1
    else:
        print("  全部值偶校验成立  [PASS]")

    print()
    print("✅ 自检通过" if err == 0 else f"❌ {err} 处失败")
    return err


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    cmd, args = sys.argv[1], sys.argv[2:]
    fns = {"encode": cmd_encode, "decode": cmd_decode, "table": cmd_table,
           "wave": cmd_wave, "selftest": cmd_selftest}
    if cmd not in fns:
        print(f"未知命令: {cmd}\n")
        print(__doc__)
        return 1
    r = fns[cmd](args)
    return r if isinstance(r, int) else 0


if __name__ == "__main__":
    # Windows 控制台默认是 GBK，直接 print 上面的 ✅/❌ 会抛
    # UnicodeEncodeError: 'gbk' codec can't encode character '\u2705'。
    # 这里把标准输出强制成 UTF-8（Python 3.7+），非 Windows 上无副作用。
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):  # 老版本 Python 或已被重定向
            pass
    raise SystemExit(main())
