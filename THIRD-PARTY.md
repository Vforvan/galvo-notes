# 第三方内容与来源说明

本仓库收录**原创学习笔记与自写代码**。体积大或涉及第三方版权的资料**不入库**，
但每一份都在这里标明来源、许可证与获取方式——本库笔记里的参数都可以按这些线索回到原文查证。

> 为什么不在仓库里附图 PDF：手册与标准原文是厂商和标准组织的版权文档，
> 公开再分发有风险；抓取缓存里还有大量重复副本（单个文件最多存了 4 份），
> 让 clone 变慢却没有额外信息。

---

## 一、已入库的第三方代码（1 个）

| 目录 | 来源 | 许可证 | 说明 |
|---|---|---|---|
| `99-附件与下载/代码/XY2Galvo-rp2040/` | <https://github.com/earlynerd/XY2Galvo> | **BSD-3-Clause** | RP2040 PIO 实现，笔记 [[02-硬件实现篇/06-开源参考实现导读]] 逐段讲解 |

BSD-3-Clause 允许再分发，**前提是保留版权声明与许可证全文**。
原件 `LICENSE` 已随目录一并保留（Copyright (c) 2025, earlynerd），请勿删除。
本仓库已移除其 `.git/`，因此它不再是一个嵌套仓库，只是一份源码快照——
需要跟进上游更新请直接访问上面的链接。

---

## 二、未入库：因许可证不兼容（2 个）

以下两个仓库是 **GPL 系 copyleft** 许可证。把它们并入本仓库会让整个仓库受 GPL 约束，
与本仓库对笔记采用的 CC BY 4.0 冲突，因此**只保留链接与讲解，不收录源码**。

| 仓库 | 许可证 | 链接 |
|---|---|---|
| OPAL（G 代码 → XY2-100 集成） | **GPL-2.0** | <https://github.com/opengalvo/OPAL> |
| georgemihaila/xy2-100（Arduino 库） | **GPL-3.0** | <https://github.com/georgemihaila/xy2-100> |

> 顺带一提：`georgemihaila/xy2-100` 与 OPAL 在**校验位覆盖范围**上都少算了一位
> （只算 16 位数据位、漏掉控制字，导致校验值相反）。
> 详见 [[01-协议篇/02-帧结构详解]]——抄代码前先看这一节。

另一个参考实现是 **sigrok** 的 XY2-100 协议解码器（`sigrok-xy2-100-decoder/`）：
它是 sigrok 项目的组成部分，沿用 sigrok 的 **GPL-3.0+**；原快照未附带许可证文件，
因此同样未入库。上游：<https://github.com/sigrokproject/libsigrok>`decoder` 分支。

---

## 三、未入库：厂商与标准文档（29 份，约 30 MB）

这些都是**版权文档**，请从官方渠道获取。下表给出用途与获取途径，
对应笔记见 [[04-资源库/01-官方文档索引]]。

### 标准原文（最重要）

| 文档 | 内容 | 获取途径 |
|---|---|---|
| **LasIA LIA202001** | **XY2-100 正式行业标准**（本库第一依据） | LasIA（Laser Industry Association）官方 |
| LasIA LIA202002 | XY3-100 标准 | 同上 |
| LasIA LIA202307 v1.1 | XY3-100 标准修订版（引脚互换的关键依据） | 同上 |

> XY2-100 有正式标准，实现符合 LIA202001 就叫"符合标准"，而不是"模仿某家厂商"。

### 接口与器件

| 类别 | 文档 |
|---|---|
| XY2-100 接口规范 | Raylase XY2-100 / XY2-100-E 数据表、Newson XY2 接口数据表 |
| 控制卡手册 | E1803D、RAYLASE SP-ICE3、SCANLAB RTC4 / RTC5 / RTC6、intelliSCAN |
| 振镜数据手册 | RAYLASE、SinoGalvo/Sintec、Cambridge Technology、SCANLAB 系列 |
| RS-422 器件 | TI AM26LS31、UA9638、AM26LV31、MAX3096 |

### 论文与书籍

SPIE / EUSPEN / Springer 论文若干，以及 *Handbook of Optical and Laser Scanning*
(2nd Edition, Marshall & Stutz) 的预览章节。清单见 [[04-资源库/04-论文书籍]]。

---

## 三·补、光学篇引用的公开来源（在线，无需下载）

光学篇（`05-光学篇/`）的结论来自厂商官网、数据手册与论文。这些**全部可公开访问**，
下表按主题索引，方便你回到原文核对。**本仓库不转载其内容，只给链接。**

### F-θ 场镜

