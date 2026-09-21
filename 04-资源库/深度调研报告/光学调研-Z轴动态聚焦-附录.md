# Z 轴动态聚焦 — 子课题一手档案汇编（附录）

> 本文件汇总子课题的完整核查档案，供主文档 `Z轴动态聚焦_调研素材.md` 交叉查询。
> 标注体系与主文档一致：✅一手 / 🟡二手 / ❌未找到（部分子档案另用 ⚪ 表示「算术推导」）。

---

## A. Z 轴传输协议核查档案（XY2-100 / XY3-100 / SL2-100 / RL3-100）

# 激光振镜接口协议 · Z 轴（动态聚焦）传输方式 事实核查档案

标签：✅一手（厂商/标准组织原始文档）｜🟡二手（第三方镜像、开源实现、论坛实测）｜❌未找到公开来源
**本环境不可达站点（已实测）**：`scanlab.de`（连接超时，多次重试均失败）、`halaser.eu`（TLS 握手失败）、`sourceforge.net`（Cloudflare 403）、`lasia.org`（401）、`web.archive.org`（对 lasia.org PDF 返回爬虫拦截页）、`scribd.com`（仅能取到标题）。`raylase.de` 与 `sigrok.org`、`alaser.com.tw` 为**间歇可达**（重试后 200）。相关事实改由可访问的镜像/同源文档佐证，并已标注。

---

## 0. 对比总表

| 协议 | 定义方 | 通道数 | 比特深度 | 更新率/时钟 | Z 轴如何传 | 一手/二手 |
|---|---|---|---|---|---|---|
| **XY2-100** | 无单一发明方的既成事实标准；公开格式规范由 **LasIA** 发布（LIA202001） | 标配 2 轴（X、Y）；**Z 为可选第 3 路数据通道**；每轴另有独立回传（STATUS） | 16 bit（offset binary，偶校验） | 帧 20 bit / 10 µs = **100 kHz**；CLK **2 MHz** | 第 3 对差分数据线（DB25 **5/18 = Z−/Z+**），与 X/Y **共用 CLK 与 SYNC**，同一 20 bit 帧结构 | ✅一手 |
| **XY2-100 Enhanced (-E)** | 同上（RAYLASE 实现文档最完整） | 同上（X、Y、Z） | **16 bit 或 18 bit**（18 bit 用奇校验）+ 命令帧（8 bit 命令 + 8 bit 参数） | 帧长仍 20 bit；RAYLASE SS-III：**CLK 最高 10 MHz，推荐 4 MHz** | 与 XY2-100 完全相同（Z 在 5/18） | ✅一手 |
| **XY2-200 / -200E** | 同 XY2-100 | 同上 | 同上 | CLK **最高 4 MHz** | 同上 | 🟡二手（sigrok） |
| **XY3-100** | **LasIA（Laser Industry Association）**，v1.0 = LIA202002，v1.1 = LIA202307 | 核心 2 轴；可选 **Z、U、W → 最多 5 轴**（DB15 版最多 3 轴） | **可变 16…26 bit**（24 bit 帧→20 bit 位置；32 bit 帧→26 bit） | 100 kHz 典型（10 µs）；24 bit 帧 = **2.4 MHz**，32 bit 帧 = **3.2 MHz** | DB25 **5/18 = Z−(E−)/Z+(E+)**，与 X/Y 共用 SYNC/CLK；"Z 通道（文档中称 E）为可选，用于 3D 硬件" | ✅一手 |
| **SL2-100** | **SCANLAB**（自研并引入） | **每连接器最多 2 轴**；3 轴/4 轴靠**第 2 个连接器**（第 2 根电缆） | 20 bit 载荷/子帧 | 1 帧 = 2 子帧 / **10 µs** = 100 kHz；官方未公布 bit/s | **不是帧内第 3 通道**：Z 走第 2 个 SCANHEAD 连接器（占该连接器两个通道） | ✅一手 |
| **RL3-100** | **RAYLASE**（自有） | **单连接器最多 6 轴**，3D/5 轴全部走同一连接器 | 20 bit | 10 µs 步进周期（100 kHz） | 与 X/Y 同一连接器、**单根电缆** | ✅一手（轴数/位深/周期）；帧级细节 ❌未找到 |

---

## 1. XY2-100 / XY2-100 Enhanced

