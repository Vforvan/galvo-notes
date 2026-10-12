# 资料索引

本项目的结论要么来自公开来源，要么明确标注为本项目假设。此文件记录来源出处与本地副本位置，方便逐条核对。

> [!note] 本地副本放在哪、为什么不在仓库里
> 本库（`galvo-notes`）**只收录原创内容**，厂商与标准组织的版权文档不入库。
> 下面这些资料已按库的既有约定放进 `99-附件与下载/pdf/`
> （**该目录被 `.gitignore` 忽略**；手册截图在 `99-附件与下载/pdf/precSYS_手册截图/`）。
> 来源、许可证与获取途径登记在库根目录的 `THIRD-PARTY.md`。
>
> 下表给出的是**相对本文件的本地路径**，按 `THIRD-PARTY.md` 取回后即可点开。

## 本地副本

| 资料 | 本地文件 | 说明 |
|---|---|---|
| SCANLAB precSYS 英文手册（02/2026） | [`SCANLAB-precSYS-EN.pdf`](../../../99-附件与下载/pdf/SCANLAB-precSYS-EN.pdf) | 全部结构尺寸与「五个振镜轴」表述的出处 |
| 手册第 2 页截图 | [`page-2.png`](../../../99-附件与下载/pdf/precSYS_手册截图/page-2.png) | 原理、系统构成、五个振镜轴 |
| 手册第 3 页截图 | [`page-3.png`](../../../99-附件与下载/pdf/precSYS_手册截图/page-3.png) | 自动精调、创新点（purely galvo-based 5-axis） |
| 手册第 8 页截图 | [`page-8.png`](../../../99-附件与下载/pdf/precSYS_手册截图/page-8.png) | 外形工程图：303.5 × 263.5 × 271 mm 等 |
| Cambridge Technology（Novanta）Calibration Wizard 用户手册 | [`CalWizard_Manual.pdf`](../../../99-附件与下载/pdf/CalWizard_Manual.pdf) | 2 轴与 3 轴扫描头校准；校正常用做法与「修正表」结构。**不是 5 轴手册** |
| DataRay BeamMap2 白皮书 | [`dataray-beammap2-whitepaper.pdf`](../../../99-附件与下载/pdf/dataray-beammap2-whitepaper.pdf) | 多平面光束轮廓仪：实时测焦点位置、M²、发散角与指向 |

### DataRay BeamMap2 白皮书要点（已核实）

标题 *Real-time Profiling for Focusing, M², Divergence & Alignment — Multi-plane Beam Profiling Speeds Development & Production*，8 页，2024-04-09 生成，有文字层。

做法是**转盘上多个 Z 平面同时测量**：四个 XY 狭缝对分布在不同 Z 平面，标准平面间距 S = 250 µm（另有 50 / 100 / 500 / 750 µm 可选），5 Hz 实时刷新。软件对四个平面的直径做**最小二乘双曲拟合**，由此给出：

| 输出 | 含义 |
|---|---|
| `2Wo` | 最小束腰直径 |
| `Zo` | 束腰 Z 位置（相对零平面） |
| `Zr` | 瑞利长度 |
| `M²` | 由 `2Wo` 与 `Phi` 推出 |
| `Phi` / `NA` | 远场发散角 / 远场数值孔径 |
| `Pt` | 指向角（aiming / bore-sight） |

**判据**：调节 Z 直到 `Zo/Zr < 0.20` 显示绿色，此时 `2Wo` 在名义值 2% 以内，估计值才升级为测量值。白皮书第 5 页明确写了这个比值与颜色对应关系。

**True-2D™ 狭缝**：常规空气狭缝在 Z 向厚 12.5 / 25 µm（最好 6 µm），对紧聚焦光束像一个部分反射的隧道，降低焦点判定精度；True2D 狭缝用光刻工艺做在蓝宝石基片上，总层厚约 **0.4 µm**，薄一个数量级。这项对本项目直接相关 —— 焦点尺寸约 10 µm 量级。

**配置**：探测器可选 Si / InGaAs / 扩展 InGaAs，覆盖 UV 至 2500 nm；束径很小（几 µm）时可切刀口（KE）模式。

**与本研究的关系（仅记事实）**：本项目的模型给出焦斑 9.84 µm、瑞利长度 0.132 mm、M² = 1.2，但这些都是**模型输入或模型输出，不是实测值**；BeamMap2 正是能实测这些量的仪器。引用时须注意：瑞利长度 0.132 mm 远小于标准平面间距 250 µm，若要用它测本项目的焦点，需选 50 µm 间距的配置，且 `Zo/Zr` 判据的可达性需另行确认。

### CalWizard 手册要点（已核实）

标题页（p1）：`Calibration Wizard — User Manual — Advanced Calibration Solutions for 2x and 3x Scanning Heads`，署名 `ENGINEERED BY CAMBRIDGE TECHNOLOGY` / `Novanta Photonics`。目录（p2–p4）显示两条独立流程：第 6 章 `Two-axis Calibration Process`（p17 起）、第 8 章 `Three-axis Calibration Process`（p62 起）。附录：A 激光/振镜时序优化（p112）、B 平板扫描头表征（p124）、C 校准栅格试件（p130）。共 145 页，PDF 元数据作者 `Joseph Remillard`，创建于 2024-01-19。