| 来源 | 用来核对什么 |
|---|---|
| [Sill Optics 技术指南 · F-Theta Lenses](https://www.silloptics.de/en/service/sill-technical-guide/laser-optics/f-theta-lenses) | F-θ 定义、桶形畸变设计、1% 渐晕前提、光阑位置定义 |
| [Thorlabs F-Theta 教程](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=10766) | 选型三参数、场曲与 f-θ 畸变曲线 |
| [SCANLAB Scan Lenses](https://www.scanlab.de/en/products/scan-components/scan-lenses) | 焦距的 5 项耦合优化 |
| [SCANLAB 术语表 · focal diameter](https://www.scanlab.de/en/service/glossary/focal-diameter-focal-spot) | 光斑 86.5% 功率口径定义 |
| [Jenoptik JENar 数据手册](https://www.jenoptik.us/-/media/websitedocuments/optics/f-theta/data-sheets/f-theta-017700-009-26-ft-03-424ft-350-1030.pdf) | **±1.5% 制造公差**（焦距/后工作距离/法兰焦距） |
| [Jenoptik 回返光图](https://www.jenoptik.us/-/media/websitedocuments/optics/f-theta/rueckreflexgraphen/f-theta-017700-405-26-rr.pdf) | 回返光位置与工况变化风险 |
| [GIAI · 光斑尺寸 vs 光束直径](https://www.giaiphotonics.com/f-theta-lens-spot-size-vs-beam-diameter/) | **C = 1.83 系数的来历**与适用条件 |
| [亚利桑那大学光学硕士报告](https://wp.optics.arizona.edu/alumni/wp-content/uploads/sites/113/2023/06/msreport-gong-chen.pdf) | 「故意引入桶形畸变抵消 tanθ」 |
| [Edmund Optics · Sill 多光谱场镜](https://www.edmundoptics.com/f/sill-optics-multispectral-f-theta-lenses/40164/) | 多光谱场镜、**LIDT 2.5 J/cm² @1ns** |
| [Coherent 高功率 F-Theta](https://www.coherent.com/optics/laser-optics/f-theta-scan-lenses/high-power-f-theta-lenses) | >6 kW、熔石英/CaF₂/蓝宝石 |
| [DGaO 热光效应论文](https://dgao-proceedings.de/download/117/117_c15.pdf) | 场镜**热致焦移**仿真与实测 |
| [RAYLASE SPICE3 手册 · 幅面畸变校正](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/F5DDE105-3406-416E-B7D0-2C1EF865BFE1.htm) | 软件标定能做什么 |
| [SCAPS SAMLight · F-Theta Factor Calibration](https://download.scaps.com/downloads/Software/SAMLight/Manual/html/f-theta_factor_calibration.htm) | 非 z=0 高度打标的 x/y 修正 |

### 振镜反射镜

| 来源 | 用来核对什么 |
|---|---|
| [Coherent galvo mirrors](https://www.coherent.com/optics/general-optics/lenses-mirrors/galvo-mirrors) | **硅基材"热稳定性优于熔融石英"**（反直觉的一手表述） |
| [Edmund Optics · 镜片面型对焦斑的影响](https://www.edmundoptics.com/knowledge-center/application-notes/optics/effects-of-laser-mirror-surface-flatness/) | λ/10 与更好时「practically indistinguishable」 |
| [Laseroptik · HR 镀膜基础](https://www.laseroptik.com/en/coating-guide/thin-film-basics/hr-standards) | 介质膜 **AOI 增大 → 中心波长蓝移** |
| [Advanced Optics · 镀膜数据](https://advancedoptics.com/technical-optical-coating-data.html) | 银膜氧化/硫化失泽、湿度加速 |
| [SCANLAB SCANcoat 355-H](https://www.apertureos.com/wp-content/uploads/2016/08/SCANcoat-355-H-rev02-.pdf) | 低表面张力镀膜抑制**镀膜致波前变形** |
| [SCANLAB SCANcoat 1064-M](http://www.apertureos.com/wp-content/uploads/2016/08/SCANcoat-1064-M-rev03.pdf) | 介质增强金，大角度入射 |
| [Mersen optoSiC](https://www.mersen.com/en/products/boostec-silicon-carbide-sic/laser-processes-galvo-scanning-and-fast-steering-mirrors) | 碳化硅扫描镜、高刚度与动态面型 |
| [Aerotech AGV-HPO](https://www.aerotech.com/product/agv-hpo-high-accuracy-laser-scan-heads/) | **闭路水冷电机 + 强制风冷镜片** |
| [Aerotech 选型指南](https://go.aerotech.com/in-motion/how-to-choose-the-right-galvo-scanner-essential-selection-guide) | 镜片越重 → 角加速度上限越低 |
| [威斯康星大学 · 动态波前畸变](https://www.ophth.wisc.edu/blog/2021/12/20/dynamic-wavefront-distortion-in-resonant-scanners/) | 动态像差以**线性斜像散占 90%** 为主 |
| [Applied Physics B 论文](https://link.springer.com/content/pdf/10.1007/s00340-026-08693-2.pdf) | 镜片惯量参与伺服环、扫描器等效低通 |
| [Henkel LOCTITE 粘接失效模式](https://www.loctitex.com/en/manuals/bonding/7.1.1-adhesive-failure/) | 界面/内聚/基材失效三分类 |

### 扩束镜与准直

| 来源 | 用来核对什么 |
|---|---|
| [Sill Optics 技术指南（总目录）](https://www.silloptics.de/en/service/sill-technical-guide) | 符号表 `β′ = d_out/d_in`、出射直径受孔径限制 |
| [SUKH · 单模光纤准直](https://www.sukhamburg.com/support/technotes/fiberoptics/coupling/collimatingsm/diameter.html) | `Ø = 2·f′·NA`、不同电平的 F_NA 系数 |
| [SUKH · 多模光纤准直](https://www.sukhamburg.com/support/technotes/fiberoptics/coupling/mm/collimatingmm.html) | 多模准直后**固有的几何发散角** |
| [SUKH · 准直实用判据](https://www.sukhamburg.com/support/technotes/fiberoptics/coupling/mm/collimatingmm/practicalcollimation.html) | 现场判断准直是否调好的方法 |
| [Coherent 准直单元数据手册](https://www.coherent.com/resources/datasheet/components-and-accessories/collimating-units-1030-1090nm-ds.pdf) | 焦距档位、**Z 向公差 ±100 μm**、热致焦移 |

### 5 轴架构与动态聚焦

| 来源 | 用来核对什么 |
|---|---|
| [RAYLASE AM MODULE III（新闻稿）](https://www.raylase.de/en/about-raylase/press/am-module-iii-setting-new-standards-for-industrial-additive-manufacturing.html) | **in-focus zoom + RAYVOLUTION DRIVE 动态 Z 轴** |
| [RAYLASE AM MODULE III（产品页）](https://www.raylase.de/en/products/prefocusing-deflection-units/am-modul-III.html) | 集成准直光学、一体化 5 轴增材模块 |
| [SCANLAB excelliSHIFT](https://www.scanlab.de/en/products/z-axes-3d-add-ons/excellishift) | 把 2D 扫描头扩展成 3D 系统 |
| [SCANLAB 产品总览](https://www.raylase.de/en/products.html) | FOCUSSHIFTER 光学 Z 轴（2.5D 加工） |
| [Novanta LIGHTNING II 三轴](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf) | 集成 DFM 动态聚焦的三轴扫描头 |
| [PMDi Polaris 3D](https://pmdi.com/products/galvoscanners/polaris-3d-galvoscanner/) | 「5 轴」另一种含义：振镜 + 5 轴平台 IFOV |

### 损伤阈值与安全

| 来源 | 用来核对什么 |
|---|---|
| [Edmund Optics · LIDT 测试](https://www.edmundoptics.com/knowledge-center/application-notes/lasers/laser-damage-threshold-testing/) | 「LIDT 测试未标准化」 |
| [Electro Optics LIDT 白皮书](https://www.electrooptics.com/sites/default/files/content/white-paper/pdfs/LIDT%20of%20Laser%20Components_18_0.pdf) | **ISO 21254-1:2011** 的定义口径 |
| [Edmund Optics · 光束质量与 Strehl](https://www.edmundoptics.com/knowledge-center/application-notes/lasers/beam-quality-and-strehl-ratio/) | Strehl 比定义 |

> ⚠️ **取证等级说明**：光学篇调研期间，本机的网页正文抓取工具受网络策略限制，
> 部分数值来自搜索引擎返回的摘要片段，未能逐页打开原文核对。
> 这类条目在笔记中已用 ⚠️ 或 💡 标注。**上表链接可用于你自行复核。**
> 厂商**未公开**的指标（场镜平场性 µm 级数值、镜片动平衡工艺、场镜装反的后果等）
> 在笔记中一律写明"未找到公开来源"，**没有编造填充**。

---

## 四、未入库：网页抓取缓存（183 MB / 761 文件）

`99-附件与下载/_调研原始缓存/` 是本库调研阶段的中间产物：厂商与社区页面正文抓取、
标准原文的文本提取件、以及四个第三方仓库的整棵源码树副本。
其中含大量重复 PDF（同一份手册最多存 4 份），体积远大于信息量，故不入库。

**什么因此丢失了**：不联网时无法在库内全文搜索标准原文的文本提取件。
如果你需要离线检索，请自行按上一节的渠道取回原始文档后放回该目录——
`.gitignore` 已忽略此目录，不会影响仓库。

---

## 五、本仓库原创部分的许可证

- **笔记与文档**（`*.md`）：CC BY 4.0，见 [LICENSE](LICENSE)
- **自写代码**（`02-硬件实现篇/代码/`、`05-光学篇/代码/` 下的 `.v` / `.py`）：MIT

引用本库内容时请注明来源仓库；笔记中标 💡 的是工程经验解释，
**不同厂商可能不一致，以你手上那台设备的手册为准**。
