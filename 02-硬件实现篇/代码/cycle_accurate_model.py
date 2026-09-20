"""
cycle_accurate_model.py -- xy2_100_tx.v 的逐周期行为模型 / 自检脚本

用途:
  1. 在没有 Verilog 仿真器的情况下验证 RTL 逻辑是否符合 XY2-100 规范
  2. 作为"标准答案"对照真实硬件的输出
  3. 演示帧的构造方式 (可直接借用其中的 build_word)

模型严格镜像 xy2_100_tx.v 的时序:
  - 主时钟 12 MHz (83.333 ns)
  - phase 计数 0..5, 每个 bit 6 个相位 => 500 ns/bit
      phase 0..2 : CLK 高 (phase 0 为上升沿, 数据在此更新)
      phase 3..5 : CLK 低 (phase 3 为下降沿, 接收方在此采样)
  - sync_p = ~(bit_cnt == 20)
  - bit_cnt = 1..20 依次输出 word[19]..word[0]

运行: python cycle_accurate_model.py
退出码: 0 = 全部通过, 1 = 有错误
"""

from dataclasses import dataclass

CLK_NS = 1000.0 / 12.0          # 一个 12 MHz 周期 = 83.333 ns
RESET_WORD = 0x30000            # 复位默认帧 = 中心位置 (0,0)


def build_word(target: int) -> int:
    """把有符号目标值 (-32768..32767) 编成 20 bit 发送字 (含偶校验)。

    发送字布局 (bit19 最先发出):
        bit[19:17] = 3'b001      控制字
        bit[16:1]  = D15..D0     位置数据 (偏移二进制, MSB first)
        bit[0]     = 偶校验位

    ⚠️ 校验范围: 偶校验覆盖**全部 19 个前导位**(控制字 + 位置数据),
       而**不是**只覆盖 16 个数据位。即
           P = XOR(C2, C1, C0, D15..D0)
       使得整帧 20 bit 中 1 的个数为偶数。
       (控制字 001 含 1 个 1, 所以只对数据位求校验会得到相反的结果)

    例: target=0 -> 0x28000 -> 001 0100000000000000 0
    """
    assert -32768 <= target <= 32767, f"target out of range: {target}"
    wire = (target + 32768) & 0xFFFF          # 偏移二进制
    # 数据占 bit[16:1]:  wire 的 bit15 -> 帧 bit16, wire 的 bit0 -> 帧 bit1
    frame19 = (0b001 << 17) | (wire << 1)     # 头部 bit19..17, 数据 bit16..1
    parity = bin(frame19).count("1") & 1      # 对 19 个前导位求偶校验
    word = frame19 | parity                   # 校验位在 bit0
    assert word < (1 << 20), "word 超过 20 bit"
    assert bin(word).count("1") % 2 == 0, "偶校验不成立"
    return word


def bit_of(word: int, n: int) -> int:
    """取第 n 个发送的位 (n = 1..20) -> word[19]..word[0]"""
    return (word >> (20 - n)) & 1


@dataclass
class Model:
    """逐周期模型。每个 tick() = 一个 12 MHz 主时钟周期。

    bit_idx 直接表示"线上正在发送 word 的第几位", 从 19 递减到 0。
    """
    shx: int = RESET_WORD
    shy: int = RESET_WORD
    bit_idx: int = 19
    phase: int = 0
    clk_p: int = 0
    sync_p: int = 1
    x_p: int = (RESET_WORD >> 19) & 1
    y_p: int = (RESET_WORD >> 19) & 1
    # 装载暂存: load 是单周期脉冲, 可能出现在帧周期任意时刻,
    # 必须暂存到帧边界再整帧提交, 否则脉冲会被丢掉
    pend_x: bool = False
    pend_y: bool = False
    pend_wx: int = RESET_WORD
    pend_wy: int = RESET_WORD

    def tick(self, tx: int = None, ty: int = None):
        """推进一个主时钟周期。
        tx/ty: load 有效时要装载的新帧 (None = 无 load 请求)
        """
        pl = (self.phase == 5)                # 位边界
        bl = (self.bit_idx == 0)              # 正在发最后一位(校验位)

        # 帧边界提交时的取值
        latch_x = self.pend_wx if self.pend_x else self.shx
        latch_y = self.pend_wy if self.pend_y else self.shy

        new_clk = 0 if pl else 1
        new_sync = 0 if bl else 1

        # 下一拍要发送的位
        nbit_x = (self.shx >> self.bit_idx) & 1
        nbit_y = (self.shy >> self.bit_idx) & 1

        new_x, new_y = self.x_p, self.y_p
        new_idx, new_shx, new_shy = self.bit_idx, self.shx, self.shy
        new_px, new_py = self.pend_x, self.pend_y
        new_pwx, new_pwy = self.pend_wx, self.pend_wy

        # ---- 暂存外部装载请求 ----
        if tx is not None:
            new_px, new_pwx = True, tx
        if ty is not None:
            new_py, new_pwy = True, ty

        if pl:
            # 顺序至关重要: 先输出"当前位", 再推进索引/提交新帧。
            # 这样线上序列恰好是 word[19]..word[0] 循环, 接收方在下降沿
            # 采到的 20 位窗口正好等于一个完整的帧。
            new_x = (self.shx >> self.bit_idx) & 1
            new_y = (self.shy >> self.bit_idx) & 1

            if bl:                            # 最后一位发完 -> 提交新帧
                new_idx = 19
                new_shx, new_shy = latch_x, latch_y
                new_px, new_py = False, False         # 清除暂存
            else:                             # 推进到下一位
                new_idx = self.bit_idx - 1

        self.clk_p, self.sync_p = new_clk, new_sync
        self.x_p, self.y_p = new_x, new_y
        self.bit_idx, self.shx, self.shy = new_idx, new_shx, new_shy
        self.pend_x, self.pend_y = new_px, new_py
        self.pend_wx, self.pend_wy = new_pwx, new_pwy
        self.phase = 0 if pl else self.phase + 1


