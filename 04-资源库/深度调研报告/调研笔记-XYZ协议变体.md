# 三轴振镜控制协议调研报告：XY3-100 / XY2-100(-3D) / XYZ-100 / SL2-100-3D

调研日期：2026（本报告所有数据均来自公开来源，逐条标注原始 URL）
调研目标：XY3-100、XY2-100-3D / XYZ-100、SL2-100-3D，以及第三轴（Z / 聚焦轴）相对两轴 XY2-100 的处理方式。

## 0. 证据分级说明

- **(a) 一手/官方文档验证**：标准原文、厂商官方手册/数据手册/产品页。
- **(b) 二手来源**：博客、论坛、经销商页面、第三方镜像。
- **(c) 存疑/冲突**：来源互相矛盾时，两个数值都列出。
- 找不到的数据一律写 **未找到公开数据**，不做推测填充。

---

## 1. 结论速览（关键数值）

| 项目 | XY2-100 | XY3-100 |
|---|---|---|
| 位宽 | 16 bit（XY2-100E 为 18 bit） | 可变 16..26 bit |
| 帧率 | 100 kHz | 可变，典型 100 kHz |
| 传输率 | 100 ks/sec | 可变，典型 100 ks/sec |
| 帧长 / 时钟 | 20 bit 帧，10 µs @2 MHz（Newson/RAYLASE） | 24 bit 帧 @2.4 MHz 或 32 bit 帧 @3.2 MHz，均为 10 µs |
| 回传通道 | 20 bit 同步于 XY2-100 时钟 | 异步 RS485 串行，默认 115200 bps，可扩 |
| 物理接口 | DB25 | DB25（v1.0/v1.1）+ DB15（v1.1 新增） |
| 最大轴数 | 3（X/Y/Z），10 根信号线（3D） | 5（X/Y/Z/U/W），DB15 最多 3 轴 |
| 纠错 | 奇偶校验位 | 位置/命令数据用"1 计数"校验（P1P0 或 P3..P0），回传用二进制协议 |

*(a) 来源：LasIA XY3-100 规范 v1.1（LIA202307）第 5 页对照表 —
https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf*

**最重要的一条结论**：**XY3-100 不是"20 bit XY2-100"，也不是"18 bit"**。它是 LasIA（Laser Industry Association）定义的、位宽可在 16~26 bit 之间自适应的新标准，且与 XY2-100 **引脚兼容（pin-compatible）**，可通过固件升级实现。
*(a) 同上，第 3.1 节 "pin-compatible to XY2-100, so upgrade is possible via firmware modification"*

---

## 2. XY3-100：定义者、标准号 LIA202002、帧格式

### 2.1 谁定义 XY3-100 —— LIA202002 的真相

`LIA202002` **不是中国标准，也不是 LASER INDUSTRY ASSOCIATION 之外的什么组织**，而是 **LasIA（Laser Industry Association）自己给文档编的编号**。规范原文版权页明确写着：

> "The document and all its information ... are © by **Laser Industry Association** (named "LasIA" in this document)."
*(a) LasIA XY3-100 规范 v1.1，第 1 节 Copyright —
https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf*

文档封面直接印着两个版本号：

> **Version 1.0 LIA202002**
> **Version 1.1 LIA202307**
*(a) 同上，PDF 封面*

也就是说 **LIA202002 = XY3-100 规范 1.0 版（2020-09 发布）**，**LIA202307 = 1.1 版（2023-07 发布）**。LasIA 的文档编号规则为 `LIA<年份><序号>`，同系列还有：

| 编号 | 文档 | URL |
|---|---|---|
| LIA202001 | XY2-100 Protocol Format Specification | https://web.archive.org/web/20231206141529id_/https://lasia.org/LIA202001/xy2_100_specification.pdf |
| LIA202002 | XY3-100 Protocol Format Specification v1.0 | https://web.archive.org/web/20210122224854id_/https://lasia.org/LIA202002/xy3_100_specification.pdf |
| LIA202101 | Laser Interface Specification | https://web.archive.org/web/20231206131409id_/https://lasia.org/LIA202101/laser_interface_specification.pdf |
| LIA202102 | Analog Scanhead Specification | https://web.archive.org/web/20211022064721id_/http://lasia.org/LIA2021xx/analog_scanhead_specification.pdf |
| LIA202307 | XY3-100 Protocol Format Specification v1.1 | https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf |
| — | 配套头文件 xy3_100.h（v1.1） | https://web.archive.org/web/20231206133135id_/https://lasia.org/LIA202307/xy3_100.h |

**注意**：lasia.org 官方网站现在对所有请求返回 **HTTP 401 Unauthorized**（需认证），上述 PDF 只能通过 Wayback Machine 快照获取（2021/2022/2023 年多次存档均有）。
*(a) 直接访问 http://www.lasia.org/LIA202307/xy3_100_specification_v11.pdf 返回 401 —
http://www.lasia.org/LIA202307/xy3_100_specification_v11.pdf ；存档索引见
http://web.archive.org/cdx/search/cdx?url=lasia.org*&output=text&limit=200&collapse=urlkey*

**厂商对 LIA202002 的引用（佐证该标准号被产业界使用）**：HALaser Systems 的 E1701D / E1702S 产品页写 "20 bit XY3-100 (**certified LIA202002 standard**) interface with X and Y channel"。
*(a) https://halaser.systems/e1701.php 、https://halaser.systems/e1702s.php 、https://halaser.eu/e1701.php*

> ⚠️ **冲突提示 (c)**：LasIA 的 `xy3_100.h` 头文件明确禁止厂商使用 "certified/compliant/guaranteed compatible" 之类的措辞：
> "they are NOT ALLOWED to name it 'compliant', 'certified', 'guaranteed compatible' or in any other way that implies a guaranteed conformity"
> *(a) https://web.archive.org/web/20231206133135id_/https://lasia.org/LIA202307/xy3_100.h*
> 因此 HALaser 页面上的 "certified LIA202002 standard" 属于**厂商自述**，与 LasIA 商标条款存在措辞冲突（不排除 HALaser 另行取得了 LasIA 许可）。

### 2.2 XY3-100 帧格式（官方原文）

XY3-100 是 **SPI-like** 接口：`SYNC` 相当于片选 CS，`CLK` 相当于 SCK，`X/Y/Z/U/W` 相当于 SDI/MOSI。

> "The protocol works similar to a standard SPI interface with CS (also named SS), SCK and SDI (also named MOSI) lines. ... The beginning of a frame is marked by the **falling edge** at the SYNC-channel (CS). Whenever data at X, Y, Z, U and W channel (SDI) are valid, this is signalled by a **falling edge** on the CLK-channel (SCK)."
*(a) LasIA XY3-100 v1.1 第 5.1 节 — https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf*

**帧头 2 bit 定义**（注意：第一个 bit 是 **MSB**，即 bit31 或 bit23）：

> "The first bit (n, **31 or 23**) signalises the length of the whole frame. When it is **0**, the frame has a total length of **24 bits with a payload of 22 bits**. When it is **1**, it has a length of **32 bits with a payload of 30 bits**."
> "The second bit (n-1) specifies the mode of operation. When it is set to **1**, position data will follow. A value of **0** specifies a frame that contains **commands**..."
*(a) 同上*

#### 24 bit 位置帧（20 bit 位置数据）

```
Bit   23 22 21 20 19 18 17 16 15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0
Data   0  1            D19..D0 position data                                P1 P0
```
- 位置分辨率最大 **20 bit**；接收端（振镜）可自行选择精度，不足时**忽略低位**；发送端（控制卡）不足时**低位补 0**。
- 校验位算法：统计 `D19..D0`（bit21..bit2）中 1 的个数 → 与 `0x03` 相与 → 低 2 位分别写入 P1(0x02) 与 P0(0x01)。
- **100 ks/sec 时整帧 10 µs，对应时钟频率 2.4 MHz**；也允许更高（200 ks/sec：5 µs，**4.8 MHz**）。
*(a) 同上*

#### 32 bit 位置帧（26 bit 位置数据，官方"推荐"）

```
Bit   31 30 29 28 27 26 .. 16 15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0
Data   1  1            D25..D0 position data                                P3 P2 P1 P0
```
- 位置分辨率最大 **26 bit**。
- 官方给出的用途说明：高分辨率中间数据可全精度传给振镜，避免运输环节的精度损失，即使振镜实际输出分辨率低于 26 bit 也能减少舍入误差。
- 校验：统计 `D25..D0`（bit29..bit4）中 1 的个数 → 与 `0x0F` 相与 → 4 位分别写入 P3(0x08)、P2(0x04)、P1(0x02)、P0(0x01)。
- **100 ks/sec 时整帧 10 µs，对应时钟频率 3.2 MHz**；200 ks/sec：5 µs，**6.4 MHz**。
*(a) 同上*

#### 命令帧（24 bit / 32 bit）