**物理层与帧（一手，LasIA 格式规范）**
- 连接器通常为 DB25，信号为 **CLK+、SYNC+、X+、Y+、Z+ Data**——规范原文的信号示意里**直接画了三路数据（X+、Y+、Z+）** [来源](https://www.aaronvose.net/Quantronix_Osprey/xy2_100_specification.pdf) ✅一手（注：该镜像站为 `lasia.org/LIA202001` 的逐字镜像，但缺版权页，归属由第三方调研与 LasIA 文档编号体系佐证）
- "SYNC 上升沿标记一帧开始，SYNC 下降沿标记当前帧最后一位开始；数据在 **CLK 下降沿**有效" [来源](https://www.aaronvose.net/Quantronix_Osprey/xy2_100_specification.pdf) ✅一手
- **标准 16 bit 模式**：前 3 bit = `001`，随后 16 bit 位置数据，末位**偶校验 Pe**。位序（19…0）：bit19,18,17 = 0,0,1；bit16…bit1 = **D15…D0**；bit0 = Pe [来源](https://www.aaronvose.net/Quantronix_Osprey/xy2_100_specification.pdf) ✅一手
- **Enhanced 18 bit 模式**：bit19 = 1，随后 18 bit 位置数据，末位**奇校验 Po** [来源](https://www.aaronvose.net/Quantronix_Osprey/xy2_100_specification.pdf) ✅一手
- **⚠️ 纠正"LSB-first"说法：XY2-100 是 MSB-first。** 位表把 D15 放在 D0 之前；RAYLASE 文档亦明确 "target position (D15-D0 或 D17-D0) 被解释为无符号整数，**D0 是最低位、D15/D17 是最高位**" [来源](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf) ✅一手；sigrok 解码器同样用 `bits[3]` 作为 MSB 重建数值 [来源](https://raw.githubusercontent.com/sigrokproject/libsigrokdecode/master/decoders/xy2-100/pd.py) ✅一手
- 20 bit 字 @ **2 Mbit/s = 100 kwords/s**，帧周期 10 µs [来源](https://dvd.ilphotonics.com/Ray-Motion%20-%20galvanometers%20-%201D-2D-3D%20scanners/Motion%20Control%20-%20Optomechanics/Interface%20XY2-100.pdf) 🟡二手（RAY-MOTION/鞍山精准光学版 XY2-100 数据手册，IL Photonics 镜像）
- LasIA XY3-100 规范中的官方对照表给出 XY2-100：**16 bit（XY2-100E 为 18 bit）、100 kHz 帧、100 ks/sec、回传为与 XY2-100 时钟同步的 20 个数据位、DB25、奇偶校验位** [来源](https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf) ✅一手

**Z 轴 / "CHANNELZ"**
- sigrok 一手描述："最常见的配置使用公共时钟与同步信号，配两对数据与状态信号——一对给 X、一对给 Y。**有时 Z 轴也存在**。"解码器数据通道定义为 "**X, Y or Z axis data**" [来源](https://sigrok.org/wiki/Protocol_decoder:Xy2-100) ✅一手
- RAYLASE SS-III XY2-100-E 文档："在 XY2-100-E 中，**每一轴（x、y 以及 z）**都有一路去往振镜头的正向数据通道和一路回到控制卡的回传通道"；DB25 引脚 **5/18 = Z−/Z+（位置与命令，聚焦轴）**，**7/20 = Z_stat−/+（回传）**；状态字 bit13/5 = "Z 轴位置在跟踪误差窗口内" [来源](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf) ✅一手
- RAYLASE SP-ICE-3 头格式 `XY2_100` 的轴定义为 "**XY or XYZ**"，说明 "Legacy 16-bit protocol via XY2-100 Adapter Board" [来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/45289f65-2556-4dff-8d27-7f5918253301.html) ✅一手
- RAYLASE SS-III 引脚命名对照：XY2-100 数据手册用 **CHANNELX（3/16）、CHANNELY（4/17）** [来源](https://dvd.ilphotonics.com/Ray-Motion%20-%20galvanometers%20-%201D-2D-3D%20scanners/Motion%20Control%20-%20Optomechanics/Interface%20XY2-100.pdf) 🟡二手；**"CHANNELZ" 这一字面术语在本次检索到的一手规范中均未出现** ❌未找到——实际使用的命名是 `X+/Y+/Z+`（LasIA）、`CHAN1/CHAN2`（SCANLAB 转换器）、`Z−/Z+ focus axis`（RAYLASE SS-III）、`Z-DAC CHANNEL`（RAYLASE AXIALSCAN）。
- 开源实现佐证 3 通道：qspi4xy2-100 把 QSPI 的 IO1/IO2/IO3 分别映射为 Channel X/Y/**Channel Z**，"若配置为 2D 传感器则此引脚不用"，并注明 3D 需**至少两片差分线驱动**（三通道 + 同步 + 时钟） [来源](https://github.com/hyperchao0/qspi4xy2-100) 🟡二手
- **SCANLAB 的相反做法（重要）**：RTC6 的 XY2-100 Converter 25-pin 引脚只有 `CLOCK±、SYNC±、CHAN1±、CHAN2±、STATUS±、STATUS1±`——**没有第 3 数据通道**；"每个扫描头连接器最多可传两轴数据" [来源](https://raw.githubusercontent.com/labspiral/sirius3/main/doc/SCANLAB/RTC6_Manual.en.pdf) ✅一手。SCANLAB 的 3D 走第 2 个连接器（见 §3）。

**Standard 与 Enhanced 的差别（是否影响更新率/位深）**
- 帧长不变（20 bit）；Enhanced 增加的是：**18 bit 模式（奇校验）**、**命令帧（8 bit 命令 + 8 bit 参数，帧内 D15–D8 / D7–D0）**、以及可选的回传格式 [来源](https://www.aaronvose.net/Quantronix_Osprey/xy2_100_specification.pdf) ✅一手 + [来源](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf) ✅一手
- 命令帧会占用整整一个 10 µs 周期（该周期内不发目标位置，振镜头按前后两点线性插值） [来源](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf) ✅一手
- **更新率由时钟决定，不由 Standard/Enhanced 决定**：RAYLASE SS-III 明确 "**时钟最高频率 10 MHz，推荐 4 MHz**" [来源](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf) ✅一手；sigrok 把 4 MHz 变体命名为 XY2-200 [来源](https://sigrok.org/wiki/Protocol_decoder:Xy2-100) ✅一手。即 16 bit 与 18 bit 模式下帧长相同，位深提升**不降低**更新率。
- Enhanced 的一个已知缺陷：18 bit 位置帧（奇校验）与命令帧（偶校验）在损坏时无法区分，sigrok 会就此报警 [来源](https://sigrok.org/wiki/Protocol_decoder:Xy2-100) ✅一手

---

## 2. XY3-100（LasIA）

- 规范封面：**"XY3-100 Laser Scanner Protocol Format Specification, Version 1.0 LIA202002 / Version 1.1 LIA202307"，© 2020-2023 by LasIA** [来源](https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf) ✅一手
- 商标：`XY3-100`、XY3-100 logo、`XY4-100`、`XY5-100` 为 LasIA 商标；**未经许可只能称 "XY3-100 compatible"，不得使用 logo，也不得称 "certified"** [来源](https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf) ✅一手
- 定位："XY2-100 的后继标准"，**引脚兼容 XY2-100，可通过固件升级**；SPI-like（SYNC=CS、CLK=SCK、X/Y/Z/U/W=SDI）；**© LasIA 但为开放标准**，可免费用于振镜头与控制卡 [来源](https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf) ✅一手
- **帧格式**：帧长由**第 1 位**决定——0 = 24 bit 帧（22 bit 载荷，2.4 MHz @100 kHz）；1 = 32 bit 帧（30 bit 载荷，3.2 MHz @100 kHz）。**第 2 位**决定类型——1 = 位置帧，0 = 命令帧。位置帧为 `bit31/23=长标志` + `bit30/22=模式` + **D25..D0 或 D19..D0** + 校验位（24 bit 帧为 P1P0，32 bit 帧为 P3..P0，均为"置 1 位数"计数器低若干位） [来源](https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf) ✅一手
- **时序**：帧长固定 10 µs（100 ks/sec），帧内位数可变；**帧开始 = SYNC 下降沿**；**数据有效 = CLK 下降沿** [来源](https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf) ✅一手
- **Z 轴 = DB25 引脚 5/18（Z−/Z+，文档内代号 E）**；"Z 通道（文档中称 E）为**可选**，可用于具备 3D 能力的硬件"。U = 7/20（代号 G）、W = 8/21（代号 H）、BACK = 6/19（代号 F） [来源](https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf) ✅一手
- **功能子集递进**：2D 位置（SYNC、CLK、X、Y 为**强制核心**）→ 3D 加 **Z** → 4 通道加 U（仅 DB25）→ 5 通道加 W（仅 DB25）；回传通道仅"同步包"在使用回传时强制 [来源](https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf) ✅一手
- v1.1 新增 **DB15 版本**，含 Z，但**不含 U/W，最多 3 轴** [来源](https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf) ✅一手
- 电气：RS485 差分，须符合 **ANSI TIA/EIA-485-A 与 ISO 8482:1987**，接收端需端接 [来源](https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf) ✅一手
- 回传：**异步 RS485 串行协议**（XY2-100 是同步 20 位）——这是二者最大架构差异 [来源](https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf) ✅一手
- **⚠️ 工程陷阱：同一条 DB25 上 CLK/SYNC 互换。** XY3-100 为 `1/14 = SYNC(A)`、`2/15 = CLK(B)` [来源](https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf) ✅一手；而 XY2-100 为 `1/14 = CLOCK`、`2/15 = SYNC` [来源](https://dvd.ilphotonics.com/Ray-Motion%20-%20galvanometers%20-%201D-2D-3D%20scanners/Motion%20Control%20-%20Optomechanics/Interface%20XY2-100.pdf) 🟡二手 + [来源](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf) ✅一手。故规范中 "Same pinout as XY2-100(E)" **只在数据线上成立**。
- 发布公告 "XY3-100 Digital Scanner Interface version 1.1"（2023-07，SourceForge/LasIA 博客）在本环境被 Cloudflare 403 拦截，**仅能通过搜索摘要引用** [来源](https://sourceforge.net/p/lasia/blog/2023/07/xy3-100-digital-scanner-interface-version-11/) 🟡二手（原文不可达）

---

## 3. SL2-100（SCANLAB）

- 定义方：官方口径为 SCANLAB 自研并引入——"广泛使用的 XY2-100 协议只有 16 bit 定位分辨率，对微加工往往不再够用。**由 SCANLAB 开发并引入的 20 bit SL2-100 协议**是必要的升级。RTC5 与 RTC6 均支持该协议。" [来源](https://www.scanlab.de/en/applications/micromachining) 🟡二手（`scanlab.de` 本环境连接超时，仅有搜索摘要）
- RTC5 官方手册（镜像）："RTC5 通过新的 SL2-100 数据传输协议与扫描系统通信。该协议支持 **20 bit 控制信号**，因而相对前代 RTC4 具有 **16 倍**更高的定位分辨率。" "每 10 µs 向扫描系统输出或从其读入相应信号。" [来源](http://intech-jp.com/spec_sheet/rtc5_en_49493.pdf) ✅一手（SCANLAB RTC5 手册的另一镜像；`scanlab.de` 原始 PDF 本环境不可达）
- **官方帧结构（RTC6 手册附录 F "SL2-100 Protocol Short Information"）** [来源](https://raw.githubusercontent.com/labspiral/sirius3/main/doc/SCANLAB/RTC6_Manual.en.pdf) ✅一手：
  - 双向、串行、**需要 2 条独立通道**：Forward Channel（板→振镜）与 Return Channel（振镜→板）
  - 数据以**块（SL2-100 block）**传输；**1 block = 192 帧**，每块以 **preamble** 开头
  - **1 帧 = 2 个子帧；1 帧传输时间 = 10 µs**
  - **1 子帧 = 20 bit 载荷（控制值或状态值）+ 12 bit 附加信息（如同步）**
  - ⇒ 每帧恰好承载 **2 轴 × 20 bit**，帧率 100 kHz。**这就是"每连接器限 2 轴"的根本原因**
- "**每个扫描头连接器最多可传输两轴的数据**" [来源](https://raw.githubusercontent.com/labspiral/sirius3/main/doc/SCANLAB/RTC6_Manual.en.pdf) ✅一手
- **Z 轴传输方式（关键结论）**：SL2-100 **不是**在帧内加第 3 通道。SCANLAB RTC6 选件 "3D" 规定："xy 扫描系统必须接 **Connector for First Scan Head**；**z 轴必须接 Connector for Second Scan Head**"；"信号可由第一扫描头连接器输出给 xy 扫描头，并由**第二扫描头连接器的两个通道**输出给第 3 轴（z 轴）" [来源](https://raw.githubusercontent.com/labspiral/sirius3/main/doc/SCANLAB/RTC6_Manual.en.pdf) ✅一手。即 **Z = 第二根电缆 + 第二路 SL2-100 链路**。
- RAYLASE 侧完全一致：`SL2_Single3D` = "**XY provided on X904 Scanner1, Z provided on X905 Scanner2**"；官方注："真正的光学变焦需要共 5 轴，但 **SL 协议每连接器限 2 轴**" [来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/45289f65-2556-4dff-8d27-7f5918253301.html) ✅一手；SP-ICE-3 亦声明 "SL2-100 protocol with 20 bit position resolution and **up to 2 axes per connector**" [来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/48a53e4f-2a14-4518-ad32-d622848ab64a.html) ✅一手
- **3/4 通道变体是否存在**：作为"单连接器 3/4 通道协议"**不存在** ❌未找到。多轴一律靠多个 2 轴连接器。RAYLASE 确实有 3D/4D 头格式命名，但均跨 2 个连接器：`SL2_Single3D` / `SL2_Single3DX`(+Extra Z) / `SL2_Single3DA`(+Auxiliary) / `SL2_Single4D`(XYZ+ZoomZ) / `SL2_Single4DF`(XYZ+Defocus) / `SL2_Single4DFA` / `SL2_Single4DFX` / `SL2_Dual2D` [来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/45289f65-2556-4dff-8d27-7f5918253301.html) ✅一手
- **位速率**：SCANLAB 官方**未公布 SL2-100 的 bit/s 数值** ❌未找到。按附录 F 推算：1 帧 = 2×32 = **64 bit / 10 µs = 6.4 Mbit/s 数据率**（若线路为二电平，128 符号/10 µs = 12.8 Mbaud）——**属推算值，非一手**。
- **"2 Mbaud" 说法**：❌未找到任何一手来源支持 SL2-100 为 2 Mbaud；2 MHz 是 **XY2-100 的 CLK 频率**（20 bit ÷ 2 MHz = 10 µs）。**"100 kHz / 20 bit" 两项则已由官方确证**（见上）。

---

## 4. RL3-100（RAYLASE）

- 归属：RAYLASE **自有协议**（非 LasIA、非 SCANLAB） [来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/48a53e4f-2a14-4518-ad32-d622848ab64a.html) ✅一手
- **位深 20 bit、单连接器最多 6 轴**："RL3-100 protocol with **20 bit** position resolution and **up to 6 axes per connector**" [来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/48a53e4f-2a14-4518-ad32-d622848ab64a.html) ✅一手
- **速率**：与 SL2-100 同为 **10 µs 步进周期（100 kHz）**，20 bit 分辨率对应镜面定位分辨率 **0.75 µrad** [来源](https://www.raylase.de/_Resources/Persistent/b/a/6/6/ba66d25112e3d91511322aa417caae73c916557b/Datasheet_SP-ICE-3.pdf) ✅一手（RAYLASE SP-ICE-3 数据手册 v1.7，2025-08）
- **Z 轴如何传 —— 与 SL2-100 的本质区别**：RL3-100 的 3D 头格式全部标注 "**ALL axes provided on X904 Scanner1**"，即 X/Y/Z（乃至 Extra Z、Auxiliary、ZoomZ）**全部走同一个连接器、单根电缆**：`RL3_Single3D`、`RL3_Single3DX`、`RL3_Single3DA`、`RL3_Single3DXA`、`RL3_Single4D`(XYZ+ZoomZ)、`RL3_Single4DX` [来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/45289f65-2556-4dff-8d27-7f5918253301.html) ✅一手
- 与 XY2-100 的差异：20 bit vs 16 bit；**单连接器 6 轴 vs SCANLAB 每连接器 2 轴**；3D/5 轴可单电缆 [来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/48a53e4f-2a14-4518-ad32-d622848ab64a.html) ✅一手
- 同一台 **3 轴（含 Z）硬件三种协议可选**：RAYLASE **AXIALSCAN-50 DIGITAL II**（预聚焦式 3D 偏转单元）原文——"INTERFACES：该偏转单元**同时可用于 RL3-100 20 bit 协议与 XY2-100 16 bit 协议**，或作为替代用于 **SL2-100 20 bit 协议**"；"FEATURES：… Control via **SL2-100 protocol 20 bit** or **RL3-100 protocol 20 bit** and **XY2-100 protocol 16 bit**；**Digitally controlled high-speed Z-axis**" [来源](https://www.raylase.de/en/products/prefocusing-deflection-units/axialscan-50-digital-ii.html) ✅一手
- （补充一手引脚证据）RAYLASE **AXIALSCAN 3 轴**数字接口 25-pin：`1/14 = SENDCLOCK±`、`2/15 = SYNC±`、`3/16 = X-DAC CHANNEL±`、`4/17 = Y-DAC CHANNEL±`、**`5/18 = Z-DAC CHANNEL±`**、`6/19 = HEAD-STATUS±`，原文注明 "All signals are compatible with **RAYLASE's extended function XY2-100 standard**"——**Z 是与 X/Y 并列的第 3 路数据通道，共用 SENDCLOCK 与 SYNC** [来源](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422461085930.pdf) ✅一手（RAYLASE MN025 v2.0.3 官方手册镜像）
- **RL3-100 帧级细节（帧长、位序、校验、时钟频率、编码方式）**：❌未找到公开来源。RAYLASE 未公开发布 RL3-100 的帧格式规范文档；本次仅能确证 20 bit、≤6 轴/连接器、10 µs 步进周期。

---

## 5. SP-ICE-3（RAYLASE）支持的接口

- 扫描头/偏转单元侧：**RL3-100（20 bit，≤6 轴/连接器）、SL2-100（20 bit，≤2 轴/连接器）、XY2-100（16 bit，经可选适配板）**；激光器侧：15-pin 双模拟输出 + 差分 0–10 V 附加连接器 [来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/48a53e4f-2a14-4518-ad32-d622848ab64a.html) ✅一手
- 数据手册：最多 2 个偏转单元；**10 µs 步进周期、20 bit 位置分辨率（≈0.75 µrad）**；支持 **2/3/4/5 轴**偏转单元，或经 RL3-100 **2×3 轴**；"Support of RL3-100 protocol" [来源](https://www.raylase.de/_Resources/Persistent/b/a/6/6/ba66d25112e3d91511322aa417caae73c916557b/Datasheet_SP-ICE-3.pdf) ✅一手
- XY2-100 需适配板：订货号 **08001**（XY2-100 Adapter SP-ICE 3 Set，单头 Head 0）与 **14009**（Dual Mode Set，双头分别接 **X403 (GPIOE)** 与 **X402 (GPIOD)**） [来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/65db6d89-b141-46a3-a74c-0b0ec7df2df1.html) ✅一手
- 分辨率表：`SL2-100 = 20 bits`、`XY2-100 = 16 bits`；且 "**All X, Y, and Z ordinates fall within the range (-res/2) to (res/2)-1 inclusive**" ——**Z 的位深与 X/Y 相同** [来源](https://software.raylase.de/rpi/RAYLASE/SPICE3/UsersManual%20v2.3.5/html/9af8557b-2e37-4587-9ea2-c67b1aea40c2.html) ✅一手

---

## 6. 需纠正的常见说法（核查结论）

| 待核查说法 | 结论 |
|---|---|
| XY2-100 数据 **LSB-first** | ❌ **错误**。位表为 `001` + **D15→D0（MSB 先）** + Pe；RAYLASE 原文 "D0 是最低位" [来源](https://www.aaronvose.net/Quantronix_Osprey/xy2_100_specification.pdf) ✅一手 |
| XY2-100 **默认 2 轴、第 3 通道可选实现 3 轴** | ✅ **正确**。LasIA 规范信号图含 X+/Y+/Z+；RAYLASE SS-III Z 在 **5/18**；SP-ICE-3 `XY2_100` = "XY or XYZ" |
| XY2-100 **20 bit 帧 / 10 µs / 100 kHz / 2 MHz** | ✅ 100 kHz 与 20 bit 帧为官方口径；2 MHz 与 "100 kwords/s" 见 RAY-MOTION 数据手册 🟡二手 |
| 存在名为 **"CHANNELZ"** 的规范术语 | ❌未找到。一手规范使用 `X+/Y+/Z+`、`Z−/Z+ (focus axis)`、`Z-DAC CHANNEL`；SCANLAB 转换器侧仅有 CHAN1/CHAN2 |
| SL2-100 = **2 Mbaud** | ❌未找到一手来源。官方未公布 bit/s；100 kHz / 20 bit 已确证；2 MHz 是 XY2-100 的时钟 |
| SL2-100 有**单连接器 3/4 通道**变体 | ❌ **不存在**。官方明确"每连接器 2 轴"，多轴靠多连接器；Z 走第 2 连接器 |
| SL2-100 是**开放/厂商中立**协议 | ❌ 不符。RAYLASE 侧文档把它与 RL3-100 并列且 RL3-100 为 RAYLASE 自有；SCANLAB 侧为自研自用（第三方需经转换器/网关） |
| XY3-100 = 20 bit | ❌ 不完整。协议能力为 **16…26 bit 可变**（24 bit 帧→20 bit；32 bit 帧→26 bit）；20 bit 是具体型号（如 HALscan X20）的实现 [来源](https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf) ✅一手 |
| RL3-100 有公开帧格式规范 | ❌未找到。仅 20 bit / ≤6 轴/连接器 / 10 µs 为公开事实 |

---

## 7. 未找到公开来源清单（诚实声明）

1. **RL3-100 帧级规范**（帧长、位序、校验算法、CLK 频率、编码）：❌未找到。RAYLASE 未公开发布。
2. **SL2-100 官方 bit/s 数值与完整位域定义**（如 6 bit 模式码表、校验算法）：❌未找到。附录 F 只给到"1 帧 = 2 子帧、子帧 = 20 bit 载荷 + 12 bit 附加"这一层。
3. **SL2-100 官方连接器型号与引脚**：`scanlab.de` 引脚文档（`pin-out-intelliSCAN.pdf`）本环境不可达，未能一手确认（第三方调研记为 9-pin D-SUB，数据为 DATA IN±/DATA OUT± 两对差分）。**这是本档案中唯一因站点不可达而未能一手落实的硬件细节。**
4. **"CHANNELZ" 字面术语的一手出处**：❌未找到。
5. **"2 Mbaud" 的一手出处**：❌未找到（见 §3）。
6. **XY2-100 发明方**：无决定性证据；可确证的只是**公开格式规范由 LasIA 以 LIA202001 发布**。
7. 本环境持续不可达站点：`scanlab.de`、`halaser.eu`、`sourceforge.net`（LasIA XY3-100 v1.1 发布公告原文）、`lasia.org`、`web.archive.org`（对 lasia.org PDF 的爬虫拦截）、`scribd.com`。`raylase.de` / `sigrok.org` / `alaser.com.tw` 为间歇可达（重试后可取）。凡依赖不可达站点者均已降级标注。
8. **LasIA LIA202001（XY2-100 官方规范）原始 URL 未能一手取得**：`lasia.org` 返回 401、Wayback 对同一 PDF 返回爬虫拦截页。本档案所用版本取自 `aaronvose.net` 镜像，其标题/版式与 LasIA 的 "XY3-100 Laser Scanner **Protocol Format Specification**" 同系列，但该 3 页 PDF **无版权页**，因此"即 LIA202001 本身"这一归属属 🟡（第三方调研结论），**格式内容本身为规范文本**。核查 XY2-100 帧格式时建议以 RAYLASE SS-III 手册（一手，可访问）交叉验证——二者完全一致。

---

## B. Z 轴控制与标定核查档案（同步 / 延迟补偿 / 分辨率 / 标定 / 失效）

# 振镜 Z 轴（动态聚焦）控制与标定 —— 核查用研究档案

标签：✅一手 = 厂商手册/数据表/标准/已读论文原文；🟡二手 = 博客、经销商、论坛、百科；❌未找到 = 无公开来源；⚪本报告推导 = 由已标注来源输入值做的算术/物理推导，非引用值。

> 核查方式：`web_fetch` 在本环境不可用，全部通过 `curl` 抓取 PDF/HTML 后以 `pdftotext`/Python 本地解析。文中每条事实均附直链。**未编造任何数字**；取不到的数值一律标 ❌。

---

## 0. 关键结论速览

- Z 轴不是"另一个轴"，而是**与 X/Y 同帧、同字长、同刷新率传输的第三个坐标通道**：RAYLASE 的 XY2-100-E 厂商文档把帧类型直接写作 `16Bit command position frame (X+, Y+, Z+ to deflection unit)` 与 `18Bit command position frame (X+, Y+, Z+ to deflection unit)` [来源](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf) ✅一手 —— **协议层 Z 与 XY 天然同步，不存在独立的"Z 时间戳队列"**。
- 真正的 Z 同步难题是**动态滞后**：Z 执行器滞后（0.55–0.70 ms、0.1 ms、1.3 ms）通常比 XY（0–0.30 ms）大 2–13 倍，只能靠"提前发出 Z 设定值"或逐轴补偿参数解决。
- 16 bit 是**接口造成的硬上限**：Novanta 明确写 `Command Resolution: 24-bit (GSB) or 16-bit (XY2-100)` [来源](https://www.optoprim.de/PDF/CTI/CTI_Lightning-II_Datasheet.pdf) ✅一手 —— 用 XY2-100 就掉到 16 bit，与控制器自身位宽无关。
- 在真实系统里，**漂移与重复性通常先于量化成为精度瓶颈**：varioSCANde II 长期漂移 < 3 µm/8 h，比 16 bit 在 ±14 mm 行程下的 0.427 µm/LSB 大约 7 倍 [来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf) ✅一手。

---

## 1. Z 轴与 XY 的同步机制

### 1.1 协议层：Z 与 XY 同帧

| 事实 | 来源 | 标签 |
|---|---|---|
| SP-ICE-3 卡固件**所有矢量处理函数默认按 3D(XYZ) 矢量处理**；2D 函数等价于 Z=0 | [RAYLASE SP-ICE-3 手册 8.2.3](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/254aa48e-536e-4bbe-a569-fe200cc6a2ac.htm) | ✅一手 |
| 「Z 坐标可在**单条矢量加工过程中**变化」（Z-ordinate can change during marking of an individual vector） | [同上](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/254aa48e-536e-4bbe-a569-fe200cc6a2ac.htm) | ✅一手 |
| 3D 加工场 = 夹在两个 XY 平面之间的固定 XYZ 体（焦点可达范围），由 XY 头光学、透镜平移单元光学、以及 **3D 场校正文件 FC3** 内容共同决定 | [SP-ICE-3 手册 7.1.7](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/CE15CBDB-355A-4F69-A5B0-97611F5D1550.htm) | ✅一手 |
| XY2-100 单词 20 bit = 3 bit 控制字(C2–C0) + 16 bit 数据(D15–D0，偏移二进制) + 1 bit 偶校验；CLOCK 2 MHz，**10 µs/帧、100 kwords/s** | [XY2-100 技术数据表](https://dvd.ilphotonics.com/Ray-Motion%20-%20galvanometers%20-%201D-2D-3D%20scanners/Motion%20Control%20-%20Optomechanics/Interface%20XY2-100.pdf) | ✅一手 |
| 16 bit 帧前 3 bit 固定 `001`；**18 bit 帧由奇校验标识**（不靠控制字）；「有时也存在 Z 轴」 | [sigrok xy2-100 解码器](https://sigrok.org/wiki/Protocol_decoder:Xy2-100) | 🟡二手 |
| XY2-100-E 中命令帧占用 10 µs，**该 10 µs 内无法传输目标位置**（插命令即挤掉一帧位置） | [RAYLASE SS-III XY2-100-E 文档](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf) | ✅一手 |
| XY2-100-E 目标位置按**无符号整数**解释（D15–D0 或 D17–D0），18 bit 回读帧"精度提高四倍" | [同上](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf) | ✅一手 |

### 1.2 控制器层

- SP-ICE-3 经 SL2-100 / RL3-100 控制最多 2 个偏转单元（或 5 轴 / 2×3 轴），**20 bit 位置分辨率、10 µs 步进周期**；XY2-100 为 16 bit（需转接板）[来源](https://www.raylase.de/_Resources/Persistent/b/a/6/6/ba66d25112e3d91511322aa417caae73c916557b/Datasheet_SP-ICE-3.pdf) ✅一手
- 数据表原文列出 **"Tracking Error compensation for all axes individually"（各轴独立跟踪误差补偿）** —— 这是"Z 轴单独补偿"的直接厂商标注 [同上](https://www.raylase.de/_Resources/Persistent/b/a/6/6/ba66d25112e3d91511322aa417caae73c916557b/Datasheet_SP-ICE-3.pdf) ✅一手
- 数据表同时列出 **Sky Writing**、**Variable Jump Delay** [同上](https://www.raylase.de/_Resources/Persistent/b/a/6/6/ba66d25112e3d91511322aa417caae73c916557b/Datasheet_SP-ICE-3.pdf) ✅一手；手册有 9.5.4 Variable Poly Delay、9.5.5 Variable Jump Delay 专节 [手册目录](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/11D7AE2D-B159-4C4D-B522-0E1624FF22C0.htm) ✅一手

### 1.3 SCANLAB RTC 侧

| 事实 | 来源 | 标签 |
|---|---|---|
| RTC4：**16 bit 定位分辨率、10 µs 输出周期**、XY2-100 enhanced 协议；选件含 "Functionality for controlling of **3-axis scan systems**" | [SCANLAB RTC4 数据表](https://www.scanlab.de/sites/default/files/2020-08/14_RTC4_control%20boards.pdf) | ✅一手 |
| RTC6 把用户路径翻译为 microvector，经 **SL2-100 以 100 kHz** 下发"振镜角度设定坐标"；同时接管激光控制（分辨率 **64 MHz**） | [SCANLAB SCANahead 白皮书](https://www.scanlab.de/sites/default/files/2024-11/scanahead_en_0.pdf) | ✅一手 |
| **SCANahead** = "无跟踪误差控制技术"：实时状态控制使振镜始终以最大加速度运动；运动整体被**预览时间 t_p（preview time）**延迟，但跟踪误差 t_s = **0** | [同上](https://www.scanlab.de/sites/default/files/2024-11/scanahead_en_0.pdf) | ✅一手 |
| 配 SCANahead 的 excelliSCAN：**Tracking error = 0 ms**（14 mm 与 20 mm 口径均 0）；控制板须为 **RTC6（含 SCANahead 选件）** | [excelliSCAN 数据表](https://optoprim.com/wp-content/uploads/2022/03/Tete-scanner-standard-excelliSCAN-SCANLAB.pdf) | ✅一手 |
| intelliSCAN IV 的 SCANahead 描述含 **"auto delay function for laser and scanner synchronization"** | [DirectIndustry 产品页](https://pdf.directindustry.com/pdf/scanlab-gmbh/intelliscan-iv/39164-1067693.html) | 🟡二手（仅读到摘要，未读全文） |
| 开源库 sirius2 声称支持 RTC6 的 SCANahead / SDC，并支持 2D、3D 场校正与"3D 曲面标定工具（平面/锥面/圆柱/点云）" | [GitHub labspiral/sirius2](https://github.com/labspiral/sirius2) | 🟡二手 |

**❌未找到公开来源**：SCANLAB RTC 文档中形如 `set_focus` / `set_z` / `z_offset` 的 Z 轴列表命令名；SCANLAB 文档中亦无名为 "look-ahead" 的功能（最接近者是 SCANahead 的 preview time t_p）。**请勿在报告中编造这些命令名。**（RAYLASE 侧的对应物是 `FieldTransform` 的 Z 分量 / FC3 的 `FieldOffset.Z`，见 §5.2。）

---

## 2. 延迟 / 滞后补偿

### 2.1 补偿原理（RAYLASE，公开一手材料最完整）

- **总定位延迟 = 传输延迟(Transfer Delay) + 跟踪误差(Tracking Error，又称 Lag)**；因此 `LaserOnDelay` / `LaserOffDelay` 必须按该总和设置 [SP-ICE-3 手册 7.1.9](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/7a6d305c-a5d1-4dfb-a1d2-3afc1768b87f.htm) ✅一手
- **发送方向** TD_TX = T_K + T_C + T_Int，其中 **T_K = 13 µs**、**T_C = 20 µs**（插补例程计算时间）、T_Int = 振镜插补时间设置；**T_Int = 0 时 TD_TX = 14 µs**（近似误差 ±2 µs）[同上](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/7a6d305c-a5d1-4dfb-a1d2-3afc1768b87f.htm) ✅一手
- **回读方向** TD_RX = **36 µs**（常数，与插补时间无关）[同上](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/7a6d305c-a5d1-4dfb-a1d2-3afc1768b87f.htm) ✅一手
- 激光控制信号从卡直接发给激光器，**几乎无延迟**；卡同步发出位置命令与激光信号，但激光与振镜本身响应不同步 [同上](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/7a6d305c-a5d1-4dfb-a1d2-3afc1768b87f.htm) ✅一手
- 传输延迟可经 Enhanced Protocol 原始命令读取：**0x0556** = TD_TX；**0x0557** = TD_TX + TD_RX [同上](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/7a6d305c-a5d1-4dfb-a1d2-3afc1768b87f.htm) ✅一手
- `TrackingError` 是 **AxisParameterSet 的逐轴属性**，"通常应设为振镜数据手册给出的值"；另有 `LaserTriggerDelay`（激光侧）[SP-ICE-3 手册 7.1.6](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/e1516d08-fc0e-4025-9c02-e600785ec5e2.htm) ✅一手
- 停止类滞后用 `JumpDelay` / `MarkDelay` / `PolyDelay` 补偿；三者需随 `MarkSpeed` 等参数变化重新调整 [SP-ICE-3 手册 7.3.2 / 7.3.2.1](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/13385edc-c826-42c6-9c41-bb985514f68d.htm) ✅一手

### 2.2 SCANLAB 侧

- 常规控制：跟踪误差"有限且恒定"，**延迟必须人工测定并设置**，且需按应用分别优化 tuning；SCANahead：t_s = 0，延迟"**由 RTC6 的 auto-delay 功能设置**"，只需一套 tuning [SCANahead 白皮书](https://www.scanlab.de/sites/default/files/2024-11/scanahead_en_0.pdf) ✅一手
- 常规控制的跟踪误差导致**圆弧"缩颈效应"(necking)** 与 90° 拐角变圆；示例 150 µm 圆（v = 2.8 m/s）、300 µm 拐角（v = 1 m/s）下 SCANahead 明显改善 [同上](https://www.scanlab.de/sites/default/files/2024-11/scanahead_en_0.pdf) ✅一手

### 2.3 Z 与 XY 滞后量级对比（本档案核心数字）

| 器件 | 轴 | 滞后 / 跟踪误差 | 来源 | 标签 |
|---|---|---|---|---|
| SCANLAB varioSCANde II 20i | **Z** | **0.55 ms** | [varioSCAN II 数据表](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf) | ✅一手 |
| SCANLAB varioSCANde II 40i(FLEX) | **Z** | **0.70 ms** | [同上](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf) | ✅一手 |
| SCANLAB excelliSHIFT | **Z** | **0.1 ms** | [excelliSHIFT 数据表](https://www.scanlab.de/sites/default/files/2025-06/SCANLAB-excelliSHIFT-EN.pdf) | ✅一手 |
| RAYLASE FOCUSSHIFTER DIGITAL II（LT-II-F 线性平移模块） | **Z** | **1.3 ms** | [FOCUSSHIFTER DIGITAL II 数据表](https://shop.amstechnologies.com/media/ea/23/0d/1720719683/FOCUSSHIFTER-DIGITAL-II-Prefocusing-Deflection-Units-Raylase-Datasheet.pdf?ts=1734637907) | ✅一手 |
| Novanta LIGHTNING II 3 轴（含 DFM） | **Z** | **0.2 ms**（20/30 mm）/ **0.4 ms**（50 mm） | [LIGHTNING II 3-Axis 数据表](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf) | ✅一手 |
| SCANLAB excelliSCAN | XY | **0 ms**（SCANahead） | [excelliSCAN 数据表](https://optoprim.com/wp-content/uploads/2022/03/Tete-scanner-standard-excelliSCAN-SCANLAB.pdf) | ✅一手 |
| RAYLASE FOCUSSHIFTER DIGITAL II 同型 XY 振镜 | XY | 0.10–0.30 ms | [FOCUSSHIFTER 数据表](https://shop.amstechnologies.com/media/ea/23/0d/1720719683/FOCUSSHIFTER-DIGITAL-II-Prefocusing-Deflection-Units-Raylase-Datasheet.pdf?ts=1734637907) | ✅一手 |

- ⚪本报告推导：Z 滞后比 XY 大 **2–13 倍**（1.3 ms vs 0.10 ms 最坏 13×；0.55 ms vs 0 ms 为无穷大）。故**单一全局激光延迟无法同时对齐 XY 与 Z**；Z 通道必须单独提前（lead/forerun），或让 XY 降速匹配 Z。这与「各轴独立跟踪误差补偿」的厂商标注一致 [来源](https://www.raylase.de/_Resources/Persistent/b/a/6/6/ba66d25112e3d91511322aa417caae73c916557b/Datasheet_SP-ICE-3.pdf) ✅一手
- ⚪本报告推导：因 Z 与 XY 同帧传输（10 µs/帧），**传输层不给 Z 额外延迟**，所以补偿只能来自"设定值在时间上提前"。**❌未找到公开来源**：SCANLAB / RAYLASE 文档中明写"Z 字提前 N 个 microvector 发出"的一手描述。
- Z 执行器自身动力学：国产三维动态聚焦 Z 采用**电流环 / 速度环 / 位置环三闭环 PID**；1% 阶跃响应上升时间由传统电机 **3.35 ms** 改进到 **2.1 ms**（提升 59.5%）；正弦跟随误差约 **±0.03 V（约 3%）**；实验在 45° 斜面 120×80 mm 铝片上打 φ25 mm 圆，测不同焦深处线宽 [徐志翔,陈光胜《三维扫描振镜动态聚焦控制系统建模与仿真》, 建模与仿真 2021, 10(2):311-318](https://pdf.hanspub.org/MOS20210200000_93514507.pdf) ✅一手（开放获取期刊，已读全文；期刊层级较低，引用时请按需降权）

### 2.4 3D 标定向导

- laserDESK **3D Calibration Wizard**：对话框驱动，产出整机个性化 **3D 校正文件 (.ct5)**，"在定位精度与**焦距变化(focal variation)**方面提供最优标定"；支持所有配 varioSCAN 的 3 轴系统，兼容 **RTC5 与 RTC6** [SCANLAB 3D Calibration Wizard](https://www.scanlab.de/sites/default/files/2020-10/3D%20Calibration%20Wizard.pdf) ✅一手
- 覆盖误差项：**Z 轴焦点位置调整**、激光对准倾斜误差、扫描头固有误差（桶形/枕形畸变、振镜非线性）、拉伸因子、**3D 体焦点变化（ABC 系数调整）** [同上](https://www.scanlab.de/sites/default/files/2020-10/3D%20Calibration%20Wizard.pdf) ✅一手
- 流程：步骤 1–3 预备（载入系统 .xml 与 .ct5、核对机械距离）→ **步骤 4 机械任务：调整 Z 轴焦点位置**（打焦点环 → 光学显微镜评估 → 不好则重调）→ 步骤 5–8 标定（倾斜、XY 平面、拉伸因子、ABC，坐标测量机测值回填）[同上](https://www.scanlab.de/sites/default/files/2020-10/3D%20Calibration%20Wizard.pdf) ✅一手
- **correXion pro**："把理论计算的校正文件适配到**个体系统特性**，从而提高激光加工的绝对精度" [SCANLAB correXion pro](https://www.scanlab.de/en/products/calibration/correxion-pro) ✅一手（页面）；工艺为"激光在纸测试片上打标，再与透明网格玻璃母版叠合比对" [Photonics Buyers' Guide](https://www.photonics.com/Company.aspx?CompanyID=13136&PRID=63180) 🟡二手
- excelliSCAN 数据表把 **correXion pro、CalibrationLibrary、3D Calibration Wizard** 并列为"灵活标定方案" [excelliSCAN 数据表](https://optoprim.com/wp-content/uploads/2022/03/Tete-scanner-standard-excelliSCAN-SCANLAB.pdf) ✅一手

---

## 3. 有限 Z 轴 DAC 分辨率的后果

### 3.1 位宽从哪来

| 事实 | 来源 | 标签 |
|---|---|---|
| Novanta LIGHTNING II（2 轴）：**`Command Resolution: 24-bit (GSB) or 16-bit (XY2-100)`** | [LIGHTNING II 数据表](https://www.optoprim.de/PDF/CTI/CTI_Lightning-II_Datasheet.pdf) | ✅一手 |
| LIGHTNING II（3 轴，含 DFM）：**Command Resolution 24-bit**；采用 **24-bit 低漂移编码器技术**，Position Resolution 24-bit | [LIGHTNING II 3-Axis 数据表](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf) / [2-Axis 数据表](https://www.optoprim.de/PDF/CTI/CTI_Lightning-II_Datasheet.pdf) | ✅一手 |
| RAYLASE FOCUSSHIFTER DIGITAL II：**XY2-100-E 16-Bit → 12 µrad；SL2-100 20-Bit → 0.76 µrad** | [FOCUSSHIFTER 数据表](https://shop.amstechnologies.com/media/ea/23/0d/1720719683/FOCUSSHIFTER-DIGITAL-II-Prefocusing-Deflection-Units-Raylase-Datasheet.pdf?ts=1734637907) | ✅一手 |
| SP-ICE-3：20 bit ≈ 镜面定位分辨率 **0.75 µrad** | [SP-ICE-3 数据表](https://www.raylase.de/_Resources/Persistent/b/a/6/6/ba66d25112e3d91511322aa417caae73c916557b/Datasheet_SP-ICE-3.pdf) | ✅一手 |
| SCANLAB varioSCAN II 提供 **SL2-100 与 XY2-100 Enhanced** 两种接口 | [varioSCAN II 数据表](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf) | ✅一手 |
| 标注不一致提示：Novanta 3 轴表写 24-bit 且未提 XY2-100 限制，2 轴表才写出 16/24 二选一 | [3-Axis](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf) vs [2-Axis](https://www.optoprim.de/PDF/CTI/CTI_Lightning-II_Datasheet.pdf) | ✅一手（两表对读） |

### 3.2 数值表：±14 mm 行程下的每 LSB 位移

取 excelliSHIFT 的 **focus range ±14 mm**（配 f = 160 mm F-theta）[excelliSHIFT 数据表](https://www.scanlab.de/sites/default/files/2025-06/SCANLAB-excelliSHIFT-EN.pdf) ✅一手。满行程 = 28 mm 峰峰。公式 **LSB = 满行程 / 2^N**。

| 位宽 | 码数 2^N | 28 mm 峰峰下每 LSB | 14 mm 单程解读下每 LSB | 相对 16 bit |
|---|---|---|---|---|
| 16 bit | 65 536 | **0.427 µm**（427 nm） | 0.214 µm | 1× |
| 18 bit | 262 144 | **0.107 µm**（107 nm） | 0.0534 µm | 4× |
| 20 bit | 1 048 576 | **0.0267 µm**（26.7 nm） | 0.0134 µm | 16× |
| 24 bit | 16 777 216 | **0.00167 µm**（1.67 nm） | 0.000834 µm | 256× |

**算术过程** ⚪本报告推导：
`28 ÷ 65536 = 4.272×10⁻⁴ mm = 0.427 µm`；`28 ÷ 262144 = 1.068×10⁻⁴ mm = 0.107 µm`；`28 ÷ 1048576 = 2.670×10⁻⁵ mm = 0.0267 µm`；`28 ÷ 16777216 = 1.669×10⁻⁶ mm = 0.00167 µm`。

**厂商数字自洽性交叉验证** ⚪本报告推导：FOCUSSHIFTER 的 `12 µrad ÷ 0.76 µrad = 15.8 ≈ 16 = 2⁴`，正是 16→20 bit 的 4 个二进位。两组**独立**厂商标称值互相吻合，验证了"每加 1 bit = 分辨率改善 2 倍"的关系 [来源](https://shop.amstechnologies.com/media/ea/23/0d/1720719683/FOCUSSHIFTER-DIGITAL-II-Prefocusing-Deflection-Units-Raylase-Datasheet.pdf?ts=1734637907) ✅一手。

### 3.3 另两组真实行程

- varioSCANde II 20i 动镜行程 **±2 mm**（4 mm 峰峰）[varioSCAN II 数据表](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf) ✅一手 → ⚪推导：16 bit = `4/65536` = **61.0 nm/LSB**；20 bit = `4/1048576` = **3.81 nm/LSB**。
- FOCUSSHIFTER LT-II-F2-05 聚焦范围 **±19.0 mm**（38 mm 峰峰）[数据表](https://shop.amstechnologies.com/media/ea/23/0d/1720719683/FOCUSSHIFTER-DIGITAL-II-Prefocusing-Deflection-Units-Raylase-Datasheet.pdf?ts=1734637907) ✅一手 → ⚪推导：16 bit = `38/65536` = **0.580 µm/LSB**；20 bit = **0.0362 µm/LSB**。

### 3.4 量化误差的实际后果（分析，非引用）

- ⚪推导：衍射极限焦深（瑞利长度）z_R = π·w₀²/(M²λ)。取 w₀ = 15 µm、λ = 1064 nm、M² = 1 → z_R ≈ **0.66 mm**；取 w₀ = 10 µm → ≈ **0.30 mm**。故 ±14 mm 行程下 16 bit 的 0.427 µm/LSB 仅为焦深的约 **1/700–1/1500**，**对"光斑大小 / 离焦量"影响可忽略**。
- ⚪推导：但用于**绝对深度定位**（3D 微加工层厚控制、玻璃内雕刻）时，0.427 µm 量化步距是直接的深度误差预算项；18 bit（0.107 µm）或 20 bit（0.027 µm）才有余量。
- **对比结论**：varioSCANde II 长期漂移 **< 3 µm / >8 h** [数据表](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf) ✅一手，比 16 bit 的 0.427 µm/LSB **大约 7 倍** → ⚪推导：真实系统中漂移/重复性通常**先于**量化成为瓶颈，**升级 DAC 位宽并不自动改善聚焦精度**。
- **必带的脚注**：SCANLAB 明确声明 varioSCAN II 全部规格**仅指电机本身**，"这些规格对加工场/体内激光束实际定位的影响取决于具体光学配置" [数据表脚注 (1)](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf) ✅一手 —— 引用 µm 级指标时必须带此限定。

---

## 4. Z 轴 / 焦点实际位置的标定方法

### 4.1 (b) 打点 / 烧纸 / 烧蚀法（一手最扎实）

- **Novanta 技术通报 AN00025（厂商应用文档）**：用 CalWizard 做焦点标定时，**烧纸上最白的方格最接近焦点**；但在**黑色阳极氧化铝板**上（功率高到会烧穿纸时），**较暗的方格才代表更佳焦点，最佳焦点位于两个白方格之间** —— 因为白化是激光把黑色阳极氧化层汽化，而更暗处激光更深地侵入金属、更接近真实 Z=0 [来源](https://novantaphotonics.com/wp-content/uploads/2022/03/AN00025_Finding-Focus-Plane-with-CalWizard-on-Black-Anodized-Sheet-Metal....pdf) ✅一手
- **景深量级（决定打点步进）**：CO₂ 激光 + 烧纸时焦深约 **1 mm**；高功率光纤激光（500–1000 W）焦深显著更紧，仅 **100–200 µm**，故**焦点步进必须小于该范围** [同上](https://novantaphotonics.com/wp-content/uploads/2022/03/AN00025_Finding-Focus-Plane-with-CalWizard-on-Black-Anodized-Sheet-Metal....pdf) ✅一手
- 实例：1 kW IPG YLR，**300 µm 步进**打点、显微镜读熔线宽，0.0 中心附近熔线宽约 **80 µm**；该系统工作距离约 210 mm、场 200 mm，**理论焦斑约 20 µm** [同上](https://novantaphotonics.com/wp-content/uploads/2022/03/AN00025_Finding-Focus-Plane-with-CalWizard-on-Black-Anodized-Sheet-Metal....pdf) ✅一手。⚠️**20 µm 是"预期光斑"、80 µm 是实测熔线宽，二者都不可当作"标定精度"引用。**
- 推荐试片材料：黑色阳极氧化铝 **5005/5205**、不锈钢 **SS316/SS312** [同上](https://novantaphotonics.com/wp-content/uploads/2022/03/AN00025_Finding-Focus-Plane-with-CalWizard-on-Black-Anodized-Sheet-Metal....pdf) ✅一手
- **Kapton 膜 / 碳膜烧蚀法**（ICALEO 2002 同行评审会议论文摘要）：Kapton 膜法在光斑 **< 50 µm** 时"太厚"；改用玻璃载玻片上**亚微米厚碳膜**，100 W 脉冲 Nd:YAG + 50 mm 透镜得约 **25 µm** 光斑（约 **2.5× 衍射极限**）[来源](https://doi.org/10.2351/1.5065765) ✅一手（仅摘要）
- 🟡二手实操判据：看红光指示轮廓是否最锐，或听烧灼/爆裂声**最响**时即为焦点 [LightBurn 文档](https://docs.lightburnsoftware.com/legacy/galvo/Focusing) 🟡二手
- 🟡二手补充（arcuscnc，带公式与算例）：Z=0 处光斑最小、fluence 最高、线宽最窄；**可照搬的步骤为在 Z = −5…+5 mm 以 0.5 mm 步距打测试栅格，线宽最窄最黑者即 Z=0**；正/负离焦**视觉症状相同**，方向必须靠该扫描判定；生产中"焦点问题"多因**工件不在设计焦面**（夹具磨损沉降 0.1–0.5 mm、来料高度公差 ±0.3 mm、输送带下垂）[arcuscnc](https://arcuscnc.com/laser-marking-focus/) 🟡二手
  - ⚠️该文算例自相矛盾，**不宜引用其 z_R**：文中称束腰 0.04 mm、z_R ≈ 1.8 mm；⚪按标准式 z_R = π·w₀²/(M²λ)（w₀ = 20 µm、λ = 1064 nm、M² = 1.1）应得 ≈ **1.07 mm**，差约 1.7 倍。但其"离焦 2 mm → 光斑增大约 70%、fluence 降至 33%"的**量级结论稳健**。
- **❌未找到公开来源**：把"最小光斑直径 = Z=0"写成定量精度指标（如 ±X µm）的厂商手册原文。

### 4.2 (a) 刀口法 / 光束焦散

- **ISO 11146-1:2021** 规定激光束宽、发散角、光束传播比测试方法；束宽用**二阶矩 D4σ** 定义，腰位 z₀ = 束宽沿轴极小值处，椭圆度 ≥ 0.87 视为圆分布；正文列出 ISO/TR 11146-3 的三种替代束宽法，含**移动刀口法(moving knife-edge)** 与移动狭缝法 [ISO 11146-1:2021 预览 PDF](https://cdn.standards.iteh.ai/samples/77769/8c3dd35c9da844e0b712dec7df96c53d/ISO-11146-1-2021.pdf) ✅一手
- ⚠️**关键限制**：该免费预览 PDF **仅 11 页、只含第 1–3 章**，第 6–10 章（测量流程本体）不在可读范围内。故下述流程细节**只能引二手**，**不可标注为标准一手**。
- 🟡二手流程细节：≥10 个 z 位置（**半数落在腰位 ±z_R 内、半数在 ±2z_R 外**）；每位置 ≥30 个刀口采样点；z 行程 ≥5×z_R；erf 拟合束宽与真实 D4σ 相差约 **≤5%**；重复性 **±5%**；刀口法因衍射下限 **w₀ ≥ 50λ**（1064 nm ≈ 50 µm）；聚焦镜 F 数宜 > 4 [Photonica](https://www.photonica.io/articles/m2-beam-quality-measurement) 🟡二手
- **刀口法系统性误差**（同行评审、开放获取）：用**实体材料刀口**时，光束与刀口相互作用引入**偏振相关伪影**，使重建剖面的形状与位置偏移畸变，导致反演束径偏差，**必须修正标准流程**；实验刀口为硅光电二极管上 70 nm 厚、3 µm 宽金膜，刀口宽度不确定度 ±50 nm [Frontiers in Physics 2020](https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2020.527734/full) ✅一手
- 刀口法不确定度评估：IEEE MetroXRAINE 2023 用**数值法**评估刀口法测得光斑尺寸的标准不确定度，给出其对**实测光功率不确定度**与**刀口位移不确定度**的灵敏度；因间接测量非线性，解析计算不可行 [IEEE](https://ieeexplore.ieee.org/document/10405731) ✅一手（摘要）。**❌摘要无具体数值，全文付费墙 → 具体不确定度数字未找到公开来源。**

### 4.3 (c) 共焦 / 色散共焦位移传感器

| 传感器 | 轴向分辨率 | 线性度 | 其他 | 来源 | 标签 |
|---|---|---|---|---|---|
| Precitec CHRocodile | **2–4 nm** | **30–400 nm** | 量程 100 µm–1.2 mm；WD 1.0–19 mm；横向 1.3–5 µm；NA 0.33–0.82；控制器最高 **66 kHz** | [Precitec 数据表](https://www.precitec.com/fileadmin/fileadmin/downloads-en/CHRocodile_overview_chromatic_confocal_sensors_datasheet.pdf) | ✅一手 |
| Keyence CL-3000 | **0.003–0.1 µm** | **±0.28 – ±5.5 µm**（高精度量程） | 量程 ±1.3–±35 mm；光斑 ø300–1000 µm；采样 100–1000 µs | [Keyence 规格页](https://www.keyence.com/products/measure/laser-1d/cl-3000/specs/) | ✅一手 |
| Micro-Epsilon confocalDT IFS2405 | 静态 **<2 nm**（0.3 mm 量程）～**<17 nm**（6 mm）；动态 RMS **<18 – <190 nm** | **±0.09 – ±1.2 µm** | 光斑 6–31 µm；最大可测倾角 ±10°–±34° | [Micro-Epsilon 数据表](https://www.micro-epsilon.com/fileadmin/download/excerpts/dax--confocalDT-IFS2405--en-us.pdf) | ✅一手 |

- 🟡二手：Precitec CHRocodile C 精度典型为**量程的 2×10⁻⁴**（200 µm 量程 → 50 nm；1 mm → 200 nm；10 mm → 2 µm）[ManualsLib](https://www.manualslib.com/manual/2867421/Precitec-Chrocodile-C.html) 🟡二手
- **❌未找到公开来源**：把共焦传感器直接闭环用于**振镜 Z 轴焦点标定**并给出标定后残余误差的厂商/标准原文。

### 4.4 (d) 光束分析仪穿过焦点扫焦散

- **Cinogy CinSquare M² Tool（CS200/CS300）**：固定聚焦镜 + **电动平移台** + CinCam 相机式分析仪，按 **ISO 11146-1/2** 测完整焦散，输出 M²、腰位、发散角、腰径、瑞利长度；光谱 250–1800 nm；可测 1/e² 束径 0.5–10 mm；输入功率 ≤20 W；全自动 <1 min（快扫约 30 s）。**精度：典型 2–3%；腰尺寸/位置 3–5%** [Cinogy](http://www.cinogy.com/html/cinsquare_m2_tool.html) ✅一手
- **DataRay**：ISO 11146 合规；**相机式**适合焦斑 **≥32 µm**（190–1350 nm）、≥150 µm（1350 nm–2 µm）、≥170 µm（2–16 µm）；**扫描狭缝式**适合焦斑 **≥2 µm**（190–2500 nm）[DataRay](https://dataray.com/applications/focus-measurement) ✅一手
- **❌无法打开**：Ophir/Spiricon **BeamWatch** 官方数据表 —— ophiropt.com 三页均 JS 渲染（curl 仅得 2457 字节空壳），MKS CDN 的 `BeamWatch_2.pdf` 返回机器人验证页，DirectIndustry 镜像返回 HTML。**BeamWatch 一手指标未能取得，请勿引用。**

### 4.5 (e) 软件焦点偏置标定（一手）

- SCANLAB **3D Calibration Wizard 步骤 4「Adjust the Z-axis focal position」**：打**焦点环(focus ring)** → **光学显微镜评估** → good/bad 循环 → 进入 Step 5；校正项含 Z 轴焦点位置、倾斜、XY 平面、拉伸因子、**3D 体焦点变化（ABC 系数）**，最终生成整机个性化 **.ct5**；兼容 RTC5/RTC6 [SCANLAB 3D Calibration Wizard](https://www.scanlab.de/sites/default/files/2020-10/3D%20Calibration%20Wizard.pdf) ✅一手
- ⚠️该文档**未给出任何量化精度指标**，仅称"减少误差来源、提升定位精度与焦点一致性" [同上](https://www.scanlab.de/sites/default/files/2020-10/3D%20Calibration%20Wizard.pdf) ✅一手 → **❌ SCANLAB 未公开焦点标定后的量化精度。**
- RAYLASE **MULTI POINT EDITOR / \*.fc3 场校正**：校正文件的轴负责 **XY 位置以及预聚焦单元或 FOCUSSHIFTER 的 Z 轴**；**焦点标定只需为 Z 轴填一张表 —— 填的不是坐标，而是每个网格位置"最清晰（best in focus）线条的序号"**，中心线序号为 0，若最佳焦点在两条线之间**可填浮点数（如 1,5）**；若校正文件提供 3D 体，可在**多个焦点层**标定，**建议至少标顶层与底层、中间层插值**；另有**绝对插值**模式（直接给 Z 透镜相对行程的绝对位置），**该模式目前仅支持 Z 轴** [RAYLASE MPE 手册](https://software.raylase.de/rpi/RAYLASE/MPE/MN_MPE_EN.pdf) ✅一手
- 🟡二手：3D 动态聚焦 Z 的实现分三类 —— **音圈电机(VCM)**、**振镜电机 + 连杆动态轴**、**非球面反射光路**；其中 VCM F1 用高精度直线光栅反馈，**位置分辨率最高 25 bit** [Scanner Optics](https://www.scanneroptics.com/3d-dynamic-focus-galvo-scanner-for-laser-engraving-drilling-and-3d-printing-principles-and-performance-benefits.html) 🟡二手

---

## 5. 失效模式与诊断

### 5.1 (a) Z 轴卡死 / 抱死

- 振镜电机"不自锁"排查链（二手但步骤具体、可操作）：查接线**断路/短路**、保险丝、驱动板指示灯是否绿/黄（不亮或红 = 故障）；断电拔驱动板电源线，用万用表量输入端各端子是否 **24 V**；接负载后再量；异常则空载量开关电源输出 → 判定电源故障；上电正常时振镜系统通常**响两声**，无声则手推振镜片，若不自锁 → 驱动板损坏；用已知完好的驱动板/电机**互换法**定位到板或电机 [Scanner Optics 故障指南](https://www.scanneroptics.com/common-issues-and-solutions-for-laser-scanner-galvanometer.html) 🟡二手
- "电机不摆动"：查打标卡是否有控制信号输出、信号线是否接反/断线；否则判驱动板损坏 [同上](https://www.scanneroptics.com/common-issues-and-solutions-for-laser-scanner-galvanometer.html) 🟡二手
- **风险警告**：振镜**不可长期处于啸叫状态，否则电机可能烧毁** [同上](https://www.scanneroptics.com/common-issues-and-solutions-for-laser-scanner-galvanometer.html) 🟡二手
- 控制器侧：SP-ICE-3 进入 "operating error state" 后**无法执行列表**（会抛异常），但其余 API 仍可用；状态含初始化失败、配置失败、`ScannerMonitoringRuntimeError`；须查卡上错误日志并用 `ResetOperatingState` 清除 [SP-ICE-3 手册 18.2](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/765ABC4A-1A84-EB54-66CE-AACDCB4A9745.htm) ✅一手
- **❌未找到公开来源**：SCANLAB varioSCAN / excelliSHIFT 或 RAYLASE FOCUSSHIFTER 的 Z 轴"卡死"厂方服务通告或故障树。以上为同族振镜/驱动器通用机制，**不能直接等同于动态聚焦 Z 执行器**。

### 5.2 (b) 回零 / 参考位置丢失

- 动态聚焦 Z 的位置语义由**参考平面**定义：RAYLASE 规定"卡参考平面"位于 3D 加工场正中；要使"用户参考平面"与"光学参考平面"重合，需把 FC3 文件头里的 **`FieldOffset.Z`** 作为 `FieldTransform` 的 Z 参数使用 [SP-ICE-3 手册 7.1.7](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/CE15CBDB-355A-4F69-A5B0-97611F5D1550.htm) ✅一手 → ⚪推论：**该 Z 偏移一旦丢失或误置，整个 3D 场会沿光轴整体平移**，现象与"回零丢失"一致。
- RAYLASE 标准 FC3 对 FOCUSSHIFTER 把 `FieldOffset.Z` 设为"卡参考平面与光学参考平面之差"；对 AXIALSCAN 则假定光学参考平面位于 3D 加工场**顶部** [同上](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/CE15CBDB-355A-4F69-A5B0-97611F5D1550.htm) ✅一手
- 增量式 vs 绝对式零点（**机床领域类比，非振镜专属**）：绝对坐标方式每次上电**不需回零**，零点建立后由后备电池保存在 SRAM，断电不丢失 [百度文库：FANUC 加工中心 Z 轴无法回原点](https://wenku.baidu.com/view/a39a2d2351ea551810a6f524ccbff121dd36c5e0.html) 🟡二手（CNC 机床，**不可直接外推到振镜**）
- ⚪推论：RAYLASE 的**绝对插值模式仅支持 Z 轴**（见 §4.5）[MPE 手册](https://software.raylase.de/rpi/RAYLASE/MPE/MN_MPE_EN.pdf) ✅一手 —— 说明 Z 轴恰恰是那个"位置语义特殊、需要绝对参考"的通道，是"回零丢失"问题集中在 Z 上的结构性原因。
- **❌未找到公开来源**：任何厂商文档明确写"varioSCAN / FOCUSSHIFTER 上电后丢失回零/参考位置"。此条在公开资料中**无一手依据**。

### 5.3 (c) 聚焦漂移 / 长期漂移

| 器件 | 漂移指标 | 来源 | 标签 |
|---|---|---|---|
| SCANLAB varioSCANde II（Z 电机） | **长期漂移 (>8 h) < 3 µm**；重复性 < 0.5 µm；动镜典型速度 ≥280 / ≥140 mm/s | [varioSCAN II 数据表](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf) | ✅一手 |
| RAYLASE FOCUSSHIFTER DIGITAL II | 长期漂移 8 h（无水冷）**< 60 µrad**；有水冷 **< 40 µrad**；最大增益漂移 **15 ppm/K**；最大零偏漂移 **10 µrad/K**；位置噪声 < 4.5 µrad(RMS)；重复性 < 2.0 µrad | [FOCUSSHIFTER 数据表](https://shop.amstechnologies.com/media/ea/23/0d/1720719683/FOCUSSHIFTER-DIGITAL-II-Prefocusing-Deflection-Units-Raylase-Datasheet.pdf?ts=1734637907) | ✅一手 |
| Novanta LIGHTNING II | **热漂移 < 2 µrad/°C**；长期漂移 < 10 µrad（预热 30 min 后 8 h）；重复性 < 2 µrad | [3-Axis 数据表](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf) | ✅一手 |
| 漂移测试条件（必须一并引用） | 30 min 预热后、**恒温环境**、指定工艺负载；"各轴、光学角度" | [FOCUSSHIFTER 脚注 1/2](https://shop.amstechnologies.com/media/ea/23/0d/1720719683/FOCUSSHIFTER-DIGITAL-II-Prefocusing-Deflection-Units-Raylase-Datasheet.pdf?ts=1734637907) / [LIGHTNING II 脚注 3](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf) | ✅一手 |
| 无水温控时漂移值会**增大** | "SUPERSCAN 可不带温控(N)运行，其结果是漂移值可能上升" | [FOCUSSHIFTER 数据表](https://shop.amstechnologies.com/media/ea/23/0d/1720719683/FOCUSSHIFTER-DIGITAL-II-Prefocusing-Deflection-Units-Raylase-Datasheet.pdf?ts=1734637907) | ✅一手 |
| 光学侧热透镜机理与时间常数：高占空比打标（连续 > 20–60 min）使 F-theta 镜吸收微量激光功率升温 → 折射率变化 → **有效焦距偏移**，焦点上下移动；**症状为班次开始时质量良好、30–60 min 内渐变劣化、待镜片热平衡后在较低质量水平稳定** | [arcuscnc](https://arcuscnc.com/laser-marking-focus/) | 🟡二手 |
| 热漂移诊断法：**班次开始时打一试片，30 min 后再打同一试片比较线宽**；明显变宽即发生热透镜。对策：生产前留 **20–30 min 预热**，以预热后焦点作为生产基准；>50 W 系统考虑镜片主动冷却 | [同上](https://arcuscnc.com/laser-marking-focus/) | 🟡二手 |
| **易混淆项**：离焦 → 线宽**变大**；镜片/保护窗污染 → 线宽**基本不变**但深度与黑度下降 | [同上](https://arcuscnc.com/laser-marking-focus/) | 🟡二手 |
| 热漂移症状（另一二手源）：加工中标记**逐渐变浅**、调焦改善不明显、**冷却后恢复**、长时生产更明显 | [Thunder Laser 知识库](https://support.thunderlaser.com/portal/en/kb/articles/understanding-thermal-lensing-thermal-drift-and-heat-accumulation-in-laser-marking-systems) | 🟡二手（页面 JS 渲染，**仅读到搜索摘要**） |

⚪推导：varioSCANde II 20i 的 Z 光杠杆 —— 同配置下动镜行程 ±2 mm 对应焦点位移 ±32 mm（20-20 FT 配置）[数据表](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf) ✅一手 → 约 **16×** 放大。故 16 bit 在该配置折算到焦点约 **0.98 µm/LSB**，与 < 3 µm/8 h 的长期漂移**同量级** —— 即此配置下量化与漂移需同时纳入误差预算。（注：数据表 "Focus shift" 一栏按光学配置分列，引用前请核对具体型号列。）

### 5.4 (d) 异响 / 啸叫

- 啸叫处置链：先查打标卡信号、接线、**外部干扰**；仍在啸叫则调整振镜驱动板**滤波板上的电位器**；若无法消除需**返厂精调**；**切勿长期处于啸叫状态，否则可能烧毁振镜电机** [Scanner Optics](https://www.scanneroptics.com/common-issues-and-solutions-for-laser-scanner-galvanometer.html) 🟡二手
- "标记没封口 / 封过头"类同步问题：先改 **jump delay、关光延时**等参数；均无效说明振镜未完全标定，应返厂；**不要随意乱调电位器** [同上](https://www.scanneroptics.com/common-issues-and-solutions-for-laser-scanner-galvanometer.html) 🟡二手
- RAYLASE 侧等效手段：`TrackingError`（过短/过长都恶化质量）、`LaserTriggerDelay`、`JumpDelay`/`MarkDelay`/`PolyDelay` 均配"过大/过小"症状图 [SP-ICE-3 手册 7.1.6](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/e1516d08-fc0e-4025-9c02-e600785ec5e2.htm) ✅一手
- 控制器端可观测性：SP-ICE-3 的 **Scanner Monitoring** 可独立监测偏转单元，失败时置 `ScannerMonitoringRuntimeError` [SP-ICE-3 手册 18.2](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/765ABC4A-1A84-EB54-66CE-AACDCB4A9745.htm) ✅一手；数据表称可记录最多 **2400 万条**来自偏转单元的测量值（目标/实际位置等），用于开发优化与运行监测 [SP-ICE-3 数据表](https://www.raylase.de/_Resources/Persistent/b/a/6/6/ba66d25112e3d91511322aa417caae73c916557b/Datasheet_SP-ICE-3.pdf) ✅一手
- **❌未找到公开来源**：动态聚焦 Z 轴（varioSCAN / excelliSHIFT / FOCUSSHIFTER）的噪声或振动 dB 限值，以及专用异响故障树。

---

## 6. 核验清单

**✅ 已实际下载并打开读取**
- SCANLAB：RTC4 数据表、SCANahead 白皮书、3D Calibration Wizard、varioSCAN II、excelliSHIFT、excelliSCAN（Optoprim 镜像）
- RAYLASE：SP-ICE-3 数据表、FOCUSSHIFTER DIGITAL II、SS-III XY2-100-E 文档、SP-ICE-3 手册 10 个页面（8.1 / 8.2.3 / 8.3 / 7.1.6 / 7.1.7 / 7.1.9 / 7.3.2 / 7.3.2.1 / 18 / 18.2）、MULTI POINT EDITOR 手册
- Novanta：LIGHTNING II 2 轴与 3 轴数据表、技术通报 **AN00025**
- 其他一手：Ray-Motion XY2-100 数据表、ISO 11146-1:2021 预览 PDF（**仅第 1–3 章**）、Frontiers in Physics 2020、Cinogy CinSquare 页、DataRay 页、Keyence CL-3000 规格页、Precitec CHRocodile 数据表、Micro-Epsilon IFS2405 数据表
- 论文：Hans《建模与仿真》中文论文全文；IEEE MetroXRAINE 2023（**仅摘要**）；ICALEO 2002（**仅摘要**）

**🟡 仅读到搜索摘要 / 页面未渲染出正文**
- sigrok xy2-100 解码器页、DirectIndustry intelliSCAN IV 页、GitHub sirius2、Photonics correXion pro 条目、Thunder Laser 知识库（JS 渲染，2457 字节空壳）、LightBurn 文档、ManualsLib Precitec、Ophir 光束宽度准确度页
- **已打开并完整读取**的二手页：Scanner Optics 故障指南、arcuscnc 焦点问题页、Scanner Optics 3D 动态聚焦页

**❌ 无法打开 / 内容不可用（未编造）**
- `https://www.scanlab.de/.../12_RTC6_control%20boards.pdf` —— 返回 HTML 错误页而非 PDF → **RTC6 数据表原文未获取**（RTC6 事实仅来自 SCANahead 白皮书与 excelliSCAN 数据表）
- `https://www.aaronvose.net/Quantronix_Osprey/xy2_100_specification.pdf` —— 连接失败
- `https://raw.githubusercontent.com/georgemihaila/xy2-100/.../xy2_100_specification.pdf` —— 连接失败
- `https://www.politesi.polimi.it/bitstream/10589/167367/...pdf` —— 端口 443 连接失败 / 后被重定向为 HTML
- `https://files.stankee.ru/docs/sino-galvo/SINO-GALVO SG2208 ... .pdf` —— 超时
- `https://www.precitec.com/.../CHRocodile_overview_chromatic_confocal_sensors_datasheet.pdf` —— 本机 TLS 握手失败 2 次（该数据表由并行核查成功下载并读出数值）
- **全部 Ophir / BeamWatch URL**：ophiropt.com 三页均 JS 渲染；`api.p1.mks.com` 的 `BeamWatch_2.pdf` 返回 6074 字节机器人验证页；DirectIndustry 镜像返回 HTML → **BeamWatch 官方数据表未取得**
- IEEE Xplore 全文 —— 付费墙

**⚠️ 三处公开资料空白（写"未找到"时可直接引用）**
1. **SCANLAB 与 RAYLASE 均未公开焦点标定后的量化精度** —— 两家的标定文档只讲流程，无精度数字。
2. **ISO 11146-1 免费预览只到第 3 章** —— 测量流程细节（z 位置数、采样点数、拟合偏差、重复性）**只能引二手文章**，不能标注为标准一手；IEEE 刀口不确定度论文的具体数值亦未公开。
3. **动态聚焦 Z 轴的"卡死 / 回零丢失 / 异响 dB 限值"无厂商一手故障树** —— 现有可引材料均为同族振镜/驱动器通用机制或机床领域类比，**不可直接外推**。

---

## C. 标定方法专题（焦斑法 / 刀口法 / 共焦法）

# Q4 调研：激光振镜扫描系统 Z 轴（动态聚焦）实际焦点位置标定方法

> 调研方式：仅记录**实际下载并打开**的资料。`web_fetch` 在本环境被封锁，全部通过 `curl` 抓取 PDF/HTML 后本地解析（`pdftotext` / Python）。未能打开的 URL 在末尾单独列出，**未编造任何数据**。

---

## (a) 刀口法 / 刀口扫描光束焦散（caustic）——ISO 11146-1/-2

- **ISO 11146-1:2021（第二版，2021-07 发布）** 规定激光束宽、发散角、光束传播比的测试方法；束宽采用**二阶矩 D4σ 定义**，光束腰位置 z₀ 定义为束宽沿轴取极小值处；椭圆度 ≥ 0,87 视为圆分布。[来源](https://cdn.standards.iteh.ai/samples/77769/8c3dd35c9da844e0b712dec7df96c53d/ISO-11146-1-2021.pdf) ✅一手
- 该标准正文明确列出 **ISO/TR 11146-3 中的三种替代束宽测量方法**：可变光阑法、**移动刀口法（moving knife-edge）**、移动狭缝法；标准章节结构为 6 测量装置与设备 / 7 束宽 / 8 发散角 / 9 腰位置与传播比联合测定 / 10 测试报告。[来源](https://cdn.standards.iteh.ai/samples/77769/8c3dd35c9da844e0b712dec7df96c53d/ISO-11146-1-2021.pdf) ✅一手
- ⚠️ 重要限制：该免费预览 PDF **共 11 页，实际只含封面+第 1～5 页（第 1～3 章）**，Clause 6～10（即测量流程本体）**不在可读范围内**。因此下文"≥10 个 z 位置、半数在 ±z_R 内"等流程细节只能引二手来源。
- 刀口法不确定性：IEEE MetroXRAINE 2023 论文提出用**数值方法评估刀口法测得光斑尺寸的标准不确定度**，得到光斑尺寸不确定度对**实测光功率不确定度**与**刀口位移不确定度**等输入量的灵敏度；因刀口法间接测量是非线性的，解析计算不可行，故基于实验数据数值求解，并对两种不同激光源做了灵敏度计算。[来源](https://ieeexplore.ieee.org/document/10405731) ✅一手（同行评审论文，摘要原文经 Semantic Scholar API 读取，DOI 10.1109/MetroXRAINE58569.2023.10405731）
- ❌该论文**摘要中未给出具体不确定度数值**，全文在 IEEE 付费墙后未能获取 → ❌未找到公开的具体数值来源。
- 刀口法**系统性误差**（同行评审、开放获取）：使用**纯材料刀口**（金属、半导体等）时，光束与刀口的相互作用会引入**偏振相关的伪影**，导致重建光束剖面的**形状与位置发生偏移和畸变**，进而使**反演出的束径出现偏差**；因此**必须对标准刀口法评估流程做修正**。实验中刀口为硅光电二极管基底上厚 70 nm、宽 3 μm 的金膜，刀口宽度测量不确定度 ±50 nm。[来源](https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2020.527734/full) ✅一手
- 🟡二手流程细节：ISO 11146-1 要求**至少 10 个 z 位置**——**一半落在腰位 ±z_R 内、一半落在 ±2z_R 之外**；每个位置**≥30 个刀口采样点**；z 轴行程 ≥5×z_R；对高斯束用 erf 拟合所得束宽与真实 D4σ **相差约 5% 以内**；重复测量一致性 **±5%**；刀口法因衍射存在下限 **w₀ ≥ 50λ**（1064 nm 时约 50 μm）；聚焦镜 F 数宜 >4。[来源](https://www.photonica.io/articles/m2-beam-quality-measurement) 🟡二手
- 🟡二手（仅搜索摘要，页面未能打开）：Ophir 称"用可变光阑时，D4σ 测量比刀口法略更准确"。[来源](https://www.ophiropt.com/en/n/beam-width-measurement-accuracy) 🟡二手

---

## (b) 焦点光斑 / 烧纸法（打点法）/ 烧蚀法

- **Novanta 技术通报 AN00025（主源，厂商应用文档）**：CalWizard 焦点标定用**烧纸**时，**最白的方格代表最接近焦点**；但在黑色阳极氧化铝板上（激光功率太高、烧纸会被烧穿时），**较暗的方格才代表更佳焦点**，最佳焦点位于**两个白方格之间**。原因是白化是激光把黑色阳极氧化层汽化掉，而更暗的方格处激光能量**更深地侵入金属、接近 0.0 中心焦点标记**。[来源](https://novantaphotonics.com/wp-content/uploads/2022/03/AN00025_Finding-Focus-Plane-with-CalWizard-on-Black-Anodized-Sheet-Metal....pdf) ✅一手
- 同一文档给出**景深（DoF）量级**：CO₂ 激光 + 烧纸时焦点深度约 **1 mm**；高功率光纤激光（500 W～1000 W）DoF **显著更紧，约 100 μm～200 μm**，因此**焦点步进必须小于该范围**。[来源](https://novantaphotonics.com/wp-content/uploads/2022/03/AN00025_Finding-Focus-Plane-with-CalWizard-on-Black-Anodized-Sheet-Metal....pdf) ✅一手
- 实例（IPG YLR 1000，1 kW）：以 **300 μm** 步进打点，用显微镜观察熔线宽度判读；0.0 中心附近熔线宽约 **80 μm**；该 3 轴系统工作距离约 210 mm、场 200 mm，理论焦斑约 **20 μm**，但因金属熔化行为，实测线宽可比光斑更宽。[来源](https://novantaphotonics.com/wp-content/uploads/2022/03/AN00025_Finding-Focus-Plane-with-CalWizard-on-Black-Anodized-Sheet-Metal....pdf) ✅一手（注意：**20 μm 是"预期"光斑，80 μm 是实测熔线宽，二者不可混为标定精度**）
- 推荐材料：黑色阳极氧化铝 **5005/5205**、不锈钢 **SS316/SS312**（熔化更少、更易分辨小步进下的焦点差异）。[来源](https://novantaphotonics.com/wp-content/uploads/2022/03/AN00025_Finding-Focus-Plane-with-CalWizard-on-Black-Anodized-Sheet-Metal....pdf) ✅一手
- **Kapton 膜 / 碳膜烧蚀法**（同行评审会议论文 ICALEO 2002，摘要原文）：Kapton 膜法是常用的工艺控制手段，但在光斑 **<50 μm** 时 Kapton 膜"太厚"；改用玻璃显微镜载玻片上**亚微米厚碳膜**。用 100 W 脉冲 Nd:YAG、50 mm 焦距透镜，获得约 **25 μm** 光斑（约 **2.5× 衍射极限**），并比较了碳-玻璃法、Kapton 膜法与 CCD 相机法。[来源](https://doi.org/10.2351/1.5065765) ✅一手（摘要）
- 🟡二手旁证：光纤激光打标/雕刻机的取焦实操多为**试错+感官判据**——观察红光指示的轮廓是否最锐利，或听烧灼/爆裂声**最响**时即为焦点；镜头标称焦距（F160/F330）因制造差异仍需微调。[来源](https://docs.lightburnsoftware.com/legacy/galvo/Focusing) 🟡二手
- ❌未找到公开来源：把"最小光斑直径对应 Z=0"写成定量精度指标（如 ±X μm）的厂商手册原文。

---

## (c) 共焦 / 色散共焦位移传感器测焦点位置

- **Precitec CHRocodile 色散共焦点传感器**（厂商数据表）：轴向分辨率 **2～4 nm**；线性度 **30～400 nm**；量程 **100 μm～1.2 mm**；工作距离 **1.0～19 mm**；横向分辨率 **1.3～5 μm**；NA **0.33～0.82**。控制器 CHRocodile 2 S/2 SE 测量速率最高 **66,000 Hz**，2×模拟输出（±10 V，16 bit），RS-422/Ethernet，可在干涉模式与色散共焦模式间切换。[来源](https://www.precitec.com/fileadmin/fileadmin/downloads-en/CHRocodile_overview_chromatic_confocal_sensors_datasheet.pdf) ✅一手
- 🟡二手（Precitec 官方手册文本，但托管在第三方站点）：CHRocodile C 精度典型值为**量程的 2×10⁻⁴**；具体探头为 200 µm 量程 → **50 nm**，1 mm → **200 nm**，4 mm → **0.8 µm**，10 mm → **2 µm**（实验性指标，对应高度偏差绝对值的最大值）。[来源](https://www.manualslib.com/manual/2867421/Precitec-Chrocodile-C.html) 🟡二手
- **Keyence CL-3000 共焦位移传感器**（厂商规格页）：分辨率 **0.003～0.1 μm**；线性度（高精度量程）**±0.28～±5.5 μm**、标准量程 **±0.36～±5.5 μm**；量程 **±1.3～±35 mm**；光斑直径 **ø300～ø1000 μm**；采样周期 100/200/500/1000 μs 四档；探头 IP67。[来源](https://www.keyence.com/products/measure/laser-1d/cl-3000/specs/) ✅一手
- **Micro-Epsilon confocalDT IFS2405**（厂商数据表）：静态分辨率 **<2 nm**（0.3 mm 量程）～**<17 nm**（6 mm）；动态（RMS）**<18～<190 nm**；线性度（位移）**±0.09～±1.2 μm**、厚度 **±0.18～±2.4 μm**；光斑 **6～31 μm**；NA 0.22～0.60；最大可测倾角 ±10°～±34°。[来源](https://www.micro-epsilon.com/fileadmin/download/excerpts/dax--confocalDT-IFS2405--en-us.pdf) ✅一手
- 🟡二手：Precitec CHRocodile 在激光加工中被用于 3D 计量与焊接，CHRocodile Mini 达每秒 4,000 次（可选升级 10,000 Hz），CLS 色散共焦线传感器可达 **192 个同时测量点**。[来源](https://www.expo21xx.com/additive_manufacturing/14775_st3_laser_processing/default.htm) 🟡二手
- ❌未找到公开来源：把共焦传感器直接闭环用于**振镜 Z 轴焦点标定**、并给出标定后残余误差的厂商/标准原文。

---

## (d) 光束分析仪（beam profiler）穿过焦点扫焦散

- **Cinogy CinSquare M² Tool（CS200/CS300）**：由**固定聚焦镜 + 电动平移台 + CinCam 相机式光束分析仪**构成，按 **ISO 11146-1/2** 测量完整光束焦散，给出 M²、腰位置、发散角、腰径、瑞利长度，支持 2D/3D 焦散拟合；光谱 250～1800 nm；可测 1/e² 束径 **0.5～10 mm**；输入功率最高 20 W；全自动测量 <1 分钟（快扫约 30 s）。**精度：典型 2～3%；腰尺寸/位置等 3～5%**。[来源](http://www.cinogy.com/html/cinsquare_m2_tool.html) ✅一手
- **DataRay**：ISO 11146 合规的光束分析仪；相机式适合**焦斑 ≥32 μm**（190～1350 nm）、≥150 μm（1350 nm～2 μm）、≥170 μm（2～16 μm）；扫描狭缝式适合**焦斑 ≥2 μm**（190～2500 nm）；高功率需重成像/放大时用 ILMS（集成高功率取样器）。[来源](https://dataray.com/applications/focus-measurement) ✅一手
- ❌未找到公开来源：Ophir/Spiricon BeamWatch 的官方数据表（说明见下）。

---

## (e) 软件焦点偏置标定

- **SCANLAB laserDESK 3D Calibration Wizard**（厂商 PDF）：**第 4 步（Step 4）机械任务即"Adjust the Z-axis focal position"**，流程为**打标焦点环（focus ring）→ 用光学显微镜评估 → 判断 good/bad 并循环调整 → 进入 Step 5**。可校正项包括 **Z 轴焦点位置调整**、激光对准倾斜误差、扫描头固有误差（桶形/枕形畸变、振镜非线性）、拉伸因子、**3D 体焦点变化（ABC 系数调整）**；第 1～3 步为预备、第 5～8 步为标定任务（倾斜、XY 平面、拉伸因子、ABC），最终生成整机的**个性化 3D 校正文件（.ct5）**；兼容 RTC5/RTC6，适用于配 varioSCAN 的所有 3 轴扫描系统。[来源](https://www.scanlab.de/sites/default/files/2020-10/3D%20Calibration%20Wizard.pdf) ✅一手
- ⚠️该文档（2017-11 版）**未给出任何量化精度指标**，仅称"减少误差来源、提升定位精度与焦点一致性" → ❌未找到公开的具体精度数值。
- **RAYLASE MULTI POINT EDITOR / *.fc3 场校正**（厂商手册 V2.2）：MPE 用于打开、查看、编辑、保存场校正文件（**\*.fc3 / \*.gcd**）与功率校正文件（**\*.pc3**），以适配各激光系统的实际光机状态；校正文件的轴**负责 XY 位置以及预聚焦单元或 FOCUSSHIFTER 的 Z 轴**，还可控 RAYSPECTOR 的 SensorZ、AM-MODULE 的 ZoomZ 与 Aux 轴。[来源](https://software.raylase.de/rpi/RAYLASE/MPE/MN_MPE_EN.pdf) ✅一手
- RAYLASE **焦点标定操作**：对预聚焦偏转单元**建议先做焦点标定**；在 Measurements 页**只需为 Z 轴填一张表**——与场标定（填实测坐标）不同，**填的是每个网格位置"最清晰（best in focus）线条的序号"**，中心线序号为 0；若最佳焦点不在某条线上而在两条线之间，**可填浮点数，例如 1,5**。若校正文件提供 3D 体，**焦点标定与扫描场标定可在多个焦点层进行，建议至少标定顶层与底层，中间层由插值得到**。[来源](https://software.raylase.de/rpi/RAYLASE/MPE/MN_MPE_EN.pdf) ✅一手
- RAYLASE 还支持**绝对插值**模式：直接提供 Z 透镜相对其行程的**绝对位置**，此时计算模式须设为"absolute interpolation"并选定 Z 轴；**该模式目前仅支持 Z 轴**。[来源](https://software.raylase.de/rpi/RAYLASE/MPE/MN_MPE_EN.pdf) ✅一手
- RAYLASE **SP-ICE 3** 固件的所有矢量处理函数**默认即按 3D（XYZ）处理**，2D 函数等价于 Z=0；RAYLASE 现有两大 3D 扫描系统为 **FOCUSSHIFTER 与 AXIALSCAN**。[来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/254aa48e-536e-4bbe-a569-fe200cc6a2ac.htm) ✅一手
- 🟡二手（厂商技术博客）：3D 动态聚焦 = XY 振镜 + 实时 Z 轴调焦机构，Z 与 XY 实时协同；实现方式分三类——**音圈电机（VCM）**、**振镜电机 + 连杆动态轴**（旋转转直线）、**非球面反射光路**。其中 VCM F1 采用高精度直线光栅反馈，**位置分辨率最高 25 bit**。[来源](https://www.scanneroptics.com/3d-dynamic-focus-galvo-scanner-for-laser-engraving-drilling-and-3d-printing-principles-and-performance-benefits.html) 🟡二手

---

## 精度指标汇总表

| 方法 | 典型精度 / 分辨率 | 来源标签 |
|---|---|---|
| 刀口法（高斯 erf 拟合 vs 真实 D4σ） | 差异约 ≤5%；重复性 ±5% | 🟡二手 [来源](https://www.photonica.io/articles/m2-beam-quality-measurement) |
| 刀口法适用下限 | w₀ ≥ 50λ（1064 nm ≈ 50 μm） | 🟡二手 [来源](https://www.photonica.io/articles/m2-beam-quality-measurement) |
| 刀口法不确定度（数值评估法） | ✅方法有，❌具体数值未公开 | ✅一手 [来源](https://ieeexplore.ieee.org/document/10405731) |
| 烧纸/阳极氧化板判焦（CalWizard） | 步进 300 μm；CO₂ DoF≈1 mm；光纤 DoF 100～200 μm | ✅一手 [来源](https://novantaphotonics.com/wp-content/uploads/2022/03/AN00025_Finding-Focus-Plane-with-CalWizard-on-Black-Anodized-Sheet-Metal....pdf) |
| Kapton/碳膜烧蚀测光斑 | 可测至约 25 μm（≈2.5× 衍射极限）；<50 μm 时 Kapton 已偏"厚" | ✅一手 [来源](https://doi.org/10.2351/1.5065765) |
| 色散共焦（Precitec CHRocodile） | 轴向分辨率 2～4 nm；线性度 30～400 nm | ✅一手 [来源](https://www.precitec.com/fileadmin/fileadmin/downloads-en/CHRocodile_overview_chromatic_confocal_sensors_datasheet.pdf) |
| 色散共焦（Keyence CL-3000） | 分辨率 0.003～0.1 μm；线性度 ±0.28～±5.5 μm | ✅一手 [来源](https://www.keyence.com/products/measure/laser-1d/cl-3000/specs/) |
| 色散共焦（Micro-Epsilon IFS2405） | 静态 <2～<17 nm；动态 <18～<190 nm；线性度 ±0.09～±1.2 μm | ✅一手 [来源](https://www.micro-epsilon.com/fileadmin/download/excerpts/dax--confocalDT-IFS2405--en-us.pdf) |
| 分析仪扫焦散（Cinogy CinSquare） | **典型 2～3%；腰尺寸/位置 3～5%** | ✅一手 [来源](http://www.cinogy.com/html/cinsquare_m2_tool.html) |
| 相机式分析仪最小可测焦斑（DataRay） | 32 μm（190–1350 nm）／扫描狭缝 2 μm | ✅一手 [来源](https://dataray.com/applications/focus-measurement) |
| SCANLAB 3D Calibration Wizard（Step 4） | 流程明确（焦点环+显微镜判读），**未公布量化精度** | ✅一手 [来源](https://www.scanlab.de/sites/default/files/2020-10/3D%20Calibration%20Wizard.pdf) |
| RAYLASE 焦点标定（.fc3） | 人工判读"最清晰线序号"，允许 0.5 级次插值；多层插值 | ✅一手 [来源](https://software.raylase.de/rpi/RAYLASE/MPE/MN_MPE_EN.pdf) |

---

## 实际验证 vs 无法打开的 URL

**✅ 成功下载并读取内容：**
1. `https://cdn.standards.iteh.ai/samples/77769/8c3dd35c9da844e0b712dec7df96c53d/ISO-11146-1-2021.pdf` — 560 KB，11 页预览（仅第 1～5 页）
2. `https://www.scanlab.de/sites/default/files/2020-10/3D%20Calibration%20Wizard.pdf` — 754 KB，全文
3. `https://software.raylase.de/rpi/RAYLASE/MPE/MN_MPE_EN.pdf` — 2.4 MB，全文（RAYLASE 网站 HTTPS 正常，无需重试）
4. `https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/254aa48e-536e-4bbe-a569-fe200cc6a2ac.htm` — 6 KB
5. `https://www.photonica.io/articles/m2-beam-quality-measurement` — 629 KB HTML
6. `https://www.precitec.com/fileadmin/fileadmin/downloads-en/CHRocodile_overview_chromatic_confocal_sensors_datasheet.pdf` — 372 KB，全文
7. `https://www.keyence.com/products/measure/laser-1d/cl-3000/specs/` — 规格表完整读出
8. `https://www.micro-epsilon.com/fileadmin/download/excerpts/dax--confocalDT-IFS2405--en-us.pdf` — 2.4 MB，全文
9. `https://novantaphotonics.com/wp-content/uploads/2022/03/AN00025_Finding-Focus-Plane-with-CalWizard-on-Black-Anodized-Sheet-Metal....pdf` — 225 KB，全文
10. `http://www.cinogy.com/html/cinsquare_m2_tool.html` — 精度数字读出
11. `https://dataray.com/applications/focus-measurement` — 读出
12. `https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2020.527734/full` — 43 KB 正文文本
13. `https://docs.lightburnsoftware.com/legacy/galvo/Focusing` — 读出
14. `https://www.scanneroptics.com/3d-dynamic-focus-galvo-scanner-...performance-benefits.html` — 84 KB HTML
15. `https://www.scanlab.de/en/products/calibration/hardware-configuration-and-control` — 112 KB（基本为导航，有效内容仅指向 3D Calibration Wizard PDF）
16. `https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/metroxraine58569.2023.10405731` — 取得 IEEE 论文**完整摘要**（首次请求 429 限流，重试成功）
17. `https://api.crossref.org/works?query.bibliographic=...` — 取得 ICALEO 2002 Kapton 论文摘要

**❌ 无法打开 / 内容不可用（明确说明，未编造）：**
- `https://www.ophiropt.com/en/f/beamwatch-am-laser-measurement` — 页面 JS 渲染，curl 仅得 2,457 字节壳，无正文
- `https://www.ophiropt.com/en/f/beamwatch-non-contact-profiler` — 同上，正文为空
- `https://www.ophiropt.com/en/n/beam-width-measurement-accuracy` — 同上（JS 渲染，2,457 字节），**仅能引用搜索摘要**
- `https://api.p1.mks.com/mam/celum/celum_assets/op/resources/BeamWatch_2.pdf?0`（及无 `?0` 版本）— 返回 6,074 字节 **"Embed Iframe" 机器人验证页**，非 PDF
- `https://pdf.directindustry.com/pdf/ophir-optronics/beamwatch/12595-662560.html` — 返回 HTML 而非 PDF
- `https://www.politesi.polimi.it/bitstream/10589/167367/1/la%20tesina%20revised-converted.pdf` — 返回 HTML（5,750 字节），非 PDF
- `https://re.public.polimi.it/handle/11311/1260836` — 可访问但未渲染出摘要（仅确认作者与年份）
- IEEE Xplore 全文 — 付费墙；仅取得摘要

**结论性提示（供父级参考）**：5 个子方法中，(b)(c)(d) 的一手来源最扎实且**都有明确数字**；(e) 的两个厂商工具流程描述非常明确，但**SCANLAB 与 RAYLASE 均未公开标定后的量化精度**，这是本主题最明显的公开资料空白；(a) 的 ISO 流程细节因免费预览只到第 3 章而**无法从标准本体一手引证**，且 IEEE 刀口不确定度论文的具体数值未公开。

---

## D. 一手原文落盘位置索引

# D. 一手原文落盘位置索引

本次调研下载并解析的一手 PDF/HTML 已缓存在 vault 内，可直接复查：

| 内容 | 路径 |
|---|---|
| **LasIA XY2-100 官方规范 LIA202001** | `99-附件与下载/_调研原始缓存/标准原文文本/lasia_LIA202001_xy2_100.txt`（PDF: `xyz/lasia_xy2_LIA202001.pdf`） |
| **LasIA XY3-100 v1.0 (LIA202002)** | `99-附件与下载/_调研原始缓存/标准原文文本/lasia_LIA202002_xy3_v10.txt` |
| **LasIA XY3-100 v1.1 (LIA202307)** | `99-附件与下载/_调研原始缓存/标准原文文本/lasia_LIA202307_xy3_v11.txt`（PDF: `xyz/lasia_xy3_v11_LIA202307.pdf`） |
| **SCANLAB RTC6 手册 附录 F（SL2-100 帧结构）** | `99-附件与下载/_调研原始缓存/标准原文文本/rtc6_appF.txt`、`rtc6_appF2.txt` |
| **RAYLASE SS-III XY2-100-E 手册（Z 通道引脚 5/18）** | `99-附件与下载/_调研原始缓存/xyz/raylase_xy2-100-E_ss3.txt`（PDF 同目录） |
| SCANLAB excelliSHIFT 数据手册 | `99-附件与下载/_调研原始缓存/xyz/scanlab_excellishift.pdf` |
| SCANLAB varioSCAN II 手册 | `99-附件与下载/_调研原始缓存/xyz/scanlab_varioscan2.pdf` |
| RAYLASE SP-ICE 3 数据手册 / 接口页 | `99-附件与下载/_调研原始缓存/raylase/datasheet_spice3.pdf`、`spice3_interfaces.txt` |
| RAYLASE SP-ICE 3 用户手册全文（含 7.1.9 延迟补偿） | `99-附件与下载/_调研原始缓存/raylase/spice3_all.txt`、`spice3_delay_relevant.txt` |
| Novanta LIGHTNING II 3 轴数据手册 | `99-附件与下载/_调研原始缓存/xyz/novanta_lightningII_3axis.pdf` |
| SCANLAB RTC4 / RTC5 / RTC6 控制卡数据手册 | `99-附件与下载/_调研原始缓存/rtc/rtc4_boards.pdf`、`rtc5_boards.pdf`、`rtc6_boards.pdf` |
| SCANLAB SCANahead 白皮书 | `99-附件与下载/_调研原始缓存/analog/scanlab_scanahead.pdf` |
| SCANLAB RTC6 头文件（API 级证据） | `99-附件与下载/_调研原始缓存/rtc/scanlab_rtc6.h`、`scanlab_RTC6expl.h` |
| sigrok XY2-100 解码器源码（位序证据） | `99-附件与下载/代码/sigrok-xy2-100-decoder/pd.py` |
| Ray-Motion XY2-100 技术数据表 | `99-附件与下载/_调研原始缓存/analog/xy2_100_raylase_ti.pdf` |
| Thorlabs 场曲曲线原图（读图核对用） | `research_src/sub_opt/tl_gr_fth160.gif`、`tl_gr_fth100.gif`、`tl_gr_fth254.gif`、`tl_gr_fth160m39.gif` |

**⚠️ 注意**：`research_src/` 为本次会话的临时目录，可能被清理；`99-附件与下载/_调研原始缓存/` 为 vault 既有缓存，更稳定。
**⚠️ 未落盘**：3 个后台子代理的部分中间下载（`sub_opt` 的 PDF 缓存）在会话中期被清理，其**结论已全部并入主文档与附录 A**，但原始 PDF 需按上表 URL 重新获取。


---