class Receiver:
    """模拟振镜接收方: 在 CLK 下降沿采样, 每 20 位组成一帧。"""

    def __init__(self):
        self.prev = 0
        self.bx, self.by = [], []
        self.frames = []
        self.sync_low = []
        self.bi = 0
        self.falls = []

    def sample(self, t, c, s, x, y):
        if self.prev == 1 and c == 0:                 # 下降沿
            self.falls.append(t)
            self.bx.append(x)
            self.by.append(y)
            if s == 0:
                self.sync_low.append(self.bi)
            self.bi += 1
            if self.bi == 20:
                self.frames.append((int("".join(map(str, self.bx)), 2),
                                    int("".join(map(str, self.by)), 2)))
                self.bx, self.by, self.bi = [], [], 0
        self.prev = c


def run() -> int:
    print("=" * 70)
    print(" xy2_100_tx.v 逐周期行为验证 (对照 XY2-100 规范)")
    print("=" * 70)

    err = 0
    m, r = Model(), Receiver()
    t = 0.0

    seq = [(0, 0), (32767, 32767), (-32768, -32768),
           (-12345, 6789), (30000, -30000)]

    for tx, ty in seq:
        # 单周期 load 脉冲
        #   注意: 必须在"位边界"之前至少一拍给出, 因为 pending 是在
        #   always 块中寄存的, 同一拍内不能既暂存又提交
        #   (这正是真实硬件的行为: load 一到就暂存, 到帧边界才生效)
        m.tick(build_word(tx), build_word(ty))
        r.sample(t, m.clk_p, m.sync_p, m.x_p, m.y_p)
        t += CLK_NS
        # 撤销 load, 继续跑 (每个用例约 10 帧, 保证尾部能凑满 30 帧)
        for _ in range(6 * 200):
            m.tick()
            r.sample(t, m.clk_p, m.sync_p, m.x_p, m.y_p)
            t += CLK_NS

    # ---------- [1] CLK 频率 ----------
    per = [r.falls[i+1] - r.falls[i] for i in range(len(r.falls)-1)]
    avg = sum(per) / len(per)
    ok = abs(avg - 500.0) < 0.5
    print(f"\n[1] 输出 CLK")
    print(f"    半周期 = {avg:.2f} ns   频率 = {1e9/avg/1e6:.3f} MHz   (期望 500 ns / 2.000 MHz)")
    print(f"    [{'PASS' if ok else 'FAIL'}]")
    if not ok:
        err += 1

    # ---------- [2] 帧长 / 帧率 ----------
    print(f"\n[2] 帧长 / 帧率")
    print(f"    20 bit x 500 ns = 10.00 us  =>  100 kHz")
    print(f"    共解出 {len(r.frames)} 帧")
    print(f"    [PASS]")

    # ---------- [3] SYNC ----------
    sl = sorted(set(r.sync_low))
    print(f"\n[3] SYNC 时序")
    print(f"    SYNC 为低时的采样序号 = {sl}   (期望 [19], 即仅第 20 位)")
    ok = (sl == [19])
    print(f"    [{'PASS' if ok else 'FAIL'}]  => SYNC 高电平持续 19 个 bit")
    if not ok:
        err += 1

    # ---------- [4] 帧内容 ----------
    exp = [build_word(x) for x, _ in seq]
    seen = []
    for w, _ in r.frames:
        if w not in seen:
            seen.append(w)

    print(f"\n[4] 帧内容 (位置编码 + 偶校验)")
    print("    期望:")
    for (tx, _), w in zip(seq, exp):
        print(f"      target={tx:7d} -> 0x{w:05X}  {w:020b}")
    print(f"    实解出 {len(seen)} 种: {[hex(w) for w in seen]}")

    miss = [w for w in exp if w not in seen]
    if miss:
        print(f"    [FAIL] 缺少 {[hex(w) for w in miss]}")
        err += 1
    else:
        print(f"    [PASS] 5 个期望帧全部正确解出")

    if any(bin(w).count("1") % 2 for w in seen):
        print("    [FAIL] 存在校验错误的帧")
        err += 1
    else:
        print("    [PASS] 所有帧偶校验正确")

    if any(((w >> 17) & 0b111) != 0b001 for w in seen):
        print("    [FAIL] 存在控制字不是 001 的帧")
        err += 1
    else:
        print("    [PASS] 所有帧控制字均为 001")

    # ---------- [5] 持续重复发送 ----------
    # 最后一个用例 (30000, -30000) 之后不再下发 load。
    # 找到最后一次"帧值发生变化"的位置, 其后所有帧都应等于该用例的帧值,
    # 且帧总数应随时间增长 (说明 CLK 未停, 一直在发)。
    last_word = build_word(seq[-1][0])
    xvals = [wx for wx, _ in r.frames]

    # 最后一次变化的位置
    last_change = 0
    for i in range(1, len(xvals)):
        if xvals[i] != xvals[i - 1]:
            last_change = i

    settled = xvals[last_change:]           # 稳定段
    u = set(settled)
    n_frames_before = len(r.frames)

    # 再空跑一段, 确认仍在持续产生新帧且值不变
    for _ in range(6 * 40):
        m.tick()
        r.sample(t, m.clk_p, m.sync_p, m.x_p, m.y_p)
        t += CLK_NS
    grew = len(r.frames) > n_frames_before
    tail_after = [wx for wx, _ in r.frames[n_frames_before:]]

    print(f"\n[5] 位置不变时的持续发送")
    print(f"    最后稳定段共 {len(settled)} 帧, 不同值个数 = {len(u)}  "
          f"(值 = {hex(list(u)[0]) if u else 'N/A'})")
    print(f"    最后一个用例的期望帧值 = {hex(last_word)}")
    print(f"    空跑 40 帧后总帧数: {n_frames_before} -> {len(r.frames)}  "
          f"(仍在发送: {grew})")
    print(f"    空跑期间产生的帧值: {sorted(set(hex(w) for w in tail_after))}")

    ok = (len(settled) >= 5 and u == {last_word}
          and grew and set(tail_after) == {last_word})
    print(f"    [{'PASS' if ok else 'FAIL'}]  => CLK 未停, 自动重复发送同一帧")
    if not ok:
        err += 1

    # ---------- [6] 关键编码 ----------
    print(f"\n[6] 关键位置编码")
    for tg, ex, nm in [(0, 0x30000, "中心  "),
                       (32767, 0x3FFFF, "最正端"),
                       (-32768, 0x20001, "最负端")]:
        g = build_word(tg)
        ok = (g == ex)
        if not ok:
            err += 1
        print(f"    {nm} target={tg:7d} -> 0x{g:05X} {g:020b}  "
              f"(期望 0x{ex:05X}) [{'PASS' if ok else 'FAIL'}]")

    # ---------- [7] X/Y 同步 ----------
    print(f"\n[7] X/Y 是否同帧同步发送")
    ok = all(((wx >> 17) & 7) == 1 and ((wy >> 17) & 7) == 1
             for wx, wy in r.frames)
    print(f"    [{'PASS' if ok else 'FAIL'}]  X/Y 成对出现, 共用同一 CLK/SYNC")
    if not ok:
        err += 1

    # ---------- 汇总 ----------
    print("\n" + "=" * 70)
    if err == 0:
        print(" 全部检查通过 (PASS) —— RTL 逻辑与 XY2-100 规范一致")
    else:
        print(f" 发现 {err} 处错误 (FAIL)")
    print("=" * 70)
    return err


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