```
24 bit:  Bit 23 22 = 0 0 ,  D19..D0 command data ,  P1 P0
32 bit:  Bit 31 30 = 1 0 ,  Bit29..24 = X(未使用，建议置0但参与校验) , D19..D0 command data , P3 P2 P1 P0
```
*(a) 同上*

**已定义的 20 bit 控制命令**（*(a) 同上，第 5.1.1 节*）：

| 命令 | 值 | 说明 |
|---|---|---|
| `XY3_CMD_AUTOCALIB_ON` | 0x800XX | 打开自动校准/调整，低 5 bit 为轴选择 |
| `XY3_CMD_AUTOCALIB_OFF` | 0x40000 | 关闭自动校准 |
| `XY3_CMD_CALIB_START` | 0xC0000 | 触发一次校准 |
| `XY3_CMD_REF_START` | 0x20000 | 触发回零/参考运行 |
| `XY3_CMD_BACK_RATE57` | 0xA0000 | 回传速率 → 57600 bit/s |
| `XY3_CMD_BACK_RATE115` | 0xE0000 | 回传速率 → 115200 bit/s（默认） |
| `XY3_CMD_BACK_RATE230` | 0x10000 | 回传速率 → 230400 bit/s |
| `XY3_CMD_BACK_RATE460` | 0x90000 | 回传速率 → 460800 bit/s |
| `XY3_CMD_BACK_RATE912` | 0xD0000 | 回传速率 → 921600 bit/s |
| `XY3_CMD_TEMPCOMP_ON` | 0x880XX | 打开动态温度补偿 |
| `XY3_CMD_TEMPCOMP_OFF` | 0x48000 | 关闭动态温度补偿 |
| `XY3_CMD_BACK_RATE`（v1.1 新增） | 0xC80XX | 可变回传波特率：低 8 bit × 28800 = bps（如 0xC8004 → 4×28800 = 115200） |

轴标志位：`AXIS_FLAG_X=0x00001`、`Y=0x00002`、`Z=0x00004`、`U=0x00008`、`W=0x00010`。
*(a) https://web.archive.org/web/20231206133135id_/https://lasia.org/LIA202307/xy3_100.h*

### 2.3 XY3-100 硬件接口与连接器（第三轴在此）

**DB25（v1.0 与 v1.1 均有）** *(a) 规范 v1.1 第 4.1 节*：

| 引脚 | 信号 | 引脚 | 信号 |
|---|---|---|---|
| 1 | **SYNC- (A-)** | 14 | SYNC+ (A+) |
| 2 | **CLK- (B-)** | 15 | CLK+ (B+) |
| 3 | X- (C-) | 16 | X+ (C+) |
| 4 | Y- (D-) | 17 | Y+ (D+) |
| **5** | **Z- (E-)** | **18** | **Z+ (E+)** |
| 6 | BACK- (F-) | 19 | BACK+ (F+) |
| 7 | U- (G-) | 20 | U+ (G+) |
| 8 | W- (H-) | 21 | W+ (H+) |
| 9/10 | V+ | 22 | V+ |
| 11 | GND | 23/24 | GND |
| 12/13 | V- | 25 | V- |

**DB15（v1.1 新增，最多 3 轴）** *(a) 规范 v1.1 第 4.2 节*：

| 引脚 | 信号 | 引脚 | 信号 |
|---|---|---|---|
| 1 | SYNC- (A-) | 9 | SYNC+ (A+) |
| 2 | CLK- (B-) | 10 | CLK+ (B+) |
| 3 | X- (C-) | 11 | X+ (C+) |
| 4 | Y- (D-) | 12 | Y+ (D+) |
| **5** | **Z- (E-)** | **13** | **Z+ (E+)** |
| 6 | BACK- (F-) | 14 | BACK+ (F+) |
| 7 | 未使用 | 15 | GND |
| 8 | GND | — | — |

> 原文："Comparing to the full-size DB25 connector the U- and W-channels ... are not supported with this interface **limiting the DB15-connection to a maximum of three axes**."
*(a) 同上*

**26-pin IDC（可选，通常白色）** *(a) 规范 v1.1 第 4.1 节表*：1/2=SYNC、3/4=CLK、5/6=X、7/8=Y、9/10=Z(可选)、11/12=BACK(可选)、13/14=U(可选)、15/16=W(可选)、17~25=电源。

**16-pin IDC（DB15 的 IDC 版本）**：1/2=SYNC、3/4=CLK、5/6=X、7/8=Y、9/10=Z、11/12=BACK、13=未使用、14/15=GND。
*(a) 规范 v1.1 第 4.2 节表*

**电气层**：RS485，需符合 **ANSI/TIA/EIA-485-A** 与 **ISO 8482:1987**，接收端需正确端接。
*(a) 规范 v1.1 第 4.1/4.2 节："Transmission on RS485 data lines need to be conform to ANSI Standard TIA/EIA−485−A and ISO 8482:1987 and require a proper termination on receiver side."*

> ⚠️ **规范原文笔误 (c)**：v1.1 第 4.1 节 26-pin IDC 表中第 4 脚写作 "CLK- (B+)"，按上下文应为 "CLK+ (B+)"。

### 2.4 XY3-100 回传通道（BACK）—— 与 XY2-100 最大的架构差异

XY2-100 的回传是**同步**的 20 bit 状态流；XY3-100 换成**完全独立于位置时钟的异步 RS485 串口**：

> "The backchannel via the BACK–lines (F+/F+) is completely independent from the CLK line of the position data channels. It is an RS485 serial interface with a default transmission rate of **115200 bps, 8 data bits, 1 stop bit and no parity**."
*(a) 规范 v1.1 第 5.2 节*

包结构固定为 4 段：`Head(8bit, 恒为 0x48)` + `Type(8bit)` + `Length(8bit)` + `Payload`。同步包为 `48 41 00`（无载荷），接收端在数据流中发现 `0x48 0x41 0x00 0x48` 即判定重新同步。
*(a) 同上*

包类型（*(a) 同上 + https://web.archive.org/web/20231206133135id_/https://lasia.org/LIA202307/xy3_100.h*）：

| Type | 名称 | 载荷 |
|---|---|---|
| 0x41 | SYNC（同步包） | 无 |
| 0x01 | Vendor 厂商名 | 3..200 B ASCII |
| 0x02 | Model 型号 | 3..200 B ASCII |
| 0x03 | Firmware 版本字符串 | 3..200 B ASCII |
| 0x04 | Serial Number 序列号 | 3..200 B ASCII |
| 0x05 | Temperature 温度 | 最多 22 个 int16，单位 1/100 ℃；不支持填 −32767 |
| 0x06 | Frame Error Count 帧错误计数 | 5×uint32（X/Y/Z/U/W 各自 parity error 累计数，上电以来）|
| 0x07 | Error State 错误状态 | 最多 22 个 uint8（0=正常，1=温度，2=数据，3=超程，4=电源，5=其他电气，6=调整，7=其他机械，100..255 厂商自定义）|
| 0x08 | Debug | 3..200 B（仅开发用）|
| 0x09 | Working Hours 工作时长 | 最多 22 个 uint32（小时）|
| 0x0A | Actual Position Delta（v1.1 新增）| 最多 5 个 int16，各轴相对上次本包的位置变化（单位 bit）；32767 = 正向 ≥32767 bit，−32768 = 负向 ≥32768 bit |

组件索引（温度/错误/工时三张表共用 `enum components`）：`0 Head, 1 DSP, 2 DAC X, 3 DAC Y, 4 DAC Z, 5 DAC U, 6 DAC W, 7 Driver X, 8 Driver Y, 9 Driver Z, 10 Driver U, 11 Driver W, 12 Galvo X, 13 Galvo Y, 14 Galvo Z, 15 Galvo U, 16 Galvo W, 17 Mirror X, 18 Mirror Y, 19 Mirror Z(=focus optics), 20 Mirror U, 21 Mirror W`。
*(a) 规范 v1.1 第 5.2 节*

### 2.5 XY3-100 v1.0（LIA202002）vs v1.1（LIA202307）差异

*(a) 规范 v1.1 "2 Document history" 表*

| 日期 | 变更 |
|---|---|
| 07/2020 | Initial version（初版）|
| 07/2020 | Frame length information corrected to **10 usec** |
| 07/2020 | Description of 32 bit frame clarified；Frame Error Count Packet 描述修正；补全回传索引值 |
| 08/2020 | 版权信息更新 |
| **09/2020** | **Version 1.0 released（= LIA202002）** |
| 07/2021 | **新增 DB15 连接器引脚定义** |
| 10/2021 | 新增 RS485 传输线技术标准（TIA/EIA-485-A、ISO 8482:1987）|
| 02/2022 | 新增回传通道数据使用建议 |
| 03/2022 | 新增 Actual Position Delta Packet |
| 05/2022 | 新增命令 `XY3_CMD_BACK_RATE` |
| 10/2022 | 少量修正 |
| **07/2023** | **Version 1.1 released（= LIA202307）** |

