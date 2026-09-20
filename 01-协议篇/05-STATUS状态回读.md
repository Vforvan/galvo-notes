---
title: STATUS 状态回读
tags:
  - 协议
  - XY2-100
  - STATUS
  - 反馈
created: 2026-02-14
---

# 📊 STATUS 状态回读

> [!info] 一句话版本
> STATUS 是振镜**回传给控制卡**的状态信号，用一根（一对）差分线异步传输。
> 它同时承担两个角色：**① 一个简单的"故障告警"位**，**② 一整个 20 位的状态字**。

> [!warning] 这一篇是"进阶但极其实用"的内容
> 大部分中文教程只讲 STATUS 是"一个告警位"。
> 但官方控制卡手册里其实给出了**完整的 20 位状态字定义**——
> 包括伺服就绪、温度、跟踪误差、通道校验错等。这在你调试振镜时价值极高。

---

## 1. STATUS 的两种理解层次

### 层次一：单个告警位（最基础）

规范最原始的用法：STATUS 就是**一根线**，表示"振镜状态好不好"。

> [!quote] 规范原文（Newson 技术数据表）
> The STATUS bit is **'0'** when:
> - the X axis position < maximum position error **and**
> - the Y axis position < maximum position error **and**
> - the effective rotor X current < warning level **and**
> - the effective rotor Y current < warning level **and**
> - the digital regulator runs.
>
> The STATUS bit is **'1'** when at least one of these conditions is false.
> — `Documents_TD_XY2-100_R0703.pdf` 第 2 页

**翻译成大白话**：

| STATUS 值 | 含义 |
|---|---|
| **`0`** | ✅ 一切正常：X/Y 位置误差都在允许范围内，电机电流正常，调节器在跑 |
| **`1`** | ⚠️ **至少有一项不正常**：位置跟不上、电流过高、或调节器停了 |

> [!important] 直觉记忆
> **`0` = 好，`1` = 坏。**
> 它是"故障告警位"，不是"就绪位"。
> ⚠️ 注意这与很多信号"高电平有效"的习惯相反，写代码时容易搞反。

### 层次二：20 位状态字（进阶，官方控制卡手册定义）

> [!quote] 规范原文
> "The status bit is sent by the deflection system, **it is not synchronised with the SENDCK input**."
> — `Documents_TD_XY2-100_R0703.pdf` 第 2 页

虽然规范说 STATUS "不同步"，但实际实现中它**以和 CLK 相同的节拍串行输出一个 20 位字**。
官方控制卡（halaser E1803D）的手册给出了完整定义：

---

## 2. 完整 20 位状态字定义 ✅

**2D 振镜（XY 两轴）**：

| 位 | 名称 | 值 | 含义 |
|---|---|---|---|
| 19 / C2 | 识别位 | `0` | Identification bit |
| 18 / C1 | 识别位 | `1` | Identification bit |
| 17 / C0 | 识别位 | `1` | Identification bit |
| **16 / S15** | Power state | — | **电源状态** |
| **15 / S14** | Temperature state | — | **温度状态** |
| **14 / S13** | In-field | — | **在范围内** |
| **13 / S12** | X-position ACK | — | **X 位置应答** |
| **12 / S11** | Y-position ACK | — | **Y 位置应答** |
| 11 / S10 | — | `1` | 固定值 |
| 10 / S9 | — | `0` | 固定值 |
| 9 / S8 | — | `1` | 固定值 |
| **8 / S7** | Power state | — | 电源状态（第二组） |
| **7 / S6** | Temperature state | — | 温度状态（第二组） |
| **6 / S5** | In-field | — | 在范围内（第二组） |
| **5 / S4** | X-position ACK | — | X 位置应答（第二组） |
| **4 / S3** | Y-position ACK | — | Y 位置应答（第二组） |
| 3 / S2 | — | `1` | 固定值 |
| 2 / S1 | — | `0` | 固定值 |
| 1 / S0 | — | `1` | 固定值 |
| 0 / Par | 校验位 | `0` | 偶校验位，固定为 0 |

**3D 振镜（XYZ 三轴）**：

