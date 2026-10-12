# SCANLAB RTC 控制卡家族 调研报告
## (RTC4 / RTC5 / RTC6 及 SP-ICE、syncAXIS、SCANalone 相关产品)

> 调研日期：2026
> 来源标注约定：
> - **(a)** = 一手/官方文档已验证（厂商官网、官方 PDF、官方手册）
> - **(b)** = 二手来源（代理商、分销商、论坛、产品目录站）
> - **(c)** = 存疑/冲突（来源之间数值不一致，两个值都给出）
> - **未找到公开数据** = 无法找到公开数值，未做任何推测

---

# 0. 核心概念确认（最重要的结论）

## 0.1 RTC 家族是「PC 主机接口型控制卡」，不是振镜侧串行协议

**结论：RTC 家族是位于 PC 与扫描振镜（scan head）之间的控制器插卡/盒式控制器。它们的"上行"接口是 PC 总线（PCI / PCIe / Ethernet / USB），"下行"接口才是振镜侧的扫描头协议（XY2-100 / SL2-100）。RTC 本身不是一种振镜协议。**

一手证据：

- SCANLAB 官方 RTC 控制卡产品页原文："Control boards of the RTC family enable the intelligent and flexible control of scan systems, lasers and peripheral devices in real time. Thanks to the **PCI Express or Ethernet interfaces**, they can be integrated quickly and flexibly."
  → 明确说明 RTC 卡与 PC 的连接方式是 PCI Express / Ethernet。
  (https://www.scanlab.de/en/products/control-electronics/rtc-control-boards) **(a)**

- 官方 RTC 合集手册的"Overview"对比表把接口明确分成两栏：`PC interface`（PCI Express, Gigabit Ethernet / PCI, PCI Express / PCI Express, Ethernet）与 `Scan head interface`（SL2-100 / SL2-100 / XY2-100）。
  → 即：**PC 接口 ≠ 扫描头接口**，两者是卡的两个不同侧。
  (https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf) **(a)**

- 官方 RTC6 手册（产品手册）原文："**PCIe bus interface, Ethernet interface** … **SL2-100 transfer protocol** (control of scan systems with XY2-100 transfer protocol via an optional converter) … 20-bit positioning resolution"
  → RTC6 上行是 PCIe/以太网，下行是 SL2-100。
  (https://www.scanlab.de/sites/default/files/2020-08/12_RTC6%20control%20boards.pdf) **(a)**

- RTC6 手册中的系统框图（System Integration）显示信号链为：`PC 程序 → RTC 软件 → Driver → DLL → RTC 板 → SL2-100/XY2-100 → Scan head`，另有 Laser 与 Peripherals 支路。
  (https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf, 第 151–186 行 "System Integration") **(a)**

- RTC5 手册原文把 RTC5 直接称为 "PC interface board"："It is available as a **PC interface board**, or as a PCI-Express board."
  (https://www.scanlab.de/sites/default/files/2020-08/13_RTC5_control%20boards.pdf) **(a)**

### 结论性数据流示意

```
上位机 PC
   │  PCI / PCIe / Gigabit Ethernet / USB 1.1        ← RTC 的「主机侧」接口
   ▼
RTC4 / RTC5 / RTC6 控制卡（板载 DSP + 列表缓冲 + 校正表 + 激光时序）
   │  XY2-100 (16-bit)  或  SL2-100 (20-bit)          ← RTC 的「振镜侧」接口
   ▼
振镜扫描头 Scan Head (galvo)
   │
   └─ 激光控制：15-pin D-SUB（RTC5/RTC6）或 9-pin D-SUB（RTC4）
```

**对 XY100 项目的直接含义：** 若目标是复现/对接"振镜协议"，RTC 卡对外的振镜侧协议是 **XY2-100 / SL2-100（以及经转换器实现 XY2-100）**。RTC 与 PC 之间的通信是 SCANLAB 的私有 DLL/驱动协议 + PCIe/以太网，不是振镜协议。

---

# 1. RTC4

## 1.1 型号 / 总线变体（共 4 种接口选项）

| 变体 | 主机接口 | 一手/二手来源 |
|---|---|---|
| RTC4 PCI | PCI | **(b)** |
| RTC4 PCIe | PCI Express | **(a)** |
| RTC4 SCANalone | **USB 1.1**（+ MMC 存储卡） | **(a)** |
| RTC4 Ethernet | Ethernet 10/100 Mbit/s | **(a)** |

- 官方 RTC4 产品手册（09/2022 版）："The RTC4 series of control boards is available with two different interfaces: **PCI Express (RTC4 PCIe)**、**Ethernet (RTC4 Ethernet)**."
  (https://www.scanlab.de/sites/default/files/2020-08/14_RTC4_control%20boards.pdf) **(a)**
- DirectIndustry 上 SCANLAB 官方 RTC4 目录（含更早的四种接口选项表）原文："Interface Options: **PCI Express (RTC4 PCIe) and PCI (RTC4 PCI)**: Support multi-board functionality with **up to 16 boards in one PC**. **USB (RTC4 SCANalone)**: Allows stand-alone operation with **up to 8 boards connected to one PC**. **Ethernet (RTC4 Ethernet)**: Eliminates the need for a PC near the scan system."
  (https://pdf.directindustry.com/pdf/scanlab-gmbh/rtc4/39164-694240.html) **(b)**
  → 该页摘要亦经 web_search 片段二次确认："available with four interface options: PCI Express, PCI, USB, and Ethernet."
- RTC4 SCANalone 为 USB 的一手证据（SCANLAB 官方新闻稿，2003-09-05）："Marking data can be loaded via a removable **MMC memory card** or by using the built-in **USB 1.1 interface**."
  (https://www.scanlab.de/en/news-events/press-releases/control-scan-systems-and-lasers-without-requiring-pc) **(a)**
- RTC4 Ethernet 为以太网的一手证据（SCANLAB 官方新闻稿，2015-05-21）："Unlike the **USB-based RTC 4 SCANalone board** driver installation isn't needed anymore and direct network connectivity eliminates cable-length restrictions."
  (https://www.scanlab.de/en/news-events/press-releases/scan-system-control-board-ethernet-interface-simpler-industrial) **(a)**

> **注：用户提问中的 "RTC4 SCANalone USB" 得到证实 —— 该变体确实存在且为 USB 1.1。** 但官方 2022 年现行手册只列出 PCIe 与 Ethernet 两种，PCI 与 USB 变体属早期/历史型号。**(c)（现行在售 vs 历史型号的差异）**

## 1.2 RTC4 数值规格

以下除特别注明外，均来自官方 RTC 合集手册 Overview 对比表 **(a)**：
(https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf)
以及官方 RTC4 产品手册 **(a)**：
(https://www.scanlab.de/sites/default/files/2020-08/14_RTC4_control%20boards.pdf)

| 项目 | 数值 | 来源 |
|---|---|---|
| PC 接口 | PCI Express、Ethernet（10/100 Mbit/s）；历史另有 PCI、USB 1.1 | **(a)** 手册 / **(b)** DirectIndustry |
| 独立运行 (Standalone) | **否**（RTC4 无 standalone 项）；但 RTC SCANalone 是独立的 USB 变体 | **(a)** |
| 远程接口 (Remote interface) | 否 | **(a)** |
| 数据流 (Data streaming) | 否 | **(a)** |
| **扫描头接口** | **XY2-100**（RTC4 手册称 "**XY2-100 enhanced protocol**"） | **(a)** |
| 电气隔离 (Galvanic isolation) | **否** | **(a)** |
| 轴数 / 通道数 | **2 / 3** | **(a)** |
| **定位分辨率** | **16 bit**（脚注 1：z 轴控制时为 16 bit） | **(a)** |
| 扫描头连接器 | **25-pin D-SUB** | **(a)** |
| 激光连接器 | **9-pin D-SUB** | **(a)** |
| SCANahead 支持 | 否 | **(a)** |
| 校正文件格式 | **ctb** | **(a)** |
| 校正文件数量 2D / 3D | **2 / 1** | **(a)** |
| POF（on the fly）轴数 | 2（选项） | **(a)** |
| POF 虚拟加工场值域 | –（无） | **(a)** |
| 列表内存 (List memory) | **约 8,000** 条 | **(a)** |
| 记录通道 / 数值 | 2 / 2^15 | **(a)** |
| **最大位图像素频率** | **50 kHz** | **(a)** |
| **模拟输出 / 分辨率** | **2 / 10 bit**（脚注 5：输出引脚与 +5 V 或 LaserOn 信号共用，可用焊锡跳线配置） | **(a)** |
| McBSP (OIE 支持) | 否 (否) | **(a)** |
| RS232 | 有（**仅 Ethernet 变体**） | **(a)** |
| 步进电机控制 | 有（**仅 PCI Express 变体**） | **(a)** |
| 激光同步 (Laser synchronization) | **否** | **(a)** |
| **激光延迟分辨率** | **1 µs** | **(a)** |
| 主/从 (Master/Slave) | 否 | **(a)** |
| 天空书写 (Sky writing) | 否 | **(a)** |
| 日期/时间/字体 | 否 | **(a)** |
| 速度相关激光控制 | 否 | **(a)** |
| IO 端口 8 / 16 bit | 有 | **(a)** |
| **输出周期** | **10 µs**（"Every 10 μs, a 16-bit control signal is transmitted to the scan system"） | **(a)** |
| 数字 I/O | 16 路数字输入 + 16 路数字输出；另有 1 路 8-bit 数字输出；1 路 16-bit 数字输出 + 1 路 16-bit 数字输出（用于控制外部组件） | **(a)** |
| 最大卡数 / PC | PCIe 与 PCI：**最多 16 张**；USB SCANalone：**最多 8 张** | **(a)** 手册(PCIe 16) / **(b)** DirectIndustry(USB 8) |
| 供电 | PCIe 变体：经 PCIe 总线；Ethernet 变体：**+12 … 48 V DC，最大功耗 2 W** | **(a)** |
| 机械尺寸 | RTC4 PCIe：(161 × 106) mm；RTC4 Ethernet：(96 × 90) mm | **(a)** |
| 驱动 | Windows 10 / 8 / 7 / Vista / XP（32 & 64 bit）+ DLL | **(a)** |
| 历史销量 | "over 20,000 units sold since product introduction"（截至 2015） | **(a)** |

### RTC4 SCANalone 专有规格 **(a)**
(https://www.scanlab.de/en/news-events/press-releases/control-scan-systems-and-lasers-without-requiring-pc)
- 无需 PC 即可实时控制扫描系统与激光；**运行仅需外部电源**
- 加工数据经**可插拔 MMC 存储卡**或内置 **USB 1.1** 接口载入
- 板载内存可容纳 **最多 100 万条 list 指令**
- 外部控制信号可启动/影响内存中程序的执行；为此配备 **16-bit 数字输入 + 16-bit 数字输出**
- 每 **10 µs** 同步输出 16-bit 数字控制信号给扫描系统与激光
- 也可通过 USB 连接的 PC 操作，此时**功能等同于 RTC4 PC 接口板**
- 软件接口与硬件连接能力**与 RTC4 PC 接口板基本兼容**；RTC4 PC 接口板的所有选件（如 3D、POF）在 SCANalone 上同样可用

### RTC4 可选功能 **(a)**
(https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf)
- 3 轴扫描系统控制（3D）
- POF（加工运动中的物体）
- 同时控制两套扫描系统（双头）
- 定制化软件扩展：**无**
- UltraFastPixelMode (UFPM)：**无**
- Spot Distance Control (SDC)：**无**
- SCANahead：**无**
- laserDESK 支持：**无**（RTC6/RTC5 有）

---

# 2. RTC5

## 2.1 型号 / 总线变体

| 变体 | 主机接口 | 来源 |
|---|---|---|
| RTC5 PCI | PCI | **(a)** |
| RTC5 PCIe / RTC5-Express | PCI Express (**PCIe-x1 version 1.0**) | **(a)** |
| RTC5 PC/104-Plus | PC/104-Plus | **(b)** |
| RTC5 PCIe/104 | PCIe/104 | **(b)** |

- 官方 RTC5 手册："It is available as a PC interface board, or as a **PCI-Express board**." / "**PCI bus interface or PCI-Express interface (PCIe-x1 version 1.0)**" / "**Any number of RTC5 PCI or PCIe boards in one PC**"
  (https://www.scanlab.de/sites/default/files/2020-08/13_RTC5_control%20boards.pdf) **(a)**
- RTC5 官方手册标题页列举的完整型号族："The RTC 5 PC Interface Board, RTC 5-Express Board, RTC 5 PC/104-Plus Board and RTC 5 PCIe/104 board for Real Time Control of Scan Heads and Lasers"
  (https://www.manualslib.com/manual/2909604/Scanlab-Rtc-5-Pc-Interface-Board.html) **(b)**
  → **注：PC/104-Plus 与 PCIe/104 变体在现行 SCANLAB 产品页与 2022 版对比表中均未出现，应视为历史/嵌入式变体。** **(c)**

## 2.2 RTC5 数值规格

来源：官方 RTC 合集手册对比表 **(a)** (https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf)、官方 RTC5 产品手册 **(a)** (https://www.scanlab.de/sites/default/files/2020-08/13_RTC5_control%20boards.pdf)

| 项目 | 数值 | 来源 |
|---|---|---|
| PC 接口 | **PCI、PCI Express（PCIe-x1 version 1.0）** | **(a)** |
| 独立运行 (Standalone) | **否** | **(a)** |
| 远程接口 | 否 | **(a)** |
| 数据流 | 否 | **(a)** |
| **扫描头接口** | **SL2-100** | **(a)** |
| 电气隔离 | **是** | **(a)** |
| 轴数 / 通道数 | **2 / 2** | **(a)** |
| **定位分辨率** | **20 bit**（"16x higher positioning resolution compared to the RTC4 predecessor board"） | **(a)** |
| 扫描头连接器 | **9-pin D-SUB** | **(a)** |
| 激光连接器 | **15-pin D-SUB** | **(a)** |
| SCANahead 支持 | 否 | **(a)** |
| 校正文件格式 | **ct5** | **(a)** |
| 校正文件数量 2D / 3D | **4 / 4**（脚注 3：使用 3 或 4 个校正文件时测量数据内存减半） | **(a)** |
| POF 轴数 | 2 | **(a)** |
| POF 虚拟加工场值域 | **24 bit** | **(a)** |
| 列表内存 | **2^20（约 100 万）**；手册称 "Configurable list buffers with 1,000,000 list positions" | **(a)** |
| 记录通道 / 数值 | 2 / 2^20 或 4 / 2^19 | **(a)** |
| **最大位图像素频率** | **308 kHz**（对比表） / **"up to 300 kHz"**（RTC5 产品手册正文） | **(c)** 两个值均出自 SCANLAB 官方文档 |
| **模拟输出 / 分辨率** | **2 / 12 bit（0…10 V）** | **(a)** |
| McBSP (OIE 支持) | 有 (否) | **(a)** |
| RS232 | 有 | **(a)** |
| 步进电机控制 | 有 | **(a)** |
| 激光同步 | 有（"output synchronization"，可与外部激光时钟同步） | **(a)** |
| **激光延迟分辨率** | **1/2 µs** | **(a)** |
| 激光信号分辨率 / 电流 | **15 ns 分辨率、20 mA 输出电流** | **(a)** |
| 主/从 | 有 | **(a)** |
| 天空书写 | 有 | **(a)** |
| 日期/时间/字体 | 有 | **(a)** |
| 速度相关激光控制 | **limited（受限）** | **(a)** |
| IO 端口 8 / 16 bit | 有 | **(a)** |
| 数字 I/O | 16-bit 数字输出与输入；8-bit 数字输出；2-bit 数字输出与输入 | **(a)** |
| **输出周期** | **10 µs** | **(a)** |
| 编码器输入（POF 选项） | **2 路编码器输入，32-bit 计数器，最多 8 个物体**（trigger 与打标位置之间）；2D fly 功能 | **(a)** |
| 最大卡数 / PC | **"Any number of RTC5 PCI or PCIe boards in one PC"（任意数量）** | **(a)** |
| 驱动 | Windows 10 / 8 / 7 / Vista（32 & 64 bit） | **(a)** |
| iDRIVE 技术支持 | 支持（intelliSCAN、intellicube、intelliDRILL、intelliWELD、powerSCAN i 等全数字伺服电子扫描系统） | **(a)** |

### RTC5 可选功能 **(a)**
- 3 轴扫描系统控制
- POF（运动物体加工，2 路编码器 + 32-bit 计数器，最多 8 物体）
- 双头能力（同时控制两套扫描系统）
- 定制化扩展
- **UFPM：无**、**SDC：无**、**SCANahead：无**

---

# 3. RTC6

## 3.1 型号 / 总线变体

| 变体 | 主机接口 | 说明 | 来源 |
|---|---|---|---|
| **RTC6 PCIe** | PCI Express | 插卡式 | **(a)** |
| **RTC6 Ethernet** | Gigabit Ethernet | 支持 standalone / 远程接口 / 数据流 | **(a)** |
| **RTC6 EtherBox** | Gigabit Ethernet | RTC6 Ethernet 放在高档外壳内，支持 EN 60715 顶帽导轨安装 | **(a)** |

- 官方 RTC6 手册："**PCIe bus interface, Ethernet interface**" / "**Up to 255 RTC6 control boards per PC**"
  (https://www.scanlab.de/sites/default/files/2020-08/12_RTC6%20control%20boards.pdf) **(a)**
- 官方 RTC6 EtherBox 手册：内嵌 RTC6 Ethernet 控制板，**支持 standalone 模式**；**24/7 运行**；**可同步多台 RTC6 EtherBox**；供电 **12 – 30 V**；尺寸 **221.5 × 177 × 51 / 44 / 26 mm**；符合 RoHS / EMC / FCC；符合 EN 60715 顶帽导轨
  (https://www.scanlab.de/sites/default/files/2021-11/RTC6_EtherBox_en.pdf) **(a)**
- 官方 RTC 产品页："RTC6 EtherBox — The RTC6 Ethernet is also available in a high-quality housing … Synchronization of multiple RTC6 EtherBox units possible"
  (https://www.scanlab.de/en/products/control-electronics/rtc-control-boards) **(a)**
- 软件版本与硬件修订版（官方下载页）：**RTC6 Software 2.0.0（2026-06-16，对应 RTC6 PCIe / RTC6 Ethernet Hardware Revision 2）**、**RTC6 Software 1.25.0（2026-08-17，对应 Hardware Revision 1）**
  (https://www.scanlab.de/en/products/software/rtc-software/download) **(a)**
  → 说明 RTC6 目前存在 **HW Rev 1 与 HW Rev 2** 两代硬件。**(a)**

> **关于 "RTC6 Board" / "RTC6 compact"：** SCANLAB 现行产品页与官方手册中，RTC6 的变体为 **PCIe / Ethernet / EtherBox** 三种。**未找到公开数据** 表明存在名为 "RTC6 Board" 或 "RTC6 compact" 的独立型号（"RTC6 Ethernet 控制板" 是被 EtherBox 内嵌的那块板）。**(c)**

## 3.2 RTC6 数值规格

来源：官方 RTC 合集手册对比表 **(a)** (https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf)、官方 RTC6 产品手册 **(a)** (https://www.scanlab.de/sites/default/files/2020-08/12_RTC6%20control%20boards.pdf)

| 项目 | 数值 | 来源 |
|---|---|---|
| PC 接口 | **PCI Express、Gigabit Ethernet** | **(a)** |
| 独立运行 (Standalone) | **是（仅 Ethernet 变体）** | **(a)** |
| 远程接口 (Remote interface) | **是（仅 Ethernet 变体）** | **(a)** |
| 数据流 (Data streaming) | **是（仅 Ethernet 变体）** | **(a)** |
| **扫描头接口** | **SL2-100** | **(a)** |
| 电气隔离 | **是** | **(a)** |
| 轴数 / 通道数 | **2 / 2** | **(a)** |
| **定位分辨率** | **20 bit** | **(a)** |
| 扫描头连接器 | **9-pin D-SUB** | **(a)** |
| 激光连接器 | **15-pin D-SUB** | **(a)** |
| SCANahead 支持 | **是**（可选，用于 excelliSCAN 系列） | **(a)** |
| 校正文件格式 | **ct5** | **(a)** |
| 校正文件数量 2D / 3D | **8 / 8**（"up to eight 3D correction files"） | **(a)** |
| POF 轴数 | 2（脚注 4：通过编码器值外推获得更高精度） | **(a)** |
| POF 虚拟加工场值域 | **29 bit** | **(a)** |
| 列表内存 | **2^23（约 800 万）**；手册称 "more than 8 million list positions" | **(a)** |
| 记录通道 / 数值 | 2 / 2^24 或 4 / 2^23 | **(a)** |
| **最大位图像素频率** | **800 kHz；可选 UFPM 提升到 3.2 MHz** | **(a)** |
| **模拟输出 / 分辨率** | **2 / 12 bit（0…10 V）** | **(a)** |
| 激光信号分辨率 / 电流 | **15 ns 分辨率、20 mA 输出电流** | **(a)** |
| McBSP (OIE 支持) | **有 (有)** | **(a)** |
| RS232 | 有 | **(a)** |
| 步进电机控制 | 有 | **(a)** |
| 激光同步 | **有（n × 100 kHz）** | **(a)** |
| **激光延迟分辨率** | **1/64 µs（≈15.625 ns）** | **(a)** |
| 主/从 (Master / Slave) | **有** | **(a)** |
| 天空书写 | 有 | **(a)** |
| 日期/时间/字体 | 有 | **(a)** |
| 速度相关激光控制 | **有** | **(a)** |
| IO 端口 8 / 16 bit | 有 | **(a)** |
| 数字 I/O | 16-bit 数字输出与输入；8-bit 数字输出；2-bit 数字输出与输入；位图模式下附加数字端口可作为输出端口 | **(a)** |
| **输出周期** | **10 µs**（"10 µs output period"、"Synchronization of the 10 µs RTC clock to an external laser clock signal"） | **(a)** |
| 编码器输入（POF 选项） | **2 路编码器输入，32-bit 计数器，最多 8 个物体** | **(a)** |
| 最大卡数 / PC | **最多 255 张 RTC6 控制卡** | **(a)** |
| 驱动 | Windows 10 / 8 / 7（32 & 64 bit）；多线程、多进程 | **(a)** |
| 其他 | Download verification、增强的 list 与执行状态、可定义/可选字符集、日期/时间/序列号打标、圆与椭圆打标、所有 list 命令的条件执行 | **(a)** |

## 3.3 RTC6 相对 RTC5 的改进（官方对比） **(a)**
(https://www.scanlab.de/sites/default/files/2020-08/12_RTC6%20control%20boards.pdf)

| 项目 | RTC6 | RTC5 |
|---|---|---|
| PC 接口 | PCIe, Ethernet | PCI, PCIe |
| SCANahead 控制 | 用于 excelliSCAN（可选） | 无 |
| 同步（扫描系统控制） | **10 µs RTC 时钟同步** | 输出同步 |
| 位图模式像素频率 | **800 kHz 最大** | 308 kHz 最大 |
| UltraFastPixelMode (UFPM) | **3.2 MHz 最大（可选）** | 无 |
| 列表内存 | **800 万 list 位置** | 100 万 list 位置 |
| 3D 校正文件 | **最多 8 个 3D 校正文件** | 最多 2 个 3D 校正文件 |
| 输出周期 | 10 µs | 10 µs |
| 传输协议 | SL2-100 | SL2-100 |
| 驱动 | Windows 10/8/7 (32/64-bit) | Windows 10/8/7 (32/64-bit)、Vista / XP (ab SP2) |

## 3.4 RTC6 的 3D 能力 **(a)**

- "the synchronization of the usually faster x/y scan axes with the slower **z-axis**. This allows more precise results in **3D processing**."
  (https://www.scanlab.de/sites/default/files/2020-08/12_RTC6%20control%20boards.pdf) **(a)**
- 选项列表包含 "**Control of 3-axis scan systems**"；对比表列出 "Number of correction files **2D / 3D**" RTC6 = **8/8**。
  (https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf) **(a)**
- DirectIndustry 把 RTC6 直接归类为 "**3-axis motion control card RTC6**"。
  (https://www.directindustry.com/prod/scanlab-gmbh/product-39164-523087.html) **(b)**
- SCANLAB 官方 z 轴/3D 附件产品线为 **excelliSHIFT**（把 2D 扫描头扩展为 3D 扫描系统）与 **varioSCAN II**。
  (https://www.scanlab.de/en/products/z-axes-3d-add-ons) / (https://www.scanlab.de/en/products/z-axes-3d-add-ons/excellishift) **(a)**
- RTC4 手册亦提到 "Functionality for controlling of **3-axis scan systems**" 选件。 **(a)**

## 3.5 RTC6 特有能力 **(a)**
(https://www.scanlab.de/en/products/control-electronics/rtc-control-boards) / (https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf)

**所有 RTC6 共有的亮点：**
- **SCANahead 技术**：具备 SCANahead 控制的扫描系统可**独立于扫描速度**以**最大可能加速度**运行
- **Multiplexing（复用）**：最新一代扫描系统支持通过 **SL2-100 返回通道**回传多项扫描系统参数，用于分析与监控
- **Short Vector Processing**：短共线标记预处理软件扩展（Short Vector DLL，加购软件）

**RTC6 Ethernet 额外亮点：**
- **Data streaming**：扫描系统状态数据与卡状态可永久、与作业无关地传给任意应用程序
- **Standalone functionality**：**预定义激光作业可存入 flash 存储器**，由系统控制器启动（PC 无关）
- **Remote interface**：平台无关的远程控制，便于连接 **PLC、Linux 系统或嵌入式 PC**

---

# 4. 各 RTC 的振镜侧接口（扫描头接口）总表

| | RTC6 | RTC5 | RTC4 |
|---|---|---|---|
| **扫描头接口** | **SL2-100** | **SL2-100** | **XY2-100** |
| 电气隔离 | 是 | 是 | 否 |
| 轴数 / 通道数 | 2 / 2 | 2 / 2 | 2 / 3 |
| 定位分辨率 | **20 bit** | **20 bit** | **16 bit**（z 轴控制时 16 bit） |
| 连接器 | 9-pin D-SUB | 9-pin D-SUB | 25-pin D-SUB |

**(a)** 来源：(https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf)

## 4.1 关于 XY2-100 到 SL2-100 的兼容

- **RTC5、RTC6 也可驱动 XY2-100 协议扫描头，但需通过可选的转换器。** 官方原文：
  - RTC6："SL2-100 transfer protocol (control of scan systems with **XY2-100 transfer protocol via an optional converter**)"
  - RTC5："SL2-100 transfer protocol (control of scan systems per **XY2-100 transfer protocol via an optional converter**)"
  **(a)** (https://www.scanlab.de/sites/default/files/2020-08/12_RTC6%20control%20boards.pdf) / (https://www.scanlab.de/sites/default/files/2020-08/13_RTC5_control%20boards.pdf)

- 转换器官方产品名：**XY2-100 Converter (SL2-100 => XY2-100)**，SCANLAB 官方文档 © SCANLAB GmbH 2017。关键接口信息 **(a)**：
  - 直接插到 **RTC5 板的主扫描头连接器**，或经**尽可能短的 1:1 线缆**接到 RTC5 板的**副扫描头连接器**对应引脚
  - **SL2-100 侧：9-pin male D-Sub** —— `DATA OUT +/-(1/6)`、`3.3 V(2,4)`、`DATA IN +/-(5/9)`、`GND(7,8)`
  - **XY2-100 侧：25-pin female D-Sub** —— `CLOCK ±(1/14)`、`SYNC ±(2/15)`、`CHAN1 ±(3/16)`、`CHAN2 ±(4/17)`、`STATUS ±(6/19)`、`STATUS1 ±(8/21)`
  - 尺寸：62 × 52 × 12.5 mm（mm）
  - 备注：对 iDRIVE 类扫描系统（intelliSCAN、intelliSCANde、intelliDRILL、intellicube、intelliWELD、varioSCANde），`STATUS±` 是轴 2（X 轴）的状态通道，`STATUS1±` 是轴 1（Y 轴）的状态通道；对其它扫描系统 `STATUS1±` 不可用
  (https://cdn.casmart.com.cn/file/20220117/3810e78a3b25488eb3abdc20d7d4d7dd.pdf) **(a)（SCANLAB 原始文档，托管于代理商 CDN）**
  - RTC6 手册目录中亦列有 "43 Accessories for the RTC6 PCIe Board / 44 **XY2-100 Converter**"
    (https://www.manualslib.com/products/Scanlab-Rtc6-Pcie-Board-14108968.html) **(b)**

- SCANLAB 官方对协议定位的说明："The widely used **XY2-100 protocol with only 16-bit positioning resolution** is often no longer adequate for micro-machining. Here, the **20-bit SL2-100 protocol, developed and introduced by SCANLAB**, is a necessary upgrade. High-end scan systems and control boards such as **RTC5 and RTC6 support this protocol**."
  (https://www.scanlab.de/en/applications/micromachining) **(a)**

## 4.2 关于 XY3-100

- **XY3-100 不属于 SCANLAB RTC 家族的接口。** 在 SCANLAB 官方 RTC 文档与产品页中均**未找到** RTC4/RTC5/RTC6 支持 XY3-100 的记载 → **未找到公开数据**。
- XY3-100 出现在 **AEROTECH** 的产品上：Aerotech **Automation1 GI4** 激光扫描头控制器 —— "The GI4 commands industrial scan heads using the **XY2-100 protocol or the new higher resolution XY3-100 protocol**"，并支持 IFOV（infinite field of view）、MOTF、Part-Speed PSO；通过 **HyperWire** 与 Automation1 控制器在线连接；支持 2 轴与 3 轴扫描头；激光控制支持 YAG、CO2 与通用模式。
  (https://www.aerotech.com/product/automation1-gi4-laser-scan-head-controller/) **(a)**
  (https://www.aerotech.com/wp-content/uploads/2021/11/Automation1-GI4-Data-Sheet-D20220401.pdf) **(a)**

## 4.3 关于模拟接口

- RTC 家族对**扫描头**使用**数字串行协议**（XY2-100 / SL2-100），**不提供面向振镜的模拟输出**。
- RTC 板上的**模拟输出是用于激光功率控制**的：RTC5/RTC6 为 **2 × 12 bit（0…10 V）**；RTC4 为 **2 × 10 bit**。
  **(a)** (https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf)
- 例外：RTC4 PCIe 变体可控制 **varioSCANFLEX（带步进电机扩展）**。 **(a)**

---

# 5. SP-ICE — 归属问题的最终结论

## 5.1 结论：SP-ICE 是 **RAYLASE** 的产品，**不是 SCANLAB 的**

**用户记忆中的 "SP-ICE-3 是 RAYLASE 产品" 是正确的。"SP-ICE = SCANLAB 旧名" 是错误的。**

### 一手证据（全部 RAYLASE 官方）**(a)**

1. **SP-ICE-3 官方产品页与数据手册**：
   "**SP-ICE 3 CONTROL CARD** … The SP-ICE-3 control card is the universal solution for every laser system with deflection units."
   → 页面位于域名 **raylase.de**，页脚版权 "© 2026 **RAYLASE GmbH**"，地址 Argelsrieder Feld 2+4, 82234 Wessling, Germany。
   (https://www.raylase.de/en/products/electronics-control-cards/sp-ice-3.html) **(a)**
   (https://www.raylase.de/_Resources/Persistent/b/a/6/6/ba66d25112e3d91511322aa417caae73c916557b/Datasheet_SP-ICE-3.pdf) **(a)**

2. **SP-ICE-3 官方用户手册**（在线 HTML 版）："SP-ICE Control Electronics: SP-ICE 3 User's Manual"，版权行 "Copyright © 2017-2025 **RAYLASE GmbH**"。
   (https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/d6107a36-ef4e-4e13-a21c-6cda62a65fd6.htm) **(a)**

3. **SP-ICE 2 官方硬件手册**（PDF）：封面 "Hardware Manual — **SP-ICE 2 Control Card**"，文内 "This manual has been compiled by **RAYLASE** for its customers and employees"，制造商章节明确写 "**RAYLASE AG**, Argelsrieder Feld 2+4, 82234 Wessling, Germany"，文档号 MN043 / v1.0.2。
   (http://alaser.com.tw/db/upload/webdata4/6alaser_201571916204379297.pdf) **(a)（RAYLASE 原始文档，托管于代理商站点）**

4. **SP-ICE-1 PCI PRO**：RAYLASE SP-ICE-1 PCI PRO Hardware Manual（ManualsLib 收录，标题含 "RAYLASE"）。
   (https://www.manualslib.com/manual/2120338/Raylase-Sp-Ice-1-Pci-Pro.html) **(b)**

5. RAYLASE 官方电子控制卡产品线页面标题即 "**CONTROL ELECTRONICS — SP-ICE**"，当前在售型号仅 **SP-ICE 3**。
   (https://www.raylase.de/en/products/electronics-control-cards.html) **(a)**

### 关于「SCANLAB 是否有 SP-ICE 产品」

- 对 SCANLAB 官网（scanlab.de）的抓取中，**产品目录、软件目录、下载目录里均无 SP-ICE**；SCANLAB 的控制电子类目只有 **RTC Control Boards / RTC Features / Open Interface Extension**。
  (https://www.scanlab.de/en/products/control-electronics/rtc-control-boards) **(a)**
- 多次检索 "SCANLAB SP-ICE" 未找到任何将 SP-ICE 归属于 SCANLAB 的权威来源。
  → **结论：SP-ICE 与 SCANLAB 无关，SCANLAB 从未有名为 SP-ICE 的产品。SCANLAB 的对标产品是 RTC 系列。** **(a)**

### SP-ICE / RTC 的竞争关系

- RAYLASE GmbH（Wessling, Germany）与 SCANLAB GmbH（Puchheim, Germany）是**德国两家互相竞争的激光振镜/控制卡厂商**。
- **关键交叉点**：RAYLASE 的 SP-ICE-3 也支持 **SL2-100** 协议（SCANLAB 开发并引入的 20-bit 协议），说明 SL2-100 已成为跨厂商的行业接口。
  (https://www.raylase.de/_Resources/Persistent/b/a/6/6/ba66d25112e3d91511322aa417caae73c916557b/Datasheet_SP-ICE-3.pdf) **(a)**
  (https://www.scanlab.de/en/applications/micromachining) **(a)**

## 5.2 SP-ICE-3 数值规格 **(a)**
(https://www.raylase.de/_Resources/Persistent/b/a/6/6/ba66d25112e3d91511322aa417caae73c916557b/Datasheet_SP-ICE-3.pdf)
(https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/48a53e4f-2a14-4518-ad32-d622848ab64a.htm)

| 项目 | 数值 |
|---|---|
| 厂商 | RAYLASE GmbH（Wessling, Germany） |
| **主机接口** | **PCIe-x1 Version 2.1**（内部安装）或 **Gigabit Ethernet**（外部 / standalone） |
| 最大卡数 | **任意数量**（"an arbitrary number of cards can be installed in a single PC"） |
| standalone 供电 | **12 V / max 2 A** |
| 控制偏转单元数 | 最多 **2 台**（通过 SL2-100 / RL3-100）；**RL3-100 下最多 5 轴，或 2×3 轴** |
| **位置分辨率** | **20 bit**（SL2-100、RL3-100）；**XY2-100 为 16 bit**（需可选适配板） |
| **步进周期** | **10 µs** |
| **镜面定位分辨率** | **0.75 µrad**（由 20 bit / 10 µs 推导） |
| 跟踪误差补偿 | 所有轴独立补偿 |
| **最大激光频率** | **最高 16 MHz** |
| 位图模式 | **最高 1 MHz 像素频率、15 ns 分辨率** |
| MOTF（On-The-Fly） | **2 个正交解码器（差分输入）**；**最多缓冲 32 个工件**；内置可编程正交编码器模拟器 |
| 虚拟加工场 | 常规场的 **8 倍** |
| 测量记录 | **最多 2400 万条测量值** |
| 内存 | **1 GB DDR3 RAM** + **1 GB DDR3 RAM 用于 2D/3D 场校正** + **32 GB microSD**（设置/程序/list） |
| 数字 I/O | **2 × 16 bit GPIO（3.3 V 或 5 V TTL）**；**2 × 24 bit 3.3 V LVCMOS**（亦供定制适配板）；**1 × 16 bit 输入（5 V 或 24 V）** |
| 激光接口 | 15-pin 接口带 2 路模拟输出；另加带**差分 0–10 V 模拟输出**的连接器 |
| 其他接口 | RS232 V.24；**USB 2.0** |
| 驱动 | Windows 11 / 10 / 8 / 7（32 & 64 bit）；**.NET 与 Windows Native 及 Linux DLL**；C# / C++ 示例 |
| 尺寸 / 重量 | 100 mm（宽）× 180 mm（长）/ **156 g** |
| 环境 | +15 °C…+35 °C；存储 0 °C…+80 °C；相对湿度 < 80% 非凝露 |
| 其他功能 | 可变 Jump Delay、Sky Writing、功率斜坡（可选 2 套独立 ramp）、可配置 Lissajous 曲线（摆动焊接）、功率标定/激光线性化、任意数量与大小的 list（仅受 RAM 限制）、循环/跳转/子程序、条件执行、独立监控偏转单元、 **卡上执行客户定制 list 与 .NET 程序** |

## 5.3 SP-ICE 2 数值规格 **(a)**
(http://alaser.com.tw/db/upload/webdata4/6alaser_201571916204379297.pdf) — RAYLASE MN043 / v1.0.2

| 项目 | 数值 |
|---|---|
| 厂商 | RAYLASE AG |
| 控制能力 | **最多 4 个扫描头 + 2 个激光单元**；支持 2 轴与 3 轴偏转单元 |
| **主机接口** | **PCI 总线** 或 **LAN（10 Mbit/s 或 100 Mbit/s）** |
| **扫描头接口** | **XY2-100 enhanced 标准**（RAYLASE 功能扩展），25-pin D-SUB |
| **分辨率** | **16 bit 或 18 bit**（工作场内） |
| **最短输出间隔** | **10 µs（可按 ≤1 µs 步进变化）**；数据输出可缩放、分辨率优于 1 µs |
| 模拟输出 | **2 路 0 V…+10 V ±1%**，输出电流 ≤5 mA，带宽 1 kHz，**DAC 分辨率 16 bit**；或 1 路 16-bit 数字输出（用于二极管/灯电流） |
| 命令语言 | JavaScript 基础，**1,000,000+ 条** |
| 板载存储 | 非易失存储作业；**SD 卡最高 2 GB** |
| MOTF | 选项，**最多 3 个位置编码器**（差分输入，9-pin Sub-D） |
| 其他接口 | **USB 2.0（12 Mbit/s）**；**RS-232 9600–115200 Baud**；Slave 接口（26-pin，最多 3 块 SP-ICE2 从板，实现 4 个扫描单元并行）；Versa 接口（SPI，内部用）；可选步进电机接口（最多 3 个） |
| 数字 I/O 扩展 | 通过附加卡 **PCIDIOEX** 提供 **最多 32 路光隔离 I/O（24 V）** |
| 实时时钟 | 有，电池备份约 **60 天** |
| 尺寸 / 重量 | W 107 mm × L 195 mm；**150 g** |
| 环境 | 工作 +15…+35 °C；存储 −20…+60 °C；湿度 ≤80% 非凝露 |
| 供电 | 经 PCI 总线，或外部 **12 V / +5 V**（standalone 时） |
| 驱动 | DLL 与 .NET for Windows XP / Vista / 7（**仅 32-bit**） |
| 板载 OS | 嵌入式 Linux |

---

# 6. syncAXIS、SCANalone、XL SCAN

## 6.1 syncAXIS —— 它是**软件**，不是控制卡

**结论：syncAXIS 是 SCANLAB 的控制软件，用于 XL SCAN，不是一块控制器板。**

一手证据（SCANLAB 官方下载页）**(a)**：
(https://www.scanlab.de/en/downloads/software/syncaxis)

- "**syncAXIS Software** … syncAXIS control software allows fast and intuitive creation of user programs for **XL SCAN**."
- 最新 syncAXIS 软件需要 **current dongle**（dongle 可解锁 1.x 版本）
- 兼容 **Windows 7 及更新的 Windows**（32-bit 与 64-bit）
- **硬件前提：`RTC6 PCIe with option "syncA" enabled`** —— 且 **RTC 文件必须来自 syncAXIS 软件包，不能来自 RTC 软件包**
- 还需 **ACS SLEC FPGA 3.31** 与 **ACS Firmware 3.10**
- 官方下载项还包括 "**XL SCAN with syncAXIS control**" 与 "Dongle Upgrade: LicenseUpgradeTool"

→ 因此 syncAXIS = 软件层；对应的硬件是 **RTC6 PCIe（需启用 "syncA" 选件）+ ACS 的 SLEC 同步节点**。**(a)**

## 6.2 XL SCAN —— SCANLAB 与 ACS Motion Control 联合开发

一手证据 **(a)**：

- SCANLAB 官方："**XL SCAN** is a scan solution for synchronously controlling a **2D scan head and two mechanical axes**, for example an XY stage with two servo axes. The system was **co-developed by SCANLAB and ACS Motion Control** and provides a **virtually limitless working area**."
  (https://www.scanlab.de/en/products/advanced-scanning-solutions/xl-scan) **(a)**
- ACS Motion Control 官方："**ACS Motion Control Ltd. and SCANLAB GmbH jointly developed XL SCAN**: a solution that fully synchronizes the control of **galvo scanner(s) and motion stages**." / "Supported by all **SPiiPlus Platform** controllers and drive products with **SLEC synchronization node**" / 支持多扫描头、高级激光控制选项（含 **Spot Distance Control**）
  (https://acsmotioncontrol.com/capabilities/motion-to-process-synchronization/xl-scan/) **(a)**

> **注：syncAXIS 不是 "OEM 控制器"，而是配套 XL SCAN 的同步控制软件 + dongle 授权。**

## 6.3 SCANalone —— 无 PC 独立运行

**SCANalone 有两层含义：**

**(1) RTC SCANalone 独立板（2003 年发布，USB 1.1 变体）** **(a)**
(https://www.scanlab.de/en/news-events/press-releases/control-scan-systems-and-lasers-without-requiring-pc)
- "**RTC SCANalone** — SCANLAB's RTC SCANalone Board enables real-time control of scan systems and lasers **without requiring a PC**."
- 运行仅需**外部电源**
- 数据载入：**可插拔 MMC 存储卡** 或 **内置 USB 1.1**
- **板载内存最多 100 万条 list 指令**
- 外部控制信号可启动/影响程序执行；配备额外 **16-bit 数字输入 + 16-bit 数字输出**
- 每 **10 µs** 同步输出 16-bit 数字控制信号
- 也可用 USB 连接 PC 操作，**功能等同 RTC4 PC 接口板**；软件接口与硬件连接能力与 RTC4 PC 接口板**基本兼容**；RTC4 的全部选件（如 3D、POF）均可用
- DirectIndustry 官方目录补充：**USB (RTC4 SCANalone) 允许 standalone 运行，且一台 PC 最多可连接 8 块板** **(b)**
  (https://pdf.directindustry.com/pdf/scanlab-gmbh/rtc4/39164-694240.html)

**(2) RTC6 Ethernet 的 standalone 功能（现代实现）** **(a)**
(https://www.scanlab.de/en/products/control-electronics/rtc-control-boards)
- "**Standalone functionality** — PC-independent control of scan systems: **Predefined laser jobs can be stored in flash memory and started by a system controller**."
- 对比表：Standalone operation = **yes（仅 Ethernet 变体）**。RTC5、RTC4 均为 **no**。
- **RTC6 EtherBox** 亦具备 standalone 功能，并支持 **24/7 运行**、多台 EtherBox 同步。 **(a)**
  (https://www.scanlab.de/sites/default/files/2021-11/RTC6_EtherBox_en.pdf)

---

# 7. 最大扫描速度 / 运动学数值

## 7.1 控制器层面的「最大扫描速度」

**未找到公开数据** —— SCANLAB 的 RTC4 / RTC5 / RTC6 官方产品手册与对比表中**没有**给出控制卡本身以 m/s 或 rad/s 为单位的"最大扫描速度"规格。RTC 板对速度的约束是通过以下**时间与分辨率参数**间接体现的：

| 约束项 | RTC4 | RTC5 | RTC6 | 来源 |
|---|---|---|---|---|
| **输出周期** | 10 µs | 10 µs | 10 µs | **(a)** |
| → 等效位置更新率 | 100 kHz | 100 kHz | 100 kHz | 由输出周期推导 |
| **定位分辨率** | 16 bit | 20 bit | 20 bit | **(a)** |
| **激光延迟分辨率** | 1 µs | 1/2 µs | 1/64 µs | **(a)** |
| **最大位图像素频率** | 50 kHz | 308 kHz（或 300 kHz） | 800 kHz / UFPM 3.2 MHz | **(a)/(c)** |

**(a)** 来源：(https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf)

> 实际可达到的扫描速度由**所接扫描头（galvo）的动力学**决定，而非 RTC 卡。SCANLAB 把速度指标放在扫描头数据表中。

## 7.2 扫描头（excelliSCAN + SCANahead + RTC6）的速度数据 —— 作为参考

**注意：以下为扫描头数据，不是 RTC 控制卡数据。** **(a)**
(https://optoprim.com/wp-content/uploads/2022/03/Tete-scanner-standard-excelliSCAN-SCANLAB.pdf) — SCANLAB excelliSCAN 数据表（经销商托管）

| 应用 | SCANahead 控制 | 常规控制 |
|---|---|---|
| Positioning, jump & shoot | **< 30 m/s** | < 16 m/s |
| Line scan / raster scan | **< 30 m/s** | < 16 m/s |
| Typical vector marking | **< 4 m/s** | < 2.5 m/s |
| 加速度 | **51,000 m/s²**（对应角加速度 **3.2 × 10^5 rad/s²**） | 25,600 m/s²（对应 **1.6 × 10^5 rad/s²**） |
| 接口 | SL2-100 | SL2-100 |

- 同文档另给出对比图例数值 **v = 2.8 m/s**（SCANahead）与 **v = 1 m/s**（常规）。
- 官方描述："With SCANahead control, the excelliSCAN **always reaches the set scan speed using the maximum acceleration** of the galvos."
- SCANahead 选项在 RTC6 上为**可选**（`SCANahead control … for controlling excelliSCAN (optional)`）。
  (https://www.scanlab.de/sites/default/files/2020-08/12_RTC6%20control%20boards.pdf) **(a)**

> 与 RTC6 的 10 µs 输出周期对照：30 m/s 下 10 µs 对应 0.3 mm 位移，这在 20-bit 分辨率、典型 100 mm 场（LSB ≈ 0.1 µm）下**远未触及分辨率极限**，印证了"速度受扫描头限制，不受 RTC 卡限制"。**（此段为推导，非文档直述）**

---

# 8. 校正表 / 编码器 / I/O 数值汇总

## 8.1 校正表 (Correction tables)

| | RTC6 | RTC5 | RTC4 |
|---|---|---|---|
| **格式** | **ct5** | **ct5** | **ctb** |
| **数量 2D / 3D** | **8 / 8** | **4 / 4** | **2 / 1** |
| 备注 | 最多 8 个 3D 校正文件 | 使用 3 或 4 个校正文件时**测量数据内存减半** | — |

**(a)** (https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf) / (https://www.scanlab.de/sites/default/files/2020-08/12_RTC6%20control%20boards.pdf)

- RTC6 手册："3D correction files — **up to eight 3D correction files**"（对比 RTC5 的 "up to two 3D correction files"，注：此处 RTC6 手册写 RTC5 为 2，合集手册写 RTC5 为 4 → **数值冲突，两值并存** **(c)**）
- RTC5 亦支持 **iDRIVE 技术**的全部能力（实时监控与远程诊断、仿真辅助工艺优化、不同动力学调谐选择）。 **(a)**

## 8.2 编码器输入（POF 选项）

| | RTC6 | RTC5 | RTC4 |
|---|---|---|---|
| POF 轴数 | 2（通过编码器值外推获得更高精度） | 2 | 2（选项） |
| 编码器输入 | **2 路，32-bit 计数器** | **2 路，32-bit 计数器** | 手册未列出编码器位数 → **未找到公开数据** |
| 缓存物体数 | 最多 **8 个**（trigger 与打标位置之间） | 最多 **8 个** | 未找到公开数据 |
| 虚拟场值域 | 29 bit | 24 bit | –（无） |

**(a)** (https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf) / (https://www.scanlab.de/sites/default/files/2020-08/12_RTC6%20control%20boards.pdf)

## 8.3 数字 / 模拟 I/O 汇总

| | RTC6 | RTC5 | RTC4 |
|---|---|---|---|
| 模拟输出 | **2 × 12 bit (0…10 V)** | **2 × 12 bit (0…10 V)** | **2 × 10 bit**（引脚与 +5 V / LaserOn 共用，焊锡跳线配置） |
| 16-bit 数字 I/O | 输出 + 输入 | 输出 + 输入 | 16 输入 + 16 输出 |
| 8-bit 数字输出 | 有 | 有 | 有 |
| 2-bit 数字 I/O | 输出 + 输入 | 输出 + 输入 | 未在对比表列出 |
| IO 端口 8/16 bit | 有 | 有 | 有 |
| McBSP (OIE) | 有 (有) | 有 (否) | 否 (否) |
| RS232 | 有 | 有 | 有（**仅 Ethernet 变体**） |
| 步进电机 | 有 | 有 | 有（**仅 PCI Express 变体**） |

**(a)** (https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf)

- **McBSP / OIE**：SCANLAB 官方设有 "**Open Interface Extension**" 页面作为 RTC 控制电子类目下的一级条目，对应对比表中的 McBSP 行。
  (https://www.scanlab.de/en/products/control-electronics/open-interface-extension) **(a)**

---

# 9. 冲突与不确定项清单

| 项目 | 值 A | 值 B | 判定 |
|---|---|---|---|
| RTC5 最大位图像素频率 | **308 kHz**（官方合集手册对比表） | **300 kHz**（官方 RTC5 产品手册正文 "up to 300 kHz"） | **(c)** 两值均出自 SCANLAB 官方文档 |
| RTC5 的 3D 校正文件数 | **4**（官方合集手册对比表 "4 / 4"） | **2**（官方 RTC6 产品手册 "RTC5: up to two 3D correction files"） | **(c)** 两值均出自 SCANLAB 官方文档 |
| RTC4 现行在售变体 | **仅 PCIe 与 Ethernet**（2022 版官方手册） | **PCIe / PCI / USB / Ethernet 四种**（官方 DirectIndustry 目录与 2003、2015 新闻稿） | **(c)** 时间差：PCI 与 USB 为早期型号 |
| RTC5 总线变体 | **PCI、PCI Express**（官方手册/对比表） | 另有 **PC/104-Plus、PCIe/104**（RTC5 手册标题页，经 ManualsLib 二手转录） | **(c)** 嵌入式变体，现行产品页未列 |
| "RTC6 Board" / "RTC6 compact" | 官方产品页与手册仅有 **PCIe / Ethernet / EtherBox** | 未找到独立型号 | **未找到公开数据** |
| RTC4 编码器位数 / POF 物体数 | 对比表未给出 | — | **未找到公开数据** |
| RTC 控制卡的 m/s 或 rad/s 最大扫描速度 | 官方文档未给出该规格 | 扫描头 excelliSCAN 数据可作参考（见 §7.2） | **未找到公开数据**（控制器层） |
| RTC 是否支持 XY3-100 | SCANLAB 文档无记载 | XY3-100 见于 Aerotech GI4 | **未找到公开数据**（SCANLAB 侧）；XY3-100 非 SCANLAB 接口 |

---

# 10. 完整原始 URL 清单

## SCANLAB 官方（一手）

| URL | 内容 |
|---|---|
| https://www.scanlab.de/en/products/control-electronics/rtc-control-boards | RTC 控制卡产品页（RTC6/5/4、EtherBox、standalone、highlights） |
| https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf | **RTC 控制卡合集手册（核心对比表，2024-02 版）** |
| https://www.scanlab.de/sites/default/files/2022-04/uebersicht_rtc_en.pdf | RTC Overview 对比表（英文） |
| https://www.scanlab.de/sites/default/files/2022-04/uebersicht_rtc_de.pdf | RTC Overview 对比表（德文） |
| https://www.scanlab.de/sites/default/files/2020-08/12_RTC6%20control%20boards.pdf | **RTC6 产品手册（07/2021）** |
| https://www.scanlab.de/sites/default/files/2020-08/13_RTC5_control%20boards.pdf | **RTC5 产品手册（09/2022）** |
| https://www.scanlab.de/sites/default/files/2020-08/14_RTC4_control%20boards.pdf | **RTC4 产品手册（09/2022）** |
| https://www.scanlab.de/sites/default/files/2021-11/RTC6_EtherBox_en.pdf | **RTC6 EtherBox 产品手册（09/2022）** |
| https://www.scanlab.de/en/products/control-electronics/rtc-features | RTC Features 页 |
| https://www.scanlab.de/en/products/control-electronics/open-interface-extension | Open Interface Extension (OIE / McBSP) |
| https://www.scanlab.de/en/products/software/rtc-software/download | RTC 软件下载页（RTC6 SW 2.0.0 / 1.25.0，HW Rev 1/2） |
| https://www.scanlab.de/en/downloads/software/syncaxis | **syncAXIS 软件页（需 RTC6 PCIe "syncA" + ACS SLEC 3.31）** |
| https://www.scanlab.de/en/products/advanced-scanning-solutions/xl-scan | XL SCAN 产品页 |
| https://www.scanlab.de/en/applications/micromachining | SL2-100 20-bit vs XY2-100 16-bit 说明 |
| https://www.scanlab.de/en/products/z-axes-3d-add-ons | z 轴与 3D 附件产品线 |
| https://www.scanlab.de/en/products/z-axes-3d-add-ons/excellishift | excelliSHIFT（3D z 轴） |
| https://www.scanlab.de/en/news-events/press-releases/control-scan-systems-and-lasers-without-requiring-pc | **RTC SCANalone 新闻稿（2003-09-05，USB 1.1 + MMC）** |
| https://www.scanlab.de/en/news-events/press-releases/scan-system-control-board-ethernet-interface-simpler-industrial | **RTC4 Ethernet 新闻稿（2015-05-21，含 RTC4 PCI 20,000 台）** |
| https://cdn.casmart.com.cn/file/20220117/3810e78a3b25488eb3abdc20d7d4d7dd.pdf | **XY2-100 Converter (SL2-100 => XY2-100) 官方尺寸与引脚文档（© SCANLAB 2017）** |

## RAYLASE 官方（一手，SP-ICE）

| URL | 内容 |
|---|---|
| https://www.raylase.de/en/products/electronics-control-cards.html | RAYLASE 控制卡产品线（SP-ICE） |
| https://www.raylase.de/en/products/electronics-control-cards/sp-ice-3.html | SP-ICE 3 产品页 |
| https://www.raylase.de/_Resources/Persistent/b/a/6/6/ba66d25112e3d91511322aa417caae73c916557b/Datasheet_SP-ICE-3.pdf | **SP-ICE-3 官方数据手册（v1.7，2025-08）** |
| https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/d6107a36-ef4e-4e13-a21c-6cda62a65fd6.htm | SP-ICE-3 官方用户手册（在线 HTML 版） |
| https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/5a9bd0eb-8de4-4575-807c-987b0f219e46.htm | SP-ICE-3 手册 2 Product Overview（PCIe 或 Gbit-Ethernet） |
| https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/529caef8-cd68-49bd-8d7c-ba68086d1298.htm | SP-ICE-3 手册 2.1 Technical Data（100×180 mm，156 g） |
| https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/522ac573-dca6-4fe2-935c-29b1798fea95.htm | SP-ICE-3 手册 2.3 Main Features |
| https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/48a53e4f-2a14-4518-ad32-d622848ab64a.htm | **SP-ICE-3 手册 2.4 Interfaces（PCIe-x1 v2.1、RL3-100/SL2-100/XY2-100）** |
| https://shop.amstechnologies.com/media/98/e8/44/1720719690/SP-ICE-3-Deflection-Unit-Control-Card-Raylase-Datasheet.pdf?ts=1734637413 | SP-ICE-3 数据手册（分销商镜像） |
| http://alaser.com.tw/db/upload/webdata4/6alaser_201571916204379297.pdf | **RAYLASE SP-ICE 2 硬件手册 MN043 / v1.0.2（一手）** |

## 第三方 / 二手

| URL | 内容 |
|---|---|
| https://pdf.directindustry.com/pdf/scanlab-gmbh/rtc4/39164-694240.html | SCANLAB 官方 RTC4 目录（DirectIndustry 托管；四种接口选项、16/8 卡）— 脚本访问被 403 拦截，内容取自 web_search 片段 |
| https://www.directindustry.com/prod/scanlab-gmbh/product-39164-523087.html | DirectIndustry："3-axis motion control card RTC6" |
| https://pdf.directindustry.com/pdf/scanlab-gmbh-39164.html | SCANLAB 在 DirectIndustry 的全部目录索引 |
| https://www.manualslib.com/manual/3518902/Scanlab-Rtc6-Pcie-Board.html | RTC6 PCIe Board 安装与操作手册（1004 页，RTC6 SW V1.16）— 403 拦截 |
| https://www.manualslib.com/products/Scanlab-Rtc6-Pcie-Board-14108968.html | RTC6 手册目录（含 "44 XY2-100 Converter"） |
| https://www.manualslib.com/manual/2909604/Scanlab-Rtc-5-Pc-Interface-Board.html | RTC5 手册标题页（RTC5 / 5-Express / 5 PC/104-Plus / 5 PCIe/104） |
| https://www.manualslib.com/manual/1581336/Scanlab-Rtc-4.html | RTC4 安装与操作手册 |
| https://www.manualslib.com/manual/2120338/Raylase-Sp-Ice-1-Pci-Pro.html | RAYLASE SP-ICE-1 PCI PRO 硬件手册 |
| https://www.manualslib.com/manual/2485490/Raylase-Sp-Ice-2.html | RAYLASE SP-ICE 2 硬件手册 |
| https://manualzz.com/doc/33762234/raylase-sp-ice-2-control-card-hardware-manual | RAYLASE SP-ICE 2 手册（Manualzz 镜像）— 403 拦截 |
| https://www.aerotech.com/product/automation1-gi4-laser-scan-head-controller/ | **Aerotech Automation1 GI4：XY2-100 / XY3-100** |
| https://www.aerotech.com/wp-content/uploads/2021/11/Automation1-GI4-Data-Sheet-D20220401.pdf | Aerotech GI4 数据表（XY3-100 支持） |
| https://acsmotioncontrol.com/capabilities/motion-to-process-synchronization/xl-scan/ | ACS Motion Control：XL SCAN 联合开发、SPiiPlus + SLEC |
| https://optoprim.com/wp-content/uploads/2022/03/Tete-scanner-standard-excelliSCAN-SCANLAB.pdf | SCANLAB excelliSCAN 数据表（扫描头速度 30/16/4/2.5 m/s、51,000 m/s²） |
| https://www.expo21xx.com/additive_manufacturing/21633_st3_laser_3d_printing/default.htm | 提到 XL SCAN 与 syncAXIS 控制软件 |

## 明确无法访问的站点（脚本访问被拦截）

- `pdf.directindustry.com` → HTTP 403（内容已通过 web_search 片段获取）
- `manualslib.com` → HTTP 403
- `manualzz.com` → HTTP 403
- `blog.csdn.net` → HTTP 521（已知）
- `gitcode.com` → HTTP 418（已知）

---

# 11. 一页速查（关键数值）

| 规格 | RTC4 | RTC5 | RTC6 | SP-ICE-3 (RAYLASE) |
|---|---|---|---|---|
| 厂商 | SCANLAB | SCANLAB | SCANLAB | **RAYLASE** |
| 主机接口 | PCI / PCIe / USB 1.1 / Ethernet 10-100 | PCI / PCIe-x1 v1.0 | PCIe / GbE | PCIe-x1 v2.1 / GbE |
| **振镜接口** | **XY2-100** | **SL2-100**（XY2-100 需转换器） | **SL2-100**（XY2-100 需转换器） | SL2-100 / RL3-100（XY2-100 需适配板） |
| 定位分辨率 | **16 bit** | **20 bit** | **20 bit** | **20 bit**（XY2-100 时 16 bit） |
| 轴数 | 2（3 通道） | 2 | 2 | 2（RL3-100 下最多 5 轴） |
| 输出周期 | **10 µs** | **10 µs** | **10 µs** | **10 µs** |
| 模拟输出 | 2 × 10 bit | 2 × 12 bit | 2 × 12 bit | 2 路 0-10 V |
| 激光延迟分辨率 | 1 µs | 1/2 µs | **1/64 µs** | — |
| 位图频率 | 50 kHz | 308 kHz / 300 kHz | **800 kHz（UFPM 3.2 MHz）** | 1 MHz |
| 最大激光频率 | — | — | n × 100 kHz 同步 | **16 MHz** |
| 列表内存 | ~8,000 | 2^20（~100 万） | **2^23（~800 万）** | 仅受 RAM 限制（1 GB） |
| 校正文件 2D/3D | 2/1 (ctb) | 4/4 (ct5) | **8/8 (ct5)** | 1 GB 专用 DDR3 |
| 最大卡数/PC | 16 (PCI/PCIe) / 8 (USB) | 任意 | **255** | 任意 |
| Standalone | 仅 SCANalone 变体 | 否 | **是（Ethernet）** | **是（GbE）** |
| SCANahead | 否 | 否 | **是（可选）** | — |
| 3D | 选项 | 选项 | **选项，8 个 3D 校正表** | RL3-100 支持 3/5 轴 |