**关键：帧格式（24/32 bit、2.4/3.2 MHz、P1P0/P3..P0）在 v1.0 与 v1.1 中完全一致**，逐字比对无差异。v1.1 只增加了 DB15、RS485 线路标准、可变波特率命令和位置增量包。
*(a) 对比 https://web.archive.org/web/20210122224854id_/https://lasia.org/LIA202002/xy3_100_specification.pdf 与
https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf 第 5.1 节*

### 2.6 中文二手来源的交叉验证（(b)）

星移控制科技（Xymotion）的《XY3-100协议简介》逐条复述了 LasIA 规范内容并注明 "*协议部分内容来自 LasIA"，与官方原文完全吻合：
- "XY3-100 协议具有灵活的位宽设置（位置坐标位宽 **16-26bit**）"
- 24 bit 帧："0 表示位宽为 24bit，1 表示位宽 32bit（推荐）"；"第二个 bit ... 1 表示该数据帧为位置坐标，0 表示该数据帧为控制指令（暂不支持）"
- "位置坐标信号位宽最大 20bit ... 时钟（CLK）可以提高到 **2.4Mhz** 以保证 **10us** 的刷新周期"
- "位置坐标信号位宽最大 26bit ... **P3/P2/P1/P0** ... 数据 BIT29-BIT4 ... 同 0xF 进行与处理 ... 时钟（CLK）可以提高到 **3.2Mhz**"
*(b) https://www.xymotion.cn/index.php?m=home&c=View&a=index&aid=52*

> 注：该文中 20 bit 与 26 bit 两段并存，**不是矛盾**——分别对应 24 bit 帧与 32 bit 帧两种帧长。

**Xymotion 实测波形（(b)，与规范数值自洽）**：《如何通过XY3-100协议获取电机实时坐标数据》给出示波器抓取的 32 bit 帧实例，可直接用于验证：
- X 轴下发 `0xE0000000`：bit31=1（32bit 帧）、bit30=1（位置帧）、bit29..bit4 全 0（坐标居中）、bit3..bit0 = P3..P0 = 0000（0 个 1 → 0 % 16 = 0）✓
- XR 回传 `0x9FFFE101`：bit31=1、bit30=0（回传/控制帧）、bit29..bit4 = 0x1FFFE1、bit3..bit0 = 0001。0x1FFFE1 中 1 的个数 = **17**，17 % 16 = **1** → P3P2P1P0 = 0001 ✓
- 结论："总线下发的 X 轴坐标数据为 0x8000，反馈的当前实时坐标数据为 0x7FFF，误差为 1"
*(b) https://www.xymotion.cn/index.php?m=home&c=View&a=index&aid=51*

> ⚠️ **冲突/偏差 (c)**：Xymotion 驱动器（XY80xx 系列）的 IDC 端子表为
> `CLK PIN1-/2+`、`SYNC PIN3-/4+`、`X PIN5-/6+`、`Y PIN7-/8+`、`Z PIN9-/10+`、`YR PIN11-/12+`、`ZR PIN13-/14+`、`XR PIN15-/16+`
> 即 CLK 在 1/2、SYNC 在 3/4，且用 **3 对独立差分线 YR/ZR/XR** 做坐标回传，而**不是** LasIA 规范里的 `SYNC 1/2、CLK 3/4` + 单对 RS485 `BACK 11/12`。这是**厂商私有变体**，不能当作 XY3-100 标准实现。
*(b) 同上；对照 (a) LasIA XY3-100 v1.1 第 4.1/4.2 节*

---

## 3. XY2-100 的第三轴（Z）：XY2-100-3D / XYZ-100

### 3.1 结论：不存在独立的 "XY2-100-3D" / "XYZ-100" 标准，3 轴只是 XY2-100 多加一对 Z 差分线

**XY2-100 本身就被定义为最多 3 轴（X/Y/Z）**。HALaser Systems 的协议对照表明确列出：

| | XY2-100 | XY2-100E | XY3-100 |
|---|---|---|---|
| Accuracy | 16 bit（64K steps） | 18 bit（256K steps） | 16..26 bit（64K..64M steps）|
| **Maximum number of axes** | **3** | **3** | **5** |
| **Number of wires (2D)** | **8** | 8 | 8 |
| **Number of wires (3D)** | **10** | **10** | **10** |
| Backchannel | synchronous, 20 fixed data bits | synchronous, 20 fixed data bits | asynchronous, variable multi-purpose data |
| Error Detection | parity bit | parity bit | parity counter / protocol data structure |

*(a) https://halaser.systems/compare.php （表格"Number of wires"行、3D 行中 Analogue=6 / XY2-100=10 / XY2-100E=10）*

10 根线 = 5 对差分 = CLK±、SYNC±、X±、Y±、**Z±**。8 根线 = 4 对 = 去掉 Z±。

### 3.2 RAYLASE XY2-100-E：官方 DB25 三轴引脚定义（一手证据）

RAYLASE SS-III XY2-100-E 接口手册原文：

> "With XY2-100-E each axis (**x, y and also z**) of the deflection units has a data channel to the head and a data channel back to the control card. Additionally each axis has a common clock line and data line."
*(a) RAYLASE《Documentation of the SS-III XY2-100-E Interface》第 2 节 —
http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf*

DB25 引脚（*(a) 同上 第 2.1.1 节*）：

| Pin | 方向 | 信号 | Pin | 方向 | 信号 |
|---|---|---|---|---|---|
| 1 / 14 | in | CLK− / CLK+ | | | |
| 2 / 15 | in | SYNC− / SYNC+ | | | |
| 3 / 16 | in | X− / X+（position und command，small mirror）| | | |
| 4 / 17 | in | Y− / Y+（position und command，big mirror）| | | |
| **5** | in | **Z−（position und command, focus axis）** | **18** | in | **Z+（focus axis）** |
| 6 / 19 | out | Y_stat− / Y_stat+（feed-back channel）| | | |
| **7** | out | **Z_stat−（feed-back channel）** | **20** | out | **Z_stat+** |
| 8 / 21 | out | X_stat− / X_stat+ | | | |
| 9,10,12,13,22,25 | — | don't connect（选配 ±15V 供 head）| | | |
| 11,23,24 | — | GND | | | |

**时序与帧格式**（*(a) 同上 第 2.2 / 3.1 节*）：
- "A frame consists of **20 Bits**. The last bit of a frame is shown by a '0' on the SYNC line pair."
- "During the **positive edge** of the CLK+ line, data changes on the X-, Y- and Z-line pairs toward deflection unit."
- "During the **negative edge** of the CLK+ line, data changes on the X_stat-, Y_stat- and Z_stat-line pairs from the deflection unit."（回传通道比下发通道延迟约半个时钟）
- **时钟最高 10 MHz，推荐 4 MHz**；推荐线驱动 UA9638CD，线接收 MAX3096 或 UA9637，也可用 AM26LV32。
*(a) 同上*

**X/Y 定义冲突提示 (c)**：RAYLASE 定义"激光先打到的那面镜子（较小的镜子）为 X 轴"，而"Some other producers define the axis which is first hit by the laser as Y-Axis"，因此"the pins of the X and Y channels are **swapped**"。替换振镜时 X/Y 可能需要对调。
*(a) 同上 第 2.1.2 节*

### 3.3 XY2-100 基础版（非 -E）的标准帧格式（一手证据）

**LasIA 官方 LIA202001《XY2-100 Laser Scanner Protocol Format Specification》全文只有 3 页，只规定帧格式，不给引脚表**：

> "The rising edge on SYNC marks the beginning of a XY2-100 frame, the **falling edge on SYNC** signals the beginning of the **last bit** of the current XY2-100 frame. Data are valid on **falling edge on CLK**."
> 标准 16 bit 模式：前 3 bit = `001`，随后 16 bit 位置数据 D15..D0，最后 1 bit **偶校验 Pe**。
> 增强 18 bit 模式：第 1 bit = `1`，随后 18 bit 位置数据 D17..D0，最后 1 bit **奇校验 Po**。
*(a) https://web.archive.org/web/20231206141529id_/https://lasia.org/LIA202001/xy2_100_specification.pdf*

> 注：同一份 PDF 被第三方镜像在 https://www.aaronvose.net/Quantronix_Osprey/xy2_100_specification.pdf （文件字节数 36177，与 LasIA LIA202001 完全一致）和 GitHub https://github.com/georgemihaila/xy2-100/blob/main/docs/xy2_100_specification.pdf 。
*(a/b) 上述 URL*

**Newson 官方 XY2-100 技术数据表（含引脚与完整时序，一手）**：

