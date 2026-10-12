# F-θ 场镜事实核查汇总（素材版）

> 采集说明：本次会话 `web_fetch` 工具被沙箱拦截（所有域名解析到非公网 IP），`Invoke-WebRequest` 直连超时。
> 因此**证据等级仅到"搜索引擎返回的页面标题 + 摘要片段"**，未能逐页打开正文核对数值表。
> 已严格区分标记，未找到的数据一律写「❌ 未找到」，不做推算填充。
> 标记含义：✅ 摘要/标题中直接可见该事实；🟡 来源页面存在但数值未经正文核对；❌ 未找到公开来源。

---

## 1. 为什么需要 F-θ 场镜

✅ 普通球面单透镜把焦点落在**球面**上（场曲），且落点按 r = f·tanθ 分布；F-θ 镜提供**平场**聚焦面，并使像面位置正比于扫描角。
- 来源：Sill Optics 技术指南 [来源](https://www.silloptics.de/en/service/sill-technical-guide/laser-optics/f-theta-lenses)（厂商官网）
- 来源：RP Photonics《Scanning Lenses》 [来源](https://www.rp-photonics.com/scanning_lenses.html)（技术百科）
- 来源：Thorlabs F-Theta 教程 [来源](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=10766)（厂商官网）

✅ "F-θ 镜通过**故意引入桶形畸变**来抵消 tanθ 的正向误差"。
- 来源：亚利桑那大学光学硕士报告《Design of Large Working Area F-Theta Lens》 [来源](https://wp.optics.arizona.edu/alumni/wp-content/uploads/sites/113/2023/06/msreport-gong-chen.pdf)（论文）

✅ 定义式 y = f·θ（y = 焦点离场中心距离，f = 有效焦距，θ = 光束偏转角）。
- 来源：GIAI《F-Theta Scan Field Size Calculation》 [来源](https://www.giaiphotonics.com/f-theta-scan-field-size-calculation/)（二手/经销商）
- 来源：Thorlabs「output beam displacement is proportional to the product of focal length f and scan angle θ」 [来源](https://www.thorlabs.co.jp/f-theta-scan-lenses)

### 对照表（本表为**我方纯算术**，基于两个定义式，非引用数据）

设 f 归一化为 1（单位焦距），机械半角 θ_m，光学角 θ = 2θ_m。

| 参数 | 10° | 20° | 30° |
|---|---|---|---|
| θ (rad) | 0.174533 | 0.349066 | 0.523599 |
| tanθ | 0.176327 | 0.363970 | 0.577350 |
| r_ftan = f·tanθ | 0.176327 f | 0.363970 f | 0.577350 f |
| r_fθ = f·θ | 0.174533 f | 0.349066 f | 0.523599 f |
| Δ = f(tanθ − θ) | 0.001794 f | 0.014904 f | 0.053751 f |
| Δ/r_fθ | 1.028 % | 4.270 % | 10.266 % |

**落点误差换算（f = 254 mm 为例）**：10° → 0.456 mm；20° → 3.79 mm；30° → 13.65 mm。

---

## 2. 关键参数与互相制约

✅ 选型首要三参数：**工作波长、光斑尺寸、扫描场直径 SFD**；由此再约束入瞳光束直径、振镜偏转量、镜片位置。
- 来源：Thorlabs F-Theta 教程 [来源](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=10766)（厂商官网）

✅ 焦距/后焦距按"波长、激光功率、光斑尺寸、像场尺寸、工作距离"共同优化——即这 5 项是耦合的，不是独立可选。
- 来源：SCANLAB Scan Lenses 产品页 [来源](https://www.scanlab.de/en/products/scan-components/scan-lenses)（厂商官网）

✅ 短焦 → 短工作距离 + 紧凑系统；长焦 → 可在无外部轴情况下加工大像场。
- 来源：SCANLAB（DirectIndustry 产品页转述） [来源](https://www.directindustry.com/prod/scanlab-gmbh/product-39164-2152251.html)（🟡 二手转述）

✅ 有效打标场大致**正比于焦距**。
- 来源：思特光学《F-Theta Lens Selection Guide》 [来源](https://www.scanneroptics.com/f-theta-lens-selection-guide.html)（经销商）

### 厂商实际参数（可核对的条目）

| 厂商/型号 | 波长 | 焦距 | 幅面 | 入瞳/输入光束 | 工作距离 | 来源 |
|---|---|---|---|---|---|---|
| VONJAN f-254M-10-1064（Mini） | 1064 nm | 254 mm | 175×175 mm | 最大输入 10 mm | — | ✅ 数据手册 [PDF](https://www.vonjan-tech.de/en/lasers-optics-scanheads/f-theta-lenses/1064-nm-optical-glass-mini/f-254m-10-1064.pdf) |
| VONJAN f-550-30-915-M112 | 915–980 nm | 550 mm | 最大 350×350 mm | 30 mm | — | ✅ 产品页 [来源](https://www.vonjan-tech.de/en/lasers-optics-scanheads/f-theta-lenses/915-980-nm-fused-silica/f-550-30-915-m112.html)（熔石英，M112 接口） |
| SCANLAB hurrySCAN 30（整机+场镜） | 1064 nm | 160 mm | 30×30 mm | — | — | ✅ 典型扫描角 ±0.35 rad(光学)、典型光斑 11 µm @M²=1.0 [来源](https://www.scanlab.de/en/products/scan-systems/hurryscan/standard-series/hurryscan-30) |
| Coherent High Power F-Theta | 高功率 | 32–920 mm | 6×6 至 710×710 mm | — | — | ✅ 熔石英/CaF₂/蓝宝石，>6 kW [来源](https://www.coherent.com/optics/laser-optics/f-theta-scan-lenses/high-power-f-theta-lenses) |
| Jenoptik JENar™ 350-1030…1080-452 | 1030–1080 nm | 350 mm | 大幅面 | — | — | ✅ [PDF](https://www.jenoptik.us/-/media/websitedocuments/optics/f-theta/data-sheets/f-theta-017700-009-26-ft-03-424ft-350-1030.pdf) |
| Jenoptik JENar™ 170-532-160 | 532 nm | 170 mm | — | — | — | ✅ [PDF](https://www.jenoptik.com/-/media/websitedocuments/optics/f-theta/data-sheets/f-theta-017700-206-26-ft-170-532-160.pdf) |
| Jenoptik JENar™ APTAline 639-1030…1080-580-AL | 1030–1080 nm | 639 mm | — | — | — | ✅（SLS 用）[来源](https://www.jenoptik.com/products/optical-systems/objective-lenses-for-high-precision-laser-material-processing/f-theta-lens) |
| Jenoptik JENar 108（远心） | 355 nm 系 | — | — | — | — | ✅ [PDF](https://www.jenoptik.us/-/media/websitedocuments/optics/f-theta/data-sheets/f-theta-017700-203-26-ft-03-75ft-108.pdf) |
| 波长光电 SL-355-170-255-D10 | 355 nm | 255 mm(有效) | 170×170 mm | — | 302.46 mm | 🟡 经销商页 [来源](https://www.soar-laser.cn/product/sl-355-170-255-d10/)；外径 89 mm，M85×1 |
| 波长光电 BC SL-355-175-254-D12 | 355 nm | 254 mm | 175×175 mm | 12 mm | — | 🟡 光斑 20–30 µm、透过率 ≥95% [来源](https://www.soar-laser.cn/product/sl-355-175-254-d12/) |
| Sill Optics 标准系列 | 1064 nm 玻璃 | 覆盖 420/1254/163 等多型 | — | — | — | ✅ 数据手册 PDF [S4LFT0420-126](https://www.unice-eo.com/archive/Download/Sill%20Optics/F-Theta%20Lenses/Glass/S4LFT0420-126.pdf)、[S4LFT0163-126](https://www.mjlinc.com/img_up/shop_pds/mjct/design/datasheet/Sill/f-theta%20lens/s4lft0163-126.pdf) |
| Sill Optics 远心熔石英 | 1030–1090 nm | — | — | — | — | ✅ [PDF S4LFT4147-328](https://www.unice-eo.com/archive/Download/Sill%20Optics/F-Theta%20Lenses/Fused%20Silica/S4LFT4147-328.pdf) |

✅ Jenoptik 明确声明：**后工作距离、法兰焦距、焦距因制造公差有 ±1.5 % 偏差**（重要：选型不能按名义值卡死机械行程）。
- 来源：Jenoptik 数据手册 [PDF](https://www.jenoptik.us/-/media/websitedocuments/optics/f-theta/data-sheets/f-theta-017700-009-26-ft-03-424ft-350-1030.pdf)
- 佐证：同款声明见 [JENar Silverline 55-355](https://www.jenoptik.com/-/media/websitedocuments/optics/f-theta/data-sheets/f-theta-605678-sl-55-355-21.pdf)

✅ Sill Optics：**通光孔径/光阑位置**定义为"振镜两镜几何中心到镜筒机械端面的距离"，其目录中扫描长度/面积按"典型扫描头的镜间距"计算，并**已计入最大 1 % 渐晕**。
- 来源：Sill Optics 技术指南 [来源](https://www.silloptics.de/en/service/sill-technical-guide/laser-optics/f-theta-lenses)

✅ 建议：**入射光束直径不超过场镜入瞳的 50–75 %**，以避免截光。
- 来源：思特光学选型指南 [来源](https://www.scanneroptics.com/f-theta-lens-selection-guide.html)（经销商，🟡 经验准则非厂标）

✅ 光束直径至少应为入瞳的一半（"lens diameter ≥ 2× 输入光束直径"）以免削掉高斯翼。
- 来源：Lasercalculator [来源](https://lasercalculator.com/laser-spot-size-calculator/)

🔴 **关键单位陷阱**：Sill Optics 明示：扫描速度 = 焦距 × 定位速度；Raylase 给出算例 f = 254 mm、40 rad/s → v = 10.1 m/s。
- 来源：RAYLASE FOCUSSHIFTER DIGITAL II 手册 [PDF](https://www.raylase.de/_Resources/Persistent/5/b/9/0/5b9058dcb0c4f361859551b86d9c55d6d35478d1/RAYLASE_FOCUSSHIFTER%20DIGITAL%20II_en.pdf)

---

## 3. 光斑尺寸计算

✅ 两种主流形式并存，**系数不可混用**：

| 形式 | 适用条件 | 系数 | 来源 |
|---|---|---|---|
| d = C·λ·f/A，**C = 1.83** | A 为在 **1/e² 处被截断**的高斯光束入瞳直径 | 1.83 | ✅ 上海光学 [来源](https://www.shanghai-optics.com/assembly/f-theta-lenses/)；✅ SUPERIOR [来源](https://www.superiorcctv.com/f-theta-lenses-tutorial/) |
| d = 4λf/(πD) ≈ 1.273 λf/D | 理想（未截断）高斯，d 为 1/e² 直径 | 4/π | ✅ calculatorhub [来源](https://calculatorhub.com/tools/laser-spot-size-calculator/)；✅ ePhotonics [来源](https://ephotonics.com/calculators/laser-beam-spot-size/) |

✅ 1.83 的来历：把入瞳按 1/e² 直径**硬截断**后，孔径衍射的主瓣变宽并出现旁瓣，故系数从 1.273 抬到 1.83。
- 来源：GIAI 指南明确写「Most f-theta lens vendors, including Thorlabs and LINOS, publish spot size calculations using C = 1.83, which applies when the entrance beam is truncated at its 1/e² diameter」 [来源](https://www.giaiphotonics.com/f-theta-lens-spot-size-vs-beam-diameter/)（二手，但明确点名厂商）

✅ M² 直接乘在光斑直径上：d = C·λ·f·M²/D；单模光纤激光 M² ≲ 1.2，多模/高功率固体/直接半导体激光可显著更高。
- 来源：GIAI [来源](https://www.giaiphotonics.com/f-theta-lens-spot-size-vs-beam-diameter/)（🟡 二手；M² 定义 ✅ 见 [everycalculators](https://everycalculators.com/laser-spot-size-calculator.html)）

✅ Sill Optics 用的是同一逻辑：d_min = λ·f·APO·M² / d_L（APO = 光束直径与入瞳之比因子，d_L = 1/e² 光束直径）。
- 来源：Sill Optics《Laser Optics – General explanations》 [来源](https://www.silloptics.de/en/service/sill-technical-guide/laser-optics/laser-optik-grundlegende-erklaerungen)

✅ **光斑定义坑**：SCANLAB 定义焦点直径为"包含 86.5 % 总功率的光束腰直径，对高斯光束等于 1/e² 直径"。Sill 数据手册则明确写「spot diameter at **86.5 %** level for a Gaussian beam (M²=1)」。
- 来源：SCANLAB 术语表 [来源](https://www.scanlab.de/en/service/glossary/focal-diameter-focal-spot)
- 来源：Sill 数据手册 [PDF](https://www.mjlinc.com/img_up/shop_pds/mjct/design/datasheet/Sill/f-theta%20lens/s4lft0163-126.pdf)

✅ DOF 形式：DOF = π·d²/(2·M²·λ)（d 为光斑直径）。
- 来源：best-calculators [来源](https://best-calculators.com/education-academic/laser-spot-size-calculator/)（🟡 计算器站，非厂标）

### 选型算例（我方算术，公式与系数均来自上述来源）

**任务**：1064 nm 单模光纤激光，M² = 1.1，准直后 1/e² 光束直径 D = 8 mm，目标幅面 110×110 mm，振镜光学扫描角 ±0.35 rad。

1. 幅面对角半径 r = 110√2/2 = **77.8 mm** → f = r/θ = 77.8/0.35 = **222 mm**。
   - 注意：厂标幅面（如 Vonjan f-254M → 175×175）通常**大于** 2fθ 的方形内切值，因为标注的是可用的方形场，需按厂标核对。
2. 取 f = 254 mm（标准档）：r = 254×0.35 = **88.9 mm** → 方形内切 125.7×125.7 mm ✅ 覆盖 110×110。
3. 光斑：d = 1.83×1.064e-3×254×1.1/8 = **68.0 µm**（1/e² 直径，按截断公式）。
   - 若误用未截断式：4×1.064e-3×254×1.1/(π×8) = **47.3 µm** —— 差 **44 %**，这就是系数不能混用的实证。
4. 若改 f = 160 mm（120 mm 幅面档）：d = 1.83×1.064e-3×160×1.1/8 = **42.8 µm**，r = 56 mm（内切 79 mm 方形，不够 110 mm）。
5. 若要 25 µm 光斑 @ f=254：需 D = 1.83×1.064e-3×254×1.1/25 = **21.8 mm** → 需配入瞳 ≥ 29–44 mm 的大口径场镜，并须扩束，且此时焦深骤降。
6. 焦深：θ_div = λ·M²/(π·w₀)，w₀ = d/2 = 34 µm → θ_div = 1.064e-3×1.1/(π×0.034) = **10.95 mrad** → DOF(2z_R) = 2w₀/θ_div = **6.2 mm**。（校验：πd²/(2M²λ) = π×0.068²/(2×1.1×1.064e-3) = 6.2 mm ✔ 自洽）

---

## 4. 焦深与平场性

✅ Thorlabs：场镜数据图中同时给出**场曲（mm）与 f-θ 畸变（%）随扫描角的变化**；工程上应把**零场曲点放在扫描中段**，以限制全行程内的场曲量。
- 来源：Thorlabs F-Theta 教程 [来源](https://www.thorlabs.co.jp/f-theta-lenses-tutorial)（厂商官网，✅ 直接可见）

✅ Edmund Optics：**Field flatness** 描述"为保持全幅面对焦，目标面需要多平"；影响因素为**接受孔径（acceptance aperture）与焦距**两项。
- 来源：Edmund Optics 应用笔记 [来源](https://www.edmundoptics.com/knowledge-center/application-notes/optics/chromatically-corrected-f-theta-lenses-for-ultrafast-laser-applications/)（厂商官网）

✅ Sill：场镜提供"平聚焦面 + 全幅面**近乎恒定**的光斑尺寸"——注意措辞是"almost constant"，不是"constant"。
- 来源：Sill Optics [来源](https://www.silloptics.de/en/service/sill-technical-guide/laser-optics/f-theta-lenses)

✅ 边缘光斑变大的机制（Ronar-Smith）：场镜在平面上的光斑尺寸**存在随 X/Y 两镜角度变化的典型波动**，其应用笔记给出光斑变化图与计算式（Figure 3/4）。
- 来源：Ronar-Smith 应用笔记 [来源](https://wavelength-oe.com/f-theta-scan-lens/)（厂商官网）

🟡 大幅面边缘劣化的工程解释：扫到边缘时线速度加快、能量沉积减少，叠加场曲与像散导致离焦与畸变，出现"线条一头深一头浅"。
- 来源：CASTECH（福晶）技术文 [来源](https://gb.castech.com/news_detail/9.html)（厂商，二手表述）
- 来源：JGZOE《Why Edge Distortion Happens in Large Area F-theta Lenses》 [来源](https://www.jgzoe.com/news/why-edge-distortion-happens-in-large-area-f-theta-lenses/)

❌ **未找到**：任何厂商数据手册给出的明确"平场性 flatness = ±X µm over Y mm 幅面"的**可核对数值**（Sill/Jenoptik/Thorlabs 手册页未能打开正文）。

---

## 5. 畸变类型与可校正性

✅ f-θ 畸变 / 线性度误差典型规格区间：**< 0.1 % 至 < 1 %**。
- 来源：Dayy Photonics 知识库 [来源](https://www.dayyphotonics.com/knowledge-base/f-theta-lens)（🟡 经销商，区间值非具体型号）

✅ F-θ 镜**故意设计成桶形畸变**以抵消 tanθ。
- 来源：亚利桑那大学论文 [PDF](https://wp.optics.arizona.edu/alumni/wp-content/uploads/sites/113/2023/06/msreport-gong-chen.pdf)（论文）
- 来源：SUPERIOR「With a barrel distortion F-Theta Lenses is ideal for engraving and labeling systems…」 [来源](https://www.superiorcctv.com/f-theta-lenses-tutorial/)

✅ 三种畸变表述方式的区别（F-Tan(θ) / F(θ) / TV 畸变）见 e-con Systems 综述；TV 畸变属"RIAA TV distortion"体系，与几何畸变并列。
- 来源：e-con Systems [来源](https://www.e-consystems.com/blog/camera/technology/optics/a-beginners-guide-to-lens-distortion-parameters-f-theta-f-tan-theta-and-tv-distortion/)
- 来源：Edmund Optics《Distortion》 [来源](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/distortion/)

✅ 渐晕：Sill 目录值**已按最大 1 % 渐晕**计算（即厂标幅面本身就带渐晕前提，超幅面使用时光斑/功率会掉）。
- 来源：Sill Optics [来源](https://www.silloptics.de/en/service/sill-technical-guide/laser-optics/f-theta-lenses)
- 佐证：Edmund Optics 版 Sill 数据手册「The stated values are based on a vignetting of less than 1 %」 [PDF](https://www.edmundoptics.com/ViewDocument/spec_70146.pdf)

### 软件可校正 vs 不可校正

✅ **可校正**：标定/软件补偿可显著降低全视场畸变。RAYLASE SPICE3 手册专设"7.1.4 Correction of Marking Field Distortion"，说明 F-θ 镜本身完成**光学**校正（把焦点面压平到打标面）；SCAPS SAMLight 还提供"**F-Theta Factor Calibration**"用于在非 z=0 高度打标时修正 x/y 坐标。
- 来源：RAYLASE SPICE3 用户手册 [来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/F5DDE105-3406-416E-B7D0-2C1EF865BFE1.htm)（厂商官网）
- 来源：SCAPS SAMLight 手册 [来源](https://download.scaps.com/downloads/Software/SAMLight/Manual/html/f-theta_factor_calibration.htm)（厂商官网）

✅ **必须实测标定**：GitHub `matthewSorensen/scanner-calibration` 明确指出——尽管 F-θ 镜设计上保证角度-位置线性，"essentially all high precision applications require additional empirical calibration"。
- 来源：[GitHub](https://github.com/matthewSorensen/scanner-calibration)（开源工具）

🟡 标定流程实例：LightBurn 用 9 点网格打样、测量后反算修正值；用户论坛反映 200×200 / F290 镜"100 mm 处短 2 mm"，说明**残余标定误差按比例放大**，小尺寸画不出正确的缩放。
- 来源：[LightBurn 指南](https://haotianlasers.com/fiber-laser-lens-focus-calibration-lightburn/)（🟡 二手）
- 来源：[LightBurn 论坛帖](https://forum.lightburnsoftware.com/t/f-theta-lens-calibration-question/170516)（🟡 用户案例）

**判据（我方综合，未找到厂标权威表述）**：与落点 x/y 相关的**几何**畸变可软件校正；**光斑尺寸变化、渐晕能量损失、场曲导致的离焦、热致焦移**属光学量，软件无法补偿（离焦可借 z 轴/3D 校正部分弥补）。

---

## 6. 多波长与宽带场镜

✅ 核心规则：场镜必须按**实际使用波长**设计；532 nm 镜不是 1064 nm 镜的"高分辨率版"，1064 nm 镜除非设计与镀膜明确覆盖双波长，否则**不应**用于 532 nm。
- 来源：GIAI《1064nm vs 532nm F-Theta Scan Lens》 [来源](https://www.giaiphotonics.com/1064nm-vs-532nm-f-theta-scan-lens/)（🟡 二手）

✅ Ronar-Smith 消色差场镜设计目标：「limit spherical and chromatic aberration, and bring in two different wavelengths (**working and visible**) onto the same plane」——即消色差的目的之一是让**可见指示光与工作光共焦**。
- 来源：Ronar-Smith 应用笔记 [来源](https://wavelength-oe.com/f-theta-scan-lens/)（厂商官网）

✅ Sill Optics 有多光谱场镜产品线，「Multispectral Design Wavelength of 532nm and 1064nm」；Edmund Optics 描述其「Corrected for Nd:YAG fundamental 1064nm and the second harmonic 532nm，features a common mounting thread」。
- 来源：Edmund Optics 产品页 [来源](https://www.edmundoptics.com/f/sill-optics-multispectral-f-theta-lenses/40164/)（厂商经销商页，✅）
- 来源：Edmund Optics 品类页 [来源](https://www.edmundoptics.com/c/f-theta-lenses/1255/)

✅ **可核对的 LIDT 数值（少见的一手数字）**：Sill 多光谱场镜 1064/532 nm 双波长版本，**2.5 J/cm² (1 ns, 50 Hz)** 脉冲、**2.5 MW/cm²** 连续。
- 来源：Edmund Optics [来源](https://www.edmundoptics.com/f/sill-optics-multispectral-f-theta-lenses/40164/)（✅ 直接可见具体数值）

❌ **未找到**：复合/消色差场镜与单波长场镜的**具体价格倍数**或成本结构拆解（"为什么贵很多"的量化依据）。只能给出定性机制（更多镜片/更多材料牌号/双波长镀膜/更严公差），未找到可引用来源。

---

## 7. 大功率场镜

✅ Jenoptik Silverline® 定位：为高功率、短脉冲应用开发，**全石英（full quartz glass）**、低吸收。
- 来源：Jenoptik F-Theta 产品组合页 [来源](https://www.jenoptik.com/products/optical-systems/objective-lenses-for-high-precision-laser-material-processing/f-theta-lens/standard-portfolio)（厂商官网）

✅ Coherent 高功率场镜：基于低吸收材料 + 低吸收镀膜工艺，材料可选 **熔石英 / CaF₂ / 蓝宝石**，面向 **>6 kW**，焦距 32–920 mm，幅面 6×6 至 710×710 mm。
- 来源：Coherent [来源](https://www.coherent.com/optics/laser-optics/f-theta-scan-lenses/high-power-f-theta-lenses)（厂商官网）

✅ 紫外场镜：**UV 级熔石英**是 355 nm 的标准选择（低吸收、高 LIDT）；**CaF₂** 用于特定高功率或深紫外设计（低色散）。
- 来源：Nandi Optics [来源](https://www.nandioptics.com/f-theta-lens)（🟡 厂商/经销商）

✅ 水冷场镜确实存在：HPAW 提供"Water cooling quartz F-Theta lens"，全系熔石英，幅面 100×100 / 140×140 / 160×160 / 200×200 / 255×255 mm，接口 M85×1 / M95×1。
- 来源：HPAW 产品页 [来源](https://www.hpaw.com/en/Product/Optical_Lens/544.html)（厂商官网，🟡 国内厂商）

✅ 热透镜/热致焦移是一手论文级现象：
- DGaO 会议论文《Simulation and measurement of thermo-optical effects in an f-theta lens》——以 **ZnSe** 场镜为例仿真并实测热致焦移。[来源](https://dgao-proceedings.de/download/117/117_c15.pdf)（论文）
- ResearchGate《Optical design and performance of F-Theta lenses for high-power and high-precision applications》——高功率辐射在光学元件中的**非均匀（梯度）加热**导致热透镜、近轴焦移与像差，进而改变光斑尺寸。[来源](https://www.researchgate.net/publication/282653504_Optical_design_and_performance_of_F-Theta_lenses_for_high-power_and_high-precision_applications)（论文）
- ScienceDirect：高功率 1064 nm 水导激光系统中热透镜效应的理论+数值+实验研究，揭示功率上升与光束半径减小对温升、折射率梯度、焦移的影响，并验证熔石英 + 主动水冷。[来源](https://www.sciencedirect.com/science/article/pii/S135044952600544X)（论文）
- Laser Focus World：高功率系统中"最显著的效应是热透镜引起焦移"。[来源](https://www.laserfocusworld.com/optics/article/14104004/careful-optical-system-design-enables-cutting-edge-high-power-laser-applications)（行业媒体）

✅ Sill 技术指南中把"**Absorption and thermal focus shift**（吸收与热致焦移）"单列为一项规格条目——说明该指标在其数据手册中是有位置的。
- 来源：Sill Optics 技术指南目录 [来源](https://www.silloptics.de/en/service/sill-technical-guide)（厂商官网）

✅ LIDT 的规范与不可跨条件套用：ISO 21254-1:2011 定义为"损伤概率外推为零时的最高激光辐射量"；LIDT **不是标准化测试**，且随波长、脉宽、光斑直径变化，跨条件必须重新评估。
- 来源：Electro Optics LIDT 白皮书 [PDF](https://www.electrooptics.com/sites/default/files/content/white-paper/pdfs/LIDT%20of%20Laser%20Components_18_0.pdf)（白皮书，✅ 含 ISO 标准号）
- 来源：Edmund Optics LIDT 计算器 [来源](https://www.edmundoptics.com/knowledge-center/tech-tools/laser-damage-threshold-scaling/)（厂商官网）
- 来源：Edmund Optics《Laser Damage Threshold Testing》「Testing LIDT is not standardized」 [来源](https://www.edmundoptics.com/knowledge-center/application-notes/lasers/laser-damage-threshold-testing/)

❌ **未找到**：石英 vs 玻璃场镜在**具体吸收系数/ppm·cm** 或 **LIDT (J/cm² @ 1064nm, 10ns)** 上的对偶数值表。

---

## 8. 选型流程 checklist

厂商标称的约束项（✅ Thorlabs / SCANLAB）：**波长 → 光斑尺寸 → 扫描场直径 SFD → 入瞳光束直径 → 振镜偏转量 → 镜片位置/镜间距**。
- 来源：Thorlabs [来源](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=10766)；SCANLAB [来源](https://www.scanlab.de/en/products/scan-components/scan-lenses)

思特光学版四步法（🟡 经销商）：四关键参数为**焦距、扫描场、入瞳直径、波长**。
- 来源：[来源](https://www.pls-optic.com/news/f-theta-lens-selection-guide.html)；[来源](https://www.scanneroptics.cn/f-theta-lens-selection-guide.html)

### 决策链（我方整理，逻辑依据上列来源）

```
1. 波长 λ（决定镜片材料与镀膜，不可跨用）
2. 幅面需求 → 半对角 r
3. 振镜可用光学扫描角 θ_max（查振镜手册，如 SCANLAB ±0.35 rad）
   → f_min = r / θ_max   （注意厂标幅面通常含 1% 渐晕前提）
4. 目标光斑 d → 反解所需输入光束直径 D = C·λ·f·M²/d （C=1.83 截断式）
5. 校验 D ≤ 入瞳 × (50~75%)          [否则削光、光斑变差]
6. 解 DOF = πd²/(2M²λ) ≥ 工艺容差（工件平面度 + 装夹误差 + 热漂移）
7. 校验机械：法兰焦距/后工作距离（含 ±1.5% 公差）↔ 振镜镜间距 ↔ z 轴行程
8. 校验热与损伤：平均功率/峰值功率密度 vs 镀膜 LIDT；> 数百 W 或高占空比 → 考虑熔石英/水冷
9. 校验回返光：厂方 back-reflection 图（Jenoptik 每款都有）
```

✅ 第 9 步依据：Jenoptik 为每型场镜提供**回返光位置图**，并声明"回返光在图示位置之外、镜内回返光被优化到避开所有镜面；所有数值仅对**准直光束**及正确使用有效，**改变系统设置或工况会导致回返位置变化并造成损伤**"。
- 来源：Jenoptik 回返光图 [PDF](https://www.jenoptik.com/-/media/websitedocuments/optics/f-theta/rueckreflexgraphen/f-theta-601787-rr.pdf)；[PDF](https://www.jenoptik.us/-/media/websitedocuments/optics/f-theta/rueckreflexgraphen/f-theta-017700-405-26-rr.pdf)

✅ 焦距与场镜尺寸档位存在行业惯例：Cloudray 论坛实例"F160 (110×110mm) 换成 F420 (300×300mm)"；EZCAD 标准系列覆盖紫外到红外、焦距 **63 mm 至 1450 mm**。
- 来源：Cloudray 论坛 [来源](https://forum.cloudray.com/t/setting-after-change-the-f-theta-lens/432)
- 来源：EZCAD 产品页 [来源](https://www.ezcad.com/products/f-theta-l-ens-flat-field/)（🟡 经销商）

---

## 9. 装反的后果 与 机械接口

❌ **未找到公开来源**明确描述"场镜装反"的后果。检索到的厂商资料只有 **Reversed Mode** 这一条目名（Sill 技术指南目录中列出），但**未能打开正文**确认其含义是否为"反向使用"。
- 仅有目录条目：Sill Technical Guide 目录含 "Reversed Mode" [来源](https://www.silloptics.de/en/service/sill-technical-guide)（❌ 内容未确认）

🟡 间接相关：Jenoptik 声明系统设置改变会使回返光位置变化并**可能导致损伤**——这是"非设计工况使用"最接近的厂方风险表述。 [来源](https://www.jenoptik.us/-/media/websitedocuments/optics/f-theta/rueckreflexgraphen/f-theta-017700-405-26-rr.pdf)

⚠️ 我方能给的**仅限光路推理**（非引用事实，请勿当结论）：场镜是强非对称多片结构，反向入射会改变工作距离/法兰距离匹配、破坏已优化的场曲与畸变补偿、并让回返光落在未设计的位置。**需实测验证，无来源。**

### 机械接口

✅ M85×1 是打标机场镜的**事实标准螺纹**：「features a standard M85x1 threading, allowing for easy replacement or upgrade in most compatible laser marking machines」。
- 来源：Cloudray F-Theta 说明书 [PDF](https://manuals.plus/asin/B07CD8KJK2.pdf)（厂商文档）

✅ 355 nm 紫外场镜实例：外径 89 mm，**M85×1**；工作距离 302.46 mm。
- 来源：波长光电 SL-355-170-255-D10 [来源](https://www.soar-laser.cn/product/sl-355-170-255-d10/)（🟡 经销商）

✅ M112×1 用于**大口径/长焦**场镜：VONJAN f-550-30-915-**M112**（入瞳 30 mm，幅面 350×350 mm）——型号后缀即接口代号。
- 来源：VONJAN [来源](https://www.vonjan-tech.de/en/lasers-optics-scanheads/f-theta-lenses/915-980-nm-fused-silica/f-550-30-915-m112.html)（厂商官网）

✅ 其他接口档：水冷场镜提供 **M85×1 / M95×1**。
- 来源：HPAW [来源](https://www.hpaw.com/en/Product/Optical_Lens/544.html)（厂商官网）

🟡 补偿件：市面上有"F-theta Lens Male Thread Reverse Adapter Ring"（18 mm / 34 mm 高）与"Lens Adjust Mount"，用于解决场镜与机身螺纹高度不匹配、把场镜装到正确焦面。
- 来源：Amazon/Cloudray 转接环 [来源](https://www.amazon.com/Cloudray-F-Theta-Adjust-Marking-Machine/dp/B08976BJS5)（🟡 电商）

⚠️ 检索命中一条声称「DIN 332 中心孔 + M85×1 + 85.0±0.05 mm 孔径」的说法，来源为 AliExpress 的 SEO 页面，**可信度低，不建议引用**： [来源](https://www.aliexpress.com/s/wiki-ssr/article/din-332-center-hole-dimensions-pdf)（❌ 不采信）

---

## ⚠️ 常见误解（按可引用程度排列）

1. **「场镜让光斑全幅面一样大」** ❌ → 厂方原文是 "**almost** constant spot size"，且 Ronar-Smith 明确给出光斑随双镜角度变化的波动图。 [来源](https://www.silloptics.de/en/service/sill-technical-guide/laser-optics/f-theta-lenses) / [来源](https://wavelength-oe.com/f-theta-scan-lens/)

2. **「光斑公式随便挑一个用」** ❌ → 1.83（1/e² 截断）与 4/π≈1.273（未截断高斯）在 f=254、D=8、M²=1.1、1064 nm 下差 44 %（68.0 vs 47.3 µm）。 [来源](https://www.giaiphotonics.com/f-theta-lens-spot-size-vs-beam-diameter/)

3. **「标称幅面就是能用的最大方场」** ❌ → Sill 目录值基于"典型扫描头镜间距"且**已按 1 % 渐晕**计算；Edmund 版手册原文「based on a vignetting of less than 1 %」。换振镜后幅面会变。 [来源](https://www.edmundoptics.com/ViewDocument/spec_70146.pdf)

4. **「焦距名义值就是机械尺寸」** ❌ → Jenoptik：后工作距离、法兰焦距、焦距均有 **±1.5 %** 制造公差。 [来源](https://www.jenoptik.us/-/media/websitedocuments/optics/f-theta/data-sheets/f-theta-017700-009-26-ft-03-424ft-350-1030.pdf)

5. **「1064 镜可以拿来打 532」** ❌ → 必须按实际波长设计，除非设计与镀膜明确声明双波长。 [来源](https://www.giaiphotonics.com/1064nm-vs-532nm-f-theta-scan-lens/)

6. **「畸变全都能软件标定掉」** ⚠️ → 几何落点畸变可标定（RAYLASE SPICE3 / SCAPS F-Theta Factor / LightBurn 9 点网格）；但光斑尺寸变化、渐晕能量损失、场曲离焦、热致焦移**不是**坐标修正能解决的。 [来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/F5DDE105-3406-416E-B7D0-2C1EF865BFE1.htm) / [来源](https://download.scaps.com/downloads/SAMLight/Manual/html/f-theta_factor_calibration.htm)

7. **「LIDT 数值可以跨条件搬用」** ❌ → LIDT 依赖波长/脉宽/光斑直径，且**测试本身未标准化**；ISO 21254-1:2011 只给出定义口径。 [来源](https://www.edmundoptics.com/knowledge-center/application-notes/lasers/laser-damage-threshold-testing/) / [来源](https://www.electrooptics.com/sites/default/files/content/white-paper/pdfs/LIDT%20of%20Laser%20Components_18_0.pdf)

8. **「入瞳直径 = 可用光束直径」** ❌ → 建议光束 ≤ 入瞳的 50–75 %；且场镜口径至少 2× 光束直径以免削高斯翼。 [来源](https://www.scanneroptics.com/f-theta-lens-selection-guide.html) / [来源](https://lasercalculator.com/laser-spot-size-calculator/)

9. **「扫描角就是振镜机械角」** ⚠️ → SCANLAB 标的是**光学角**（±0.35 rad）；反射镜偏转 θ_m 对应光束偏转 2θ_m，算幅面时差 2 倍。 [来源](https://www.scanlab.de/en/products/scan-systems/hurryscan/standard-series/hurryscan-30)

10. **「场镜装反只是不能聚焦」** ❌/❓ → **未找到公开来源**。可引用的最接近表述是 Jenoptik"工况改变会使回返光位置变化并造成损伤"。**本条不要写进正式文档。**

---

## 遗留缺口（建议后续补查）

- ❌ 平场性 flatness 的具体 µm 级数值（需打开 Sill/Jenoptik PDF 正文）
- ❌ Sill "Reversed Mode" 的确切定义
- ❌ 石英 vs 玻璃的吸收系数 / LIDT 对偶数值
- ❌ 复合（消色差）场镜 vs 单波长场镜的价格倍数
- ❌ 场镜装反的厂商明确警告文本
- ⚠️ 本会话 `web_fetch` 被沙箱拦截；以上所有条目仅到"搜索摘要"级证据，**所有数值在写入正式文档前建议逐页复核 PDF**