**3 轴相对 2 轴多出的步骤**（p3 目录）：`8.3 Align Laser`、`8.6 Set Center-Focus Offset`、`8.8 Adjust Focal Plane`。也就是 3 轴流程多出的是**焦点/焦面相关的 Z 向调节**，另加激光准直。

**校准方式**（第 6.5 / 8.9 节）四种：box/cross 栅格数据（快速、"good-enough"）、引导式栅格测量（视场大于 300×300 mm 时）、自动扫描分析（限于 300×300 mm 视场）、以及分析用户自备的栅格测量文件。

**与本研究的关系**：该校准器把误差存成**修正表（correction table）**——由实测栅格得到的查表/插值结构（p9 `Correction Table Structure`、p10 `Using Correction Tables`、p11 `Figure 2 - SMC Correction Table Mapping`）。本项目用的是**二阶多项式系数矩阵**（21×5），属于另一种误差表示。两者都做「指令 → 修正量」的映射，但前者是实测离散表、后者是解析拟合；本项目尚未做两者的对比。

> 该手册讲的是 2 轴与 3 轴扫描头，**不覆盖 5 轴**，也不涉及 precSYS。引用时不得把它当作五轴校准的依据。

## 来源链接

| 来源 | 链接 |
|---|---|
| precSYS 手册 PDF | <https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-precSYS-EN.pdf> |
| precSYS 产品页 | <https://www.scanlab.de/en/products/advanced-scanning-solutions/precsys-micromachining-system> |
| SCANLAB 校准产品页 | <https://www.scanlab.de/en/products/calibration> |
| CalWizard 手册 PDF | <https://novantaphotonics.com/wp-content/uploads/2022/04/CalWizard_Manual.pdf> |
| DataRay BeamMap2 白皮书 PDF | <https://assets.dataray.com/pdf/dataray-beammap2-whitepaper.pdf> |

## 视频资料

| 视频 | 链接 | 本地副本 | 已核实内容 |
|---|---|---|---|
| 五轴校准视频（用户提供） | <https://www.youtube.com/watch?v=xrGgiiWXKjY> | 无 | **未核实**：本机无法访问 YouTube（域名解析到非公网地址），检索也未收录该视频 ID，因此标题、发布方、时长与内容均未确认 |

## 关于「五轴测量」：三份资料里都没有完整答案

逐份核对结果：

| 资料 | 是否覆盖 5 轴测量 | 实际覆盖 |
|---|---|---|
| CalWizard 手册 | **否** | 只有 2 轴（第 6 章）与 3 轴（第 8 章）校准流程 |
| BeamMap2 白皮书 | **部分** | 测 X、Y、Z 位置 + 指向角（Pt，即光束方向相对仪器轴的两维角） |
| precSYS 手册 | **提到，但没讲方法** | 有「beam position measuring unit（Automatic Fine Adjustment）」；规格表列出 5 个出厂标定轴 |

### 细节

**precSYS 手册 p8 规格表**明确写了轴的构成：

> `Axes — 5 factory calibrated axes (x, y, z coordinates and 2 incidence angles a, b)`

同一页还有两项与角度精度有关的指标：`Theoretical resolution of incidence angle 2 µrad`、`Repeatability in image field ≤ 0.5 µm`。

**p2「Automatic Fine Adjustment」**说明这套测量单元的用途是**内部对零**：

> 光束位置测量单元监测光束位置；若超出容差，软件用系统内部五个振镜轴把光束调回原始零位。

**但手册没有说明**：该测量单元测的是哪几个自由度、精度多少、能否测 AOI。这是本项目最需要、而资料里缺的一项。

**BeamMap2** 能测的 5 个量是 X、Y、Z 位置 + 两个指向角（`Pt`，aiming / bore-sight），那是**光束方向相对仪器轴**的角度，**不是**相对工件表面的 AOI（α、β）。两者定义不同，不可互换。

### 对本项目的结论

要实测本模型的 5D 位姿 `T=[X,Y,Z,α,β]`，现有资料**不足以支撑**：

- `X, Y, Z`：BeamMap2 可测
- `α, β`（相对工件表面的入射角）：**三份资料都没有给出测量方案**。BeamMap2 的指向角是相对仪器轴，要转成相对工件表面还需工件法线与面内参考轴（这一点与 `assembly-reference.md` 中「暂定工件为水平面、法线 +Z」的假设直接相关）
- 校准侧的 5 轴流程：CalWizard 只到 3 轴

**待补**：precSYS 测量单元的自由度与精度；或寻找讲解 5 轴扫描系统 AOI 实测的独立资料。

## 待补

- 上表视频的标题、发布方、发布日期；若确认与 precSYS 五轴校准相关，再补充「哪一段对应哪个校准动作」。
- 视频要点若被本文档或 `assembly-reference.md` 引用，需先核实再写，并在对应位置标注来源与时间点。
- 「五轴测量」一节列出的缺口：precSYS 光束位置测量单元的自由度与精度；AOI（相对工件表面入射角）的实测方案。

## 引用纪律

- 不得把本项目假设写成来源结论；引用处区分「公开依据」「本项目推导」「工程假设」三类。
- 未核实的来源只登记链接，不据此下结论。