> "The XY2-100 interface is used to send X and Y coordinates ... It is a serial interface using **20-bit words**, sent with a speed of **2 Mbit/s or 100 kwords/s**."
> "The first 3 bits are used as a control word (**C2-C0**). The next **16 bits** are data information (D15-D0, **offset binary**) and the last bit is a parity bit (P, **even parity**)."
> "C2 C1 C0 = **0 0 1** → motor setpoint value"
> "The SYNC bit goes **high when the first bit can be sent**. It remains high for **19 bits** and goes **low when the parity** can be sent."
> "The clock signal runs at a frequency of **2 MHz**. When it goes high, the data bit changes. When it goes low, the data bit is sampled by the deflection system."
> STATUS："not synchronised with the SENDCK input"
*(a) Newson Engineering《rhothor X7 I/O configuration: XY2-100 TECHNICAL DATASHEET》Rev 0703 —
https://www.newson.be/doc.php?id=XY2-100*

Newson 的引脚表（2 轴用法，第 5/18 与 7/20 脚留空 —— 这正是三轴时 Z 与 Z_stat 的位置）：

| Pin | 名称 | 说明 | 方向 |
|---|---|---|---|
| 1 / 14 | IO1− / IO1+ | **SENDCK**（连续时钟）| In |
| 2 / 15 | IO2− / IO2+ | **SYNC** | In |
| 3 / 16 | IO3− / IO3+ | CHANNELX | In |
| 4 / 17 | IO4− / IO4+ | CHANNELY | In |
| **5 / 18** | IO5− / IO5+ | **（2 轴时未使用 → 3 轴时的 Z）** | — |
| 6 / 19 | IO6− / IO6+ | STATUS | Out |
| **7 / 20** | IO7− / IO7+ | **（2 轴时未使用 → 3 轴时的 Z_STAT）** | — |
| 13 | REF_IO | 接控制卡 GND | — |

*(a) 同上*

### 3.4 其他一手证据

**sigrok 协议解码器（(a)，开源项目官方文档）**：
> "The most often encountered setups use common clock and sync signals with two pairs of data and status signals - one for the X and one for the Y axis. **Sometimes, a Z axis is also present.** Electrically, all signals are transmitted differentially."
> "XY2-100 is the base variant with a clock frequency of up to **2 MHz**；XY2-200 is XY2-100 with a clock frequency of up to **4 MHz**；XY2-100E and XY2-200E are enhanced variants, offering the possibility to send additional commands to the scanner and the user can influence the format of the status channel"
> "The primary functionality ... is submitting **16-bit signed integers** to the scanner to control the galvanometer position, with **0 being the center**. The protocol also allows this to be extended to **18 bits**... the 18-bit mode is in part indicated by an **inverted parity bit (odd parity)** while the command mode available in the -E variants uses the default **even parity**."
> 状态/反馈信号至少有 **3 种变体**：backwards-compatible 16 bit、standard 16 bit、18 bit，"They can't be distinguished from another"。
*(a) https://sigrok.org/wiki/Protocol_decoder:Xy2-100*

**HALaser E1803D 手册（(a)）**：XY2-100 接线为 `CLK 1/2`、`SYNC 3/4`、`X 5/6`、`Y 7/8`、`Z 9/10`、`STATUS 11/12`（26-pin IDC 编号）；D-SUB25 为 CLK−/SYNC−/X−/Y−/Z−/STATUS− 同一套信号。手册还给出"20 bit 帧 = 10 µs ≈ 100 kHz"，XY2-200 为"20 bit 帧 = 5 µs ≈ 200 kHz"。
*(a) https://halaser.systems/manuals/e1803_manual.pdf （7.6 节与 Appendix B）*

**PMDi Polaris（(a)，厂商产品页）**：
> "The Polaris XY2-100 Module ... has one or two **DB25** connectors. **Each connector supports XY scanner motors and a Z focus motor. The XY2-100, and XY2-100-E protocols are both supported.**"
> "The Polaris SL2-100 Module ... has two sets of Galvoscanner connectors. **Each row supports two scanner motors and one focus motor.**"
*(a) https://pmdi.com/posts/product/hardware/xy2-100-galvoscanner-module/ 、
https://pmdi.com/posts/product/hardware/sl2-100-galvoscanner-module/*

**Novanta / Cambridge Technology LIGHTNING II 3-axis（(a)，厂商数据手册）**：3 轴数字扫描头，集成 Dynamic Focusing Module (DFM) 做 z 轴；`Command Resolution: 24-bit`；孔径 20/30/50 mm；跟踪延迟 0.2/0.2/0.4 ms；重复性 <2 µrad；长期漂移 <10 µrad；热漂移 <2 µrad/℃。
*(a) https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf*

**Novanta LIGHTNING II XY2-100 接线须知（(a)，官方说明，经 ManualsLib 转载）**：
> "Make sure that the X-axis galvo connects to X-axis servo, Y-axis galvo connects to Y-axis and **for 3-Axis Scan Head that the Z-axis galvo** [connects to the Z-axis servo]"
*(a/b) https://www.manualslib.com/manual/2643580/Novanta-Lightning-Ii-Xy2-100.html*

### 3.5 "XYZ-100" 是什么？

**不存在名为 "XYZ-100" 的公开标准**。该字符串在公开资料中只出现在：
- **Synrad（Novanta）SMC 控制器的商品描述**："SMC controller **XYZ-100 Galvo Command interface**"，同一台设备还标注 "Scan head L2B50X3C**XY2**A-25-A001 **3 Axis**" —— 即厂商市场用语，底层接口是 XY2-100 三轴。
*(b) https://surplusrecord.com/listing/synrad-octiv-co2-laser-900-watt-smc-controller-xyz-100-galvo-command-interface-2023-473129/ 、
https://www.machinio.com/synrad/laser-cutters/co2-lasers/united-states 、
https://revelationmachinery.com/product/900w-synrad-octiv-co2-laser-2023-barely-used/*
- 以及若干**完全无关**的产品（Langantech XYZ-100 柔性补偿模块、Queensgate NPS-XYZ-100 纳米定位台），属于命名巧合。
*(b) https://www.langantech.com/product/en/compensator-XYZ-100.html 、 https://www.gmp.ch/pdf/Datasheets/Queensgate/NPS-XYZ-100A-Z15H.pdf*

**结论**：工程实现时应使用准确名称 —— 两轴/三轴 XY2-100、XY2-100-E（18 bit + 独立 status）、或 XY3-100。术语 "XY2-100-3D"、"XYZ-100" 都不是标准名称，**未找到公开数据**支持其为独立协议。

---

## 4. SCANLAB 的第三轴 / Z 轴方案

SCANLAB **没有** "SL2-100-3D" 这一命名。其 3D 方案是**"2D 扫描头 + 独立 Z 轴模块 + 支持 3 轴的控制卡"**，Z 轴模块自带 SL2-100（或 XY2-100 Enhanced）接口。

### 4.1 SL2-100 协议参数

> "Here, the **20-bit SL2-100 protocol, developed and introduced by SCANLAB**, is a necessary upgrade. High-end scan systems and control boards such as **RTC5 and RTC6** support this protocol."
*(a) https://www.scanlab.de/en/applications/micromachining*

> "The RTC5 communicates with scan systems via the new SL2-100 data transfer protocol. This protocol supports **20-bit control signals** and thereby a **16x higher positioning resolution compared to the RTC4** predecessor board."
*(a) https://www.scanlab.de/sites/default/files/2020-08/13_RTC5_control%20boards.pdf*

> RTC6: "Scan System Control — **SL2-100 transfer protocol** (control of scan systems with **XY2-100** transfer protocol via an **optional converter**); **20-bit positioning resolution**; Virtual processing field (29 bit); **10 µs output period**; Synchronization of the 10 µs RTC clock to an external laser clock signal"；选项列表含 "**Control of 3-axis scan systems**"。
*(a) https://www.scanlab.de/sites/default/files/2020-08/12_RTC6%20control%20boards.pdf*

**RTC 系列对照表（含 Z 轴分辨率脚注）** *(a) https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf*：

| | RTC6 | RTC5 | RTC4 |
|---|---|---|---|
| Scan head interface | SL2-100 | SL2-100 | XY2-100 |
| Galvanic isolation | yes | yes | no |
| **Number / Channels** | **2 / 2** | **2 / 2** | **2 / 3** |
| **Positioning resolution** | **20 bit** | **20 bit** | **16 bit** ¹⁾ |
| Connector | 9-pin D-SUB | 9-pin D-SUB | 25-pin D-SUB |
| Correction file format 2D/3D | ct5 | ct5 | ctb |
| Value range virtual image field | 29 bit | 24 bit | – |
| 选项：Control of 3-axis scan systems | • | • | • |

> **脚注 1)：`16 bit at z-axis control`** —— 即 RTC4 用 XY2-100 做 3 轴时，**Z 轴只有 16 bit**。
*(a) 同上*

### 4.2 SCANLAB Z 轴硬件