| 位 | 3D 振镜含义 |
|---|---|
| 16 / S15 | X **servo ready**（X 伺服就绪） |
| 15 / S14 | X **temperature state**（X 温度状态） |
| 14 / S13 | X **tracking error**（X 跟踪误差） |
| 12 / S11 | Y **servo ready** |
| 11 / S10 | Y **temperature state** |
| 10 / S9 | Y **tracking error** |
| 8 / S7 | Z **servo ready** |
| 7 / S6 | Z **temperature state** |
| 6 / S5 | Z **tracking error** |
| 4 / S3 | **X channel parity error**（X 通道校验错） |
| 3 / S2 | **Y channel parity error**（Y 通道校验错） |
| 2 / S1 | **Z channel parity error**（Z 通道校验错） |
| 1 / S0 | **CLK channel error**（时钟通道错误） |

> [!success] 怎么区分 2D 还是 3D 振镜
> 用 `HEAD_STATE_MASK` 与读回值做 AND：
> - 结果 = `HEAD_STATE_2D_HEAD` → 2D 振镜头
> - 结果 = `HEAD_STATE_3D_HEAD` → 3D 振镜头
>
> 控制卡手册原文：
> "the returned value can be AND-concatenated with HEAD_STATE_MASK to find out what kind of head is connected"

---

## 3. 最有价值的几个状态位 💡

在实际调试中，下面这几个位最有诊断价值：

| 状态位 | 值为 1（或异常）时说明什么 | 怎么处理 |
|---|---|---|
| **tracking error**<br/>（跟踪误差） | 振镜**跟不上**你的指令 | ⭐ 最常见的问题！降低扫描速度 / 减小加速度 / 减少拐角急停 |
| **temperature state**<br/>（温度） | 振镜过热 | 检查散热、降低占空比、别长时间满功率连续扫描 |
| **power state** / **servo ready** | 伺服未就绪，可能欠压/过压 | 检查电源电压和电流能力 |
| **channel parity error** | ⭐ **你的校验位算错了** | 检查偶校验算法（见下文） |
| **CLK channel error** | 时钟有问题 | 检查时钟频率、是否连续、差分线是否接好 |
| **In-field** | 位置在有效范围内 | 如果你的目标点跑出了振镜范围，这里会报警 |

> [!tip] 💡 实战用法
> **把 tracking error 位接到逻辑分析仪上，和你的轨迹数据一起抓。**
> 你就能直观看到：**轨迹的哪一段让振镜跟不上了**。
> 这是优化加工参数最快的方法，比反复试参数快得多。

---

## 4. 一个重要的坑：STATUS 不同步 ⚠️

> [!quote] 规范原文
> "The status bit is sent by the deflection system, **it is not synchronised with the SENDCK input**."
> — `Documents_TD_XY2-100_R0703.pdf` 第 2 页

这意味着：

| 问题 | 说明 |
|---|---|
| 不能用于精确定时 | STATUS 的变化时刻与控制卡的时钟**没有确定关系** |
| 可能需要过采样 | 想稳定读取，需要在多个时钟周期内采样并做多数表决 |
| 位对齐不确定 | 不知道它相对你的帧在哪一位开始 → 需要靠固定值位（如 bit 11/9/8 = 1,0,1）来对齐 ⭐ |

> [!note] 💡 固定位的作用
> 注意状态字里有若干**固定值位**：bit 11 = `1`、bit 10 = `0`、bit 9 = `1`、bit 3 = `1`、bit 2 = `0`、bit 1 = `1`。
> 这些固定模式（`101` ... `101`）**就是给你做帧对齐用的同步标志**。
> 因为 STATUS 不同步，你必须靠这些已知位找到字的边界。

> [!warning] ⚠️ 各家 STATUS 定义可能不同
> **表里的定义来自 halaser E1803D 控制卡手册，是"官方参考实现"级别的资料，但不代表所有振镜都一样。**
> 控制卡手册自己也声明了：
> "The exact usage of these fields depends on the used head,
> so for further details please refer to the related scanhead manual."
>
> **铁律：换振镜必须重新查它的 STATUS 定义。**

---

## 5. 如果厂商不提供状态字

很常见的情况：便宜的国产振镜**完全不提供状态字**，STATUS 线要么悬空，要么只输出最基础的告警位。

