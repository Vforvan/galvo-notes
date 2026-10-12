# XY2-100 振镜扫描控制协议技术报告

> 编制说明：本报告所有规格均标注来源链接。凡标注「未找到公开数据」处，表示在本次检索范围内未找到可靠公开资料；凡「来源冲突」处，均并列给出各来源数值，不做单一断言。代码级结论均来自实际开源实现源码，非推测。

## 证据分级约定

| 标记 | 含义 |
|---|---|
| **【一手】** | 厂商官方数据手册 / 官方接口文档 / 可直接阅读的原始源码。可复现、可核对 |
| **【二手】** | 博客、论坛、技术文章、第三方分析。方向可能正确，数值需自行验证 |
| **【存疑】** | 来源互相矛盾，或原文表述含糊，或由本报告从源码推导（非原文直接陈述） |
| **【推导】** | 本报告基于已下载源码/数据计算得出，**不是**任何来源的原文陈述 |

**检索方法说明**：本次调研中 `web_fetch` 工具在本环境**不可用**（对任意主机均返回 "URL hostname resolves to a non-public IP address"），全部网页改用 `pwsh` + `Invoke-WebRequest` 抓取后本地转文本（`pdftotext`）。`blog.csdn.net` 间歇性返回 HTTP 521、`gitcode.com` 返回 418、`zhihu.com` 返回 403、`wenku.baidu.com` 返回安全验证页 —— 这些站点的内容只能通过 `web_search` 摘要间接引用，已相应标注为【二手】。**所有标注「已验证 HTTP 200」的 URL 均经实际请求确认。**

**核心一手来源**（互相独立、可交叉验证）：
1. ⭐ **LasIA LIA202001《XY2-100 Laser Scanner Protocol Format Specification》** —— **XY2-100 的正式标准原文**（经 MD5 校验，即网上流传的 aaronvose/Quantronix 版）
2. ⭐ **LasIA LIA202002 / LIA202307《XY3-100 Protocol Format Specification》** —— XY2-100 的官方后继标准（含官方对照表与 DB25 引脚表）
3. ⭐ **SCANLAB RTC6 Manual Doc. Rev. 1.1.4 附录 F（p.1214）** —— **SL2-100 官方定义**
4. **SCANLAB RTC4 手册 §6.3 + intelliSCAN / XY2-100 Converter 引脚文档** —— SCANLAB 侧引脚定义
5. **Newson Engineering rhothor X7 XY2-100 Technical Datasheet**（Rev 0703）—— 引脚、时序、控制字、STATUS 语义
6. **RAYLASE SS-III XY2-100-E Interface Documentation**（44 页）—— Enhanced 协议最完整的一手文档
7. **sigrok libsigrokdecode `xy-100/pd.py` 源码 + HALaser E1803D 手册** —— 帧类型判定与模式对照表