| 产品 | 关键数值 | Z 轴通信接口 | 来源 |
|---|---|---|---|
| **varioSCAN II**（变焦/聚焦单元）| 行程 ±2 mm（20i）/ ±3 mm（40i）；典型移动速度 ≤280 / ≤140 mm/s；长期漂移 <3 µm；重复性 **<0.5 µm**；跟踪误差 0.55 / 0.70 ms；重量 0.5–0.7 / ~2.4 / ~4.4 kg | **Interfaces: SL2-100, XY2-100 Enhanced** | (a) https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf |
| **excelliSHIFT**（高速动态 z 轴）| 孔径 14 mm；波长 515–532 nm / 1030–1070 nm；跟踪误差 **0.1 ms**；光束引导为纯反射式（无透射元件）；尺寸 115×160×142 mm³；重量 3.7 kg；激光功率 120 W(green)/200 W(IR)；**聚焦范围 ±14 mm**；**像场内聚焦速度 up to 30 m/s**（配 f=160 mm F-theta） | 图中标注 "**connections for SL2-100 and POWER IN**" | (a) https://www.scanlab.de/sites/default/files/2020-07/11_excelliSHIFT_high-speed%20z%20axis.pdf 、 https://www.scanlab.de/en/products/z-axes-3d-add-ons/excellishift |
| **excelliSCAN 20** | 定位分辨率 20 bit*；"20 bit: based on the full angle range (e.g. positioning resolution 0.7 µrad for angle range ±0.36 rad), **resolutions better than 16 bit (11 µrad) only together with SL2-100 interface**" | Control interface: digital **SL2-100** | (a) https://www.scanlab.de/en/products/scan-systems/excelliscan/excelliscan-20 |
| **intelliSCAN III 20** | "resolutions better than 16 bit (11 µrad) only together with SL2-100 interface" | Control interface (alternatives): digital **SL2-100**, digital **XY2-100 Enhanced** | (a) https://www.scanlab.de/en/products/scan-systems/intelliscan/iii-series/intelliscan-iii-20 |
| intelliSCAN III 10 | 同上 | digital SL2-100, digital XY2-100 Enhanced；Advanced diagnosis: yes (iDRIVE) | (a) https://www.scanlab.de/en/products/scan-systems/intelliscan/iii-series/intelliscan-iii-10 |
| SCANcube 10 | — | digital SL2-100, digital XY2-100 standard, analog ±4.8 V | (a) https://www.scanlab.de/en/products/scan-systems/scancube/standard-series/scancube-10 |

**SCANLAB intelliSCAN 官方引脚定义** *(a) https://www.scanlab.de/sites/default/files/2020-09/pin-out-intelliSCAN.pdf*：

- **SL2-100 接口（数据与电源分开连接器）**：9-pin 母 D-SUB：`DATA IN+ (1)`、`DO NOT CONNECT (2)(3)`、`+3.3 V (DO NOT CONNECT)* (4)`、`DATA OUT+ (5)`、`DATA IN− (6)`、`GND (7)(8)`、`DATA OUT− (9)`。脚注：3.3 V 仅供 SCANLAB 的光纤（POF）转换器使用。
  → 即 **SL2-100 = 2 对差分（DATA IN ±、DATA OUT ±），双向**。
- **XY2-100-Enhanced 接口（数据与电源共用一个连接器）**：25-pin 母 D-SUB：`CLOCK− (1)`、`SYNC− (2)`、`CHAN1− (3)`、`CHAN2− (4)`、`NC (5)`、`STATUS2− (6)`、`NC (7)`、`STATUS1− (8)`、`+30 V (9)(10)`、`NC (11)`、`GND (12)(13)`、`CLOCK+ (14)`、`SYNC+ (15)`、`CHAN1+ (16)`、`CHAN2+ (17)`、`NC (18)`、`STATUS2+ (19)`、`NC (20)`、`STATUS1+ (21)`、`+30 V (22)`、`NC (23)(24)`、`GND (25)`。
  → **注意**：SCANLAB 的两轴定义只占用了 CHAN1/CHAN2 与 STATUS1/STATUS2，**第 5/18 与第 7/20 脚（即 RAYLASE 的 Z / Z_stat 位置）标注为 "DO NOT CONNECT"**。三轴时 Z 应由第 5/18 脚承担（与 RAYLASE 一致），但 SCANLAB 未公开发布 3 轴版 XY2-100-Enhanced 的引脚表 → **未找到公开数据**。

### 4.3 SL2-100 的电气/时序细节

- SL2-100 = SCANLAB 自研、**专有且封闭**（HALaser 对照表：`Protocol: proprietary and closed`；`License fees: unknown / not licensed to 3rd parties`；`Backwards Compatibility: incompatible in both, hardware and data format`）。
*(a) https://halaser.systems/compare.php*
- 线数：SL2-100 **2D 用 2 根线，3D 用 4 根线**（即 1 对 / 2 对差分）。
*(a) 同上，"Number of wires" 行*
- **SL2-100 的时钟频率、帧结构、编码方式（是否 Manchester/加密 sync）：未找到公开数据。** SCANLAB 未公开发布该协议的电平时序规范。论坛（Photonlexicon）亦仅有猜测："No clue other then the fact that it will have encrypted sync sequence or be something like Manchester Encoded, thus self clocking. Protocol Data will have to come from Scanlab."
*(b) https://www.photonlexicon.com/forums/showthread.php/28608-SL2-100-Protocol-for-scanner*

### 4.4 另有一家厂商的 3 轴专有协议：RAYLASE RL3-100

> "**RL3-100** protocol with **20 bit** position resolution and **up to 6 axes per connector**. SL2-100 protocol with 20 bit position resolution and up to 2 axes per connector. XY2-100 protocol with 16 bit position resolution (via optional adapter)."
*(a) RAYLASE SP-ICE 3 User's Manual 第 2.4 节 —
https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/48a53e4f-2a14-4518-ad32-d622848ab64a.htm*

> "RL3-100 supports 20-bit scanner commands and **up to 6 axes per connector**. A scanner with up to 6 axes can be run on a single data connection. Even the most sophisticated scanner with 3D, Zoom, and a second Z axis can be operated with a single cable."
*(a) 同上 第 7.1.1 节 —
https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/45289f65-2556-4dff-8d27-7f5918253301.htm*

> "For a scanner with 3 or 4 axes, **two SL2-100 connections (and consequently two cables) are required**."
*(a) 同上*

---

## 5. 支持三轴的控制器 / 扫描头清单（含精确型号与规格）