| 情况 | 表现 | 怎么办 |
|---|---|---|
| 完全不接 STATUS | 读回全 `1` 或 `0xFFFFFFFF` | 正常，忽略即可 |
| 只输出告警位 | 读到的是单一电平 | 按层次一使用：`0` 正常，`1` 异常 |
| 输出专有格式 | 不符合上表 | 查该型号手册，或直接放弃使用 |
| 读到 `0xFFFFFFFF` | 控制卡判定"无有效数据" | ✅ 正常，说明该振镜不提供状态字 |

> [!quote] 控制卡手册原文
> "Returns head status information in case the connected scanhead provides such data via STATUS signal of XY2-100 interface.
> When the head does not provide such information or returns invalid data or a proprietary data format, the function returns **0xFFFFFFFF**."

---

## 6. 接线注意

| 项目 | 说明 |
|---|---|
| 线对数 | STATUS 也是**差分对**（STATUS+ / STATUS−） |
| 方向 | **振镜 → 控制卡**（与其他信号相反！） |
| 是否需要接 | 可选，但强烈建议接上 |
| 接反会怎样 | 逻辑取反 → `0` 和 `1` 的含义颠倒 ⚠️ 很危险，会误判 |

> [!danger] STATUS 接反是最阴险的错误
> 因为 `0` = 好、`1` = 坏，**接反之后"好"会变成"坏"**。
> 症状：振镜一切正常，但你的程序一直报"故障"。
> 或者更糟：你的程序把"正常"当"故障"，不断重启设备。

---

## 7. 读回代码示例

### 简单的告警位读取（层次一）

```c
/* 假设 STATUS 接在某个 GPIO 上 */
#include <stdbool.h>

bool galvo_is_faulty(void)
{
    /* STATUS = 1 表示异常 */
    return gpio_read(STATUS_PIN) != 0;
}

void check_galvo(void)
{
    if (galvo_is_faulty()) {
        /* 不要立刻停机！先观察，判断是暂时还是持续 */
        log_warn("振镜报告异常状态");
    }
}
```

> [!tip] 💡 工程建议：加去抖/滤波
> STATUS 是**瞬时**的，扫描快的时候 tracking error 可能只是**极短暂**地跳一下。
> 直接据此停机 → 误报频繁。
>
> 建议：**连续 N 次（例如 100 帧 = 1 ms）都异常才判定为真故障**。
> ```c
> static int fault_count = 0;
> if (galvo_is_faulty()) {
>     if (++fault_count > 100) { /* 确认故障 */ }
> } else {
>     fault_count = 0;
> }
> ```

### 完整的 20 位状态字解析（层次二）

```c
#include <stdint.h>
#include <stdio.h>

/* 解析 2D 振镜的 20 位状态字 */
void parse_head_state_2d(uint32_t s)
{
    printf("识别位 C2C1C0 = %u%u%u (应为 011)\n",
           (s >> 19) & 1, (s >> 18) & 1, (s >> 17) & 1);

    if ((s >> 16) & 1) printf("  [16] 电源状态异常\n");
    if ((s >> 15) & 1) printf("  [15] 温度状态异常\n");
    if ((s >> 14) & 1) printf("  [14] 超出范围 (In-field)\n");
    if (((s >> 13) & 1) != ((s >> 5) & 1))
        printf("  [13/5] X 位置应答不一致\n");
    if (((s >> 12) & 1) != ((s >> 4) & 1))
        printf("  [12/4] Y 位置应答不一致\n");

    /* 校验固定位，用于确认对齐正确 */
    uint32_t fixed = (s >> 1) & 0x7;   /* bit 3,2,1 */
    if (fixed != 0x5)                  /* 应为 101 = 5 */
        printf("  ⚠️ 固定位不匹配 (读到 %u，应为 5)，可能未对齐\n", fixed);
}

/* 解析 3D 振镜状态字 */
void parse_head_state_3d(uint32_t s)
{
    if (((s >> 16) & 1) == 0) printf("  X 伺服未就绪\n");
    if ((s >> 15) & 1)        printf("  X 温度告警\n");
    if ((s >> 14) & 1)        printf("  X 跟踪误差超限\n");

    if (((s >> 12) & 1) == 0) printf("  Y 伺服未就绪\n");
    if ((s >> 11) & 1)        printf("  Y 温度告警\n");
    if ((s >> 10) & 1)        printf("  Y 跟踪误差超限\n");

    if (((s >> 8) & 1) == 0)  printf("  Z 伺服未就绪\n");
    if ((s >> 7) & 1)         printf("  Z 温度告警\n");
    if ((s >> 6) & 1)         printf("  Z 跟踪误差超限\n");

    if ((s >> 4) & 1)         printf("  ⚠️ X 通道校验错 —— 检查你的偶校验算法！\n");
    if ((s >> 3) & 1)         printf("  ⚠️ Y 通道校验错\n");
    if ((s >> 2) & 1)         printf("  ⚠️ Z 通道校验错\n");
    if ((s >> 1) & 1)         printf("  ⚠️ 时钟通道错误 —— 检查 CLK 线\n");
}
```