> 🚨 **本报告最重要的一条结论（详见 [2.3 节 (0)](#23-引脚定义四种厂商--官方标准对照)）**：
> **XY2-100 与 XY3-100 在同一条 DB25 上，CLK 与 SYNC 是互换的。**
> XY2-100 为 `1/14 = CLK`、`2/15 = SYNC`（RAYLASE / SCANLAB / Newson / Ray-Motion 四家一手一致）；
> XY3-100 为 `1/14 = SYNC (A)`、`2/15 = CLK (B)`（LasIA 官方标准）。
> 因此 XY3-100 规范中 "Same pinout as XY2-100(E)" 这句话**只在数据线上成立**。

---

## 目录

1. [协议定位与命名](#1-协议定位与命名)
2. [物理层](#2-物理层)
3. [时序规范](#3-时序规范)
4. [帧结构](#4-帧结构)
5. [位置编码与量程映射](#5-位置编码与量程映射)
6. [反馈/状态通道](#6-反馈状态通道)
7. [协议族对比](#7-协议族对比)
8. [实现要点（FPGA / MCU）](#8-实现要点fpgamcu)
9. [工程陷阱与实战经验](#9-工程陷阱与实战经验)
10. [实用数字：带宽、角度、分辨率、应用](#10-实用数字带宽角度分辨率应用)
11. [数据冲突与未确认项](#11-数据冲突与未确认项)
12. [参考链接](#12-参考链接)

---

## 0. 关键结论速查

| 项目 | 数值 |
|---|---|
| 帧长 | **20 bit / 轴 / 帧** |
| 位置字长 | 16 bit（标准）/ 18 bit（Enhanced） |
| 标称时钟 | **2 MHz**（周期 500 ns） |
| 帧周期 | **10 µs**（20 × 500 ns） |
| 帧率 / 更新率 | **100 kwords/s**（= 100 kHz） |
| 数据发送边沿 | CLK **上升沿**变化 |
| 数据采样边沿 | CLK **下降沿**被振镜采样 |
| SYNC 极性 | 高电平持续 **19** 个时钟，第 20 位（校验位）为低 |
| 校验 | **偶校验**（标准，对全部 19 个前导位）/ **奇校验**（18 bit Enhanced） |
| 位序 | **MSB first**（先发 C2 C1 C0，再发 D15…D0） |
| 位置编码 | **偏移二进制（offset binary）**，0x8000 = 中心 = 0 |
| 控制字 | `001` = 位置帧；`111` = 命令帧（仅 Enhanced） |
| 电气 | **差分 RS-422**（**不是 LVDS**），双绞线；RAYLASE SS-III 与 SCANLAB RTC4 **无电气隔离**（RTC5/6 的 SL2-100 才有） |
| 连接器 | **DB25 / 25-pin D-SUB**（RTC5/6 的 SL2-100 为 9-pin D-SUB） |
| **分辨率上限** | **16 bit = 11 µrad**（@ ±0.36 rad 光学角）—— 这是 XY2-100 的精度天花板 |
| 典型系统延迟 | 前向 **数十 µs**（TD_TX = 13 + 20 + T_Int µs）；反馈 **36 µs** |
| **官方标准编号** | **LasIA LIA202001**（XY2-100）；后继标准 XY3-100 = LIA202002 / LIA202307 |
| 🚨 **最危险陷阱** | **XY2-100 与 XY3-100 在同一 DB25 上 CLK/SYNC 互换**（1/14：XY2-100=CLK，XY3-100=SYNC） |

---

## 1. 协议定位与命名

XY2-100 是**同步串行**协议，用于把 X/Y（可选 Z）坐标从控制卡发送到振镜（检流计扫描器）偏转系统。它是行业事实标准，其后被大量厂商实现（SCANLAB、RAYLASE、金橙子 JCZ、世纪桑尼、大族、Ray-Motion 等）。

- 命名解读：`XY` = 双轴；`2` = 第二代；`100` = **100 kwords/s** 更新率。
- SCANLAB 官方把该接口称为 **XY2-100**（RTC4 控制卡）与 **XY2-100-Enhanced**（intelliSCAN 系列）。
- RAYLASE 官方文档称 **XY2-100-E**（Enhanced）。
- 相关变体：**XY2-200**（4 MHz / 200 kHz 版本）、**SL2-100**（SCANLAB 新一代 20 bit 数字接口）、**XY3-100**（LasIA 定义的官方后继标准）。

### 1.1 ⭐ 官方标准归属：LasIA（重要更正）

**XY2-100 并非"只有厂商手册、没有正式标准"——它是一份有编号的正式行业标准。**

| 标准编号 | 名称 | 版本 | 发布方 |
|---|---|---|---|
| **LIA202001** | **XY2-100 Laser Scanner Protocol Format Specification** | — | **LasIA**（Laser Industry Association） |
| **LIA202002** | XY3-100 Laser Scanner Protocol Format Specification | v1.0（2020-09） | LasIA |
| **LIA202307** | XY3-100 Laser Scanner Protocol Format Specification | **v1.1**（2023-07） | LasIA |
| — | **SL2-100 Protocol Short Information** | RTC6 手册 Doc Rev 1.1.4 附录 F | SCANLAB |

**关键证实（本报告已用 MD5 校验）**：网上广为流传的那份「XY2-100 Laser Scanner Protocol Format Specification」（托管于 aaronvose.net / Quantronix、并被多个 GitHub 仓库转存）**就是 LasIA LIA202001 本身**——两份文件 **MD5 完全一致**（`604A8F106749B320657ED90134266909`）。

> **获取方式提示**：`lasia.org` 现返回 401、SourceForge 403，但可通过 **Wayback Machine 的 `id_` 直链**取得原始 PDF：
> - LIA202001（XY2-100）：`https://web.archive.org/web/20231206141529id_/https://lasia.org/LIA202001/xy2_100_specification.pdf`
> - LIA202307（XY3-100 v1.1）：`https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf`
> - LIA202002（XY3-100 v1.0）：`https://web.archive.org/web/20210122224854id_/https://lasia.org/LIA202002/xy3_100_specification.pdf`
> - XY3-100 官方 C 头文件：`https://web.archive.org/web/20231206133135id_/https://lasia.org/LIA202307/xy3_100.h`

**⚠️ 关于"发明方"的重要澄清**：任务背景称"originally from SCANLAB / Raylase"。经核查，**XY2-100 的原始发明方在公开资料中存在多种说法，未找到决定性证据**。可以确定的是：
- **标准文本**由 **LasIA** 发布（LIA202001），LasIA 是一个行业协会而非公司；
- **SCANLAB** 与 **RAYLASE** 是最大的两个实现方与文档提供方，两家文档互为补充；
- 不要断言"XY2-100 是 SCANLAB 发明的"——**该说法未获一手证据支持**。

> **XY3-100 的定位（官方原文）**：*"The XY3-100 protocol is intended to be used as **successor of the XY2-100 standard**."* 且官方明确 **"XY3-100, the XY3-100-logo, XY4-100, XY5-100 and others are copyright / trademark / legal trademark of LasIA."** —— 说明 LasIA 规划了完整的 XY*n*-100 系列。
>
> 来源：[LasIA LIA202001](https://web.archive.org/web/20231206141529id_/https://lasia.org/LIA202001/xy2_100_specification.pdf)、[LasIA LIA202307 v1.1](https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf)、[LasIA LIA202002 v1.0](https://web.archive.org/web/20210122224854id_/https://lasia.org/LIA202002/xy3_100_specification.pdf)

### 1.2 官方 XY2-100 vs XY3-100 对照表（LasIA 原文）

| 项目 | **XY2-100** | **XY3-100** |
|---|---|---|
| 分辨率（位宽） | **16 bit**（18 bit via XY2-100E） | **Variable from 16 to 26 bit** |
| 分辨率（帧率） | **100 kHz** | Variable，100 kHz typically |
| 传输速率 | **100 ks/sec** | Variable，100 ks/sec typically |
| 回传通道 | **20 data bits synchronous to XY2-100 clock** | **Flexible, asynchronous RS485 serial communication protocol** |
| 硬件 | DB25 connector | DB25 connector |
| 硬件兼容性 | — | **Same pinout as XY2-100(E), no hardware changes needed** |
| 纠错 | Parity bit | Parity counter on position/command data, binary protocol on backchannel |

来源：[LasIA LIA202307 v1.1 §3 Overview](https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf)

> ⚠️ **注意上表最后一行"Same pinout as XY2-100(E)"——这句话只在数据线上成立，CLK/SYNC 实际上是互换的。详见 [2.3 节](#23-引脚定义四种厂商--官方标准对照) 的专门警告。**

> **重要认知**：XY2-100 并**没有**一个"双轴合一"的复合帧。X 与 Y 各走**独立的数据线**，各自串行发送自己的位置字，共享同一组 CLOCK 与 SYNC。
> 来源：[CSDN 差分信号与时序设计](https://blog.csdn.net/weixin_29171129/article/details/164417972)

---

## 2. 物理层

### 2.1 信号线构成

最常见的配置是：**共用 1 组 CLOCK + 1 组 SYNC，X 与 Y 各 1 组数据线**，另外每轴可带 1 组状态/反馈线。有时还存在 Z 轴。

| 信号 | 方向 | 数量 | 说明 |
|---|---|---|---|
| CLOCK（CLK / SENDCK） | 控制卡 → 振镜 | 差分 1 对 | 连续运行的时钟 |
| SYNC | 控制卡 → 振镜 | 差分 1 对 | 帧同步 / 锁存信号 |
| CHAN1（X 轴数据） | 控制卡 → 振镜 | 差分 1 对 | X 位置与命令 |
| CHAN2（Y 轴数据） | 控制卡 → 振镜 | 差分 1 对 | Y 位置与命令 |
| CHAN3 / Z | 控制卡 → 振镜 | 差分 1 对（可选） | Z 聚焦轴（3D） |
| STATUS / STAT | 振镜 → 控制卡 | 差分 1 对/轴（可选） | 状态或完整反馈字 |

**电气特性**（RAYLASE 官方）：*"All signals are transmitted electrically and differentially without galvanic isolation."*（所有信号以差分方式传输，**无电气隔离**）；正负两线以**双绞线对**引出。
来源：[RAYLASE SS-III XY2-100-E 接口文档](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)

**差分电气标准：RS-422（TIA/EIA-422），不是 LVDS。** 这一点由厂商推荐的器件型号确证——所有推荐接收器都是 RS-422 输入阈值的器件，而非 LVDS 的约 350 mV 差分阈值器件：

| 用途 | 推荐型号 | 标准 |
|---|---|---|
| 线驱动器（Line driver） | **UA9638CD** | RS-422 |
| 线接收器（Line receiver） | **MAX3096** 或 **UA9637**，也可用 **AM26LV32** | RS-422 |
| 线驱动器（开源方案采用） | **AM26LS31**（5 V 供电，输入兼容 3.3 V TTL，输出 TIA/EIA-422 兼容） | RS-422 |

来源：[RAYLASE SS-III XY2-100-E 接口文档 §2.2](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)、[hyperchao0/qspi4xy2-100 README](https://github.com/hyperchao0/qspi4xy2-100)

> ⚠️ **不建议用 LVDS 器件替代 RS-422 器件**——差分摆幅（LVDS ≈ 350 mV vs RS-422 ≈ 2 V）与共模范围不同。**本次检索未找到任何厂商推荐 LVDS 器件（SN65LVDS / DS90LV 系列）用于 XY2-100 的权威出处**（尽管网上常有人把该接口称作 LVDS）。

**实践做法**（Teensy 库作者）：Teensy 以 **3.3 V 信号"差分"输出，短线可直接连振镜**；可靠场合强烈建议使用**带电气隔离的 RS-485 驱动器**。
来源：[Tuet/XY2_100 README](https://github.com/Tuet/XY2_100)

> **关键硬件要点 1 — 必须互补输出（伪差分）**：MCU 直连时必须用**两根 GPIO 互补输出**构成伪差分（`+` 输出该位、`−` 输出其反），**不是单端单线**。Tuet 库的 `DifferentialWirePair::set()` 正是此思路。
>
> **关键硬件要点 2 — 驱动器输出需加上/下拉**：
> > *"To avoid the high impedance state of the differential line driver, the output of the line driver should be connected pull-up or pull-down resistors."*
> > （为避免差分驱动器处于高阻态，其输出应接上拉或下拉电阻。）
> > 来源：[hyperchao0/qspi4xy2-100 README](https://github.com/hyperchao0/qspi4xy2-100)
>
> **关键硬件要点 3 — 负端需直流偏置（单点来源，存疑）**：某 ESP32 实现的中文注释写道 `//pin1-4 需要相对GND有1.2v`，即 DB25 的 **pin 1–4（各差分对的负端）需相对 GND 有约 1.2 V 直流偏置**，单端驱动才能被差分接收器正确识别。
> ⚠️ **该"1.2 V"具体数值未获任何厂商文档确认，标记为单点二手来源（存疑）**；但"负端需要直流参考"这一机理与 RS-422 接收器工作原理一致，可作为调试方向。
> 来源：[txpzyr/xy2_100](https://github.com/txpzyr/xy2_100)

### 2.2 连接器类型

- 常规使用 **DB25（25-pin D-SUB）插头**，控制卡与振镜两侧**一一对应直连（1:1）**。
- 也有 **IDC 连接器**形式。
- **SCANLAB RTC5 / RTC6** 的 SL2-100 接口改用 **9-pin D-SUB**（数据）+ 3-pin 电源；**RTC4** 为 **25-pin D-SUB**。
- SCANLAB intelliSCAN 的 XY2-100-Enhanced 有**共用 25-pin D-SUB**与**数据/电源分离**两种接法。

来源：[cnblogs XYMOTION](https://www.cnblogs.com/xymotion/p/12987507.html)、[SCANLAB RTC PDF](https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf)、[SCANLAB intelliSCAN 引脚定义](https://www.scanlab.de/sites/default/files/2021-11/pinout_intelliSCAN.pdf)

### 2.3 引脚定义（四种厂商 + 官方标准对照）

⚠️ **各厂商引脚定义并不完全一致，尤其是电源脚与 Z 轴脚，替换设备时必须逐一核对。**

#### 🚨 (0) 最高优先级陷阱：XY2-100 与 XY3-100 在同一条 DB25 上 **CLK 与 SYNC 是互换的**

这是本报告发现的**最危险的兼容性陷阱**，做双协议兼容板或替换扫描头时会直接导致通信完全失效：

| 协议 | **Pin 1 / 14** | **Pin 2 / 15** | 来源 |
|---|---|---|---|
| **XY2-100** | **CLK − / CLK +** | **SYNC − / SYNC +** | RAYLASE SS-III §2.1.1、SCANLAB RTC4 §6.3、Newson rhothor X7、Ray-Motion —— **四家一手一致** |
| **XY3-100** | **SYNC − / SYNC +（A）** | **CLK − / CLK +（B）** | **LasIA LIA202307 v1.1 §4.1 DB25 Connector（官方标准原文）** |

**XY3-100 官方规范 §4.1 的 DB25 引脚表（原文照录）**：

| 引脚 | 信号（官方命名） | 引脚 | 信号（官方命名） |
|---|---|---|---|
| **1** | **SYNC − (A−)** | **14** | **SYNC + (A+)** |
| **2** | **CLK − (B−)** | **15** | **CLK + (B+)** |
| 3 | X − (C−) | 16 | X + (C+) |
| 4 | Y − (D−) | 17 | Y + (D+) |
| 5 | Z − (E−) 可选 | 18 | Z + (E+) 可选 |
| 6 | **BACK − (F−)** 可选回传 | 19 | **BACK + (F+)** 可选回传 |
| 7 | U − (G−) 可选 | 20 | U + (G+) 可选 |
| 8 | W − (H−) 可选 | 21 | W + (H+) 可选 |
| 9 | V+ | 22 | V+ |
| 10 | V+ | 23 | GND |
| 11 | GND | 24 | GND |
| 12 | V− | 25 | V− |
| 13 | V− | — | — |

> 官方说明：*"the control lines **SYNC and CLK (named as A and B** in end user documents)"* —— 即 **A = SYNC、B = CLK**。

**因此**：XY3-100 规范中那句 **"Same pinout as XY2-100(E), no hardware changes needed"** **只在数据线（X/Y/Z/U/W）上成立**，**CLK 与 SYNC 是交换的**。

**同卡双模式交叉验证（一手）**：HALaser E1803D 在 XY2-100 模式下 26-pin 为 `1/2 = CLK、3/4 = SYNC`；切到 XY3-100 模式后变为 `1/2 = A = SYNC、3/4 = B = CLK` —— **同一块卡在两种模式下的引脚功能确实互换**。
来源：[HALaser E1803D Manual](https://halaser.eu/manuals/e1803_manual.pdf)

> **工程结论**：**做兼容 XY2-100 与 XY3-100 双协议的控制器时，CLK 与 SYNC 必须设计为可交换（跳线、模拟开关或软件可配置的差分对映射）。** 直接沿用单一引脚定义必然失败。

**其他 XY3-100 物理层要点（官方）**：
- 可用 **DB25**（全功能，最多 5 轴 + BACK）或 **DB15**（v1.1 起可选，最多 3 轴，不支持 U/W）；也可用 **26-pin IDC**（推荐白色）或 **16-pin IDC**
- 线序命名体系：**A = SYNC、B = CLK、C = X、D = Y、E = Z、F = BACK、G = U、H = W**（8 对差分线）
- **数据线须符合 ANSI/TIA/EIA-485-A 与 ISO 8482:1987，且"require a proper termination on receiver side"（接收端必须加终端电阻）**
  > 注：**XY2-100 官方文档对终端电阻无任何规定**（见 11.2 节），XY3-100 则明确要求 —— 这是两协议在电气上的又一差异。
- 最少需支持 **SYNC、CLK、X、Y** 四对线（2D 位置数据）

来源：[LasIA LIA202307 v1.1 §4 Hardware interface](https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf)

#### (a) SCANLAB RTC4 控制卡「Primary Scan Head」接口（官方 25-pin，最经典）

RTC4 手册原文：*"The 25-pin D-SUB connector for the scan head is **compatible with most scan heads which use the XY2-100 standard**."*

| 引脚 | 信号 | 引脚 | 信号 |
|---|---|---|---|
| 1 | CLOCK − | 14 | CLOCK + |
| 2 | SYNC − | 15 | SYNC + |
| 3 | CHAN1 − | 16 | CHAN1 + |
| 4 | CHAN2 − | 17 | CHAN2 + |
| **5** | **CHAN3 −（可选，第 3 轴）** | **18** | **CHAN3 +（可选）** |
| **6** | **STATUS −** | **19** | **STATUS +** |
| 7 | 不连接 | 20 | 不连接 |
| **8** | **STATUS1 − \*** | **21** | **STATUS1 + \*** |
| 9 | 不连接 | 22 | 不连接 |
| 10 | 不连接 | **23** | **GND** |
| **11** | **GND** | **24** | **GND** |
| 12 | 不连接 | 25 | 不连接 |
| 13 | 不连接 | — | — |

\* **STATUS1± 通道仅可与 intelliSCAN®、intellicube®、intelliWELD®、intelliDRILL 扫描系统配合使用，否则为 "DO NOT CONNECT"。**

**通道功能（原文）**：
> *"Data channels CHAN1 through CHAN3 transmit control values to the scan head. The SYNC and CLOCK channels transmit synchronization and clock signals to the scan system. The CHAN3 channel is optionally provided for controlling a **third axis in a 3-axis system**."*
> *"The STATUS channel receives **XY2-100 standard compliant status signals** returned by the scan system. Consult your scan system's operating manual to determine which status signals are generated by your scan system and how they can be applied for monitoring purposes."*

> ✅ **交叉验证**：RTC4 官方引脚把 **CHAN3（第 3 轴）放在 pin 5/18**，与 **RAYLASE SS-III 的 Z 轴 pin 5/18 完全一致** —— 两家厂商在 3 轴扩展上使用相同引脚，**互为独立印证**。
>
> ✅ 另注：**RTC4 的 GND 为 pin 11/23/24**，与 SCANLAB XY2-100 Converter 的"引脚 11、23、24 相互连通"说明吻合。

来源：[SCANLAB RTC4 PC Interface Board Manual Rev 1.4e, §6.3 Primary Scan Head Connector](https://www.scanlab.de/en/downloads)（本地缓存 `RTC4_1_4_english.pdf`）

#### (a2) SCANLAB intelliSCAN XY2-100-Enhanced（25-pin 母 D-SUB）

| 引脚 | 信号 | 引脚 | 信号 |
|---|---|---|---|
| 1 | CLOCK − | 14 | CLOCK + |
| 2 | SYNC − | 15 | SYNC + |
| 3 | CHAN1 − | 16 | CHAN1 + |
| 4 | CHAN2 − | 17 | CHAN2 + |
| 5 | 不连接 | 18 | 不连接 |
| 6 | STATUS2 − | 19 | STATUS2 + |
| 7 | 不连接 | 20 | 不连接 |
| 8 | STATUS1 − | 21 | STATUS1 + |
| 9 | +30 V | 10 | +30 V |
| 22 | +30 V | 11 | 不连接 |
| 12 | GND | 13 | GND |
| 23 | 不连接 | 24 | 不连接 |
| 25 | GND | — | — |

来源：[SCANLAB intelliSCAN Standard Connector Positions and Pin-Outs](https://www.scanlab.de/sites/default/files/2021-11/pinout_intelliSCAN.pdf)（© SCANLAB GmbH 2021）

#### (b) RAYLASE SS-III XY2-100-E（25-pin DSUB 母，两侧 1:1）

| 引脚 | 信号 | 方向（振镜侧） | 说明 |
|---|---|---|---|
| 1 / 14 | CLK − / CLK + | 输入 | 时钟 |
| 2 / 15 | SYNC − / SYNC + | 输入 | 同步 |
| 3 / 16 | X − / X + | 输入 | 位置与命令（**小镜**） |
| 4 / 17 | Y − / Y + | 输入 | 位置与命令（**大镜**） |
| 5 / 18 | Z − / Z + | 输入 | 位置与命令（**聚焦轴**） |
| 6 / 19 | Y_stat − / Y_stat + | **输出** | 反馈通道 |
| 7 / 20 | Z_stat − / Z_stat + | **输出** | 反馈通道 |
| 8 / 21 | X_stat − / X_stat + | **输出** | 反馈通道 |
| 9 / 22 / 10 | 可选 +15 V（标准 SS-III 不用） | — | **不连接** |
| 11 / 23 / 24 | GND | — | 地 |
| 12 / 25 / 13 | 可选 −15 V（标准 SS-III 不用） | — | **不连接** |
| 屏蔽层 | GND | — | 接控制卡地 |

来源：[RAYLASE SS-III XY2-100-E 接口文档](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)

⚠️ RAYLASE 特别提示：**RAYLASE 的 X 轴是激光首先打到的轴（小镜）**，部分其他厂商把先被打到的轴定义为 Y 轴，因此**不同厂商的 X/Y 通道引脚是互换的**。

#### (c) Ray-Motion / 鞍山精准光学（DB25）

| 引脚 | 名称 | 说明 | 方向 |
|---|---|---|---|
| 1 / 14 | CLOCK − / CLOCK + | 连续运行时钟 | 输入 |
| 2 / 15 | SYNC − / SYNC + | 同步数据传输 | 输入 |
| 3 / 16 | CHAN1 − / CHAN1 + | X 轴数据 | 输入 |
| 4 / 17 | CHAN2 − / CHAN2 + | Y 轴数据 | 输入 |
| 5/18、6/19、7/20、8/21 | — | 未用 | — |
| 9 / 10 / 22 | POWER + | **+15 V** | 输入 |
| 11 / 23 / 24 | GND | 地 | 输入 |
| 12 / 13 / 25 | POWER − | **−15 V** | 输入 |

来源：[Ray-Motion XY2-100 technical datasheet](https://dvd.ilphotonics.com/Ray-Motion%20-%20galvanometers%20-%201D-2D-3D%20scanners/Motion%20Control%20-%20Optomechanics/Interface%20XY2-100.pdf)

#### (d) Newson rhothor X7（DB25）

| 引脚 | 名称 | 说明 | 方向 |
|---|---|---|---|
| 1 / 14 | IO1− / IO1+ | SENDCK：连续运行时钟 | 输入 |
| 2 / 15 | IO2− / IO2+ | SYNC：同步数据传输 | 输入 |
| 3 / 16 | IO3− / IO3+ | CHANNELX：X 轴数据 | 输入 |
| 4 / 17 | IO4− / IO4+ | CHANNELY：Y 轴数据 | 输入 |
| 5 / 18 | IO5− / IO5+ | 未用 | — |
| **6 / 19** | **IO6− / IO6+** | **STATUS：振镜头状态** | **输出** |
| 7 / 20 | IO7− / IO7+ | 未用 | — |
| 13 | REF_IO | 参考 I/O，接控制卡 GND | — |

来源：[Newson rhothor X7 XY2-100 Technical Datasheet](https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/171/Documents_5F00_TD_5F00_XY2_2D00_100_5F00_R0703.pdf)

### 2.4 电缆要求

| 项目 | 要求 | 来源 |
|---|---|---|
| 接线方式 | 1:1 直连（pin-to-pin） | RAYLASE SS-III |
| 差分走线 | 每路差分信号的正负线必须走**双绞线对** | RAYLASE SS-III |
| 屏蔽 | 屏蔽层接 GND | RAYLASE SS-III |
| 电气隔离 | RAYLASE SS-III：**无隔离**；SCANLAB RTC4：**无隔离**；SCANLAB RTC5/RTC6（SL2-100）：**有隔离** | RAYLASE / SCANLAB |
| 短线直连 | 3.3 V 差分信号短线可直接连振镜；可靠场合建议加隔离 RS-485 驱动 | Tuet/XY2_100 |
| 具体线长/阻抗/线规 | **未找到公开数据** | — |

---

## 3. 时序规范

### 3.1 时钟频率 —— 存在多个官方数值

| 参数 | 数值 | 来源 |
|---|---|---|
| **标称时钟频率** | **2 MHz**（周期 500 ns） | [Ray-Motion DS](https://dvd.ilphotonics.com/Ray-Motion%20-%20galvanometers%20-%201D-2D-3D%20scanners/Motion%20Control%20-%20Optomechanics/Interface%20XY2-100.pdf) / [Newson DS](https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/171/Documents_5F00_TD_5F00_XY2_2D00_100_5F00_R0703.pdf) |
| **数据传输速率** | **2 Mbit/s**，即 **100 kwords/s** | 同上 |
| XY2-100 基型时钟上限 | **≤ 2 MHz** | [sigrok](https://sigrok.org/wiki/Protocol_decoder:Xy2-100) |
| **XY2-200** | **≤ 4 MHz**（其余与 XY2-100 相同） | [sigrok](https://sigrok.org/wiki/Protocol_decoder:Xy2-100) |
| **RAYLASE SS-III XY2-100-E 最大时钟** | **10 MHz**，**推荐 4 MHz** | [RAYLASE SS-III](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf) |
| 实测可用 | Teensy 4.1 用 SAI 外设产生 **10 Mbit/s** 输出 | [PJRC 论坛](https://forum.pjrc.com/index.php?threads/implementing-xy2-100-serial-protocol-on-teensy-4-1.62819/) |

> **来源冲突提示**：经典 XY2-100 规格为 2 MHz，但 **RAYLASE 的 XY2-100-E 明确支持到 10 MHz、推荐 4 MHz**。二者不矛盾——Enhanced 变体提高了时钟上限。选用时应以**所配振镜手册**为准，不要假设所有 XY2-100 设备都能跑 4 MHz 以上。

### 3.2 时序表

| 项目 | 符号 | Min | Typ | Max | 单位 | 来源 |
|---|---|---|---|---|---|---|
| 时钟频率 | f_CLK | — | **2** | 10（Enhanced） | MHz | Ray-Motion / RAYLASE |
| 时钟周期 | T_CLK | — | **500** | — | ns | 由 2 MHz 推算 |
| 时钟占空比 | — | — | **50 %** | — | — | 实践值，[PJRC 论坛](https://forum.pjrc.com/index.php?threads/implementing-xy2-100-serial-protocol-on-teensy-4-1.62819/)；官方文档**未给出**占空比规格（未找到公开数据） |
| 每帧时钟数 | — | — | **20** | — | clk | Ray-Motion / Newson |
| 帧周期 | T_frame | — | **10** | — | µs | Ray-Motion / Newson / RAYLASE |
| 帧率（更新率） | — | 理论无下限 | **100** | 500（10 MHz 时） | kHz | 由 20 bit 推算 |
| SYNC 高电平宽度 | — | — | **19** 个时钟（9.5 µs @2 MHz） | — | — | Ray-Motion / Newson / RAYLASE |
| 数据建立时间 | **tDS** | **50** | — | — | ns | Ray-Motion / Newson |
| 数据保持时间 | **tDH** | **100** | — | — | ns | Ray-Motion / Newson |
| 反馈通道相对前向延迟 | — | — | **半个时钟周期** | — | — | [RAYLASE SS-III](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf) |

### 3.3 边沿约定（关键）

| 事件 | 约定 |
|---|---|
| CLK **上升沿** | 数据在 X/Y/Z 线上**变化**（控制卡输出新位） |
| CLK **下降沿** | 振镜**采样**数据位 |
| CLK 下降沿（反馈） | 振镜在 X_stat/Y_stat/Z_stat 上**变化**反馈数据 → 反馈相对前向**延迟约半周期** |
| SYNC **上升沿** | 标记一帧的**开始**（第 1 个可发送位） |
| SYNC **保持高** | 持续 **19** 个时钟 |
| SYNC **下降沿** | 标记**最后一位（校验位）**的开始，同时作为**锁存信号** |

来源：[Quantronix/aaronvose XY2-100 规范 PDF](https://www.aaronvose.net/Quantronix_Osprey/xy2_100_specification.pdf)、[Ray-Motion DS](https://dvd.ilphotonics.com/Ray-Motion%20-%20galvanometers%20-%201D-2D-3D%20scanners/Motion%20Control%20-%20Optomechanics/Interface%20XY2-100.pdf)、[RAYLASE SS-III](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)

原文摘录（Ray-Motion / Newson）：
> *"The SYNC bit goes high when the first bit can be sent. It remains high for 19 bits and goes low when the parity can be sent."*
> *"The clock signal runs at a frequency of 2 MHz. When it goes high, the data bit changes. When it goes low, the data bit is sampled by the deflection system."*

PJRC 论坛上 Paul Stoffregen 用示波器实测用户代码后也独立验证了 SYNC 极性：
> *"Comparing these waveforms to the SS-III XY2-100-E documentation, I see the sync signal polarity is high for 19 of the 20 clocks."*
> 来源：[PJRC 论坛](https://forum.pjrc.com/index.php?threads/implementing-xy2-100-serial-protocol-on-teensy-4-1.62819/)

### 3.4 延迟（Latency）—— 实测/官方量化数据

**协议本身**的反馈延迟为**半个时钟周期**（见 3.2 节）。但**系统级延迟**远大于此——它主要由振镜内部的插值算法与计算时间决定。

RAYLASE SP-ICE 3 官方手册给出了**可直接用于工程计算的量化公式**（适用于 Scanner Firmware Dicon2.5 / FW v6973+ / FPGA v6921+ / SP-ICE 3 Firmware v2.0.2+）：

| 延迟项 | 定义 | 数值 |
|---|---|---|
| **Transfer Delay (TX)** | **从控制卡发出位置命令，到该命令被振镜控制器算法识别**之间的时间。**取决于振镜内设定的插值时间** | 见下方公式 |
| **Transfer Delay (RX)** | 从振镜控制器发出测量位置，到控制卡收到该位置之间的时间 | **36 µs**（恒定，与插值时间无关） |
| 激光控制信号 | 控制卡 → 激光器 | **几乎无延迟** |

**Transfer Delay (TX) 计算公式**（精度 ±2 µs）：

| 条件 | 公式 |
|---|---|
| T_Int > 0 | **TD_TX = T_K + T_C + T_Int** |
| T_Int = 0 | **TD_TX = 14 µs** |

| 因子 | 数值 | 说明 |
|---|---|---|
| **T_K** | **13 µs** | 插值时间 > 0 时的恒定延迟因子 |
| **T_C** | **20 µs** | 插值例程的**计算时间**（固定值） |
| **T_Int** | 设定值 | 插值时间设置 |

**工程建议（原文）**：
- **插值时间设为小于 20 µs 一般没有意义**（受振镜控制器插值算法限制）；SP-ICE 3 通常建议设为**步进周期的 2 倍的较小非零倍数，例如 20 µs**。
- **Positioning Delay（定位延迟）= Transfer Delay + Tracking Error（即 Lag）**；应据此设置 `LaserOnDelay` 与 `LaserOffDelay`。
- Transfer Delay **与振镜的 Tuning 无关**，但所选 Tuning 会影响振镜的 **Tracking Error** 值。

**可通过 Enhanced Protocol 命令在线读取**：

| 延迟值 | Enhanced Protocol 原始命令 |
|---|---|
| Transfer Delay (TX) | **0x0556** |
| Transfer Delay (TX) + Transfer Delay (RX) | **0x0557** |

来源：[RAYLASE SP-ICE 3 User's Manual §7.1.9 Transfer Delay with Digital Scanners](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/7a6d305c-a5d1-4dfb-a1d2-3afc1768b87f.htm)

> **与 XY2-100 的关系**：上述公式出自 RAYLASE 的**数字振镜**（Enhanced 协议）体系，其 `SetInterpolation (0x90)` 默认值 120 µs 正是同一机制（见 9.5）。因此 XY2-100-E 系统的典型总延迟量级为 **数十微秒**（13 + 20 + T_Int，再加 36 µs 反馈），**远大于 10 µs 的帧周期**——这正是必须做延时补偿的根本原因。

### 3.5 连续帧与空闲行为

- **连续帧（coherent frames）**是允许且正常的：一帧的校验位紧接下一帧的第 1 位，SYNC 只在该位拉低一个时钟周期。RAYLASE 文档 Diagram 2 明确给出该时序。
  来源：[RAYLASE SS-III](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)
- **CLOCK 必须连续运行**，即使没有新位置数据也要持续输出时钟与 SYNC。厂商文档把这一点写死在引脚定义里：
  > Pin 1/14 — **CLOCK-/CLOCK+ — CLOCK : Continuously running clock** — Input
  > （Ray-Motion；Newson 同样写作 "Continuously running clock"，信号名 `SENDCK`）
- **时钟/同步出错时的可观测行为**（RAYLASE SS-III 面板 LED 原文）：
  > **PX / PY** — *"Illuminates red if a parity error occurs on the X-/Y-channel of the XY2-100 Interface. **Illuminates permanently if clock or sync signal of the XY2-100 interface has an error.** The illumination period has been extended to make short failures visible too."*
  > **EX / EY** — *"Illuminates red in case of an error on the X-/Y-axis and during the booting of the axis... **If this LED illuminates the output stage of the X-/Y-axis is deactivated.**"*

⚠️ **重要的安全结论**：振镜**能检测** clock/sync 异常并点亮常亮故障指示；且**轴故障时输出级被关闭（output stage deactivated）**——**即振镜不是"保持最后位置"，而是关闭功率输出**，镜片失去保持力矩。**这点对安全设计至关重要。**

> **"时钟停止后保持最后位置"这一常见说法：未找到任何厂商文档明确承诺。** 能找到的最接近表述是"输出级被关闭"。**标记为：未找到公开数据 / 不推荐依赖。**

来源：[RAYLASE SS-III XY2-100-E 接口文档 §5 Status-LEDs](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)、[Ray-Motion DS](https://dvd.ilphotonics.com/Ray-Motion%20-%20galvanometers%20-%201D-2D-3D%20scanners/Motion%20Control%20-%20Optomechanics/Interface%20XY2-100.pdf)

**反面证据：协议对时钟频率并不敏感。** 帧边界由 SYNC 上升沿界定，与时钟速度无关；georgemihaila 作者自述 Arduino Nano 慢速位操作"seems to be able to drive a galvo just fine"；RAYLASE 允许 10 MHz 上限。

> **结论：时钟可以慢，但不能停。** 空闲期也必须继续输出时钟与 SYNC 帧（通常做法是**重复发送当前位置**）——这正是 georgemihaila 库中 `tickingDelay()` 的作用。

### 3.6 时序余量分析

规范只给出数据侧的建立/保持时间（tDS ≥ 50 ns、tDH ≥ 100 ns，共需 **150 ns** 稳定窗口），**未规定时钟占空比、抖动（jitter）、上升/下降时间** → **未找到公开数据**。

由 tDS/tDH 反推电气余量：
- 2 MHz 下周期 T = 500 ns。若占空比 = 50%（高 250 ns / 低 250 ns），则**250 ns 的余量对 50/100 ns 的要求有 2.5–5 倍裕量** ⇒ 规范对占空比并不苛刻。
- **但严重抖动会直接吃掉这个裕量**——软件位操作被中断打断时尤其危险。

**实测建议**（用示波器同时观察 CLK 与 DATA）：
1. 每个数据位的稳定窗口是否 ≥ 150 ns；
2. 帧周期是否稳定在 ~10 µs（抖动 > 数百 ns 说明软件路径被抢占）；
3. 是否存在时钟毛刺（软件位操作或 DMA 冲突时常见）。

---

## 4. 帧结构

### 4.1 标准 16 bit 位置帧（XY2-100 基型）

每轴 20 bit。第 1 位对应位号 BIT19，最后一位为 BIT0。**MSB first**。

| 位号 | 19 | 18 | 17 | 16 | 15 | 14 | 13 | 12 | 11 | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 内容 | C2 | C1 | C0 | D15 | D14 | D13 | D12 | D11 | D10 | D9 | D8 | D7 | D6 | D5 | D4 | D3 | D2 | D1 | D0 | P |
| 值 | **0** | **0** | **1** | ← | ← | ← | ← | 16 位位置数据 | ← | ← | ← | ← | ← | ← | ← | → | → | → | → | 偶校验 |

即：**3 位控制字 `001` + 16 位位置数据（D15…D0，偏移二进制）+ 1 位偶校验 = 20 bit**。

来源：[Quantronix/aaronvose XY2-100 规范 PDF](https://www.aaronvose.net/Quantronix_Osprey/xy2_100_specification.pdf)、[Ray-Motion DS](https://dvd.ilphotonics.com/Ray-Motion%20-%20galvanometers%20-%201D-2D-3D%20scanners/Motion%20Control%20-%20Optomechanics/Interface%20XY2-100.pdf)、[Newson rhothor X7 DS](https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/171/Documents_5F00_TD_5F00_XY2_2D00_100_5F00_R0703.pdf)

**控制字（C2 C1 C0）定义**：

| C2 | C1 | C0 | 含义 | 来源 |
|---|---|---|---|---|
| 0 | 0 | 1 | **电机设定值（motor setpoint value）** ← 正常位置指令 | Newson 官方表格 |
| 1 | 1 | 1 | **命令帧（command frame，仅 XY2-100-E）** | sigrok 解码器源码 |
| 1 | — | — | **18 bit 增强模式**（第 1 位固定为 1） | Quantronix 规范 |
| 其余组合 | | | **未找到公开数据** | — |

来源：[Newson rhothor X7 DS](https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/171/Documents_5F00_TD_5F00_XY2_2D00_100_5F00_R0703.pdf)、[sigrok libsigrokdecode `decoders/xy-100/pd.py`](https://raw.githubusercontent.com/sigrokproject/libsigrokdecode/master/decoders/xy-100/pd.py)

**sigrok 官方解码器的帧类型判定逻辑**（目前能找到的最明确的一手判定依据）：

```python
# sigrok libsigrokdecode decoders/xy-100/pd.py
### 16-bit position
elif (type_3_value == 1):                        # 前三位 = 0b001 = 1
    type = frame_type_16bit_pos
### Command
elif (type_3_value == 7) and (parity_even == 1): # 前三位 = 0b111 = 7
    type = frame_type_command
### 18-bit position
if (type_1_value == 1) and (parity_odd == 1):    # 第 1 位 = 1 且为奇校验
    type = frame_type_18bit_pos
```
来源：[sigrok libsigrokdecode `decoders/xy-100/pd.py`](https://raw.githubusercontent.com/sigrokproject/libsigrokdecode/master/decoders/xy-100/pd.py)

> **修正**：本项目早期整理曾称"除 `001` 外的控制字未找到公开数据"。经查 sigrok 官方解码器源码，**命令帧控制字为 `111`**，且命令帧使用**偶校验**。

### 4.2 Enhanced 18 bit 位置帧（XY2-100 Enhanced / XY2-100-E）

| 位号 | 19 | 18 | 17 | 16 | 15 | 14 | 13 | 12 | 11 | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 内容 | **1** | D17 | D16 | D15 | D14 | D13 | D12 | D11 | D10 | D9 | D8 | D7 | D6 | D5 | D4 | D3 | D2 | D1 | D0 | Po |
| 说明 | 固定 | ← | ← | ← | ← | ← | 18 位位置数据 | ← | ← | ← | ← | ← | ← | ← | → | → | → | → | → | **奇校验** |

即：**第 1 位固定为 `1` + 18 位位置数据（D17…D0）+ 1 位奇校验 = 20 bit**。

来源：[Quantronix/aaronvose XY2-100 规范 PDF](https://www.aaronvose.net/Quantronix_Osprey/xy2_100_specification.pdf)、[cnblogs XYMOTION](https://www.cnblogs.com/xymotion/p/12987507.html)

⚠️ **18 bit 模式的固有缺陷**（sigrok 明确指出）：18 bit 模式**部分依靠"校验位取反（奇校验）"来标识**，而 Enhanced 的命令帧仍使用默认的**偶校验**。因此**无法区分"被破坏的命令帧"与"合法的 18 bit 位置帧"**（反之亦然）。sigrok 的解码器会因此发出告警。
来源：[sigrok](https://sigrok.org/wiki/Protocol_decoder:Xy2-100)

### 4.3 Enhanced 命令帧

RAYLASE 文档定义了三种前向帧类型，可任意顺序混合：

| # | 帧类型 | 结构 |
|---|---|---|
| 1 | 16 bit 目标位置帧 | 取自标准 XY2-100：`C2 C1 C0` + `D15…D0` + `Pe` |
| 2 | 16 bit 目标位置帧（RAYLASE SuperScan / SS-II 兼容） | 同上，兼容旧型号 |
| 3 | **命令帧** | `C2 C1 C0` + **8 bit 命令码（C7…C0）+ 8 bit 参数（P7…P0）** + `Pe` |

命令帧的 16 个"数据位"被复用为 `D15–D8 = 命令码`、`D7–D0 = 命令参数`。

来源：[RAYLASE SS-III XY2-100-E 接口文档](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)

**RAYLASE SS-III 已定义命令集**（部分）：

| 命令码 | 功能 |
|---|---|
| 0x05 | SetMode：选择反馈通道输出的信号 |
| 0x0A | UpdatePermanentMemory：把当前设置写入永久存储 |
| 0x11 | SelectControlDefinition：切换镜头整定参数组（最多 3 组） |
| 0x12 | SetPositionScale：定义机械偏转量（SS-III 不支持） |
| 0x15 | SetPosAcknowledgeLevel：定义跟踪误差窗口 |
| 0x17 | Store/RestoreTransmissionMode：保存/恢复反馈通道设置 |
| 0x21 | SetEchoMode：回显模式，用于检测传输错误 |
| 0x90 | SetInterpolationTime：设置插值模式与插值时间 |

来源：[RAYLASE SS-III XY2-100-E 接口文档](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)

⚠️ 命令帧**占用整整 10 µs**，期间无法发送目标位置；振镜会用**相邻两个采样点做线性插值**来补上缺失的位置信息。
来源：同上

### 4.4 校验位算法 —— 已用接收端实现确证

**结论：校验位 P = XOR(C2, C1, C0, D15…D0)**，即对**全部 19 个前导位**做偶校验，使**整帧 20 位中 "1" 的个数为偶数**。

依据（接收端解码器，最权威）：Saleae 的 XY2-100 分析仪源码逐位检查，控制位 C2/C1 为高时计入 `x_par_ctr`；C0 为高时计入；16 个数据位为高时计入；最后判定：

```cpp
// if we counted an odd number of 1's, P should be 1
// if we counted an even number, it should be 0
// in other words, the ctr LSB and P bit should be the same
x_parity_ok = ((mX->GetBitState() == BIT_HIGH) == (x_par_ctr & 0x01));
```
来源：[danmcb/Saleae-XY2-100](https://github.com/danmcb/Saleae-XY2-100)

**⚠️ 实现分歧（重要）**——开源实现中确实存在不一致：

| 实现 | 校验范围 | 是否包含 C0 | 全帧 20 bit 的奇偶性 |
|---|---|---|---|
| [sigrok libsigrokdecode](https://raw.githubusercontent.com/sigrokproject/libsigrokdecode/master/decoders/xy-100/pd.py)（官方解码器） | `parity = 0; for ss, es, value in self.bits[:-1]: parity ^= value` → 对 bit0..bit18 求 XOR | **包含** | **偶** ✔ |
| [danmcb/Saleae-XY2-100](https://github.com/danmcb/Saleae-XY2-100)（解码器） | 逐位计数含控制位 | **包含** | **偶** ✔ |
| [earlynerd/XY2-100_HLA](https://github.com/earlynerd/XY2-100_HLA)（解码器） | `bits_for_parity_check = data_word >> 1`（即 bit19..bit1） | **包含** | **偶** ✔ |
| [Tuet/XY2_100](https://github.com/Tuet/XY2_100) | `Ch=(X<<1)\|0x20000`，统计 20 位后置 bit0 | **包含** | **偶** ✔ |
| [hyperchao0/qspi4xy2-100](https://github.com/hyperchao0/qspi4xy2-100) | `xp` 初值=1，逐数据位翻转 | **包含**（初值 1 等效 C0） | **偶** ✔ |
| [georgemihaila/xy2-100](https://github.com/georgemihaila/xy2-100) | `even_parity ^= current_bit` 仅 16 数据位 | **不包含** | ⚠️ **奇** |
| [NOBIC-NTU / OPAL](https://github.com/NOBIC-NTU/MiniGalvoControl) | `parity(data)` 仅 16 数据位 | **不包含** | ⚠️ **奇** |

**逐位证明二者不等价**：设 16 个数据位中 "1" 的个数为 k。

- **参考实现**：`P = XOR(001, data) = (1 + k) mod 2`
  → 全帧 20 bit 中 "1" 的总数 = `1 + k + (1+k) mod 2` = **恒为偶数** ✔（这是标准偶校验）
- **georgemihaila / OPAL**：`P = k mod 2`
  → 全帧 "1" 的总数 = `1 + k + (k mod 2)`。对 k = 0,1,2,3,4 分别得 **1, 3, 3, 5, 5** —— **恒为奇数**，事实上变成了**奇校验**，与 16 bit 模式的规范相反。

> **建议**：实现时对**全部 19 位**求偶校验（即 `P = XOR(C2,C1,C0,D15..D0)`）。这是被 **3 个独立解码器 + 2 个发送实现**共同验证过的唯一定义。
>
> 那两个只算 16 位的实现"能工作"的可能原因（**推测，未获证实**）：(a) 目标振镜不严格检查校验位；(b) 振镜只对数据域校验；(c) 使用者恰好接受了该行为。**本次检索未找到任何厂商文档说明振镜如何校验 P，也未找到这两个项目对该差异的讨论。**

---

## 5. 位置编码与量程映射

### 5.1 编码方式

- **偏移二进制（offset binary）**，**无符号整数**解释：`D0` 为最低位，`D15`（或 `D17`）为最高位。
  来源：[Ray-Motion DS](https://dvd.ilphotonics.com/Ray-Motion%20-%20galvanometers%20-%201D-2D-3D%20scanners/Motion%20Control%20-%20Optomechanics/Interface%20XY2-100.pdf)、[RAYLASE SS-III](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)
- **中心 = 0x8000**（16 bit）/ **0x20000**（18 bit）。

**代码级确证**：Verilog 解码器复位值即为中心值，并从 20 位移位寄存器中取出 `[16:1]` 作为位置：

```verilog
// 412910609/galvoMC  XY2_100.v
always @ (posedge sys_clk or negedge rst_n)
    if(!rst_n) out_x_data <= 16'h8000;      // 中心
    else       out_x_data <= out_x_data_n;

// bit_cnt == 20 时取 20 位移位寄存器的 [16:1]
if(bit_cnt == 5'd20) out_x_data_n = shift_x_data[16:1];
```
`shift_x_data[16:1]` 恰好是 D15…D0，**位号 19/18/17 是控制字、位号 0 是校验位**——与 4.1 节表格完全吻合。
来源：[412910609/galvoMC](https://github.com/412910609/galvoMC)（源码 `XY2_100.v`）

其他实现同样处理：

| 实现 | 代码 | 含义 |
|---|---|---|
| Tuet | `setSignedXY`: `xu = X + 32768`，注释 `// -32768 => 0; 32767 => 65535;` | 有符号 ↔ 偏移二进制 |
| earlynerd (RP2040) | `ix = 0x8000 + x; iy = 0x8000 - y;` | 注意 Y 轴**反向** |
| hyperchao0 | `x & (0x8000 >> i)`，MSB 先发 | MSB first 确证 |

来源：[Tuet/XY2_100](https://github.com/Tuet/XY2_100)、[earlynerd/XY2Galvo](https://github.com/earlynerd/XY2Galvo)、[hyperchao0/qspi4xy2-100](https://github.com/hyperchao0/qspi4xy2-100)

### 5.2 码值 → 角度映射

XY2-100 帧中的 16 bit 是**归一化的全量程比例**，不是绝对电压或绝对角度。全量程对应的机械/光学角度由**振镜本身的标定**决定。

换算关系：

```
角度 = (Code − 0x8000) / 32768 × 角度全量程半宽      （16 bit）
角度 = (Code − 0x20000) / 131072 × 角度全量程半宽    （18 bit）
```

以 SCANLAB 公开数据反推（**光学角 ±0.36 rad，全角程 0.72 rad**）：

| 位深 | 步数 | 单步分辨率 | SCANLAB 官方标注值 | 一致性 |
|---|---|---|---|---|
| 16 bit | 65 536 | 0.72 / 65536 = **11.0 µrad** | **11 µrad** | ✔ |
| 18 bit | 262 144 | 0.72 / 262144 = **2.75 µrad** | **2.8 µrad** | ✔ |
| 20 bit | 1 048 576 | 0.72 / 1048576 = **0.687 µrad** | **0.7 µrad** | ✔ |

SCANLAB 原文：
> *"20 bit: based on the full angle range (e.g. positioning resolution 0.7 µrad for angle range ±0.36 rad), resolutions better than 16 bit (11 µrad) only together with SL2-100 interface"* —— excelliSCAN 20
> *"18 bit: based on the full angle range (e.g. positioning resolution 2.8 µrad for angle range ±0.36 rad), resolutions better than 16 bit (11 µrad) only together with SL2-100 interface"* —— intelliSCAN 14

来源：[SCANLAB excelliSCAN 20](https://www.scanlab.de/en/products/scan-systems/excelliscan/excelliscan-20)、[SCANLAB intelliSCAN 14](https://www.scanlab.de/en/products/scan-systems/intelliscan/standard-series/intelliscan-14)

> **关键工程结论**：**16 bit（XY2-100 基型）= 11 µrad 是精度天花板**。想要更高分辨率，必须换用 **18 bit（XY2-100 Enhanced）或 20 bit（SL2-100）**。这就是 Enhanced 与 SL2-100 存在的根本原因。

### 5.3 关于 ±5 V / ±10 V 的说明

XY2-100 是**纯数字**接口，帧内**不传输电压**；"-32768…+32767 → −5 V…+5 V" 是**模拟振镜接口**的表述，而数字振镜内部由 **DAC** 把 16 bit 码值转换为设定电压/电流。
- 数字振镜驱动板内部含 DAC，把码值送给模拟伺服环。**具体 DAC 位宽与内部电压量程属厂商私有，未找到公开数据。**
- 关于模拟接口（±5 V / ±10 V）的详细对比见 [第 7 节](#7-协议族对比)。

---

## 6. 反馈/状态通道

公开资料中存在**两种形态**的反馈通道，务必区分：

### 形态 A：单根 STATUS 电平线（Newson rhothor X7）

一根差分 STATUS 线（pin 6/19），**不与 SENDCK 同步**，表示振镜头整体状态：

> STATUS 为 **'0'** 当且仅当**以下条件全部成立**：
> - X 轴位置 < 最大位置误差，且
> - Y 轴位置 < 最大位置误差，且
> - X 转子有效电流 < 告警电平，且
> - Y 转子有效电流 < 告警电平，且
> - 数字调节器正在运行。
>
> 以上任一条件不成立时 STATUS 为 **'1'**。

来源：[Newson rhothor X7 XY2-100 DS](https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/171/Documents_5F00_TD_5F00_XY2_2D00_100_5F00_R0703.pdf)

### 形态 B：完整 20 bit 串行反馈字（RAYLASE SS-III / 中文厂商）

每轴一条独立的反馈线（X_stat / Y_stat / Z_stat），发送**完整的 20 bit 字**，内容可由命令 `SetMode (0x05)` 动态选择。RAYLASE 文档列出了 **三种互不兼容且无法从数据本身区分的反馈帧格式**：

| 反馈帧类型 | 帧头（高位） | 结构 | 校验位 |
|---|---|---|---|
| 16 bit 向下兼容帧 | `0 0 1 1` | 帧头 4 位 + 16 位数据 = 20 | **无** |
| 16 bit 标准帧 | `0 0 0 1` | 帧头 4 位 + 16 位数据 = 20 | **无** |
| 18 bit 反馈帧 | `0 1` | 帧头 2 位 + 18 位数据 = 20 | **无** |

> ⚠️ **注意：反馈帧没有校验位。** 与向前通道（末位为 P）不同，RAYLASE 文档给出的三种反馈帧结构均为"帧头 + 数据"填满 20 位，**不含校验位**。这意味着**回读数据的完整性没有协议级保护**，只能依赖物理层的差分抗扰度。
>
> 说明：上表依据 RAYLASE 原文 Diagram 4 的位序列重建（`0 0 1 1`+16 位 / `0 0 0 1`+16 位 / `0 1`+18 位，各自构成 20 位周期）。PDF 文本提取对该图有轻微串行化，帧头**具体取值建议以原始 PDF 图为准**。
> 来源：[RAYLASE SS-III XY2-100-E 接口文档](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)

**反馈帧不可区分**（原文）：
> *"Because of the downward compatibility there are three different frame types which are not distinguishable from each other because of their structure. This doesn't matter as the control card and its user exercise the entire control over the received data format via the command frame and therefore the received frame type is known by the user."*
> —— 即：**接收方必须事先通过命令帧约定反馈格式**，无法从数据本身自识别。控制卡需为此负责。

**反馈通道可选信号（SetMode 0x05 参数表，节选）**：

| 参数 | 信号 | 帧类型 |
|---|---|---|
| 0x00 | **状态字 Status word** | 16 bit 反馈帧 |
| 0x01 | 实际角位置 Actual Angular Position | 16 bit |
| 0x02 | 设定角位置 Set Angular Position | 16 bit |
| 0x03 | 位置误差 Position Error | 16 bit |
| 0x04 | 实际电流 Actual Current | 16 bit |
| 0x05 | 相对振镜控制 Relative Galvo Control | 16 bit |
| 0x06 | 实际角速度 Actual Angular Velocity | 16 bit |
| 0x14–0x1F | 温度、电压、序列号等 | 16 bit |
| 0x20–0x3F | 物料号、固件版本、运行时间等 | 16 bit |
| 0x80 | 兼容状态字 Compatible Statusword | 16 bit 向下兼容帧 |
| 0x81/0x82/0x83 | 18 bit 实际/设定角位置、位置误差 | 18 bit |
| 0x90 | 插值配置 Interpolation Configuration | 18 bit |

来源：[RAYLASE SS-III](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)

### 6.1 状态字（Status word 0x00）位定义 —— RAYLASE 官方

状态字为 **8 bit，在高字节与低字节中重复**（即 bit15–8 与 bit7–0 内容相同）：

| 位（高/低） | =1 含义 | =0 含义 |
|---|---|---|
| **Bit 15 / Bit 7** | 轴正在工作（axis at work） | 故障（failure） |
| **Bit 14 / Bit 6** | 振镜温度正常 | 振镜温度故障（SS-III 不测该温度，恒为 OK） |
| **Bit 13 / Bit 5** | Z 轴位置在跟踪误差窗口内 | （当前未实现，恒为 1） |
| **Bit 12 / Bit 4** | **X 轴（小镜）位置在跟踪误差窗口内** | 超出窗口 |
| **Bit 11 / Bit 3** | **Y 轴（大镜）位置在跟踪误差窗口内** | 超出窗口 |
| **Bit 10 / Bit 2** | 自动标定传感器未激活（无自动标定时恒为 1） | — |
| **Bit 9 / Bit 1** | 恒为 0 | — |
| **Bit 8 / Bit 0** | 恒为 1 | — |

跟踪误差窗口可由命令 `SetPosAcknowledgeLevel (0x15)` 配置。
来源：[RAYLASE SS-III XY2-100-E 接口文档](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)

### 6.2 状态字（BACK）位定义 —— 中文厂商版本

中文一手资料（XYMOTION）给出的 20 位 BACK(STATUS) 字结构如下：

**标准 XY2-100 的 BACK（STATUS）字**：

| 位号 | 19 | 18 | 17 | 16 | 15 | 14 | 13 | 12 | 11 | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 内容 | 0 | 0 | 1 | **PSO** | **Pulse** | **X ready** | **Y ready** | **Z ready** | 保留 | 保留 | **X error** | **Y error** | **Z error** | 保留 | 保留 | 保留 | 保留 | 保留 | 保留 | **Pe** |

术语含义（原文）：

| 缩写 | 含义 |
|---|---|
| **Ready** | X/Y/Z 位置**到位**状态 |
| **Error** | X/Y/Z **故障**指示 |
| **Pulse** | 散点脉冲 |
| **PSO** | 同步位置信号状态输出（Position Synchronized Output） |
| **Pe** | Parity even 偶校验位 |
| **Po** | Parity odd 奇校验位 |

**XY2-100E 的 BACK（STATUS）字**：结构与上表相同，位 19 = **1**（其余不变），仅位置数据扩展到 18 bit。

> ⚠️ 该表的位号-内容对齐系依据原始 HTML 表格（`BIT19…BIT10` 与 `BIT9…BIT0` 两张表）重建；原表在 BIT11/BIT10 与 BIT6…BIT1 处为空白保留位。BIT9/BIT8/BIT7 = X/Y/Z error 的对应关系明确，但**BIT11/BIT10 的含义原始资料留空**。
> 来源：[cnblogs XYMOTION《XY2-100振镜控制协议》](https://www.cnblogs.com/xymotion/p/12987507.html)

> **来源冲突提示**：RAYLASE 的状态字为 **8 bit（重复两次）** 且**高有效表示正常**；中文资料的 BACK 字为 **20 bit 帧**，`ready` 表示到位、`error` 表示故障。二者**不是同一定义**，反映出不同厂商/代次的状态通道实现差异。sigrok 也指出反馈信号**至少有 3 种变体且无法互相区分**：
> > *"The status or feedback signal is unfortunately not straightforward to decode. The main reason is that there are at least 3 different variants: backwards-compatible 16 bit, standard 16 bit and 18 bit. They can't be distinguished from one another..."*
> 来源：[sigrok](https://sigrok.org/wiki/Protocol_decoder:Xy2-100)

### 6.3 「3 位状态字」的准确出处 —— 返回帧的 3 bit 头识别码

任务中提到的"XY2-100 Enhanced 的 **3 位状态字**（channel status / ready 等）"确有出处：**HALaser E1803D 官方手册 API 附录**给出了**返回帧（振镜 → 控制器）前 3 bit 的识别码定义**，并用于**区分 2D 头与 3D 头**：

| 头类型 | bit19 / C2 | bit18 / C1 | bit17 / C0 | **识别码** |
|---|---|---|---|---|
| **2D 扫描头** | 0 | 1 | 1 | **`0 1 1`** |
| **3D 扫描头** | 0 | 0 | 1 | **`0 0 1`** |

- 原文（`E180X_get_head_state()` 说明表，文档第 112 页）：`Bit 19 / C2 … 0 (Identification bit)`、`Bit 18 / C1 … 1 / 0`、`Bit 17 / C0 … 1 / 1`
- 并注明："当扫描头不提供此类信息、返回无效数据或使用私有格式时，函数返回 `0xFFFFFFFF`"。
- 来源：[HALaser Systems E1803D Scanner Controller Manual](https://halaser.eu/manuals/e1803_manual.pdf)

**因此返回帧的完整结构（HALaser 口径）为**：**3 bit 识别码 + 16 bit 状态 + 1 bit 奇偶校验 = 20 bit**。

⚠️ **但与 RAYLASE 的位划分不兼容（厂商实现差异，非文档错误）**：

| 厂商 | 返回帧位划分 |
|---|---|
| **HALaser** | **3 bit 识别位 + 16 bit 状态 + 1 bit 校验** |
| **RAYLASE** | **4 bit 帧头 + 16 bit 数据（无校验位）** |

两者都能拼满 20 bit，但位划分不同。

**此外还需注意"ready / error"三重组**：中文资料的 BACK 字中含有 3 个 **ready** 位（X/Y/Z 位置到位）与 3 个 **error** 位（X/Y/Z 故障指示）——见 6.2 节。这可能也是"3 位状态"印象的来源之一。

> **总结**：与"3 位"相关的概念共有**三个**，请勿混淆：
> 1. **前向通道的 3 位控制字 C2C1C0**（`001` = 位置帧、`111` = 命令帧）—— 见 4.1 节
> 2. **返回通道的 3 位头识别码**（`011` = 2D 头、`001` = 3D 头）—— HALaser 定义
> 3. **返回状态字中的 X/Y/Z ready 与 X/Y/Z error 三重组** —— 中文厂商定义
>
> ⚠️ **工程提醒**：**公开资料中返回通道至少有 4 种互不兼容的描述**（单根 STATUS 线 / 20 bit BACK 帧 / 8 bit 重复状态字 / 3 bit 识别码 + 16 bit 状态）。**实现时必须按具体扫描头型号的厂商手册确定，不能假定通用。**

---

## 7. 协议族对比

### 7.1 XY2-100 系列变体

**HALaser E1803D 手册（Appendix B）给出的官方模式对照表**——这是四代变体最清晰的一手数据：

| 模式 | 帧长 | 帧周期 | 等效帧率 | 位置分辨率 |
|---|---|---|---|---|
| **XY2-100** | 20 bit | **10 µs** | **100 kHz** | **16 bit** |
| **XY2-200** | 20 bit | **5 µs** | **200 kHz** | **16 bit** |
| **XY2-100E** | 20 bit | **10 µs** | **100 kHz** | **18 bit** |
| **XY2-200E** | 20 bit | **5 µs** | **200 kHz** | **18 bit** |

> 原文：*"In XY2-100 and XY2-100E mode one frame with 20 bits has a length of 10 usec which is similar to 100 kHz output clock. For the XY2-200 and XY2-200E modes a frame with 20 bits has a length of 5 usec which is similar to 200 kHz output frequency."*

来源：[HALaser Systems E1803D Scanner Controller Manual, Appendix B](https://halaser.eu/manuals/e1803_manual.pdf)

**综合对比表**：

| 特性 | **XY2-100** | **XY2-100 Enhanced (-E)** | **XY2-200 / XY2-200E** |
|---|---|---|---|
| 帧长 | 20 bit | 20 bit | 20 bit |
| 位置位宽 | 16 bit | **18 bit** | 16 bit（-E 为 18 bit） |
| 控制字 | `001`（位置）/ `111`（命令） | `001` / `111`（命令帧） | 同左 |
| 校验 | **偶校验** | **奇校验**（18 bit 模式） | 同左 |
| 帧周期 | **10 µs** | 10 µs | **5 µs** |
| 帧率 | **100 kHz** | **100 kHz** | **200 kHz** |
| 时钟 | 2 MHz | 2 MHz（RAYLASE SS-III：**上限 10 MHz，推荐 4 MHz**） | **4 MHz** |
| 反馈通道 | 单 STATUS 线，或 20 bit BACK 字 | 可经命令**动态选择**反馈信号 | 同 -E |
| 分辨率（±0.36 rad） | 11 µrad | 2.8 µrad | 11 µrad（-E：2.8 µrad） |
| 代表产品 | SCANLAB RTC4 | SCANLAB intelliSCAN、RAYLASE SS-III、HALaser E1803D | HALaser E1803D |

来源：[HALaser E1803D Manual](https://halaser.eu/manuals/e1803_manual.pdf)、[sigrok](https://sigrok.org/wiki/Protocol_decoder:Xy2-100)、[RAYLASE SS-III](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)、[Quantronix 规范 PDF](https://www.aaronvose.net/Quantronix_Osprey/xy2_100_specification.pdf)、[SCANLAB intelliSCAN 14](https://www.scanlab.de/en/products/scan-systems/intelliscan/standard-series/intelliscan-14)

### 7.2 与 SL2-100 对比

#### (a) 归属与定位（一手）

SCANLAB 官方明确声明 SL2-100 由其**开发并引入**：
> *"The widely used XY2-100 protocol with only **16-bit positioning resolution** is often no longer adequate for micro-machining. Here, the **20-bit SL2-100 protocol, developed and introduced by SCANLAB**, is a necessary upgrade. High-end scan systems and control boards such as RTC5 and RTC6 support this protocol."*
> —— SCANLAB 微加工技术页

RTC5 官方手册：
> *"The RTC5 communicates with scan systems via the new SL2-100 data transfer protocol. This protocol supports **20-bit control signals** and thereby a **16x higher positioning resolution** compared to the RTC4 predecessor board."*

16× = 2⁴，与 20 bit vs 16 bit **完全吻合** ✅

第三方（HALaser）评价其为**私有封闭**接口：
> *"SL2-100™ digital interface … **proprietary and closed** … used by few vendors only … **incompatible in both, hardware and data format**"*

来源：[SCANLAB 微加工技术页](https://www.scanlab.de/en/technologies/micromachining)、[SCANLAB RTC5 手册](https://www.scanlab.de/sites/default/files/2020-08/13_RTC5_control%20boards.pdf)、[HALaser 协议对比表](https://halaser.systems/compare.php)

#### (b) ⭐ 帧结构 —— **已获得 SCANLAB 官方原始定义（一手）**

**来源：SCANLAB RTC6 Manual, Doc. Rev. 1.1.4 en-US, 附录 F「SL2-100 Protocol Short Information」，第 1214 页**。官方原文逐条照录：

> **SL2-100 protocol:**
> - Is bidirectional
> - Is serial
> - Requires **2 separate channels**
>   - **Forward Channel**（视角为 RTC 板）：1 channel for the direction RTC board → iDRIVE scan system
>   - **Return Channel**：1 channel for the direction iDRIVE scan system → RTC board
> - Data in Forward Channel and Return Channel are transported in **blocks**（"SL2-100 block", "transmission block"）
> - With SL2-100 protocol, Forward Channel and the Return Channel are **completely independent of each other**
> - Accordingly, both have their own SL2-100 blocks
> - A block start in one direction does not automatically mean a block start in the other direction
> - The following applies:
>   - **1 block consists of 192 frames** = "block length"
>   - **Each block starts with a preamble**（generated by the RTC board）
>   - **1 frame consists of 2 sub-frames**
>   - **1 frame is transmitted in 10 µs**
>   - **1 sub-frame contains**
>     - **20 bits of payload**（control values or status values）
>     - **12 bits of further information**（for example, for synchronization）

**官方结构分解表**：

| 层级 | 构成 | 说明 |
|---|---|---|
| **Block（块）** | **192 帧** + 1 个 **preamble** | 双向**各自独立**分块，块起点互不对应 |
| **Frame（帧）** | **2 个子帧** | **10 µs**（= 100 kHz） |
| **Sub-frame（子帧）** | **20 bit 载荷 + 12 bit 附加信息 = 32 bit** | 载荷为控制值（前向）或状态值（回传）；12 bit 用于同步等 |

> 来源：[SCANLAB RTC6 Manual Doc. Rev. 1.1.4, Appendix F, p.1214](https://raw.githubusercontent.com/labspiral/sirius3/main/doc/SCANLAB/RTC6_Manual.en.pdf)（本报告已下载 24.8 MB 官方 PDF 并直接提取该页）

**与第三方逆向结果的吻合度（本报告核对）**：

| 项目 | 官方（一手） | 第三方逆向（二手） | 是否吻合 |
|---|---|---|---|
| 每帧总位数 | 2 子帧 × (20+12) = **64 bit** | X + Y 各 32 bit = **64 bit** | ✅ 完全一致 |
| 子帧位划分 | **20 载荷 + 12 附加** | 20 轴数据位 + 6 模式 + 3 控制 + 1 校验 + 1 起始 + 1 停止 = 32 | ✅ 总数一致（12 bit 附加信息的内部分配由逆向给出） |
| 帧周期 | **10 µs** | 10 µs | ✅ |
| 线路码元 | 差分曼彻斯特 → 64×2 = **128 码元/帧** | 论坛实测 **128 码元 / 10 µs** | ✅ |
| 有效数据率 | 64 bit / 10 µs = **6.4 Mbit/s** | 推算 6.4 Mbit/s | ✅ |

> **结论：第三方逆向的"每轴 32 bit、X+Y 共 64 bit、10 µs、差分曼彻斯特"与 SCANLAB 官方的"1 frame = 2 sub-frames × (20+12) bit、10 µs"精确吻合，互为独立验证。** 逆向给出的 12 bit 附加信息内部分配（起始/模式/控制/校验/停止）是官方未公开的部分。

**第三方逆向给出的子帧位布局（二手，供参考）**：

| 序号 | 字段 | 位宽 |
|---|---|---|
| 1 | 帧起始位 | 1 bit |
| 2 | **模式选择位**（选弧线 / 连续直线 / 点） | **6 bit** |
| 3 | 轴数据位（**低位先发，LSB → MSB**） | **20 bit** |
| 4 | 控制位（"就是 XY2-100 协议里的控制位，一样的"） | **3 bit** |
| 5 | 校验位（**奇校验**，覆盖模式选择位 + 轴数据 + 控制位） | 1 bit |
| 6 | 停止位 | 1 bit |
| **合计** | | **32 bit** |

- **帧起始后模式选择字段的第 1 位用于区分轴：0 = X 轴，1 = Y 轴**
- 实测波形特征：起始位/结束位组合可识别为 `11100`；20 bit 数据在物理层占 **40 个差分曼彻斯特码元**

来源：[CSDN 逆向博客 1](https://blog.csdn.net/ttstststtttt/article/details/145651470)、[CSDN 逆向博客 2](https://blog.csdn.net/weixin_51352668/article/details/161866786)

**官方定义的返回通道错误位（一手）**：SCANLAB 官方列出了 SL2-100 的若干错误指示位，包括 **Preamble（前导）错误、pulse length（脉冲长度）错误、bit count within subframe（子帧内位数）错误、parity（校验）错误**。
> 这些错误位是"差分曼彻斯特编码"逆向外挂的**最强旁证** —— 官方错误分类与曼彻斯特解码所需的帧同步、位计数、校验检查一一对应。

#### (c) 编码与位速率

- **编码**：**差分曼彻斯特编码（Differential Manchester）** —— 两个独立中文来源一致；官方的错误位分类（preamble / pulse length / bit count / parity）从侧面印证自同步编码特征。
  > ⚠️ **注意**：**SCANLAB 官方并未公开说明 SL2-100 使用曼彻斯特编码**。"差分曼彻斯特"仍属**二手逆向结论**，虽与官方错误位高度自洽，但未获官方确认。
- Photonlexicon 论坛用 RTC6 抓波形实测：**一帧 128 bit，耗时 10 µs**，编码"像 Manchester 或某种加密编码"。
- **位速率推算（本报告，基于官方结构）**：64 bit / 10 µs = **6.4 Mbit/s 有效数据率**；若为差分曼彻斯特（每 bit 2 个线路码元）→ **12.8 Mbaud 线路速率**。**与论坛实测"128 码元 / 10 µs"完全吻合** ✅
  > **官方未公开标称位速率** —— 上述数值为结构推算，非官方指标。

> ⚠️ **"26 bit" 说法核查**：**未找到任何来源支持 SL2-100 帧长为 26 bit**。出现"26 bit"的官方语境是**控制器内部运算分辨率**：
> > *"26 bit internal resolution (for better accuracy also with 16 bit or 18 bit hardware output)"* —— HALaser E1803D 手册
> HALaser 对比表中 "16..26 bit" 一栏属于 **XY3-100**，不是 SL2-100。
> **结论：26 bit 很可能是把控制器内部 26 bit 分辨率误读为 SL2-100 帧长。**
>
> ⚠️ **"10 Mbit/s" 说法核查**：**未找到任何一手文档**给出 SL2-100 的标称位速率（官方结构推算为 6.4 Mbit/s）。最接近的旁证是 Newson 的 **SDP** 协议（**不是 SL2-100**）：*"an open UART protocol with a baud rate of 10 Mbit/sec"*。**"10 Mbit/s"可能源于对 Newson SDP 的混淆。**
>
> ⚠️ **"SL2-100 帧长 26 bit / 6 位模式位"** 中的 26 bit 已证伪；6 位模式位来自逆向，官方未公开。

#### (d) 综合对比

| 特性 | **XY2-100** | **SL2-100** |
|---|---|---|
| 定位 | 上一代数字接口 | SCANLAB 新一代数字接口（**私有封闭**） |
| 位置位宽 | 16 bit | **20 bit** |
| 分辨率（±0.36 rad） | **11 µrad**（精度天花板） | **0.7 µrad**（提升 16 倍） |
| 编码 | 非归零串行，独立 CLOCK/SYNC | **差分曼彻斯特编码**（自同步，无需独立时钟线） |
| 信号线 | CLOCK / SYNC / X / Y / STATUS（多对） | **DATA IN ± / DATA OUT ±**（仅 2 对） |
| 帧长 | 20 bit/轴 | **32 bit/轴**（X+Y 共 64 bit） |
| 位序 | MSB first | **LSB first** |
| 校验 | 偶校验 | **奇校验**（覆盖模式位 + 数据 + 控制位） |
| 帧率 | 100 kHz | **100 kHz**（保持 10 µs 步进周期） |
| 连接器 | 25-pin D-SUB | **9-pin D-SUB**（数据）+ 3-pin 电源 |
| 电气隔离 | RTC4：**无** | RTC5/RTC6：**有** |
| 反馈通道 | 有限 | 支持**多参数回传**（RTC6 Multiplexing：状态数据可永久、与作业无关地传给应用） |
| 支持控制卡 | RTC4 | RTC5、RTC6 |

来源：[SCANLAB RTC 控制卡对比 PDF](https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf)、[SCANLAB 微加工技术页](https://www.scanlab.de/en/technologies/micromachining)、[SCANLAB intelliSCAN 引脚定义](https://www.scanlab.de/sites/default/files/2020-09/pin-out-intelliSCAN.pdf)

#### (e) EtherCAT ↔ SL2-100 网关（工业总线集成）

德国 Fraunhofer IWS / TU Dresden 的论文提出了把**工业现场总线 EtherCAT 直接对接 SL2-100** 的通信模块，其过程数据映射为：

| 记法 | 规格 |
|---|---|
| **Control Word** | Activation、**Interpolation Mode**（激活、插补模式） |
| **Output** | Set Position（设定位置） |
| **Input** | Feedback Position、Temperature（反馈位置、温度） |
| **Status Word** | Temperature OK、Position OK、Power OK |

> 该论文明确 SL2-100 的 Control Word 包含 **Interpolation Mode**，与中文博客所称"模式选择位选弧线/直线/点"方向一致 —— **两条独立来源互相印证**。

来源：[Lasers in Manufacturing Conference 2017, Contribution 143 (WLT)](https://www.wlt.de/lim/Proceedings2017/Data/PDF/Contribution143_final.pdf)、[Fraunhofer IWS 论文](https://www.wlt.de/lim/)

### 7.3 与 XY3-100 / 3D（三轴/多轴）对比

#### (a) 简单扩展：XY2-100 + Z

XY2-100 / XY2-100E 本身即可通过**增加一条 Z 通道**扩展为三轴：

- RAYLASE SS-III 的 25-pin DSUB 已在 **pin 5/18 定义 Z −/Z +**（聚焦轴），反馈也有独立的 **Z_stat（pin 7/20）**。
- 因此基础"3D"通常只是**在 XY2-100 基础上加一路 Z 数据线与 Z 反馈线**，帧格式、时序、时钟完全不变。
- SCANLAB RTC4 支持 **2/3 通道**（第 3 通道为 Z）；RTC5/RTC6 为 2/2，但可选项支持三轴扫描系统。
- RAYLASE SP-ICE 3 的 `ScanHeadFormat` 定义了 `XY2_100`（XY 或 XYZ，**Legacy 16-bit protocol via XY2-100 Adapter Board**）以及多种 SL2 的 3D/4D 组合（XYZ、Extra Z、Auxiliary、ZoomZ、Defocus）。
  来源：[RAYLASE SP-ICE 3 §7.1.1 Scan Head Format Definitions](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/d6107a36-ef4e-4e13-a21c-6cda62a65fd6.htm)、[SCANLAB RTC PDF](https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf)

#### (b) ⭐ XY3-100：LasIA 官方定义的 XY2-100 后继标准

> **重要更正**：本报告早期版本称 XY3-100 为"国内厂商（星移控制科技）定义的多轴扩展协议"——**这是错误的**。XY3-100 是 **LasIA（Laser Industry Association，国际激光行业协会）** 发布的**正式标准**，编号 **LIA202002（v1.0）/ LIA202307（v1.1）**。星移控制科技（XYMOTION）只是实现方之一。
>
> 官方原文：*"The XY3-100 protocol is intended to be used as **successor of the XY2-100 standard**."*

**官方 XY2-100 vs XY3-100 关键差异**：

| 特性 | XY2-100 | **XY3-100** |
|---|---|---|
| 位置位宽 | 固定 16 bit（Enhanced 18 bit） | **可变 16 – 26 bit** |
| 帧率 | 100 kHz | 可变，典型 100 kHz |
| 传输速率 | 100 ks/sec | 可变，典型 100 ks/sec |
| **回传通道** | **20 data bits，同步于 XY2-100 时钟** | **Flexible, asynchronous RS485 serial communication protocol** |
| 物理层 | DB25 | DB25 / DB15 / IDC |
| 纠错 | 1 位校验（Parity bit） | **Parity counter** on position/command data + 回传二进制协议 |
| 轴数 | X、Y（+Z） | X、Y、Z、U、W（**5 轴**）+ 独立 BACK 回传通道 |

**官方帧结构（LasIA LIA202307 v1.1 §5.1 原文照录）**：

前向数据由 **SYNC±、CLK±、X±、Y±** 及可选 **Z±、U±、W±** 传输，**固定帧长（典型 10 µs @100 ks/sec）但帧内数据位数可变**。

> 官方明确该协议 **"works similar to a standard SPI interface with CS (also named SS), SCK and SDI (also named MOSI) lines"** —— 因此**不一定要用 FPGA 接收，合适的 MCU 硬件即可**。
>
> ⚠️ **边沿约定（与 XY2-100 表述不同，务必注意）**：
> - **帧的起点由 SYNC 通道（CS）的下降沿标记**（XY2-100 是 **上升沿** 标记帧开始！）
> - **X/Y/Z/U/W 数据有效时，由 CLK 通道（SCK）的下降沿指示**

**24 bit 位置帧**：

| Bit | 23 | 22 | 21 … 2 | 1 | 0 |
|---|---|---|---|---|---|
| Data | **0** | **1** | D19 … D0（位置数据） | P1 | P0 |

- 总长 **24 bit，载荷 22 bit**（20 位位置 + 2 位校验）
- 100 ks/sec 时整帧 **10 µs**，等效时钟 **2.4 MHz**；也允许更高速率（如 200 ks/sec → 5 µs 帧长、**4.8 MHz** 时钟）
- 接收方可只用其中 ≤20 bit（不足时**忽略低位**）；发送方可只发 ≤20 bit（不足时**低位填 0**）

**32 bit 位置帧**：

| Bit | 31 | 30 | 29 … 4 | 3 | 2 | 1 | 0 |
|---|---|---|---|---|---|---|---|
| Data | **1** | **1** | D25 … D0（位置数据） | P3 | P2 | P1 | P0 |

- 总长 **32 bit，载荷 30 bit**（26 位位置 + 4 位校验）
- 接收方可只用 ≤26 bit；**26 bit 精度可用于向扫描头发送全分辨率中间数据以避免传输舍入误差**（官方说明：即使扫描头实际输出分辨率更低，更少的舍入误差也能带来更好精度）

**首 2 位的语义（官方）**：
- **第 1 位（bit 31 或 bit 23）= 帧总长指示**：`0` → 24 bit 帧；`1` → 32 bit 帧
- **第 2 位（bit 30 或 bit 22）= 工作模式**：`1` → 后续为**位置数据**；`0` → 后续为**命令帧**（可被数据接收方读取并执行，但不转换为位置数据）

> ✅ **这解决了此前"24 bit 还是 32 bit"的冲突：两种帧并存**，由首bit动态指示。官方无"推荐 32 bit"之说（此前说法来自厂商博客）。

**校验位算法（官方原文）**：

- **24 bit 帧 P1/P0**：
  1. 统计 **D19..D0（即 bits 21..2）** 中置 1 的位数
  2. 结果与 **`0x03`** 相与，取低 2 位
  3. 分别写入 **P1（掩码 0x02）** 与 **P0（掩码 0x01）**
- **32 bit 帧 P3..P0**：同理，统计位置数据位中 1 的个数，与 `0x0F` 相与后写入 P3..P0

> 注意：这是 **"校验计数器"（parity counter）**，与 XY2-100 的单比特奇偶校验不同 —— 它能携带 2 位/4 位信息，检错能力更强。

**回传通道（XY3-100 相对 XY2-100 的最大架构差异）**：
- 官方定义：**Flexible, asynchronous RS485 serial communication protocol** —— 即**异步串口**，与 XY2-100 的"同步 20 bit 回传"根本不同
- 有独立的 **BACK ± (F)** 差分对（DB25 的 6/19）
- 采用**二进制包协议**：包格式 `0x48 + Type + Len + Payload`；同步包为 `48 41 00`
- 默认 **115200 8N1**
- 数据线须符合 **ANSI/TIA/EIA-485-A 与 ISO 8482:1987**，且**接收端必须加终端电阻**

**关键工程数字汇总**：

| 项目 | 数值 |
|---|---|
| 帧长 | 24 bit 或 32 bit（首 bit 指示） |
| 位置位宽 | 16 – 26 bit 可变 |
| 帧周期 | 典型 10 µs（100 ks/sec） |
| 时钟 | 24 bit 帧 → **2.4 MHz**；32 bit 帧 → **3.2 MHz**；200 ks/sec @24 bit → 4.8 MHz |
| 校验 | 24 bit → 2 位；32 bit → 4 位（校验计数器） |
| 回传 | 异步 RS485，默认 115200 8N1 |
| 轴数 | 最多 5 轴（X/Y/Z/U/W）+ BACK |
| 引脚命名 | A=SYNC、B=CLK、C=X、D=Y、E=Z、F=BACK、G=U、H=W |

> **10 µs 刷新周期的设计约束再次得到印证**：扩展位宽时靠**提高时钟**而非拉长周期来补偿，说明 **10 µs 是被刻意维持的行业基准**。
>
> ⚠️ **再次强调**：尽管官方声称 "Same pinout as XY2-100(E)"，**CLK 与 SYNC 实际是互换的**（见 [2.3 节 (0)](#23-引脚定义四种厂商--官方标准对照)）。

来源：[LasIA LIA202307 v1.1（XY3-100 官方标准）](https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf)、[LasIA LIA202002 v1.0](https://web.archive.org/web/20210122224854id_/https://lasia.org/LIA202002/xy3_100_specification.pdf)、[XY3-100 官方 C 头文件](https://web.archive.org/web/20231206133135id_/https://lasia.org/LIA202307/xy3_100.h)、[星移控制科技《XY3-100协议简介》](https://www.xymotion.cn/index.php?m=home&c=View&a=index&aid=52)（厂商实现方，二手）

### 7.3b SL2-100 ↔ XY2-100 官方转换器/适配器

#### (a) SCANLAB XY2-100 Converter（配件号 #125377）

SCANLAB 官方配件，用于让只支持 XY2-100 的旧振镜接到只输出 SL2-100 的 RTC5/RTC6 控制卡上。**官方功能定义（RTC6 手册 Doc. Rev. 1.0.21）**：

> 该转换器将：
> - **SL2-100 协议控制信号（20 bit）→ XY2-100 协议控制信号（16 bit）**
> - **扫描系统的 XY2-100 协议状态信号 → SL2-100 协议状态信号**

⚠️ **关键工程数字**：
> *"When controlling scan systems, the XY2-100 Converter (Accessory) introduces a **10 µs signal propagation delay**. To compensate for this, the **LaserOn Delay and LaserOff Delay must be increased by 10 µs each**."*
>
> 即：**该转换器引入 10 µs 信号传播延迟**，必须在 `LaserOnDelay` 与 `LaserOffDelay` 上**各增加 10 µs** 予以补偿。

**注意位宽有损**：SL2-100 的 20 bit → XY2-100 的 16 bit，**分辨率从 0.7 µrad 退化到 11 µrad**（见 5.2 节）。

**物理规格**：9-pin 公 D-SUB（插 RTC6 的 SCANHEAD 口，或用尽可能短的 1:1 线缆接第 2 个 SCANHEAD 口）+ 25-pin 母 D-SUB（兼容 XY2-100 标准接口振镜）；外形 62 × 52 mm，安装孔距 56.5 / 34.5 mm，厚度 12.5 mm。

**通道说明（原文）**：CHAN1、CHAN2 向振镜发送控制值；SYNC、CLOCK 向扫描系统发送同步与时钟信号；**STATUS 通道（以及适当的 STATUS1 通道）接收扫描系统返回的 XY2-100 兼容状态信号**。

**转换器 25-pin 母 D-SUB 引脚（SCANLAB 官方）**：

| 引脚 | 信号 | 引脚 | 信号 |
|---|---|---|---|
| 1 | CLOCK − | 14 | CLOCK + |
| 2 | SYNC − | 15 | SYNC + |
| 3 | CHAN1 − | 16 | CHAN1 + |
| 4 | CHAN2 − | 17 | CHAN2 + |
| 5 / 18 | 不连接 | 6 / 19 | **STATUS ±** |
| 7 / 20 | 不连接 | 8 / 21 | **STATUS1 ±** |
| 9 / 22 | 不连接 | 10 / 11 / 12 / 13 / 23 / 24 / 25 | 不连接（**注：11、23、24 三脚相互连通**） |

⚠️ **重要脚注（官方原文）**：对 **iDRIVE 扫描系统**（intelliSCAN、intelliSCANde、intelliDRILL、intellicube、intelliWELD、varioSCANde），**STATUS± 通道是轴 2（X 轴）的状态通道**（因而也称 STATUS2±），而 **STATUS1± 是轴 1（Y 轴）的状态通道**。对**其他扫描系统，STATUS1± 不可用（不连接）**。—— 这是 XY2-100 状态通道**语义随振镜型号变化**的又一例证（呼应第 6 节）。

来源：[SCANLAB RTC6 PCIe Board Manual §4.5.2 XY2-100 Converter (Accessory)](https://www.easymanua.ls/scanlab/rtc6-pcie-board/manual?p=69)、[SCANLAB XY2-100 Converter Dimensions and Pinout（镜像）](https://cdn.casmart.com.cn/file/20220117/3810e78a3b25488eb3abdc20d7d4d7dd.pdf)

#### (b) RAYLASE XY2-100 Adapter（配合 SP-ICE 3 控制卡）

RAYLASE 为 SP-ICE 3 提供两种适配器套件：

| 订货号 | 型号 | 用途 |
|---|---|---|
| **08001** | XY2-100 Adapter SP-ICE 3 **Set** | 控制 1 个 XY2-100 振镜（Head 0） |
| **14009** | XY2-100 Adapter SP-ICE 3 **Dual Mode Set** | 控制 2 个 XY2-100 振镜（Head 0 + Head 1） |

- 两个适配器必须接到**同一块 SP-ICE 3 卡**，一个经 **X403（GPIOE）**，另一个经 **X402（GPIOD）**。
- ⚠️ **Dual Mode 适配器占用 X402（GPIOD）后，该端口无法再使用任何 Laser Adapter。**
- ⚠️ **安全警告（原文）**：连接 X403 时**必须确保 SP-ICE 3 卡未上电，否则会损坏 FPGA**。
- 若要经 J2 的模拟输出控制激光功率，必须把 J4 接到卡上的 **X1000 Analog**。

来源：[RAYLASE SP-ICE 3 User's Manual §4.1 XY2-100 Adapters](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/65db6d89-b141-46a3-a74c-0b0ec7df2df1.htm)

> **形态学结论**：SCANLAB 与 RAYLASE **都以"转接板"形式**把新一代控制卡（SL2-100 / SP-ICE 3）接到传统 XY2-100 振镜上。这说明 XY2-100 的**存量设备生态极其庞大**，新一代主控普遍选择**向下兼容**而非强制更换振镜。

### 7.4 SP-ICE 与 RTC —— 澄清概念层次

**RTC 与 SP-ICE 是"控制卡"（PC ↔ 振镜之间的控制器），不是振镜侧接口协议。**

| 产品 | 厂商 | 总线 | 振镜接口 | 通道 | 定位分辨率 | 连接器 |
|---|---|---|---|---|---|---|
| **RTC4** | SCANLAB | PCI Express / Ethernet | **XY2-100** | 2/3 | **16 bit** | 25-pin D-SUB |
| **RTC5** | SCANLAB | PCI / PCI Express | **SL2-100** | 2/2 | **20 bit** | 9-pin D-SUB |
| **RTC6** | SCANLAB | PCI Express / Gigabit Ethernet | **SL2-100** | 2/2 | **20 bit** | 9-pin D-SUB |
| **SP-ICE-1 PCI PRO / SP-ICE-2** | RAYLASE | PCI | XY2-100 / XY2-100-E | — | — | — |

RTC 系列其他关键指标：

| 指标 | RTC4 | RTC5 | RTC6 |
|---|---|---|---|
| 振镜接口**电气隔离** | **无** | **有** | **有** |
| 最大位图像素频率 | 50 kHz | 308 kHz | 800 kHz（可选 3.2 MHz） |
| 模拟输出 / 分辨率 | 2 / 10 bit | 2 / 12 bit | 2 / 12 bit |
| **激光延时分辨率** | **1 µs** | **1/2 µs** | **1/64 µs** |
| Sky writing（天空书写） | **不支持** | 支持 | 支持 |
| 列表内存 | ~8 000 | ~1 000 000 | ~8 000 000 |
| 激光同步 | 无 | — | n × 100 kHz |
| SCANahead | 无 | 无 | 支持（可选） |

> RTC4 的 SP-ICE 提示：RAYLASE 文档指出 **SP-ICE-1 PCI PRO 与 SP-ICE-2 会把每个命令位置连续发送两次**，因此 SS-III 需开启 `SetInterpolation` 的 bit0（默认 '1'）忽略重复位置，否则插值后会出现**锯齿状**指令位置。
> 来源：[RAYLASE SS-III](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)

来源：[SCANLAB RTC 控制卡对比 PDF](https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf)、[SCANLAB RTC 控制卡页面](https://www.scanlab.de/en/products/control-electronics/rtc-control-boards)

### 7.5 与模拟振镜接口对比（±5 V / ±10 V）

#### 实测电压范围（一手数据）

| 厂商 / 产品 | 模拟接口电压范围 | 来源 |
|---|---|---|
| **RAYLASE HALdrive X20**（XY3-100 → 模拟转换器） | "synchronous output of analogue X and Y position data in **±5 V .. ±10 V** range"（中间值可选），**20 bit 输出分辨率** | HALaser HALdrive 手册 |
| 同上，反馈输入 | 可馈入 **−5 V .. +5 V** 模拟信号对应实际振镜位置；最小位置 −5 V / −10 V，中心 0 V，最大位置 +5 V / +10 V | 同上 |
| **SCANLAB SCANcube 10**（模拟版） | "Control interface: digital SL2-100, digital XY2-100 standard, **analog ±4.8 V**" | SCANLAB 产品页 |

> **结论**：**±5 V 与 ±10 V 都是真实存在的标准范围**，常见做法是同一硬件通过配置/跳线支持两者。SCANLAB SCANcube 用的是 **±4.8 V**（留约 4% 余量），属**厂商选择而非通用规范**。
>
#### ⭐ 标度因子（scale factor）—— 已找到一手数值，且存在 **2 倍陷阱**

> **首先必须区分"机械度"与"光学度"**：振镜镜面转动 θ 时，反射光束偏转 **2θ**。因此 **光学角 = 2 × 机械角**。厂商指标若不注明是哪种，会导致 2 倍误差。

**一手标度因子汇总**：

| 厂商 / 产品 | 标度因子 | 单位基准 |
|---|---|---|
| **Thorlabs**（模拟驱动板，可跳线选择） | **0.5 / 0.8 / 1.0 V** | **每机械度** |
| **Sino-Galvo** | **0.33 V** | 每度 |
| **Scanner Optics**（模拟驱动板） | **0.5 – 2 V** | 每机械度 |

> 🚨 **重要更正**：流传的 **"±10 V = ±20° 光学"** 这一前提**在多数实现下错了 2 倍**。以 Thorlabs 的 **0.5 V/机械度** 档为例：
> - ±10 V = **±20° 机械** = **±40° 光学**
>
> 只有按 1.0 V/机械度 档才是 ±10 V = ±10° 机械 = ±20° 光学。**引用任何模拟量程→角度换算时，必须先确认标度因子档位与"机械/光学"基准。**

来源：[Thorlabs 模拟驱动板手册](https://thorlabs-prep4cn-store.thorlabsazure.cn/api/thorlabs-products/support-documents/GVS011/20381-D02.pdf)、[Scanner Optics 模拟振镜驱动板](https://www.scanneroptics.com/products/analog-galvo-driver/)、[Sino-Galvo SG7310 手册](https://files.stankee.ru/docs/sino-galvo/SINO-GALVO%20SG7310%20-%20Galvanometer%20Scanner%20-%20Instruction%20Manual.pdf)

#### ⭐ 分辨率瓶颈：是**电源噪声**，不是 DAC 位数

**决定性一手证据 —— 同一块 Thorlabs 模拟驱动板，只更换电源**：

| 电源类型 | 位置噪声（分辨率） | 折算等效位数 |
|---|---|---|
| **线性电源** | **15 µrad** | ≈ **15.5 bit** |
| **开关电源** | **70 µrad** | ≈ **13.3 bit** |

> **结论：同一块板、同一个 DAC，仅因电源不同，分辨率就差 4.7 倍（约 2.2 bit）。** 这说明模拟接口的精度瓶颈**在于电源与噪声，而非 DAC 位数**。
>
> ⚠️ 因此流传的 **"模拟等效 12 bit"这一说法没有一手证据支持**，不建议引用。

来源：[Thorlabs 模拟驱动板手册](https://thorlabs-prep4cn-store.thorlabsazure.cn/api/thorlabs-products/support-documents/GVS011/20381-D02.pdf)

#### 结构性对比

| 维度 | **模拟接口** | **XY2-100** |
|---|---|---|
| 精度 | **受噪声与数据源分辨率限制**（无固定位数） | **16 bit（64K 步）**，协议规定的确定值 |
| 最大轴数 | 2 | **3** |
| 2D 所需线数 | **4 根** | **8 根**（CLK±、SYNC±、X±、Y±） |
| 纠错 | **无** | 奇偶校验位 |
| 反馈通道 | **无** | 同步，固定 20 bit |
| 授权费 | 无 | 无 |
| 开放性与互操作 | 广泛接受；但**收发双方必须使用同一电压范围** | **公开标准，厂商中立** |

来源：[HALaser 协议对比表](https://halaser.systems/compare.php)、[SCANLAB SCANcube 10](https://www.scanlab.de/en/products/scan-systems/scancube/standard-series/scancube-10)、[RAYLASE HALdrive 手册](https://halaser.systems/manuals/haldrive_manual.pdf)

#### 数字接口为何取代模拟接口

- **中文技术文章**：
  > *"XY2-100 与 SL2-100 均为「振镜控制卡→振镜」的数字通信协议……**替代传统模拟信号（±10V）传输，解决模拟信号易受干扰、传输距离短、精度不足的痛点**"*
- **模拟接口的三个结构性短板**：无纠错、无反馈通道、依赖收发双方电压范围一致。
- **长距离传输的官方旁证**：SCANLAB 在 SL2-100 连接器上专门提供 **+3.3 V 给 POF（聚合物光纤）转换器**做光传输 —— 官方引脚文档原文："The 3.3 V voltage is supplied for SCANLAB's POF converter for optical data transmission."
- **微加工的分辨率驱动力**："The widely used XY2-100 protocol with only 16-bit positioning resolution is often no longer adequate for micro-machining."
- **论坛实测反馈**："the SL2-100 protocol has **higher resolution and is more reliable than the XY2-100 protocol when using long distance transmission**"

来源：[CSDN 数字协议替代模拟](https://blog.csdn.net/fq1986614/article/details/159765686)、[HALaser 协议对比表](https://halaser.systems/compare.php)、[SCANLAB intelliSCAN 引脚定义](https://www.scanlab.de/sites/default/files/2020-09/pin-out-intelliSCAN.pdf)、[SCANLAB 微加工技术页](https://www.scanlab.de/en/technologies/micromachining)

### 7.6 其他振镜/扫描头协议一览

**HALaser 官方协议对比表**（厂商自述"errors expected"，仅供参考）：

| 协议 | 精度 | 最大轴数 | 2D 线数 | 反馈通道 | 开放性 | 授权费 |
|---|---|---|---|---|---|---|
| **模拟** | 受噪声/源分辨率限制 | 2 | **4** | 无 | 广泛接受 | 无 |
| **XY2-100** | **16 bit (64K)** | 3 | **8** | 同步，固定 20 bit | **公开标准** | 无 |
| **XY2-100E** | **18 bit (256K)** | 3 | 8 | 同步，固定 20 bit | **公开标准** | 无 |
| **SL2-100** | **20 bit (1M)** | 3 | **2** | 同步，20 bit | **私有封闭** | 未授权第三方 |
| **RL3-100**（RAYLASE） | **20 bit (1M)** | 未知（可能 5） | 未知（可能 2） | 未知 | 私有封闭 | 未授权第三方 |
| **SDP**（Newson） | 16 或 20 bit | 3 | 每轴 2 根 | 私有 | 有文档的私有协议 | 无 |
| **NX-02**（HALaser） | **20 bit (1M)** | 3 | 2 | 同步，20 bit | 需授权 | 需洽谈 |
| **XY3-100**（LasIA） | **16..26 bit (64K..64M)** | **5** | 8 | **异步，可变长多用途** | **开放且文档完善** | 无 |

来源：[HALaser 协议对比表](https://halaser.systems/compare.php)

**各协议要点**：

| 协议 | 要点 |
|---|---|
| **RL3-100**（RAYLASE 自有） | **20 bit** 位置分辨率，**单连接器最多 6 轴**；"即便最复杂的带 3D、Zoom 和第二 Z 轴的扫描头，也能用单根电缆运行" |
| **NX-02**（HALaser） | **20 bit**，**2 根线**，**向后兼容 SL2-100 的 2D 模式**；需 NX-02 扩展板 |
| **SDP — Shared Data Power**（Newson） | **单根同轴电缆同时供电与通信**，数据调制在电源上；**开放 UART 协议，波特率 10 Mbit/s**；支持 20 bit 与 legacy 16 bit 两种格式；**无纠错**。⚠️ **注意：常被误认为 SL2-100 的 "10 Mbit/s" 实际出自此处** |
| **HSSI / RTFE-D15D** | 出现在 PMDi（Polaris UniverseOne）振镜接口模块支持列表中；**技术规格未找到公开数据**（厂商私有，仅列名称） |
| **EtherCAT 振镜（ESL2-100 网关）** | 德国 WLT 会议论文报道的 **EtherCAT ↔ SL2-100 网关**；控制最多 2 轴；支持**过采样模式**（每个 PLC 周期最多接收 10 个位置并顺序插补） |
| **iDRIVE**（SCANLAB） | 全数字伺服电子技术（intelliSCAN、intellicube、intelliDRILL、intelliWELD 等）；实时监控与远程诊断、多种动态整定切换 |
| **SCANahead**（SCANLAB RTC6 选件） | 使扫描系统"独立于扫描速度，以最大可能加速度运行" |
| **PSO / Pulse** | XY2-100 STATUS 帧的 bit16（PSO，同步位置输出）与 bit15（Pulse，散点脉冲） |

来源：[RAYLASE SP-ICE 3 手册 RL3-100 节](https://software.raylase.de/rpi/RAYLASE/SPICE3/UsersManual%20v2.3.5/html/45289f65-2556-4dff-8d27-7f5918253301.htm)、[HALaser E1803D 手册](https://halaser.eu/manuals/e1803_manual.pdf)、[Newson rhothor SmartDeflector](http://newson.be/rhothor_SmartDeflector.htm)、[WLT 会议论文 Contribution 143](https://www.wlt.de/lim/Proceedings2017/Data/PDF/Contribution143_final.pdf)、[PMDi XY2-100 模块](https://pmdi.com/posts/product/hardware/xy2-100-galvoscanner-module/)、[pmdi HSSI 模块](https://pmdi.com/posts/product/hardware/hssi-galvoscanner-module/)

**XY3-100 归属澄清**：XY3-100 由 **LasIA（Laser Industry Association International）** 定义（星移控制科技页面标注"协议部分内容来自 LasIA"），是**开放且文档完善**的协议，可达 **5 轴**（X/Y/Z + U/W，或复用为 XR/YR/ZR 反馈总线）。详见 7.3 节。

**中国厂商的帧级协议可得性**：金橙子（JCZ）、大族激光、世纪桑尼等厂商**只公开应用层 API 与产品规格，不公开振镜侧帧级协议** → **未找到公开数据**。这从侧面印证 XY2-100 / SL2-100 的"事实标准"地位：厂商无需自研帧格式，直接采用既有标准。

---

## 8. 实现要点（FPGA / MCU）

### 8.1 发送端核心结构（FPGA）

XY2-100 发送端 = **一个 20 位移位寄存器 + 一个 5 位计数器 + 一个状态机**，全部由 2 MHz（或更高）时钟驱动：

1. 用**时钟分频器**产生连续 CLK（2 MHz 时 500 ns 周期，建议 50 % 占空比）。
2. 在每个 CLK **上升沿**前，把下一位推到数据线上；**下降沿**由振镜采样。
3. **20 位帧计数器** 0→19 循环；计数器为 0 时产生 **SYNC 上升沿**，计数 1–19 期间 SYNC 保持高，计数到 19（校验位）时 **SYNC 拉低**。
4. 发送字构造（发送端，MSB first）：

```verilog
// 20 位待发送字：{C2,C1,C0, D15..D0, P}
wire [19:0] frame = {2'b00, 1'b1, pos16, parity_even};
// parity_even = ^frame[19:1]  —— 对全部 19 个前导位求偶校验
assign parity_even = ^{2'b00, 1'b1, pos16};
```
   等价写法（Tuet C 实现，可直接对拍验证）：
```c
uint32_t Ch1 = (((uint32_t)X << 1) | 0x20000ul) & 0x3fffeul;  // C0=1, D15..D0
uint8_t parity1 = 0;
for (int i = 0; i < 20; i++) if (Ch1 & (1 << i)) parity1++;
if (parity1 & 1) Ch1 |= 1;                                     // 置偶校验位
```
   来源：[Tuet/XY2_100](https://github.com/Tuet/XY2_100)

### 8.2 接收端 / 解码端状态机（可综合 Verilog）

完整的 XY2-100 解码器状态机（含边沿检测、20 位计数、移位、完成标志）：

```verilog
// 412910609/galvoMC —— XY2_100.v（节选）
parameter IDLE = 2'b00, READ = 2'b01, END = 2'b11;

// SYNC 上升沿检测
assign det_sync_edge_n   = {det_sync_edge[0], xy_sync};
assign sync_posedge_reg_n = (det_sync_edge == 2'b01) ? 1'b1 : 1'b0;

// CLK 下降沿检测（振镜在此刻采样）
assign det_clk_edge_n    = {det_clk_edge[0], xy_clk};
assign clk_negedge_reg_n = (det_clk_edge == 2'b10) ? 1'b1 : 1'b0;

// 状态机
IDLE: if (sync_posedge_reg) state_next = READ;      // SYNC 上升沿启动
READ: if (bit_cnt == 5'd20) state_next = END;       // 收满 20 位
END:  if (finish_flag)      state_next = IDLE;

// 20 位计数，下降沿递增
if (bit_cnt >= 20 || state_current != READ) bit_cnt_n = 0;
else if (state_current == READ && clk_negedge_reg) bit_cnt_n = bit_cnt + 1;

// 移位（下降沿移入）
if (state_current == READ && clk_negedge_reg)
    shift_x_data_n = {shift_x_data[18:0], xy_x_data};

// 收满 20 位后取 [16:1] 作为 16 位位置
if (bit_cnt == 5'd20) out_x_data_n = shift_x_data[16:1];
```
来源：[412910609/galvoMC](https://github.com/412910609/galvoMC)

**要点**：`SYNC 上升沿` 启动、`CLK 下降沿` 采样、20 位计数、`[16:1]` 取数据——四个关键点全部与协议一致。

### 8.3 MCU 实现路线（各平台已验证的"奇技淫巧"）

由于 XY2-100 要求 **20 位严格同步、2 MHz+ 连续时钟**，普通 GPIO 软件翻转基本做不快，各平台都借用外设：

| 平台 | 采用外设 | 备注 | 来源 |
|---|---|---|---|
| **Teensy 4.1** | **SAI（数字音频 TDM）** | 直接生成 10 Mbit/s，20 时钟中断一次换数据；`I2S1_TDR0 = 0x20000 \| (val<<1)` | [PJRC](https://forum.pjrc.com/index.php?threads/implementing-xy2-100-serial-protocol-on-teensy-4-1.62819/) |
| **Teensy 3.2 / LC** | **DMA（DMAChannel）** | 成熟库，可接近全速 | [Tuet/XY2_100](https://github.com/Tuet/XY2_100) |
| **RP2040（Pico）** | **PIO 状态机** | 精确生成差分 CLOCK/SYNC/X/Y，双核分工 | [earlynerd/XY2Galvo](https://github.com/earlynerd/XY2Galvo) |
| **STM32F1 / 通用 STM32** | **SPI + DMA 双缓冲** | SPI 当移位寄存器用，MOSI 出数据、SCK 出时钟 | [belikoff16/XY2-100-](https://github.com/belikoff16/XY2-100-)、[CSDN 基于 STM32F103](https://blog.csdn.net/2501_93091150/article/details/150452592) |
| **RP2350 / QSPI 外设** | **QSPI** | 直接把 20 位帧编码进 QSPI 字节流 | [hyperchao0/qspi4xy2-100](https://github.com/hyperchao0/qspi4xy2-100) |
| **ESP32** | **RMT / I2S / LEDC** | 有可用的 ESP32 实现 | [txpzyr/xy2_100](https://github.com/txpzyr/xy2_100) |
| **Arduino Nano / 通用 AVR** | GPIO 位翻转 | **跑不到 2 MHz**，但实测"能驱动振镜" | [georgemihaila/xy2-100](https://github.com/georgemihaila/xy2-100) |

**PIO 实现的关键注释**（RP2040，原文）：
```
; generate 2MHz clock and sync pulse on Parity bit
nop  side (SYNC_LOW + CLOCK_HIGH) [1]   ; bit 20: parity
```
来源：[earlynerd/XY2Galvo `XY2-100.pio`](https://github.com/earlynerd/XY2Galvo)

**ESP32 / QSPI 的位序代码**（`0x8000 >> i` 明确体现 MSB first）：
```c
for (uint8_t i = 0; i < 16; i++) {
    if (x & (0x8000 >> i)) { buf[1 + j] |= 0x04; xp = !xp; }
    ...
}
```
来源：[hyperchao0/qspi4xy2-100](https://github.com/hyperchao0/qspi4xy2-100)

### 8.4 帧率与写入间隔约束

- 2 MHz 下每帧 = `(19+1) × 50 ns = 10 µs`，因此**数据写入的平均间隔不应小于 10 µs**，否则可能丢数据。
  来源：[CSDN XY2-100 驱动 Verilog 代码](https://blog.csdn.net/my_daling/article/details/153693888)
- 提高时钟可等比提高刷新率（见 3.1 节），但**必须确认振镜支持**。
- **更新率不必等于 100 kHz**：可以低于 100 kHz 发送，只要 CLOCK 与 SYNC 持续运行。Enhanced 还支持把更新率降到很低并由 `SetInterpolation (0x90)` 做线性插值（见 9.5）。

---

## 9. 工程陷阱与实战经验

### 9.1 校验位范围算错（最高频错误）

如 4.4 节所述，**必须把控制位 C0 计入偶校验**。只对 16 位数据求校验会与接收端判定不符。多个流行开源库（georgemihaila、NOBIC-NTU/OPAL）存在此问题。

### 9.2 边沿极性搞反

- **上升沿变数据、下降沿被采样**——这一条与 SPI 的常见习惯（CPOL/CPHA 组合）不同，直接用 SPI 外设时必须仔细核对 CPOL/CPHA 设置。
- 若把"下降沿变数据"当成约定，会导致采样点落在数据跳变瞬间，出现**随机误码**，且故障率随线长与时钟升高而恶化。

### 9.3 SYNC 宽度与相位搞错

SYNC **高 19 拍、低 1 拍**（低电平那拍是校验位），**不是**"1 拍高脉冲"。PJRC 论坛上就出现过用户写成"20 拍里高 1 拍"被 Paul Stoffregen 依据 RAYLASE 文档纠正的实例。
来源：[PJRC 论坛](https://forum.pjrc.com/index.php?threads/implementing-xy2-100-serial-protocol-on-teensy-4-1.62819/)

### 9.4 时钟必须连续 + 抖动

- **CLOCK 必须持续运行**，不能用"只在需要更新时才发时钟"的方案；RAYLASE 明确把 **clock/sync 出错**列为故障指示（PX/PY 红灯常亮）。
  来源：[RAYLASE SS-III](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)
- **建立/保持时间**：tDS ≥ 50 ns、tDH ≥ **100 ns**（保持时间要求比建立时间更宽松，注意别搞反）。
  来源：[Ray-Motion DS](https://dvd.ilphotonics.com/Ray-Motion%20-%20galvanometers%20-%201D-2D-3D%20scanners/Motion%20Control%20-%20Optomechanics/Interface%20XY2-100.pdf)
- 抖动（jitter）会把相位噪声引入采样时刻；在 2 MHz 下 100 ns 的保持余量并不宽裕，**避免用被高优先级中断打断的软件翻转产生时钟**。

### 9.5 更新率 vs 振镜带宽匹配 / 扫描延迟补偿

**这是决定打标质量的核心问题。** 若指令更新率远高于振镜带宽，振镜跟不上指令，会在拐角产生"圆角"；若更新率太低，则位置台阶化。

RAYLASE 提供的官方手段 —— **`SetInterpolation (0x90)`**：

| 参数位 | 含义 |
|---|---|
| Bit 7 – 1 | **最大插值时间，以 2 µs 为单位**（0→0 µs，1→2 µs，…，127→254 µs）。若命令位置以**小于该值的间隔**送达，振镜在相邻两个命令位置间做**线性插值** |
| Bit 0 | 置 '1' 时**忽略重复出现的命令位置**（用于 SP-ICE-1 PCI PRO / SP-ICE-2 这类会连续发两次相同位置的卡，避免插值后出现锯齿） |

**关键副作用（原文要点）**：
> 轴的运动会被**该插值时间所延迟**，即**整个跟踪延时（tracking delay）会增大这段时间**。位置控制本身的主跟踪延时**不变**——**被mark物体的边缘不会被圆化，只是整体晚一点画出**。必要时需相应调整**激光延时（laser delay）**。

**默认值：120 µs（参数 60）**；Bit 0 默认 '1'（激活）。
来源：[RAYLASE SS-III XY2-100-E 接口文档](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)

**延时参数体系（打标工艺）**：通常包含 5 类延时——**开光延时（Laser On Delay）、关光延时（Laser Off Delay）、跳转延时（Jump Delay）、扫描延时（Mark Delay）、曲线延时（Curve/Polygon Delay）**。其本质是**激光器响应时间与振镜响应时间不一致**。
来源：[知乎《各种延时详解》](https://zhuanlan.zhihu.com/p/1971228156716360365)、[百度文库《振镜延时的调节与现象》](https://wenku.baidu.com/view/391c752abdd5b9f3f90f76c66137ee06eff94e61.html)

**主流打标软件（LightBurn）中的实际参数名**（均为**微秒**级）：

| 分组 | 参数 | 作用 |
|---|---|---|
| Jump Settings | Jump Speed | 跳转速度。每次跳转都会引起振镜抖动，速度越高、距离越长抖动越大 |
| | **Min Jump Delay** / **Max Jump Delay** | 跳转延时上下限 |
| | Jump Distance Limit | 超过该距离的跳转使用 Max Jump Delay，低于则取上下限之间的值 |
| Delay Defaults | **Laser On TC** | 开光延时 |
| | **Laser Off TC** | 关光延时。过大导致末端过度烧蚀，过小导致缺口 |
| | **End TC** | 路径终点延时 |
| | **Polygon TC** | 拐角处振镜停顿时间。过长过度烧蚀，过短则**拐角变圆或被切掉** |

**调参经验（LightBurn 原文）**：若标记起始处线条抖动（wobbly lines），需**增大延时和/或降低跳转速度**。
来源：[LightBurn 振镜（Galvo）基础设置文档](https://docs.lightburnsoftware.com/latest/Galvo/Setup.html)

**控制卡侧的延时分辨率（SCANLAB 官方数字）**：

| 控制卡 | 激光延时分辨率 | Sky writing |
|---|---|---|
| RTC4 | **1 µs** | 不支持 |
| RTC5 | **1/2 µs** | 支持 |
| RTC6 | **1/64 µs** | 支持 |

来源：[SCANLAB RTC 控制卡对比 PDF](https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf)

**量化延迟预算示例（RAYLASE SP-ICE 3 + 数字振镜）**：

```
插值时间 T_Int = 20 µs（推荐值）
  TD_TX = T_K + T_C + T_Int = 13 + 20 + 20 = 53 µs   (前向)
  TD_RX = 36 µs                                       (反馈)
  Positioning Delay = TD_TX + Tracking Error(Lag)
  → LaserOnDelay / LaserOffDelay 必须按 Positioning Delay 设置
```
来源：[RAYLASE SP-ICE 3 §7.1.9](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/7a6d305c-a5d1-4dfb-a1d2-3afc1768b87f.htm)（详见 3.4 节）

### 9.5b Sky Writing（飞行打标 / 提前加减速）

**核心思想**（RAYLASE SP-ICE 3 手册 §9.5.1 原文）：
> *"If we extend a MARK vector linearly by a suitable amount **before its original start point and after its original end point**, the scanner can use these extensions to **accelerate and decelerate while still outside the limits of the original vector**. The scanner then moves between the original start point and the original end point of each vector at **constant velocity**."*

即：把每条 MARK 矢量在**首尾各线性延长一段**，让振镜在**延长段内完成加减速**，从而在原矢量区间内以**恒速**运动 —— 这样激光能量密度才均匀，且**拐角不会被圆化**。

**关键参数（原文）**：

| 参数 | 含义 |
|---|---|
| `SKYWRITING_MODE` | 关闭时不生成任何 Sky Writing 矢量 |
| `SKYWRITING_MIN_COH` | 相邻 MARK 矢量转角**小于**此值时抑制延长与跳转矢量 |
| `SKYWRITING_MERGED_EXTENSIONS_MAX_COH` | 启用"合并延长"（0…π） |
| `SKYWRITING_EXTENSION_TIME` | **延长距离 = 延长时长 × 标刻速度（MarkSpeed）** |
| `SKYWRITING_ACCELERATION_DELAY` | 作用于"跳转到延长起点之后、加速之前" |
| `SKYWRITING_DECELERATION_DELAY` | 作用于"MARK 矢量末端减速之后" |
| `SKYWRITING_LASERON_DELAY` / `SKYWRITING_LASEROFF_DELAY` | Sky Writing 专用的开/关光延时，**取代**普通 `LaserOnDelay` / `LaserOffDelay` |

**与常规延时的交互**：启用 Sky Writing 后，**常规 `MARK_DELAY` 被忽略**，改由 `SKYWRITING_DECELERATION_DELAY` 生效；**常规 `JUMP_DELAY` 被忽略**，改由 `SKYWRITING_ACCELERATION_DELAY` 生效。若延长距离足以让振镜完全稳定，**延时可以降到 0**；若在可用延长距离内无法充分稳定，则需增大延时。

**多矢量情形**：连续多条 MARK 矢量时，首尾都延长后可能需要插入额外的 JUMP 矢量——**SP-ICE 3 的算法会在需要时自动插入**。

来源：[RAYLASE SP-ICE 3 User's Manual §9.5.1 Sky Writing](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/4CF38177-3E6A-4E48-98D8-F5C30FBDAE14.htm)

### 9.5c 动态延时（Variable Poly/Jump Delay）

主流控制卡不把拐角延时做成全局限定值，而是**随转角动态变化**：

- **Variable Poly Delay**：`polydelay` 不再静态作用于多边形内每个点，而是**按两条线的夹角动态设定**——**直线（无夹角）不延时，180° 夹角则施加完整延时**。
  来源：[HALaser E1803D Manual](https://halaser.eu/manuals/e1803_manual.pdf)（`E180X_COMMAND_FLAG_SCANNER_VAR_POLYDELAY`，需固件 v2+）
- RAYLASE SP-ICE 3 手册同样包含 **§9.5.4 Variable Poly Delay** 与 **§9.5.5 Variable Jump Delay**。
  来源：[RAYLASE SP-ICE 3 Manual](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/4CF38177-3E6A-4E48-98D8-F5C30FBDAE14.htm)

> **结论**：固定延时要么牺牲拐角质量、要么牺牲直边效率，因此**动态延时是当代控制卡的标准做法**。

### 9.5d 四类延时的缺陷现象（学术论文）

IJMMM 2016 论文将扫描延时归纳为四类，并给出各自的缺陷现象：

| 延时 | 作用 | 过小 | 过大 |
|---|---|---|---|
| **Laser On/Off Delay** 开/关光延时 | 保持激光功率密度均匀 | 起点缺笔 / 终点未闭合 | 起点能量堆积、**终点爆点** |
| **Jump Delay** 跳转延时 | 跳转结束后等待振镜稳定 | **路径紊乱**、缺料 | 效率下降、材料过度堆积 |
| **Mark Delay** 扫描延时 | 仅在 Mark 后接 Jump 时生效 | 未到位即跳转 → **轮廓误差** | 激光空烧、效率低 |
| **Corner/Polygon Delay** 拐角延时 | 补偿拐角处两段矢量的加减速 | **轮廓误差** | 拐角处材料过度堆积 |

来源：[IJMMM Vol.6 (2016) 论文](https://www.ijmmm.org/vol6/402-EM0028.pdf)

**各厂商延时参数单位与范围（一手）**：

| 厂商/产品 | 参数 | 单位与范围 |
|---|---|---|
| HALaser E1803D | jumpdelay / markdelay / polydelay | µs，**最小分辨率 0.5 µs** |
| HALaser E1803D | ondelay（开光延时） | µs，**可为负值**（范围 −10000000…10000000） |
| HALaser E1803D | offdelay（关光延时） | µs，**必须为正值**（范围 0…10000000） |

来源：[HALaser E1803D Manual](https://halaser.eu/manuals/e1803_manual.pdf)

> **说明**：中文资料常提到"曲线延时（Poly Delay）在 Raylase 系统中设置非零值时需从 50 µs 起"、"Scanlab 系统中 MarkD 以 10 µs 为增量单位"等说法——**本次检索无法取得这些文档的正文核对（百度文库返回安全验证页），标记为二手、待核实**。

### 9.6 接地、屏蔽与差分

- 每路差分必须走**双绞线对**，屏蔽层接 GND。
- RAYLASE SS-III **无电气隔离**；若控制卡与振镜存在地电位差，会直接引入共模噪声。**RTC4 同样无隔离**，RTC5/RTC6（SL2-100）才加入隔离。
  来源：[RAYLASE SS-III](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)、[SCANLAB RTC PDF](https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf)
- 短线可用 3.3 V 差分直连；**可靠场合应加隔离 RS-485 驱动**。
  来源：[Tuet/XY2_100](https://github.com/Tuet/XY2_100)

### 9.7 引脚互不兼容（跨协议与跨厂商）

按危险程度排序：

1. 🚨 **XY2-100 ↔ XY3-100：同一 DB25 上 CLK 与 SYNC 互换**（最危险，见 [2.3 节 (0)](#23-引脚定义四种厂商--官方标准对照)）
   - XY2-100：`1/14 = CLK`、`2/15 = SYNC`（RAYLASE / SCANLAB / Newson / Ray-Motion 四家一手一致）
   - XY3-100：`1/14 = SYNC (A)`、`2/15 = CLK (B)`（**LasIA 官方标准**）
   - 尽管 XY3-100 官方声称 "Same pinout as XY2-100(E)"，**该说法只在数据线上成立**
   - → **做双协议兼容硬件时，CLK/SYNC 必须设计为可交换**
2. ⚠️ **帧起始边沿也不同**：XY2-100 由 SYNC **上升沿**标记帧开始；XY3-100 由 SYNC **下降沿**标记帧开始
3. ⚠️ **X/Y 通道可能互换**（RAYLASE 的 X 是先被激光打到的轴/小镜，部分厂商定义相反）
4. ⚠️ **Z 轴与 STATUS/BACK 脚位置不同**（RAYLASE Z 在 5/18、反馈在 6/19、7/20、8/21；SCANLAB RTC4 的 CHAN3 在 5/18、STATUS 在 6/19、STATUS1 在 8/21；XY3-100 的 BACK 在 6/19、U 在 7/20、W 在 8/21）
5. ⚠️ **电源脚不同**：Ray-Motion 为 ±15 V（9/10/22、12/13/25）；SCANLAB intelliSCAN 为 **+30 V**（9/10/22），12/13/25 为 GND；XY3-100 为 V+（9/10/22）与 V−（12/13/25）
   → **换品牌/换协议必须重新核对引脚，否则可能烧毁设备。**

> ✅ **一处有利的一致性**：**3 轴（Z）在 pin 5/18** 这一点上，RAYLASE SS-III、SCANLAB RTC4（CHAN3）与 LasIA XY3-100（Z, E 对）**三家完全一致**。

### 9.8 Enhanced 模式的兼容性陷阱

- 18 bit 与命令帧**依靠校验奇偶性区分**，导致**无法检出命令帧的传输错误**（sigrok 明确警告）。
- 命令帧耗时 10 µs，期间位置靠插值补齐，会产生额外的跟踪延时。
- 部分振镜（如 RAYLASE SS-III）**不支持** `SetPositionScale (0x12)`。

### 9.9 其他

- `SetEchoMode (0x21)` 可把参数字节回显到反馈通道（高 8 位 = 参数，低 8 位 = 参数取反），**是排查接口传输错误的好工具**。
  来源：[RAYLASE SS-III](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)
- 使用逻辑分析仪排查时可直接用现成解码器：[sigrok `xy2-100` PD](https://sigrok.org/wiki/Protocol_decoder:Xy2-100)、[Saleae 分析仪](https://github.com/danmcb/Saleae-XY2-100)。

---

## 10. 实用数字：带宽、角度、分辨率、应用

### 10.1 扫描角度与分辨率（SCANLAB 官方）

| 型号 | 典型扫描角（光学） | 定位分辨率 | 控制接口 |
|---|---|---|---|
| **excelliSCAN 20** | ±0.35 rad | **20 bit**（0.7 µrad @ ±0.36 rad） | 数字 **SL2-100** |
| **intelliSCAN 14** | ±0.35 rad | **18 bit**（2.8 µrad @ ±0.36 rad） | 数字 **SL2-100**、**XY2-100 Enhanced** |
| **SCANcube 10** | — | — | 数字 SL2-100、**XY2-100 standard**、模拟 **±4.8 V** |

来源：[SCANLAB excelliSCAN 20](https://www.scanlab.de/en/products/scan-systems/excelliscan/excelliscan-20)、[intelliSCAN 14](https://www.scanlab.de/en/products/scan-systems/intelliscan/standard-series/intelliscan-14)、[SCANcube 10](https://www.scanlab.de/en/products/scan-systems/scancube/standard-series/scancube-10)

### 10.2 分辨率换算（已验证）

| XY2-100 模式 | 位深 | 步数 | 分辨率 @ ±0.36 rad 全角程 | 精度是否够用 |
|---|---|---|---|---|
| 标准 | 16 bit | 65 536 | **11 µrad** | 天花板 |
| Enhanced | 18 bit | 262 144 | **2.8 µrad** | 提升 4 倍 |
| SL2-100 | 20 bit | 1 048 576 | **0.7 µrad** | 提升 16 倍 |

**通式**：
```
每 LSB 光学角 = 2 × θ_optical_max / 2^N
每 LSB 机械角 = 2 × θ_mech_max / 2^N      （机械角 = 光学角 / 2）
```
SCANLAB 原文：
> *"20 bit: based on the full angle range (e.g. positioning resolution 0.7 µrad for angle range ±0.36 rad), resolutions better than 16 bit (11 µrad) only together with SL2-100 interface"* —— excelliSCAN 20
> *"18 bit: based on the full angle range (e.g. positioning resolution 2.8 µrad for angle range ±0.36 rad), resolutions better than 16 bit (11 µrad) only together with SL2-100 interface"* —— intelliSCAN 14

> **关键工程结论**：**16 bit（XY2-100 基型）= 11 µrad 是精度天花板**。想要更高分辨率，必须换用 **18 bit（XY2-100 Enhanced）或 20 bit（SL2-100）**。这就是 Enhanced 与 SL2-100 存在的根本原因。

### 10.2b 真实振镜厂商的完整规格（一手数据手册）

#### RAYLASE SUPERSCAN III-10（10 mm 口径数字振镜）

| 项目 | 数值 |
|---|---|
| **接口** | **XY2-100-Enhanced Protocol / XY2-100-Protocol** |
| 典型偏转角（**光学**） | **±0.393 rad**（= ±22.5°） |
| **16 bit 分辨率（机械 / 光学）** | **6 / 12 µrad** |
| **18 bit 分辨率（机械 / 光学）** | **1.5 / 3 µrad** |
| 重复性（RMS） | **< 2 µrad** |
| 位置噪声（RMS） | < 8 µrad |
| 最大零偏漂移 | < 10 µrad/K |
| **长期漂移** | **< 60 µrad** |
| 加速度时间（LN / RA 调谐） | 0.21 ms / 0.19 ms |
| 书写速度 | 850 / 1000 cps（f = 163 mm，视场 120 × 120 mm） |
| 定位速度 | 12（LN）/ 6（RA）/ 32（ST）m/s |
| **跟踪误差时间** | **0.14 ms（LN）/ 0.11 ms（RA）** |
| 阶跃响应（ST 调谐） | 1% FS: **0.32 ms**；10% FS: **0.75 ms** |
| 调谐 | LN（低噪声，默认）/ RA（短加速时间）/ ST（最短跳转时间） |
| 电源 | ±15 V，3 A RMS，最大 10 A |

来源：RAYLASE 官方 datasheet（April 2014 v1.1）：http://alaser.com.tw/db/upload/webdata3/champway_201411262340499291.pdf

**分辨率自洽性验证**：光学量程 ±0.393 rad → 总行程 0.786 rad；16 bit → 0.786/65536 = **11.99 µrad ≈ 12 µrad** ✅；18 bit → 0.786/262144 = **3.00 µrad ≈ 3 µrad** ✅；机械角恰为光学角一半 → 6 µrad / 1.5 µrad ✅。**与手册完全吻合。**

#### Sino-Galvo SG7220-V1 / SG7220-Plus（10 mm 口径，**XY2-100 接口**）

| 项目 | SG7220-V1 | SG7220-Plus |
|---|---|---|
| **接口协议** | **XY2-100** | **XY2-100** |
| **机械扫描角** | **±11°**（可定制） | **±11°** |
| 标记速度 (1) | **10 000 mm/s** | **12 000 mm/s** |
| 定位速度 (1) | 18 000 mm/s | 18 000 mm/s |
| 书写速度 (2) | 575 cps | 600 cps |
| **阶跃响应（1% FS）** | **275 µs** | **270 µs** |
| **阶跃响应（10% FS）** | **750 µs** | **710 µs** |
| **跟踪误差时间** | **≤ 138 µs** | **≤ 138 µs** |
| **重复定位精度** | **< 8 µrad** | **< 8 µrad** |
| 线性度 | 99.9 % | 99.9 % |
| **8 小时长期漂移** | **< 0.15 mrad** | **< 0.15 mrad** |
| 零点漂移 | < 15 µrad/°C | < 15 µrad/°C |
| 比例漂移 | < 40 ppm/°C | < 40 ppm/°C |
| 波长 | 10600 / 1064 / 355 nm | 10600 / 1064 / 355 nm |
| 输入电压 | ±15 VDC / 3 A | ±15 VDC / 3 A |
| 通光孔径 | 10 mm | 10 mm |

脚注原文：(1) 使用 **f = 160 mm F-Theta 镜头**，标刻 3.5 mm 高单线字符；(2) f = 160 mm，每秒 1 个字符标刻 1 mm 高单线字符。数据预热 30 min 后测得。

来源：[Sino-Galvo SG7220-V1](https://www.sino-galvo.com/Products_detail/59.html)、[SG7220-Plus](https://www.sino-galvo.com/Products_detail/13.html)

### 10.2c ⚠️ 更正：**"16 bit ≈ 0.15 mrad 分辨率"是误传**

任务背景中提到的"16-bit = 65536 steps / ~0.15 mrad 分辨率"这一说法，**无法得到任何一手来源支持，且在数值上不成立**：

1. **0.15 mrad 的真实出处是"长期漂移"，不是分辨率**：
   > Sino-Galvo SG7220-V1/Plus：**Long-term Drift Over 8 Hours：< 0.15 mRad**
2. **实际 16 bit 分辨率比 0.15 mrad 精细约 12–25 倍**：
   - RAYLASE III-10：**12 µrad 光学 / 6 µrad 机械**（= 0.012 mrad 光学）
   - Sino-Galvo SG7220（±11° 机械 = ±0.192 rad 机械 = ±0.384 rad 光学）：0.768 / 65536 ≈ **11.7 µrad 光学 / 5.9 µrad 机械**
3. **反证**：若 16 bit 对应 0.15 mrad/LSB，则需光学行程 65536 × 0.15 mrad = **9.83 rad（≈563°）**，任何真实振镜都达不到。**该说法在数值上不可能成立。**

> **正确表述**：现代 10 mm 口径 XY2-100 数字振镜的 16 bit 分辨率约为 **6 µrad 机械 / 12 µrad 光学**；18 bit 模式约为 **1.5 µrad 机械 / 3 µrad 光学**。**0.15 mrad 是长期漂移指标。**

### 10.3 振镜带宽 —— 厂商不公开带宽指标

**⚠️ 重要发现：本次调研未能找到任何振镜厂商以"带宽（Hz/kHz）"为单位给出的公开指标。** 厂商一律给出**时域指标**：

| 时域指标 | 典型值（10 mm 口径数字振镜） | 来源 |
|---|---|---|
| 跟踪误差时间 | **110–140 µs** | RAYLASE III-10、Sino-Galvo SG7220 |
| 阶跃响应（1% FS） | **270–320 µs** | Sino-Galvo、RAYLASE III-10（ST） |
| 阶跃响应（10% FS） | **710–750 µs** | Sino-Galvo、RAYLASE III-10（ST） |
| 加速度时间 | 0.19–0.21 ms | RAYLASE III-10 |

**换算为等效带宽**（一阶近似，**仅作量级参考，不是厂商指标**）：

| 依据 | 换算 | 等效带宽 |
|---|---|---|
| 跟踪误差时间 140 µs | 1/(2π × 140 µs) | ≈ **1.1 kHz** |
| 小信号阶跃 275 µs（到 1% FS） | 1/(2π × 275 µs) | ≈ **0.6 kHz** |
| 大信号阶跃 750 µs（到 10% FS） | 1/(2π × 750 µs) | ≈ **0.2 kHz** |

> ⚠️ **与常见假设不符**：任务背景中假设的"**1–10 kHz 小信号带宽**"与上述换算**不一致**。实测/手册数据指向**亚 kHz 到约 1 kHz** 的小信号整定带宽；**1–10 kHz 更接近小角度谐振频率量级，而非"整定到指定精度的带宽"**。
>
> **【存疑】** 上述换算是本报告的一阶近似，**不是厂商给出的带宽指标**。若需要真实带宽（尤其小信号 −3 dB 带宽），**必须向厂商索取频响曲线 —— 本次检索未找到公开数据。**

**接口速率 vs 机械带宽的余量**：XY2-100 的 100 kHz 更新率比振镜机械带宽（~1 kHz）高约 **100 倍**——因此接口通常**远有余量**，实际系统更新率由振镜带宽与工艺决定。这也正是振镜内部要做插值的原因（见 9.5 节）。

### 10.3b 精度受限因素（以 f = 160 mm 镜头为例）

由 `工作面每 LSB 尺寸 = f × 每 LSB 角`：
- SG7220（±11° 机械，光学 ±0.384 rad）配 f = 160 mm → 每 LSB 光学 11.7 µrad × 160 mm = **1.87 µm**

| 误差源 | 数值 | 在 f = 160 mm 工作面上的等效值 |
|---|---|---|
| **量化误差（16 bit）** | 11.7 µrad | **~1.9 µm** |
| 量化误差（18 bit） | 2.9 µrad | ~0.47 µm |
| 重复定位精度 | < 8 µrad | ~1.3 µm |
| 零点漂移 | 15 µrad/°C | **~2.4 µm/°C** |
| 长期漂移（8 h） | < 0.15 mrad | **~24 µm/8h** |
| F-Theta 线性度 | 99.9 % | 0.1% 非线性随视场放大 |
| 跟踪误差（动态） | ≤ 138 µs | 拐角变圆、圆弧失真 |

> **结论**：若应用需要**亚 µm 精度，16 bit 不够**；且**热漂移与长期漂移往往比量化误差更大**，是长时加工的主要误差源。

### 10.3c 标刻速度与 F-Theta 焦距的关系

厂商指标均在**指定 F-Theta 焦距**下测得（RAYLASE：f = 163 mm / 视场 120×120 mm；Sino-Galvo：f = 160 mm）。

- 小角近似下工作面线速度 `v = f · ω`（ω 为角速度）。
- 换用更长焦距镜头时，同样角速度得到更高线速度，但**同样的 16 bit 量化会变成更粗的工作面分辨率**。
- **因此比较不同厂商的速度指标时，必须核对焦距与测试条件。**

### 10.4 典型应用

| 应用 | 说明 |
|---|---|
| **激光打标 / 雕刻** | 最主要应用，光纤/CO₂/紫外打标机 |
| **激光切割 / 焊接 / 微加工** | 精密加工 |
| **3D 打印（SLM / 金属增材）** | 需要 Z 轴（三轴 XY3-100/3D）；SCANLAB 有 micro-machining 专区 |
| **激光雷达 LiDAR** | 扫描式 LiDAR 使用振镜或转镜 |
| **医疗成像** | OCT、共聚焦显微镜、激光手术 |
| **机器视觉 / 结构光** | 需要 PSO（位置同步输出）配合相机 |

来源：[sigrok](https://sigrok.org/wiki/Protocol_decoder:Xy2-100)（"XY2-100(E) protocol used in laser applications"）、[SCANLAB 微加工页面](https://www.scanlab.de/en/products/micromachining)、[RAYLASE SS-III](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)

---

## 11. 数据冲突与未确认项

本节集中列出**来源互相冲突**或**未找到公开数据**的项目，供后续核实。

### 11.1 来源冲突

| 项目 | 说法 A | 说法 B | 处理建议 |
|---|---|---|---|
| **时钟频率上限** | XY2-100 基型 **≤ 2 MHz**（sigrok） | RAYLASE XY2-100-E **最大 10 MHz、推荐 4 MHz** | 二者对应不同变体；以**所配振镜手册**为准 |
| **校验位范围** | 含控制位（Saleae 解码器、Tuet、hyperchao0） | 仅 16 数据位（georgemihaila、NOBIC-NTU/OPAL） | **采用含控制位**（有接收端实现支撑） |
| **状态字定义** | RAYLASE：**8 bit 重复两次**，高有效=正常，含 axis at work / 温度 / X、Y、Z 跟踪窗口 | 中文资料：**20 bit BACK 字**，含 PSO / Pulse / X、Y、Z ready / X、Y、Z error | 不同厂商/代次；以实际手册为准 |
| **反馈帧格式** | RAYLASE：**3 种**（向下兼容 16 bit / 标准 16 bit / 18 bit），无法自区分 | Newson：**单根 STATUS 电平线**，非同步 | 两种形态并存，见第 6 节 |
| **电源引脚** | Ray-Motion：±15 V（9/10/22、12/13/25） | SCANLAB：+30 V（9/10/22），12/13/25 = GND | **换品牌必须重新核对**，接错可能损坏设备 |
| **X/Y 轴物理定义** | RAYLASE：X = 先被激光打到的轴（小镜） | 部分厂商：先被激光打到的轴定义为 Y | 会导致通道引脚互换 |
| **SL2-100 帧细节** | ~~中文博客：26 bit（6 位模式 + 20 位数据）~~ **已证伪** | ✅ **已由 SCANLAB RTC6 手册附录 F（p.1214）官方解决**：**1 块 = 192 帧 + preamble**；**1 帧 = 2 子帧**，每子帧 **20 bit 载荷 + 12 bit 附加信息**；帧周期 **10 µs** | **已解决**。"26 bit"是把控制器内部运算分辨率误读为帧长 |
| **XY2-100 与 XY3-100 的引脚兼容性** | 官方称 "Same pinout as XY2-100(E), no hardware changes needed" | 实测/逐条比对：**CLK 与 SYNC 在 DB25 上互换**（XY2-100: 1/14=CLK；XY3-100: 1/14=SYNC） | ⚠️ **官方声明与事实不符（仅数据线相同）**；官方还称 XY2-100 帧起点是**上升沿**、XY3-100 是**下降沿** |
| **XY2-100 的原始发明方** | 任务背景称 SCANLAB / RAYLASE | 三方说法并存，**未找到决定性证据** | 可确定的只是：**标准文本由 LasIA 发布（LIA202001）**，SCANLAB 与 RAYLASE 是最大实现方。**不要断言"SCANLAB 发明 XY2-100"** |
| **模拟接口标度因子** | 此前记为"未找到公开数据" | ✅ **已找到多组一手值**：Thorlabs 0.5/0.8/1.0 V 每**机械度**、Sino-Galvo 0.33 V/°、Scanner Optics 0.5–2 V/机械度 | **"±10 V = ±20° 光学"错了 2 倍**；0.5 V/mech° 档下 ±10 V = ±40° 光学 |
| **模拟接口分辨率** | 流传"等效 12 bit" | 同一 Thorlabs 板：**线性电源 15 µrad（≈15.5 bit）vs 开关电源 70 µrad（≈13.3 bit）** | **"12 bit"无一手证据，不建议引用**；瓶颈是电源噪声而非 DAC 位数 |
| **XY2-200 的时钟** | sigrok：**≤ 4 MHz** | HALaser 手册：**帧 5 µs / 200 kHz** → 20 bit/5 µs = **4 MHz** | 二者**一致**（4 MHz ↔ 5 µs）。可放心引用 |
| **XY2-100-E 时钟上限** | sigrok/HALaser：2 MHz（基型） | RAYLASE SS-III：**10 MHz 上限 / 4 MHz 推荐** | 前者是基型规格，后者是 Enhanced 实测上限；见 3.1 |
| **反馈帧是否带校验** | cnblogs：BACK 字末位为 **Pe**（有校验） | RAYLASE：三种反馈帧均为"帧头+数据"填满 20 位，**无校验** | 不同厂商实现不同；见第 6 节 |

### 11.2 未找到公开数据

**协议层**：
- 时钟**占空比**的官方规格（实践普遍用 50 %）。
- 时钟的**抖动（jitter）、上升/下降时间**规格。
- **最小**帧率 / 更新率的官方下限。
- 控制字 C2 C1 C0 中除 `001`（位置）、`111`（命令）以外的取值定义。
- **SL2-100 的 6 bit 模式码表**（官方未公开，仅逆向给出"弧线/连续直线/点"三种功能）。
- **SL2-100 的标称位速率**（官方未公开；本报告由官方结构推算 6.4 Mbit/s）。
- **SL2-100 是否真为差分曼彻斯特编码**（官方仅给出错误位分类，未明说编码方式）。
- 中文资料中 `BACK` 字 BIT11 / BIT10 以及保留位的确切含义。
- Raylase 反馈帧头精确取值（受 PDF 图形文本提取限制，建议查原始 PDF 图）。

**电气层**：
- 差分输出的**具体摆幅、共模电压范围、接收端阈值**（厂商只推荐器件型号，未给电气参数表）。
- XY2-100 是否需终端电阻及阻值（**官方对 XY2-100 无任何规定**；两份真实开源设计均**不加**端接。注意 **XY3-100 官方则明确要求接收端加终端电阻**）。
- 电缆的**线长上限、特性阻抗、线规**具体指标。
- 单端 TTL 可用的**具体电缆长度上限**（只有定性的 "for short cables"）。
- 任何**误码率 / 眼图**实测数据。

**系统层**：
- **振镜厂商均不公开"带宽（Hz/kHz）"指标**——只给时域指标（跟踪误差时间、阶跃响应）。真实 −3 dB 带宽需向厂商索取频响曲线。
- 数字振镜内部 **DAC 位宽与内部电压量程**。
- 各厂商振镜内部**是否也有插值、默认值多少**（仅 RAYLASE 有公开文档）。
- F-Theta 镜头的**畸变曲线**。
- 振镜的**转动惯量 / 摩擦力矩**。
- **SCANLAB 延时参数的默认值表**（手册需客户门户登录）。
- **时钟停止后振镜的机械行为**——只能确认"输出级被关闭"，"保持最后位置"无文档支持。
- **"SL2-100-3D" 这一命名**未见官方使用。
- **SCANLAB 三轴版 XY2-100-Enhanced 的完整引脚表**（仅知 CHAN3 在 5/18）。

**已解决（原列于此，现已由一手文档确认）**：
- ✅ ~~SL2-100 帧结构~~ → SCANLAB RTC6 手册附录 F 官方定义（192 帧/块、2 子帧/帧、20+12 bit、10 µs）
- ✅ ~~XY3-100 帧长 24 vs 32 bit 的冲突~~ → 官方：两种并存，由首 bit 指示
- ✅ ~~模拟接口标度因子~~ → Thorlabs 0.5/0.8/1.0 V 每机械度等一手数据
- ✅ ~~XY2-100 是否有正式标准~~ → **有：LasIA LIA202001**

### 11.3 对任务背景中若干预设的更正

| 任务背景中的表述 | 核查结果 |
|---|---|
| "resolution (16-bit = 65536 steps, **~0.15 mrad**)" | ⚠️ **0.15 mrad 是 Sino-Galvo 的"8 小时长期漂移"指标，不是分辨率**。实测 16 bit 分辨率约 **6 µrad 机械 / 12 µrad 光学**。若 16 bit = 0.15 mrad/LSB，需光学行程 9.83 rad（≈563°），**数值上不可能**。见 10.2c |
| "typical galvo bandwidth (**1–10 kHz small signal**)" | ⚠️ **厂商不公开带宽指标**。由手册的时域指标（跟踪误差 110–140 µs、阶跃 270–750 µs）一阶换算，小信号整定带宽约 **0.6–1.1 kHz**，**低于 1–10 kHz**。1–10 kHz 更接近小角度谐振频率量级。见 10.3 |
| "±5 V…±5 V → ±X degrees" | 数字 XY2-100 **帧内不传电压**；码值为归一化全量程比例。"±5 V" 属于**模拟**振镜接口的表述。见 5.3 |
| "3-bit status word for XY2-100 Enhanced" | ✔ **确有出处**：HALaser E1803D 官方手册定义返回帧前 3 bit 为**头识别码**（`011` = 2D 头、`001` = 3D 头）。另有两个易混概念：前向 3 位控制字 C2C1C0，以及状态字中的 X/Y/Z ready 与 error 三重组。见 6.3 |
| "时钟 nominal 2 MHz" | ✔ 正确（经典值）。但 Enhanced 变体上限更高：RAYLASE SS-III **最大 10 MHz / 推荐 4 MHz**；XY2-200 = 4 MHz。见 3.1 |
| "20 clock cycles per frame" | ✔ 正确 |
| "XY2-100 Enhanced 的 3-bit status" / "18-bit" | ✔ 18 bit 正确（首位=1 + D17..D0 + 奇校验） |
| "originally from SCANLAB (Germany) / Raylase" | ⚠️ **部分正确**。标准文本由 **LasIA** 发布（**LIA202001**），LasIA 是行业协会；SCANLAB 与 RAYLASE 是最大的两个实现方与文档提供方。**"XY2-100 由 SCANLAB 发明"这一说法未找到决定性证据**——公开资料中存在多种说法。见 1.1 |
| "XY3-100 是中国厂商定义的扩展" | ❌ **错误**。XY3-100 是 **LasIA 的正式标准**（LIA202002 v1.0 / LIA202307 v1.1），官方定位为 **XY2-100 的后继标准**。星移控制科技等只是实现方。见 7.3(b) |
| "XY3-100 帧长 24 或 32 bit（二选一，推荐 32）" | ⚠️ **两种共存**，由首 bit 动态指示（`0`=24 bit，`1`=32 bit），并非"推荐其一"。见 7.3(b) |
| "XY2-100 与 XY3-100 引脚兼容、无需硬件改动" | ❌ **官方说法有误**。**CLK 与 SYNC 在同一 DB25 上互换**（XY2-100: 1/14=CLK；XY3-100: 1/14=SYNC），帧起始边沿也相反（上升沿 vs 下降沿）。见 2.3(0) |
| 模拟接口"±10 V = ±20° 光学" | ⚠️ **多数实现下错 2 倍**。Thorlabs 0.5 V/机械度 档下 ±10 V = ±20° **机械** = **±40° 光学**。见 7.5 |
| 模拟接口"等效 12 bit" | ❌ **无一手证据**。同一 Thorlabs 板线性电源 15 µrad / 开关电源 70 µrad —— **瓶颈是电源噪声，不是 DAC 位数**。见 7.5 |
| "SL2-100 帧长 26 bit" | ❌ **已证伪**。官方：1 帧 = 2 子帧 × (20+12) bit = **64 bit**，10 µs；1 块 = **192 帧** + preamble。见 7.2(b) |

---

## 12. 参考链接

### 12.0 ⭐ 官方标准规范原文（最高优先级，一手）

| URL | 说明 |
|---|---|
| https://web.archive.org/web/20231206141529id_/https://lasia.org/LIA202001/xy2_100_specification.pdf | **LasIA LIA202001《XY2-100 Laser Scanner Protocol Format Specification》** —— **XY2-100 的正式标准原文**。经 MD5 校验，即网上流传的 aaronvose/Quantronix 版（`604A8F106749B320657ED90134266909`） |
| https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf | **LasIA LIA202307《XY3-100 Protocol Format Specification》v1.1（2023-07）** —— XY3-100 官方标准；含官方 XY2-100 vs XY3-100 对照表、DB25/DB15/IDC 引脚表、24/32 bit 帧结构、校验计数器算法、RS485 回传协议 |
| https://web.archive.org/web/20210122224854id_/https://lasia.org/LIA202002/xy3_100_specification.pdf | LasIA LIA202002《XY3-100 Protocol Format Specification》v1.0（2020-09） |
| https://web.archive.org/web/20231206133135id_/https://lasia.org/LIA202307/xy3_100.h | **XY3-100 官方 C 头文件** —— 命令码与结构体定义 |
| https://raw.githubusercontent.com/labspiral/sirius3/main/doc/SCANLAB/RTC6_Manual.en.pdf | **SCANLAB RTC6 Manual Doc. Rev. 1.1.4 en-US（官方 PDF 镜像，24.8 MB）** —— **附录 F 第 1214 页给出 SL2-100 官方定义**（192 帧/块、preamble、2 子帧/帧、20+12 bit、10 µs） |
| https://raw.githubusercontent.com/labspiral/sirius3/main/doc/SCANLAB/RTC5_Manual.en.pdf | SCANLAB RTC5 官方手册 PDF 镜像 |
| https://raw.githubusercontent.com/labspiral/sirius3/main/doc/SCANLAB/RTC4_1_4_english.pdf | SCANLAB RTC4 官方手册 PDF 镜像（含 §6.3 官方 XY2-100 引脚定义） |
| https://sourceforge.net/p/lasia/blog/2023/07/xy3-100-digital-scanner-interface-version-11/ | LasIA 官方博客：XY3-100 v1.1 发布公告 |
| https://lasia.org | LasIA（Laser Industry Association）官网 —— ⚠️ **现返回 401**，标准文档需走 Wayback Machine |

> 💡 **获取提示**：`lasia.org` 已不可直接下载（401），SourceForge 亦返回 403。Wayback Machine 的 **`id_` 直链**（`/web/<时间戳>id_/<原始URL>`）可绕过并取得**未经改写的原始 PDF**——这是本次调研的关键突破点。

### 12.0b 模拟接口（一手）

| URL | 说明 |
|---|---|
| https://thorlabs-prep4cn-store.thorlabsazure.cn/api/thorlabs-products/support-documents/GVS011/20381-D02.pdf | **Thorlabs 模拟振镜驱动板手册** —— 标度因子 0.5/0.8/1.0 V 每**机械度**；**线性电源 15 µrad vs 开关电源 70 µrad**（分辨率瓶颈是电源噪声的决定性证据） |
| https://novanta.com/precision-manufacturing/wp-content/uploads/sites/28/2026/04/Analog_vs.Digital_Galvos.pdf | Novanta（Cambridge Technology）官方白皮书：模拟 vs 数字振镜架构对比 |
| https://www.scanneroptics.com/products/analog-galvo-driver/ | Scanner Optics 模拟驱动板完整规格（标度因子 0.5–2 V/机械度） |
| https://files.stankee.ru/docs/sino-galvo/SINO-GALVO%20SG7310%20-%20Galvanometer%20Scanner%20-%20Instruction%20Manual.pdf | Sino-Galvo SG7310 完整说明书（标度因子 0.33 V/度） |
| https://camtechfiles.s3-us-west-2.amazonaws.com/s3fs-public/Datasheet%20-%20Galvos-62xxH%20Series-DS00003_R1_v4_1_1.pdf | Cambridge Technology 62xxH 系列数据手册 |
| https://www.lasercontrolcard.com/news/introduction-to-laser-galvo-scanner-technical-parameters/ | 振镜技术参数入门（二手） |

### 12.1 一手规范 / 官方数据手册（PDF，可直接下载）

| URL | 说明 |
|---|---|
| https://www.aaronvose.net/Quantronix_Osprey/xy2_100_specification.pdf | **XY2-100 Laser Scanner Protocol Format Specification** —— 最简洁的权威帧格式定义（16 bit/18 bit 位表、校验、DB25） |
| http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf | **RAYLASE SS-III XY2-100-E Interface manual**（44 页）—— Enhanced 协议最完整的一手文档：引脚、10 MHz 时钟、命令集、状态字、插值 |
| https://dvd.ilphotonics.com/Ray-Motion%20-%20galvanometers%20-%201D-2D-3D%20scanners/Motion%20Control%20-%20Optomechanics/Interface%20XY2-100.pdf | **Ray-Motion（鞍山精准光学）XY2-100 technical datasheet** —— 引脚、时序图、tDS/tDH |
| https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/171/Documents_5F00_TD_5F00_XY2_2D00_100_5F00_R0703.pdf | **Newson rhothor X7 XY2-100 Technical Datasheet** —— 引脚 + **控制字 001 = motor setpoint** + **STATUS 位语义** |
| https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf | **SCANLAB RTC Control Boards**（RTC4/5/6 对比）—— 接口、分辨率、隔离、延时分辨率、Sky writing |
| https://www.scanlab.de/sites/default/files/2020-09/pin-out-intelliSCAN.pdf | **SCANLAB intelliSCAN Standard Connector Positions and Pin-Outs** —— **官方 XY2-100-Enhanced 25-pin 引脚定义**（已验证 HTTP 200，79362 字节） |
| https://halaser.eu/manuals/e1803_manual.pdf | **HALaser Systems E1803D Scanner Controller Manual** —— **Appendix B 含 XY2-100 / XY2-200 / XY2-100E / XY2-200E 四模式官方对照表**（已验证 HTTP 200） |
| https://cdn.casmart.com.cn/file/20220117/3810e78a3b25488eb3abdc20d7d4d7dd.pdf | **SCANLAB XY2-100 Converter (SL2-100 => XY2-100) Dimensions and Pinout**（镜像，已验证可下载） |
| https://www.scribd.com/document/941573319/Xy2-100-Specification | XY2-100 Specification（Scribd）—— 标准/增强模式对照（16 bit 偶校验 vs 18 bit 奇校验） |

### 12.2 SCANLAB 官方页面与手册

| URL | 说明 |
|---|---|
| https://www.scanlab.de/en/downloads | SCANLAB 官方下载中心 |
| https://www.scanlab.de/en/products/control-electronics/rtc-control-boards | RTC 控制卡产品页（RTC4/5/6 差异） |
| https://www.easymanua.ls/scanlab/rtc6-pcie-board/manual?p=69 | **SCANLAB RTC6 PCIe Board Manual §4.5.2 XY2-100 Converter (Accessory)** —— 转换器功能定义 + **10 µs 传播延迟** + 补偿方法 |
| https://www.scanlab.de/sites/default/files/2020-08/14_RTC4_control%20boards.pdf | **SCANLAB RTC4 控制卡官方产品 PDF**（已验证 HTTP 200，3.4 MB）—— RTC4 完整手册含 **§6.3 Primary Scan Head Connector 的官方 XY2-100 25-pin 引脚定义** |
| https://www.scanlab.de/sites/default/files/2020-08/13_RTC5_control%20boards.pdf | SCANLAB RTC5 控制卡官方 PDF（已验证 HTTP 200，2.2 MB）—— SL2-100 较 RTC4 分辨率高 16 倍 |
| https://www.scanlab.de/sites/default/files/2020-08/12_RTC6_control%20boards.pdf ② | SCANLAB RTC6 控制卡官方 PDF（已验证 HTTP 200，2.3 MB） |
| https://www.scanlab.de/en/products/software/rtc-software/download | **SCANLAB RTC 软件/手册官方下载页**（RTC4/5/6 手册入口，已验证 HTTP 200） |
| https://www.scanlab.de/sites/default/files/2021-11/RTC6_EtherBox_en.pdf | SCANLAB RTC6 EtherBox 官方 PDF（工业机柜版） |
| https://www.manualslib.com/manual/3518902/Scanlab-Rtc6-Pcie-Board.html | RTC6 PCIe Board Installation and Operation Manual（第三方镜像，便于在线浏览） |
| https://github.com/co2e14/rtc_laser | GitHub：**用 Linux 控制 SCANLAB RTC6 Ethernet 板 / excelliSCAN**（开源，含 iSCANcfg 手册 PDF） |

> ② 注：RTC6 的 URL 中含空格，实际形式为 `.../12_RTC6%20control%20boards.pdf`。
| https://www.scanlab.de/en/products/scan-systems/excelliscan/excelliscan-20 | excelliSCAN 20 —— 20 bit / 0.7 µrad / ±0.35 rad / SL2-100 |
| https://www.scanlab.de/en/products/scan-systems/intelliscan/standard-series/intelliscan-14 | intelliSCAN 14 —— 18 bit / 2.8 µrad / **XY2-100 Enhanced** 接口 |
| https://www.scanlab.de/en/products/scan-systems/scancube/standard-series/scancube-10 | SCANcube 10 —— 同时提供 SL2-100 / XY2-100 / 模拟 ±4.8 V |
| https://www.scanlab.de/sites/default/files/2020-10/pin-out_SCANcube.pdf | SCANcube 引脚定义（含 POF 光纤转换器说明） |

### 12.2b RAYLASE 官方手册

| URL | 说明 |
|---|---|
| https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/d6107a36-ef4e-4e13-a21c-6cda62a65fd6.htm | **RAYLASE SP-ICE 3 User's Manual 首页/目录** |
| https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/7a6d305c-a5d1-4dfb-a1d2-3afc1768b87f.htm | **§7.1.9 Transfer Delay with Digital Scanners** —— TD_TX / TD_RX 量化公式与常量（13 µs、20 µs、36 µs） |
| https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/d6107a36-ef4e-4e13-a21c-6cda62a65fd6.htm | §7.1.1 Scan Head Format Definitions —— `XY2_100` = Legacy 16-bit protocol |
| https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/65db6d89-b141-46a3-a74c-0b0ec7df2df1.htm | **§4.1 XY2-100 Adapters** —— 订货号 08001 / 14009、连接方式与安全警告 |
| https://www.raylase.de/en/products/electronics-control-cards/sp-ice-3.html | RAYLASE SP-ICE 3 控制卡产品页 |
| https://www.raylase.de/_Resources/Persistent/b/a/6/6/ba66d25112e3d91511322aa417caae73c916557b/Datasheet_SP-ICE-3.pdf | SP-ICE 3 数据手册 PDF |
| http://alaser.com.tw/db/upload/webdata3/champway_201411262340499291.pdf | **RAYLASE SUPERSCAN III-10 官方数据手册**（2014-04 v1.1）—— ±0.393 rad 光学角、16 bit = 6/12 µrad、18 bit = 1.5/3 µrad、跟踪误差 0.14/0.11 ms、阶跃响应 0.32/0.75 ms（已验证可下载，903 KB） |

### 12.2c 振镜厂商产品规格（一手）

| URL | 说明 |
|---|---|
| https://www.sino-galvo.com/Products_detail/59.html | **Sino-Galvo SG7220-V1 规格页** —— **XY2-100 接口**、±11° 机械角、10000 mm/s、阶跃 275/750 µs、跟踪误差 ≤138 µs、重复精度 <8 µrad、长期漂移 <0.15 mrad（已验证 HTTP 200） |
| https://www.sino-galvo.com/Products_detail/13.html | **Sino-Galvo SG7220-Plus 规格页** —— 同上，标记速度 12000 mm/s、阶跃 270/710 µs |
| https://www.sino-galvo.com/ | Sino-Galvo 官网（国产振镜主要厂商之一） |
| https://www.scanlab.de/en/products/scan-systems | SCANLAB 全系列扫描系统（含各型号接口/分辨率对照） |
| https://www.scanlab.de/sites/default/files/2025-06/SCANLAB-SCANcube-Series-EN.pdf | SCANLAB SCANcube 系列数据手册 PDF |
| https://www.hansscanner.com/ | **大族思特（Han's Scanner）** —— 大族激光旗下振镜厂商（已验证 HTTP 200） |
| https://www.hanslaser.com/ | **大族激光（Han's Laser）**官网（已验证 HTTP 200） |
| https://www.bjjcz.cn/ | **北京金橙子科技股份有限公司（JCZ）**官网 —— 科创板 688291，2004 年创立，激光加工控制软件与系统（已验证 HTTP 200） |
| https://www.jcztech.com/ | 金橙子科技 JCZ 另一官方域名（已验证 HTTP 200） |
| http://www.raylase.com.cn/ | **瑞镭激光技术（深圳）有限公司** —— RAYLASE 中国分公司（2003 年进入中国，2010 年深圳建厂）（已验证 HTTP 200） |
| https://www.ray-motion.com/ | Ray-Motion 鞍山精准光学扫描技术有限公司（XY2-100 技术手册发布方） |

> ℹ️ **关于"苏州瑞雷"**：检索到的"瑞雷激光振镜说明书"实际内容是 **RAYLASE（德国瑞镭）** 的振镜资料 —— "瑞雷/瑞镭"很可能同为 **RAYLASE** 的中文译名，而非独立厂商。**该厂商与 XY2-100 协议无独立关联**，请注意区分。
>
> ℹ️ **关于"嘉泰激光"**：本次检索**未找到该公司公开的 XY2-100 帧级协议文档**；其产品资料属应用层。**未找到公开数据**。
>
> ⚠️ **关于中国厂商的帧级协议**：金橙子（JCZ）、大族、世纪桑尼等**只公开应用层 API 与产品规格，不公开振镜侧帧级协议**。这从侧面印证 XY2-100 的"事实标准"地位——厂商无需自研帧格式，直接采用既有标准。

### 12.3 协议解码器 / 工具

| URL | 说明 |
|---|---|
| https://sigrok.org/wiki/Protocol_decoder:Xy2-100 | **sigrok XY2-100(E)/XY2-200(E) 解码器文档** —— 变体说明、18 bit 校验歧义、反馈通道 3 变体、资源链接 |
| https://raw.githubusercontent.com/sigrokproject/libsigrokdecode/master/decoders/xy-100/pd.py | **sigrok 官方解码器 Python 源码** —— 帧类型判定（`001`/`111`/18 bit）与校验位算法（最权威的一手判定依据） |
| http://www.newson.be/doc.php?id=XY2-100 | Newson XY2-100 datasheet 官方取得页 |
| https://github.com/danmcb/Saleae-XY2-100 | **Saleae 逻辑分析仪 XY2-100 解码器（C++ 源码）** —— 含权威的校验位判定逻辑 |
| https://github.com/earlynerd/XY2-100_HLA | Saleae High Level Analyzer（Python）—— 校验位算法参照 |

### 12.4 开源实现（GitHub）

| URL | 说明 |
|---|---|
| https://github.com/Tuet/XY2_100 | **Teensy 3.2/LC 库（DMA）** —— 成熟实现，含正确的奇偶校验与有符号↔偏移二进制转换 |
| https://github.com/georgemihaila/xy2-100 | Arduino/ESP XY2-100 库（含规范 PDF）；**README 明示不支持 18 bit，且 2 MHz 下大概率跑不到** |
| https://github.com/georgemihaila/galvo-controller | 基于上者的 G-code 解析振镜控制器 |
| https://github.com/earlynerd/XY2Galvo | **RP2040 PIO 实现** —— 差分 CLOCK/SYNC/X/Y，双核，仿射变换，BSD-3 |
| https://github.com/txpzyr/xy2_100 | **ESP32 振镜 XY2-100 控制代码** |
| https://github.com/hyperchao0/qspi4xy2-100 | **RP2350 QSPI 实现**（三轴 X/Y/Z，MSB-first，含校验） |
| https://github.com/belikoff16/XY2-100- | STM32 SPI + DMA 双缓冲实现 |
| https://github.com/412910609/galvoMC | **Verilog XY2-100 解码器 + SDC 约束**（本报告 8.2 节状态机出处） |
| https://github.com/NOBIC-NTU/MiniGalvoControl | Arduino 迷你振镜控制（XY2_100.cpp/h） |
| https://github.com/opengalvo/OPAL | 开源振镜项目，含 XY2_100 库 |
| https://github.com/earlynerd/XY2-100_HLA | Saleae High Level Analyzer（Python），用于逻辑分析仪解码 |
| https://github.com/Megatokio/Laseroids | RP2040 PIO 振镜控制先驱项目（XY2Galvo 的基础） |
| https://github.com/leswright1977/OPAL_PCB | **OPAL 开源振镜硬件 PCB** —— 含 `Schematic_XY2_100_Interface_2022-07-04.pdf` 实际接口电路原理图（差分驱动部分参考价值高） |
| https://github.com/leswright1977/OPAL_PCB/blob/main/Schematic_XY2_100_Interface_2022-07-04.pdf | **XY2-100 接口硬件原理图 PDF（直接链接）** |

### 12.5 中文技术文章

| URL | 说明 |
|---|---|
| https://www.cnblogs.com/xymotion/p/12987507.html | **《XY2-100振镜控制协议》博客园** —— 差分信号、DB25/IDC、**标准与 XY2-100E 的完整位表 + BACK(STATUS) 位定义**（本报告 6.2 节出处） |
| https://www.xymotion.cn/index.php?m=home&c=View&a=index&aid=52 | **星移控制科技《XY3-100协议简介》** —— **XY3-100 一手定义**：24/32 bit 帧、16–26 bit 位宽、P1/P0 与 P3–P0 校验算法、2.4/3.2 MHz 时钟（已验证 HTTP 200） |
| https://blog.csdn.net/CrowLWZ/article/details/109050977 | 《XY2-100协议详解：光学振镜控制接口与拓展应用》—— 硬件引脚定义、数据传输定义（阅读 1.7 万+） |
| https://blog.csdn.net/my_daling/article/details/153693888 | 《XY2-100驱动，振镜控制Verilog代码》—— Verilog 实现，含"20 bit = 10 µs，写入间隔 ≥ 10 µs"结论 |
| https://blog.csdn.net/weixin_51352668/article/details/161866786 | 《振镜控制协议XY2_100(E)、SL2_100解析与Verilog实现》—— **XY2-100/XY2-100E/SL2-100 三者对比 + Verilog** |
| https://blog.csdn.net/2501_93091150/article/details/150452592 | 《xy2-100协议驱动原理，激光数字振镜驱动控制》—— 基于 STM32F103，参考 RAYLASE 官方文档 |
| https://blog.csdn.net/weixin_29171129/article/details/164417972 | 《XY2-100协议深度解析：差分信号与时序设计》—— 明确"XY2-100 没有双轴合并帧"、差分近似 RS-422/5 V |
| https://blog.csdn.net/weixin_29185199/article/details/165236476 | 《Teensy 4.x 实现 XY2-100 振镜协议：20位串行帧的时序与驱动解析》 |
| https://blog.csdn.net/weixin_29179311/article/details/164417955 | 《XY2-100振镜控制协议详解：从时序到调试实战》 |
| https://blog.csdn.net/weixin_30505225/article/details/159307426 | 《从原理到实践：手把手教你用XY2-100协议控制激光振镜（含引脚定义图）》 |
| https://gitcode.com/Open-source-documentation-tutorial/286a8/blob/main/README.md | 《XY2-100振镜控制协议标准中文详细解释.docx》文档仓库 —— **注：脚本访问返回 418，未能验证内容** |
| https://blog.csdn.net/gitblog_06683/article/details/142557605 | CSDN《XY2-100振镜控制协议标准中文详细解释》免费下载页 —— 中文详解文档（脚本访问返回 521，仅搜索摘要） |
| https://zhuanlan.zhihu.com/p/1971228156716360365 | 知乎《各种延时详解》—— 激光器延时 vs 振镜延时（开光/关光延时等） |
| https://wenku.baidu.com/view/391c752abdd5b9f3f90f76c66137ee06eff94e61.html | 百度文库《振镜延时的调节与现象》—— 5 种延时（开光/关光/跳转/扫描/曲线）原理 |
| https://wenku.baidu.com/view/7897bfa9aaf8941ea76e58fafab069dc502247b0.html | 百度文库《XY2-100 协议及其扩展版本 XY2-100E 协议》—— 数据位与 DAC 模拟量对应关系 |
| https://wenku.baidu.com/view/b0b45a664a7302768e9939aa.html | 百度文库《振镜式激光打标系统及工艺参数分析》 |
| https://wenku.csdn.net/column/5ffwcrpaz3 | CSDN 文库《scanlab 振镜技术性能对比》—— 扫描速率/角度/分辨率/重复精度/热稳定性 |

### 12.6 社区讨论 / 应用笔记 / 软件文档

| URL | 说明 |
|---|---|
| https://forum.pjrc.com/index.php?threads/implementing-xy2-100-serial-protocol-on-teensy-4-1.62819/ | **PJRC 论坛：Teensy 4.1 实现 XY2-100** —— Paul Stoffregen 用 SAI 生成 10 Mbit/s，并**纠正 SYNC 为 20 拍中高 19 拍** |
| https://forum.pjrc.com/index.php?threads/how-to-implement-a-2mhz-20bit-protocol-on-teensy-4-0.59174/ | PJRC 论坛：Teensy 4.0 实现 2 MHz 20 bit 协议（GPIO 同步写、FlexPWM） |
| https://docs.lightburnsoftware.com/1.7/Reference/DeviceSettings/GalvoBasicSettings/ | **LightBurn 振镜基础设置** —— Jump Speed / Min-Max Jump Delay / Jump Distance Limit / Laser On TC / Laser Off TC / End TC / Polygon TC（已验证 HTTP 200） |
| https://docs.lightburnsoftware.com/2.1/Reference/CutSettingsEditor/GalvoSpecificCutSettings/ | LightBurn 振镜专用切割参数（已验证 HTTP 200） |
| https://forum.lightburnsoftware.com/t/tc-parameters-dont-seem-to-do-anything-in-my-galvo-laser/159725 | LightBurn 论坛：**部分振镜（BJJCZ）的 TC 延时参数实测无效** —— 说明延时补偿能力取决于控制卡/固件实现 |
| https://www.photonlexicon.com/forums/showthread.php/37557-SL2-100-Protocol-for-scanner | 激光论坛 SL2-100 协议讨论 —— **SL2-100 为 SCANLAB 专有格式**；用户实测一帧约 **128 bit / 10 µs**（非官方数据，与中文博客的"26 bit"说法冲突） |
| https://www.xymotion.cn/ | 星移控制科技（XYMOTION）—— 国产振镜数字驱动器厂商，XY2-100/XY3-100 资料 |
| https://www.ray-motion.com/productinfo/460382.html | Ray-Motion（鞍山精准光学）产品页 —— XY2-100 接口振镜（已验证 HTTP 200） |
| https://www.scanlab.de/en/products/micromachining | SCANLAB 微加工应用页（HEAD 请求被拒，需浏览器访问） |
| https://www.ijmmm.org/vol6/402-EM0028.pdf | **学术论文（IJMMM Vol.6, 2016）** —— 四类扫描延时（laser on/off、jump、mark、corner）的定义与缺陷现象（已验证 HTTP 200） |
| https://forum.linuxcnc.org/additive-manufacturing/58213-galvo-head-protocol-xy2-100 | LinuxCNC 论坛：用 Mesa ENC422 把单端 TTL 转差分驱动 XY2-100（"converter is really just one chip, 26LS31 equivalent"）（已验证 HTTP 200） |
| https://www.easymanua.ls/scanlab/rtc6-pcie-board/manual | SCANLAB RTC6 PCIe 手册在线版（1004 页，含全部接口与配件章节） |
| https://www.scribd.com/document/941573319/Xy2-100-Specification | XY2-100 Specification（Scribd 转存版，常被引用） |

### 12.7 其他协议 / 工业集成 / 模拟接口

| URL | 说明 |
|---|---|
| https://halaser.systems/compare.php | **HALaser 官方协议对比表** —— 模拟 / XY2-100 / XY2-100E / SL2-100 / RL3-100 / SDP / NX-02 / XY3-100 的精度、轴数、线数、反馈、开放性、授权费横向对比 |
| https://halaser.systems/manuals/haldrive_manual.pdf | HALaser HALdrive X20 手册 —— **模拟接口 ±5 V..±10 V 输出 / −5 V..+5 V 反馈输入，20 bit 输出分辨率** |
| https://www.wlt.de/lim/Proceedings2017/Data/PDF/Contribution143_final.pdf | **WLT / Lasers in Manufacturing 2017, Contribution 143** —— EtherCAT ↔ SL2-100 网关（ESL2-100），含 SL2-100 的 Control Word / Status Word 过程数据映射 |
| http://newson.be/rhothor_SmartDeflector.htm | Newson SDP（Shared Data Power）—— **单同轴电缆供电+通信，开放 UART，10 Mbit/s**（⚠️ 常被误当作 SL2-100 的速率） |
| http://newson.be/rhothor_AIB.htm | Newson CUA 系列控制板 —— 16 bit 设定值、5 µs 周期、SDP 协议 |
| https://pmdi.com/posts/product/hardware/xy2-100-galvoscanner-module/ | PMDi XY2-100 振镜接口模块（工业运动控制集成） |
| https://pmdi.com/posts/product/hardware/hssi-galvoscanner-module/ | PMDi HSSI 振镜接口模块（第三方私有协议） |
| https://software.raylase.de/rpi/RAYLASE/SPICE3/UsersManual%20v2.3.5/html/45289f65-2556-4dff-8d27-7f5918253301.htm | RAYLASE RL3-100 协议说明 —— 20 bit、单连接器最多 6 轴、单电缆驱动复杂 3D 扫描头 |
| https://software.raylase.de/rpi/RAYLASE/SPICE3/UsersManual%20v2.3.5/html/9af8557b-2e37-4587-9ea2-c67b1aea40c2.htm | RAYLASE 坐标系定义 —— 坐标范围 (−res/2)…(res/2)−1，**原点在加工场中心** |
| https://software.raylase.de/rpi/RAYLASE/SPICE3/UsersManual%20v2.3.5/html/4CF38177-3E6A-4E48-98D8-F5C30FBDAE14.htm | RAYLASE SP-ICE 3 §9.5 **Sky Writing / Variable Poly Delay / Variable Jump Delay** |
| https://www.scanlab.de/en/technologies/micromachining | SCANLAB 微加工技术页 —— **官方声明 SL2-100 由 SCANLAB 开发并引入** |
| https://www.scanlab.de/sites/default/files/2020-08/13_RTC5_control%20boards.pdf | SCANLAB RTC5 手册 —— SL2-100 支持 20 bit，分辨率比 RTC4 高 16 倍 |
| https://blog.csdn.net/ttstststtttt/article/details/145651470 | CSDN **SL2-100 逆向工程博客** —— 32 bit/轴帧结构、差分曼彻斯特编码、位域划分（二手，但与另一来源互证） |
| https://blog.csdn.net/fq1986614/article/details/159765686 | CSDN：数字协议替代模拟 ±10 V 的动因（抗干扰、距离、精度） |
| https://www.zhihu.com/question/11396963867 | 知乎：SL2-100 差分传输与 20 bit 控制信号讨论（脚本访问 403，仅搜索摘要） |

---

## 附：一页速查卡

```
[帧结构 - 标准 16 bit，MSB first]
 BIT: 19 18 17 | 16 ......... 1 | 0
      C2 C1 C0 | D15 ...... D0  | P
       0  0  1 |  位置数据     | 偶校验
                (偏移二进制, 0x8000=中心)
 控制字: 001 = 位置帧 ; 111 = 命令帧(仅 Enhanced)
 18 bit Enhanced: 首位=1 + D17..D0 + 奇校验 Po

[校验] P = C2 ^ C1 ^ C0 ^ D15 ^ ... ^ D0     ← 含控制位！(对全部 19 个前导位求偶校验)

[时序 @2MHz]
 CLK  2 MHz, 500 ns, 50% duty, 连续运行（不能停！）
 上升沿 → 数据变化
 下降沿 → 振镜采样
 SYNC 上升沿 = 帧开始, 高 19 拍, 第 20 拍(校验位)拉低
 帧 = 20 clk = 10 µs → 100 kwords/s
 tDS ≥ 50 ns ,  tDH ≥ 100 ns
 变体: XY2-200 = 5 µs/200 kHz ; RAYLASE SS-III 上限 10 MHz/推荐 4 MHz

[引脚 - SCANLAB XY2-100-Enhanced, 25-pin D-SUB]
 1/14 CLOCK-/+   2/15 SYNC-/+   3/16 CHAN1-/+ (X)
 4/17 CHAN2-/+ (Y)   6/19 STATUS2-/+   8/21 STATUS1-/+
 9/10/22 +30V    12/13/25 GND
 ※ 各厂商引脚不同，换品牌必须重新核对！(RAYLASE 有 Z 在 5/18；
   电源脚 Ray-Motion 为 ±15V；X/Y 通道可能互换)

🚨 [最危险陷阱] XY2-100 vs XY3-100 —— 同一 DB25 上 CLK/SYNC 互换！
   XY2-100 : 1/14 = CLK     2/15 = SYNC   ← RAYLASE/SCANLAB/Newson 四家一手一致
   XY3-100 : 1/14 = SYNC(A) 2/15 = CLK(B) ← LasIA 官方标准 LIA202307
   帧起始边沿也相反: XY2-100 = SYNC 上升沿 ; XY3-100 = SYNC 下降沿
   数据线 X/Y/Z (3/16, 4/17, 5/18) 两协议一致 —— "Same pinout" 只对数据线成立
   → 做双协议兼容板时，CLK/SYNC 必须设计为可交换！
   ✅ 唯一的好消息: Z 轴都在 5/18 (RAYLASE / SCANLAB CHAN3 / XY3-100 三家一致)

[官方标准编号]
 XY2-100 = LasIA LIA202001  |  XY3-100 = LasIA LIA202002(v1.0) / LIA202307(v1.1)
 SL2-100 官方定义见 SCANLAB RTC6 手册 Doc Rev 1.1.4 附录 F (p.1214)
 lasia.org 现 401 → 用 Wayback 的 id_ 直链取原文

[SL2-100 官方结构]
 1 block = 192 帧 + preamble ; 1 帧 = 2 子帧 ; 帧周期 10 µs
 1 子帧 = 20 bit 载荷 + 12 bit 附加信息 = 32 bit
 → 64 bit/帧 → 6.4 Mbit/s 有效数据率, 12.8 Mbaud 线路(差分曼彻斯特)

[XY3-100 官方帧结构]
 24 bit 帧: 0 1 + D19..D0 + P1 P0      (2.4 MHz → 10 µs)
 32 bit 帧: 1 1 + D25..D0 + P3 P2 P1 P0 (3.2 MHz → 10 µs)
 首bit = 帧长, 次bit = 1 位置 / 0 命令 ; 回传 = 异步 RS485 (115200 8N1)

[分辨率 @ ±0.36 rad 光学角]
 16 bit → 11 µrad   18 bit → 2.8 µrad   20 bit(SL2-100) → 0.7 µrad
 ※ 16 bit 是 XY2-100 的精度天花板，想要更高必须换 Enhanced / SL2-100

[延迟预算（RAYLASE SP-ICE 3 官方公式）]
 TD_TX = 13 µs + 20 µs + T_Int   (T_Int=0 时 TD_TX = 14 µs)
 TD_RX = 36 µs
 Positioning Delay = TD_TX + Tracking Error(Lag)
 → 据此设置 LaserOnDelay / LaserOffDelay
 SS-III 插值默认 120 µs；命令帧占 10 µs（期间靠插值补位）
 SCANLAB SL2-100→XY2-100 转换器额外引入 10 µs，需补到激光延时里

[模拟接口陷阱]
 标度因子: Thorlabs 0.5/0.8/1.0 V 每【机械度】 (光学角 = 2×机械角!)
 → "±10V = ±20°光学" 错 2 倍; 0.5V/mech° 档下 ±10V = ±40° 光学
 分辨率瓶颈 = 电源噪声, 不是 DAC 位数
 → 同一 Thorlabs 板: 线性电源 15 µrad vs 开关电源 70 µrad

[故障行为] 时钟/同步出错 → PX/PY 常亮 + 输出级关闭（不是"保持位置"）
```

---

*本报告基于公开网络资料与开源源码整理，规格以厂商最新官方文档为准。*