| 厂商 | 型号 | 轴数 / 3 轴能力 | 接口与协议 | 关键数值 | 来源 |
|---|---|---|---|---|---|
| **HALaser Systems** | **E1803D** | **Full 2-axis and 3-axis galvo control**；3-axis XY2-100/XY3-100 via D-SUB25 and 26 pin | XY2-100, XY2-200, XY2-100E, XY2-200E, **XY3-100 (LIA202002 standard)**；可选扩展板支持 SL2-100 / NX-02 / SDP | 26 bit 内部分辨率；10 µs 矢量周期；命令执行低至 0.5 µs；1 GHz CPU；512 MB DDR3；100 Mbit 以太网 + USB 2.0 | (a) https://halaser.eu/e1803.php 、 https://halaser.systems/e1803.php 、 https://halaser.systems/manuals/e1803_manual.pdf |
| HALaser Systems | E1701D | **3D XY2/100 and 2D XY3/100** | 16 bit XY2-100 with **X, Y and Z channel**；18 bit XY2-100-E with X and Y；**20 bit XY3-100 (certified LIA202002 standard)** with X and Y | — | (a) https://halaser.systems/e1701.php |
| HALaser Systems | E1702S | 2D XY2-100 / 2D XY3-100；带 XY3-100 Backchannel | 16(18) bit XY2-100(-E)、20 bit XY3-100、20 bit NX-02 | — | (a) https://halaser.systems/e1702s.php |
| HALaser Systems | **HALscan 20 / 16 / 10**（扫描头） | 振镜 | **XY3-100**, 20 bit resolution | 孔径 10/16/20 mm；±15 V 供电；数据传输错误时位置外推避免随机烧点 | (a) https://halaser.systems/halscan20x20.php 、 https://halaser.eu/halscan16x20.php 、 https://halaser.systems/halscan.php |
| HALaser Systems | **HALdrive X20** | XY3-100 → 模拟转换器 | XY3-100 输入 | ±2.5 V..±10 V 模拟输出，**20 bit 分辨率**；62×45 mm；±12..±24 V 供电 | (a) https://scanhead.de/haldrive.php |
| **Aerotech** | **Automation1 GI4** | **2 axes 或 3 axes, XY2-100 or XY3-100** | XY2-100 / XY3-100；**25-Pin Axis Connector, Channel 1, 2 and 3 scan head interfaces** | **Position Command Update Rate: 100 kHz**；2× HyperWire SFP；24 VDC；PSO 选项含 Two-axis/Three-axis Part-Speed PSO；2× 40 Mcps 编码器输入；驱动阵列内存 67.1 MB | (a) https://www.aerotech.com/product/automation1-gi4-laser-scan-head-controller/ 、 https://www.aerotech.com/wp-content/uploads/2021/11/Automation1-GI4-Data-Sheet-D20220401.pdf |
| Aerotech | GI4 + Automation1-iSMC | "the iSMC's default G-code support couples nicely with the GI4's standard **3-axis XY2-100** or new higher-resolution **XY3-100** support" | — | 支持 IFOV（Infinite Field of View）与伺服轴位置反馈合成 | (a) https://www.aerotech.com/product/automation1-gi4-laser-scan-head-controller/ |
| **RAYLASE** | **SP-ICE-3** | **Controls 2-, 3-, 4- and 5-axis deflection units**；或 2×3-axis | **RL3-100** 20 bit，**up to 6 axes per connector**；**SL2-100** 20 bit，up to 2 axes per connector；**XY2-100** 16 bit，up to 3 axes (XYZ)，需选配适配板 | 10 µs step period；20 bit 位置分辨率 ↔ 镜面定位分辨率 **0.75 µrad**；PCIe-x1 Gen2.1 或 1-Gbit 以太网独立运行；1 GB DDR3 + 32 GB microSD；跟踪误差逐轴独立补偿 | (a) https://www.raylase.de/_Resources/Persistent/b/a/6/6/ba66d25112e3d91511322aa417caae73c916557b/Datasheet_SP-ICE-3.pdf 、 https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/48a53e4f-2a14-4518-ad32-d622848ab64a.htm |
| **SCANLAB** | RTC6 / RTC5 | 选项 "**Control of 3-axis scan systems**" | SL2-100（20 bit）；XY2-100 需选配转换器 | 10 µs 输出周期；20 bit 定位分辨率；虚拟加工场 29 bit（RTC6）/ 24 bit（RTC5）；最多 8 个 3D 校正文件 | (a) https://www.scanlab.de/sites/default/files/2020-08/12_RTC6%20control%20boards.pdf 、 https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf |
| SCANLAB | RTC4 | 选项 "Control of 3-axis scan systems" | XY2-100；Channels **2/3** | 16 bit 定位分辨率（**z 轴控制为 16 bit**）；25-pin D-SUB | (a) https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf |
| SCANLAB | varioSCAN II / excelliSHIFT | Z 轴模块（3D 附加件） | SL2-100 / XY2-100 Enhanced；excelliSHIFT 用 SL2-100 | 见第 4.2 节 | (a) 见第 4.2 节 URL |
| **PMDi** | Polaris **XY2-100 Galvoscanner Module** | 每个 DB25 支持 **XY scanner motors + Z focus motor** | XY2-100、XY2-100-E | Mercury 网络设备；1 或 2 个 DB25 | (a) https://pmdi.com/posts/product/hardware/xy2-100-galvoscanner-module/ |
| PMDi | Polaris **SL2-100 Galvoscanner Module** | 每排支持 **2 个扫描电机 + 1 个聚焦电机** | SL2-100（+ XY2-100）| 两组振镜连接器 | (a) https://pmdi.com/posts/product/hardware/sl2-100-galvoscanner-module/ |
| **ACS Motion Control** | SPiiPlus 平台 + **SLEC** 同步节点 | 振镜 + 运动平台同步（XL SCAN） | 与 SCANLAB 联合开发；"For scanner and deflection units" 由 SLEC 承担 | "ACS ... and **SCANLAB GmbH jointly developed XL SCAN**: a solution that fully synchronizes the control of galvo scanner(s) and motion stages"；支持多扫描头 | (a) https://acsmotioncontrol.com/capabilities/motion-to-process-synchronization/xl-scan/ |
| **Novanta / Cambridge Technology** | **LIGHTNING II 3-Axis Digital Scan Head** | 3 轴（XY + 集成 DFM 动态聚焦模块） | XY2-100 系列（官方接线须知明确 3 轴时 Z 轴 galvo 单独接线） | **Command Resolution: 24-bit**；孔径 20/30/50 mm；跟踪延迟 0.2–0.4 ms；重复性 <2 µrad；长期漂移 <10 µrad；热漂移 <2 µrad/℃ | (a) https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf |
| **星移控制科技 Xymotion** | **XY80xx 系列数字伺服驱动器** | X/Y/Z 三轴（可选 U/W） | **XY3-100**（可配置为协议兼容或可选模式）；IDC-16 接口 | 位置实时回传（XR/YR/ZR 差分输出），可支持控制器 PSO；自学习幅面/中心点校准误差可降至 **0.1% F.S.** 或更低 | (b) https://www.xymotion.cn/index.php?m=home&c=View&a=index&aid=51 、 https://www.xymotion.cn/index.php?m=home&c=View&a=index&aid=53 |
| 星移 Xymotion | SCAN-XY 系列扫描振镜 | 两轴（文档标题为"两轴封闭式数字扫描振镜"） | 全数字伺服（数字闭环）平台 | 孔径 10/14/20/30 mm；重量 1.2/3.5 kg 等 | (b) https://www.xymotion.cn/index.php?m=home&c=View&a=index&aid=45 |

---

## 6. 三轴实现方式对比（工程要点）

| 方案 | 第三轴承载方式 | 线数（3D） | 位宽 | 备注 |
|---|---|---|---|---|
| 传统 XY2-100（16 bit）| 5 对差分：CLK±, SYNC±, X±, Y±, **Z±** | 10 | 16 bit/轴 | DB25 上 Z−=5, Z+=18；可用脚位 6/19 或 7/20 回传状态 |
| XY2-100-E（18 bit，RAYLASE SS-III）| 同上，**且每轴有独立回传**：X_stat(8/21), Y_stat(6/19), **Z_stat(7/20)** | 10（+回传） | 18 bit/轴 | 时钟最高 10 MHz（推荐 4 MHz）；下发在 CLK 上升沿变化，回传在下降沿变化 |
| SCANLAB RTC4 + XY2-100 | Z 轴存在，但 **仅 16 bit** | — | Z: 16 bit | RTC 对照表脚注 "16 bit at z-axis control" |
| SCANLAB SL2-100 | 第 3/4 轴需**第二根 SL2-100 电缆**（每连接器最多 2 轴） | 4 | 20 bit/轴 | 2D 只需 2 根线；3/4 轴必须两连接器 |
| RAYLASE RL3-100 | 同一连接器最多 **6 轴** | 未找到公开数据 | 20 bit/轴 | "Even the most sophisticated scanner with 3D, Zoom, and a second Z axis can be operated with a single cable." |
| **XY3-100** | 同一连接器最多 **5 轴**（X/Y/Z + U/W 附加轴），Z 为 E± 对 | 10（2D 也是 8，3D 10）| **16..26 bit/轴（自适应）** | DB15 版本最多 3 轴；回传换为异步 RS485（115200 bps 默认）|

### ⚠️ 接线陷阱（重要，务必实测确认）

1. **XY3-100 与常规 XY2-100 的 CLK/SYNC 脚位是互换的。**
   - XY3-100 规范：DB25 `1/14 = SYNC`，`2/15 = CLK`。
   *(a) https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf 第 4.1 节*
   - 而 RAYLASE（CLK 1/14, SYNC 2/15）、Newson（SENDCK 1/14, SYNC 2/15）、SCANLAB（CLOCK 1/14, SYNC 2/15）三家一手文档都是 **CLK 在 1/14、SYNC 在 2/15**。
   *(a) http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf ； https://www.newson.be/doc.php?id=XY2-100 ； https://www.scanlab.de/sites/default/files/2020-09/pin-out-intelliSCAN.pdf*
   - 同一块卡上两种模式的差异可被证实：HALaser E1803D 在 **XY2-100 模式**下 26-pin 为 `1/2 = CLK`、`3/4 = SYNC`；切到 **XY3-100 模式**后变成 `1/2 = A = SYNC`、`3/4 = B = CLK`。
   *(a) https://halaser.systems/manuals/e1803_manual.pdf 第 7.6 节 与 XY3-100 模式引脚表*
   → 尽管 XY3-100 规范自称 "Same pinout as XY2-100(E), no hardware changes needed"，**CLK/SYNC 这一对在实际实现中是反的**，切换协议时必须核对（数据线 X/Y/Z 3/16、4/17、5/18 则确实一致）。
2. **X/Y 通道可能互换**：RAYLASE 明确其 X 轴是激光先打到的（较小）镜，与其他厂商定义相反。
   *(a) http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf 第 2.1.2 节*
3. **Xymotion 的 XY3-100 实现与 LasIA 规范 IDC 顺序不同**（CLK 在 1/2、SYNC 在 3/4，且用 3 对独立回传线）。
   *(b) https://www.xymotion.cn/index.php?m=home&c=View&a=index&aid=51*
4. **驱动芯片**：RAYLASE 推荐 UA9638CD（线驱动）/ MAX3096、UA9637、AM26LV32（线接收）。XY2-100 需 5 个驱动器（CLK、SYNC、X、Y、Z），每个 UA9638CD 含 2 路，故需 3 片；建议 ≥15 MBaud、非压摆率限制、带短路保护、±8~15 kV ESD，且**多片必须用同一型号**以免通道间偏斜。
   *(a) http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf 第 2.2 节*
   *(b) https://techoverflow.net/2021/11/01/which-line-driver-should-one-use-for-xy2-100-and-xy3-100/*