---

## 8. 🔬 动手实验

> [!example] 实验 5.1：验证校验位
> 1. 故意把你的 X 通道校验位改成错的
> 2. 观察 STATUS 的 **X channel parity error** 位（3D 振镜的 bit 4）
> 3. 如果它变成 1 → 说明你的振镜确实在检查校验 ✅
>
> 这个实验能同时回答两个问题：
> - 振镜到底检不检查校验？
> - 我校验位的**范围**算对了没有？（见 [[01-协议篇/02-帧结构详解]] 的 ⚠️ 疑点）

> [!example] 实验 5.2：观察跟踪误差
> 1. 先按振镜能跟上的速度画圆，观察 tracking error 位 → 应该一直是 0
> 2. 逐步提高速度，直到 tracking error 开始出现 1
> 3. 记录下**临界速度**
>
> 这个速度就是你这台振镜的**实际可用上限**，比说明书上的带宽参数更真实。
> 见 [[02-硬件实现篇/05-更新率与振镜带宽匹配]]。

> [!example] 实验 5.3：确认 STATUS 是否有效
> 用逻辑分析仪抓 STATUS 线：
> - 如果一直是一条直线 → 该振镜不提供状态字
> - 如果有规律的脉冲串 → 它在输出状态字，长度应该是 20 位
> - 用 sigrok 的 xy2-100 解码器可以直接解出数值 ✅

---

## ✅ 自检

- [ ] 知道 STATUS 是振镜 → 控制卡方向
- [ ] 记得 `0` = 正常，`1` = 异常
- [ ] 知道 STATUS 不与时钟同步，不能用于精确定时
- [ ] 能说出 3 个最有诊断价值的状态位
- [ ] 知道固定位（101）可以用来做帧对齐
- [ ] 明白 STATUS 定义各家可能不同，必须查手册

---

## 📖 原厂依据

> [!quote] 原始出处
> | 内容 | 出处 |
> |---|---|
> | STATUS 位定义（0=正常，1=异常的五项条件） | `Documents_TD_XY2-100_R0703.pdf` p.2 |
> | STATUS 不与 SENDCK 同步 | `Documents_TD_XY2-100_R0703.pdf` p.2 |
> | **完整 20 位状态字位表（2D/3D）** | `E1803D_Scanner_Controller_Manual.pdf` **p.112** |
> | HEAD_STATE_MASK / 0xFFFFFFFF 语义 | 同上，p.112 |
> | "各家定义可能不同"的官方声明 | 同上，p.112 |
> | 引脚位置（IO6、STATUS+/-） | `Documents_TD_XY2-100_R0703.pdf` p.1；`Raylase_Interface_XY2-100.pdf` p.1 |
> | 状态字段的另一种串行解读约定 | sigrok `xy2-100/pd.py`（`process_stat_bit`） |
>
> ⚠️ **重要提醒**：本节的 20 位状态字表来自 **halaser E1803D 控制卡手册**。
> 它描述的是"控制卡如何解读振镜的 STATUS 输出"，是**参考实现级**的资料。
> 你手上的振镜**可能是别的定义**——务必查该型号手册。

---

## 🔗 相关

- 上一篇：[[01-协议篇/04-位置数据编码]]
- 下一篇：[[01-协议篇/06-XY2-100E增强版]]
- 实测：[[03-调试与排错篇/02-逻辑分析仪抓包]]
- 性能：[[02-硬件实现篇/05-更新率与振镜带宽匹配]]
- 回到入口：[[🏠 开始这里]]