---

## 7. 未找到公开数据的项目（明确列出，不做臆测）

- **SL2-100 的电气/时序规范**：时钟频率、帧长（bit 数）、同步方式、编码方式、校验/CRC 机制 —— SCANLAB 未公开发布。**未找到公开数据**。
  - 已知的只有：20 bit 位置分辨率、2 对差分线（2D）/4 根线（3D）、10 µs 输出周期（来自 RTC 板）、iDRIVE 支持实时读回。来源见第 4.1/4.2 节。
- **"SL2-100-3D" 命名**：SCANLAB 官方未使用该名称，**未找到公开数据**。SCANLAB 的 3D = 2D 扫描头 + Z 轴模块（varioSCAN II / excelliSHIFT）+ 支持 3 轴的 RTC 卡。
- **SCANLAB 三轴版 XY2-100-Enhanced 的完整引脚表**：intelliSCAN 官方 pin-out 中第 5/18、7/20 脚标为 DO NOT CONNECT（2 轴配置），三轴配置的官方引脚表 **未找到公开数据**。
- **Aerotech GI4 在 XY3-100 模式下的具体位宽**：官方数据手册只写 "higher resolution XY3-100"、"2 axes / 3 axes, XY2-100 or XY3-100"、"Position Command Update Rate 100 kHz"，**未给出 XY3-100 下的 bit 数**（XY3-100 规范本身为 16..26 bit 可变）。**未找到公开数据**。
- **XY3-100 官方规范的公开直链**：lasia.org 现返回 401，只能通过 Wayback Machine 存档获取。已存档的时间戳见第 2.1 节表格。SourceForge 项目页 https://sourceforge.net/p/lasia/blog/2023/07/xy3-100-digital-scanner-interface-version-11/ 对所有脚本化访问返回 **HTTP 403**，Scribd 上的副本 https://www.scribd.com/document/951428348/xy3-100-specification-1 亦不可脚本抓取。

---

## 8. 完整原始 URL 清单

### 8.1 LasIA 官方标准（一手，经 Wayback Machine 存档）
1. https://web.archive.org/web/20231206143105id_/https://lasia.org/LIA202307/xy3_100_specification_v11.pdf — **XY3-100 规范 v1.1（LIA202307）全文**
2. https://web.archive.org/web/20210122224854id_/https://lasia.org/LIA202002/xy3_100_specification.pdf — **XY3-100 规范 v1.0（LIA202002）全文**
3. https://web.archive.org/web/20231206141529id_/https://lasia.org/LIA202001/xy2_100_specification.pdf — **XY2-100 规范（LIA202001）全文**
4. https://web.archive.org/web/20231206133135id_/https://lasia.org/LIA202307/xy3_100.h — **XY3-100 配套头文件 v1.1**
5. https://web.archive.org/web/20210122221252id_/https://lasia.org/LIA202002/xy3_100.h — XY3-100 头文件 v1.0
6. https://web.archive.org/web/20221208093833id_/http://lasia.org/LIA2022xx/xy3_100_specification_v11.pdf — XY3-100 v1.1（2022 存档）
7. https://web.archive.org/web/20231206131409id_/https://lasia.org/LIA202101/laser_interface_specification.pdf — Laser Interface Specification（LIA202101）
8. https://web.archive.org/web/20211022064721id_/http://lasia.org/LIA2021xx/analog_scanhead_specification.pdf — Analog Scanhead Specification（LIA202102）
9. http://web.archive.org/cdx/search/cdx?url=lasia.org*&output=text&limit=200&collapse=urlkey — lasia.org 全部存档索引
10. https://sourceforge.net/p/lasia/blog/2023/07/xy3-100-digital-scanner-interface-version-11/ — LasIA 官方发布公告（脚本访问返回 403）
11. http://www.lasia.org/LIA202307/xy3_100_specification_v11.pdf — 原始直链（现返回 HTTP 401）
12. https://www.scribd.com/document/951428348/xy3-100-specification-1 — XY3-100 规范副本（不可脚本抓取）

### 8.2 HALaser Systems（XY3-100 控制器与扫描头，一手）
13. https://halaser.eu/e1803.php — E1803D 产品页（含 "XY3-100 (LIA202002 standard)" 与 "Full 2-axis and 3-axis galvo control"）
14. https://halaser.systems/e1803.php — 同页镜像
15. https://halaser.systems/manuals/e1803_manual.pdf — **E1803D 手册（XY2-100 / XY3-100 模式引脚表、Appendix B/C、26 bit 分辨率、10 µs 周期）**
16. https://halaser.systems/compare.php — **协议对照大表（轴数、线数、精度、回传、许可）**
17. https://halaser.eu/compare.php — 同页镜像
18. https://halaser.systems/e1701.php — E1701D（3D XY2-100 / 2D XY3-100，"certified LIA202002 standard"）
19. https://halaser.systems/e1702s.php — E1702S
20. https://halaser.eu/e1701.php — E1701D 镜像
21. https://halaser.systems/halscan20x20.php — HALscan 20（XY3-100，20 bit）
22. https://halaser.eu/halscan16x20.php — HALscan 16
23. https://halaser.systems/halscan.php — HALscan 10
24. https://scanhead.de/haldrive.php — HALdrive X20（XY3-100 → 模拟，20 bit）
25. https://halaser.systems/manuals/haldrive_manual.pdf — HALdrive 手册
26. https://halaser.systems/manuals/halscan_manual.pdf — HALscan 手册
27. https://halaser.systems/download.php — HALaser 全部手册与固件下载页
28. https://www.halaser.de/manuals/e1803_manual.pdf — E1803D 手册镜像（含 "XY2-100 and XY2-100-E interface to scanhead with X, Y and optional Z channel"）
29. https://innotech-laser.de/en/laser-products/control-cards/halaser-systems/ — HALaser 控制卡经销商页（LIA202002 表述）

### 8.3 RAYLASE（XY2-100-E 三轴、SP-ICE-3、RL3-100，一手）
30. http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf — **《Documentation of the SS-III XY2-100-E Interface》（三轴 DB25 引脚、Z_stat、10 MHz/4 MHz 时钟、UA9638CD）**
31. https://www.raylase.de/_Resources/Persistent/b/a/6/6/ba66d25112e3d91511322aa417caae73c916557b/Datasheet_SP-ICE-3.pdf — **SP-ICE-3 数据手册（RL3-100 / SL2-100 / XY2-100，2..5 轴，10 µs，0.75 µrad）**
32. https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/48a53e4f-2a14-4518-ad32-d622848ab64a.htm — **SP-ICE-3 手册 2.4 Interfaces**
33. https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/45289f65-2556-4dff-8d27-7f5918253301.htm — **SP-ICE-3 手册 7.1.1 Scan Head Format Definitions（RL3_Single4DXA 等）**
34. https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/CE15CBDB-355A-4F69-A5B0-97611F5D1550.htm — SP-ICE-3 手册 7.1.7 Three Axis Scanners
35. https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/65db6d89-b141-46a3-a74c-0b0ec7df2df1.htm — SP-ICE-3 手册 4.1 XY2-100 Adapters
36. https://www.raylase.de/en/products/electronics-control-cards/sp-ice-3.html — SP-ICE 3 产品页
37. https://www.raylase.de/en/products/prefocusing-deflection-units.html — RAYLASE 3 轴偏转单元（AXIALSCAN / FOCUSSHIFTER / AXIALSCAN FIBER）
38. https://www.manualslib.com/manual/1658721/Raylase-Axialscan.html — RAYLASE AXIALSCAN 手册（3-Axis Subsystems）

### 8.4 SCANLAB（SL2-100、RTC、Z 轴模块，一手）
39. https://www.scanlab.de/sites/default/files/2020-08/12_RTC6%20control%20boards.pdf — **RTC6 数据表（SL2-100、20 bit、10 µs、"Control of 3-axis scan systems"）**
40. https://www.scanlab.de/sites/default/files/2020-08/13_RTC5_control%20boards.pdf — RTC5 数据表（SL2-100、20 bit、比 RTC4 高 16 倍）
41. https://www.scanlab.de/sites/default/files/2022-04/13_RTC_Combination.pdf — **RTC4/5/6 对照表（2/3 channels、"16 bit at z-axis control" 脚注）**
42. https://www.scanlab.de/sites/default/files/2020-09/pin-out-intelliSCAN.pdf — **intelliSCAN 官方引脚表（SL2-100 与 XY2-100-Enhanced DB25）**
43. https://www.scanlab.de/sites/default/files/2020-07/11_excelliSHIFT_high-speed%20z%20axis.pdf — **excelliSHIFT 数据表（±14 mm 聚焦范围、30 m/s、0.1 ms、SL2-100）**
44. https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf — **varioSCAN II 数据表（Interfaces: SL2-100, XY2-100 Enhanced；±2/±3 mm；<0.5 µm 重复性）**
45. https://www.scanlab.de/en/products/z-axes-3d-add-ons/excellishift — excelliSHIFT 产品页
46. https://www.scanlab.de/en/products/z-axes-3d-add-ons/varioscan-ii — varioSCAN II 产品页
47. https://www.scanlab.de/en/products/z-axes-3d-add-ons — z Axes & 3D Add-Ons 总览
48. https://www.scanlab.de/en/products/scan-systems/excelliscan/excelliscan-20 — excelliSCAN 20（20 bit，SL2-100）
49. https://www.scanlab.de/en/products/scan-systems/intelliscan/iii-series/intelliscan-iii-20 — intelliSCAN III 20（SL2-100 / XY2-100 Enhanced）
50. https://www.scanlab.de/en/products/scan-systems/intelliscan/iii-series/intelliscan-iii-10 — intelliSCAN III 10
51. https://www.scanlab.de/en/products/scan-systems/scancube/standard-series/scancube-10 — SCANcube 10 接口
52. https://www.scanlab.de/en/applications/micromachining — "20-bit SL2-100 protocol, developed and introduced by SCANLAB"
53. https://www.scanlab.de/en/news-events/press-releases/entry-level-scan-head-gains-even-more-flexibility — basiCube SL2-100 变体
54. https://pdf.directindustry.com/pdf/scanlab-gmbh/intelliscan-iii-scan-heads/39164-400641.html — intelliSCAN III 目录（第三方聚合）
55. https://www.photonlexicon.com/forums/showthread.php/28608-SL2-100-Protocol-for-scanner — 论坛讨论（SL2-100 细节未知，二手）

### 8.5 Aerotech（XY3-100 控制器，一手）
56. https://www.aerotech.com/product/automation1-gi4-laser-scan-head-controller/ — **GI4 产品页（2/3 轴，XY2-100 或 XY3-100）**
57. https://www.aerotech.com/wp-content/uploads/2021/11/Automation1-GI4-Data-Sheet-D20220401.pdf — **GI4 数据手册（100 kHz 位置命令更新率、25-Pin 3 通道、PSO）**
58. https://help.aerotech.com/automation1/hardware-manuals/Automation1-GI4-web/Default.htm — GI4 在线硬件手册入口
59. https://www.chnscs.com/manual/GI4.html — GI4 页面中文镜像
60. https://www.alldatasheet.com/datasheet-pdf/pdf/2237297/AEROTECH/AUTOMATION1-GI4.html — GI4 数据手册聚合页

### 8.6 其它厂商与控制器
61. https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf — **Novanta / Cambridge Technology LIGHTNING II 3-Axis（24-bit command resolution）**
62. https://www.manualslib.com/manual/2643580/Novanta-Lightning-Ii-Xy2-100.html — Novanta LIGHTNING II XY2-100 接线须知（3 轴 Z 轴接法）
63. https://pdf.directindustry.com/pdf/cambridge-technology/3-axis-scan-head/36210-742426.html — Cambridge Technology 3-Axis Scan Head 目录
64. https://pmdi.com/posts/product/hardware/xy2-100-galvoscanner-module/ — **PMDi Polaris XY2-100 模块（每个 DB25 支持 XY + Z focus）**
65. https://pmdi.com/posts/product/hardware/sl2-100-galvoscanner-module/ — PMDi Polaris SL2-100 模块（每排 2 电机 + 1 聚焦电机）
66. https://acsmotioncontrol.com/capabilities/motion-to-process-synchronization/xl-scan/ — **ACS XL SCAN（与 SCANLAB 联合开发，SLEC 同步节点）**
67. https://acsmotioncontrol.com/markets/laser-processing-systems/ — ACS 激光加工页
68. https://acsmotioncontrol.com/products/slec/ — ACS SLEC 同步节点
69. https://www.newson.be/doc.php?id=XY2-100 — **Newson XY2-100 技术数据表（2 MHz、2 Mbit/s、100 kwords/s、20-bit 帧、SYNC 19 bit）**
70. https://www.aaronvose.net/Quantronix_Osprey/xy2_100_specification.pdf — XY2-100 规范（与 LasIA LIA202001 同一文件，字节数一致）
71. https://github.com/georgemihaila/xy2-100/blob/main/docs/xy2_100_specification.pdf — XY2-100 规范 GitHub 镜像
72. https://www.scribd.com/document/941573319/Xy2-100-Specification — XY2-100 规范 Scribd 副本

### 8.7 中文来源与二手资料
73. https://www.xymotion.cn/index.php?m=home&c=View&a=index&aid=52 — **星移控制科技《XY3-100协议简介》（16-26 bit、2.4/3.2 MHz、P1P0/P3P2P1P0、注明内容来自 LasIA）**
74. https://www.xymotion.cn/index.php?m=home&c=View&a=index&aid=51 — **星移《如何通过XY3-100协议获取电机实时坐标数据》（IDC 引脚表、示波器实测 32 bit 帧 0xE0000000 / 0x9FFFE101）**
75. https://www.xymotion.cn/index.php?m=home&c=View&a=index&aid=53 — 星移《振镜电机的幅面和中心点》（校准误差 0.1% F.S.）
76. https://www.xymotion.cn/index.php?m=home&c=View&a=index&aid=45 — 星移 SCAN-XY 系列扫描振镜
77. https://www.xymotion.cn/index.php?m=home&c=View&a=index&aid=19 — 星移 XY80xx 系列数字伺服驱动器
78. https://sigrok.org/wiki/Protocol_decoder:Xy2-100 — **sigrok XY2-100 解码器文档（有时存在 Z 轴、XY2-200 4 MHz、16/18 bit、三种 status 变体）**
79. https://techoverflow.net/2021/11/01/which-line-driver-should-one-use-for-xy2-100-and-xy3-100/ — 线驱动选型（5 个驱动器/CLK+SYNC+X+Y+Z，3 片 UA9638CD）
80. https://techoverflow.net/2021/11/01/what-is-the-typical-maximum-clock-frequency-for-xy2-100/ — XY2-100 典型/最高时钟频率讨论
81. https://dvd.ilphotonics.com/Ray-Motion%20-%20galvanometers%20-%201D-2D-3D%20scanners/Motion%20Control%20-%20Optomechanics/Interface%20XY2-100.pdf — XY2-100 接口协议（IL Photonics 镜像，含 "20-bit works, 2 Mbit/s, 100 kwords/s"；脚本访问 403）
82. https://surplusrecord.com/listing/synrad-octiv-co2-laser-900-watt-smc-controller-xyz-100-galvo-command-interface-2023-473129/ — Synrad "XYZ-100 Galvo Command interface" 商品描述
83. https://www.machinio.com/synrad/laser-cutters/co2-lasers/united-states — Synrad SMC / XYZ-100 / 3 Axis 扫描头信息
84. https://revelationmachinery.com/product/900w-synrad-octiv-co2-laser-2023-barely-used/ — Synrad OCTIV 设备清单
85. https://manuals.plus/halscan/xy3-100-scanheads-manual.pdf — HALscan XY3-100 扫描头手册（第三方站，403）
86. https://www.manualslib.com/products/Halaser-Systems-Halscan-Xy3-100-13163865.html — HALscan XY3-100 手册索引
87. https://device.report/halaser-systems/XY3-100 — HALaser XY3-100 文档索引

---

## 9. 一句话总结

- **XY3-100 = LasIA（Laser Industry Association）定义的开放标准，编号 LIA202002（v1.0）/ LIA202307（v1.1）**，不是"20 bit XY2-100"，而是**位宽 16..26 bit 自适应**、**24 bit 帧 @2.4 MHz / 32 bit 帧 @3.2 MHz（均 10 µs = 100 kHz）**、**引脚兼容 XY2-100 可固件升级**、**回传改为异步 RS485（默认 115200 bps）**、**最多 5 轴（X/Y/Z + U/W）**；DB15 版本最多 3 轴。
- **XY2-100 本身就支持 3 轴**，第三轴只是多一对 Z± 差分线（DB25: Z−=5、Z+=18）；XY2-100-E 里第三轴还带独立回传 Z_stat（7/20）。**不存在独立的 "XY2-100-3D" 或 "XYZ-100" 标准**。
- **SCANLAB 没有 "SL2-100-3D"**：其 3D 由 2D 扫描头 + 独立 Z 轴模块（varioSCAN II / excelliSHIFT，走 SL2-100 或 XY2-100 Enhanced）+ 带 3 轴选项的 RTC 卡组成；SL2-100 是 20 bit、2 线/4 线、专有封闭协议，**其电平时序未公开**。
- **切换 XY2-100 ↔ XY3-100 时必须核对 CLK/SYNC 脚位**：两者在 DB25 上是反的（XY3-100: 1/14=SYNC, 2/15=CLK；业界 XY2-100: 1/14=CLK, 2/15=SYNC）。
