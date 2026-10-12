# Z 轴动态聚焦镜组（dynamic focusing / z-shifter / focus shifter）调研素材

> 标注约定：**✅ 一手确认** = 厂商官网/数据手册/协议规格书/规范原文，或已读全文的论文；**🟡 二手转述** = 代理商、博客、论坛、行业文章；**❌ 未找到** = 未找到公开来源。
> 所有数值均标注来源；自行算术推导的部分明确写「⚠️ 我的算术」。

---

## 1. 为什么需要动态聚焦（Z 轴）？

厂商给的官方理由（一手原文）：

- SCANLAB：varioSCAN II 的 z 轴「使 2D 扫描系统能够执行 3D 加工，或**替代昂贵的物镜以提供平面聚焦面**」[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)
- SCANLAB：excelliSHIFT「把 2D 扫描头扩展为高动态 3D 系统」，卖点是**三个轴加速度完全一致**，且**光路只用反射元件**（无透射元件 → 不同波长无色散、高功率下热透镜效应小）[来源](https://www.scanlab.de/sites/default/files/2025-06/SCANLAB-excelliSHIFT-EN.pdf)
- RAYLASE：预聚焦偏转单元（AXIALSCAN 系列）的存在理由写得很直白：「**在不做焦点校正的偏转单元中，场中心聚焦光斑在任一轴移动时都描出一条弧线，在工作场上方形成一个球面**；在场中心以外，由于镜到工件距离增加，光束**根本没有聚焦**」[来源](https://www.raylase.de/en/products/prefocusing-deflection-units.html)
- RAYLASE：预聚焦单元还解决「输出镜的成本与尺寸限制、2 轴单元的光束孔径限制」，并允许**同一台单元改变工作距离、场尺寸和光斑尺寸** [来源](https://www.raylase.de/en/products/prefocusing-deflection-units.html)
- RAYLASE FOCUSSHIFTER RD-14 数据手册：「**然而工件并不总是平的**……在深雕或钻孔切割玻璃时，还需要在加工过程中校正焦点位置」[来源](https://www.raylase.de/_Resources/Persistent/5/1/8/9/5189d9ad9239901c83aa37b1738071904ed74596/2026-03-16_Datenblatt_FOCUSSHIFTER%20RD-14_EN_v2.0.pdf)
- Novanta LIGHTNING II：DFM（Dynamic Focusing Module）「使光斑在整个工作场保持聚焦」，并「**可适应不同的工作距离和有效场尺寸**，以配合不同的待加工零件」[来源](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf)

**归纳 4 类需求**：① 3D 曲面/异形面加工（焦面必须跟随工件面，平面场镜做不到）；② 大幅面残余场曲 + 小光斑（景深小于场曲残差）；③ 同一台设备切换工作距离/场尺寸/焦距（免更换场镜）；④ 预热焦（pre-focus）架构下补偿球面焦面。

### 1.1 定量：f=160 mm 场镜在 ±100 mm 幅面上的焦面弯曲量

**⚠️ 我的算术（几何推导，非厂商数据）**：若焦面是球面（普通球面镜/未校正系统的极限情形），矢高
$$\Delta z=\sqrt{f^2+y^2}-f\approx\frac{y^2}{2f}$$

| 场镜 f | 幅面半宽 y | 严格值 √(f²+y²)−f | 近似 y²/(2f) |
|---|---|---|---|
| 100 mm | 100 mm | 41.42 mm | 50.0 mm |
| **160 mm** | **100 mm** | **28.68 mm**（√35600 = 188.6796 − 160） | **31.25 mm** |
| 254 mm | 100 mm | 18.98 mm | 19.69 mm |
| 420 mm | 100 mm | 11.74 mm | 11.91 mm |

> ⚠️ **口径提醒**：**28.68 mm 是精确值**，**31.25 mm 只是 y²/(2f) 近似**（在 y/f = 0.625 时已偏高 9%）。引用时用 **28.7 mm**。

**但这个 28.7 mm 不是真实场镜的答案。** f-θ 场镜是专门为平场设计的多片空气间隔系统，把场曲校正到远小于此的残差：

**✅ 一手（定性，厂商明确承认存在残差）**：Thorlabs（原厂 F-Theta 教程）：「f-θ 场镜被很好地设计为提供平坦像面，但**真实镜头很少达到理论值，总会存在一定的畸变与场曲**」，并给出 FTH100-1064 的场曲 mm 曲线，建议「把零曲率点放在扫描范围中段以限制整个扫描过程中的场曲量」[来源](https://www.govolition.com/product/V40-FTH160-1064)

**✅ 一手（Thorlabs 官方场曲曲线 —— 本次已直接读图核对）**：Thorlabs 为每支镜头提供 "Field Curvature (mm) vs Deflection Angle (°)" 双曲线图（蓝 = Tangential Plane 切向面，绿 = Sagittal Plane 弧矢面）。**我直接读取了 FTH160-1064 的官方曲线图**：

| 读数点（离焦量，mm） | 切向面（蓝） | 弧矢面（绿） |
|---|---|---|
| 轴上 0° | ≈ **+0.199** | ≈ +0.199（同起点） |
| 20° | ≈ +0.14 | ≈ **−0.137**（两曲线最大分离处） |
| 28°（额定最大角） | ≈ +0.11 | ≈ +0.19（回到正值） |

→ **FTH160-1064 在整个 ±28° 额定幅面内，焦面偏离理想平面的量 ≲ 0.2 mm**（同族 FTH100-1064 弧矢面在 25° 处约 −0.2 mm，量级一致）。[曲线页来源](https://www.thorlabs.com/f-theta-lenses-tutorial)（✅ 厂商一手；图为官方 780 px 原始曲线，**数值为读图值，非数据表印刷值**）

**⚠️ 我的算术（球面 → 平场的改善倍数）**：28.68 mm ÷ 0.2 mm ≈ **143 倍（两个数量级）**。即「f-θ 场镜已把场曲问题解决了约 99.3%」——**但它没有解决剩下的 0.2 mm，更没有解决「工件本身是弯的」。**

**✅ 一手**：Sill Optics 技术指南定性确认：「标准镜头把光束聚焦在**球面**上，而非理想的平场；使用 f-θ 镜头可提供**平面聚焦面**，并在整个 XY 像面上获得**几乎恒定的光斑尺寸**」[来源](https://www.silloptics.de/en/service/sill-technical-guide/laser-optics/f-theta-lenses)
**🟡 二手**：RP Photonics：「用简单球面镜时，焦点并不是都落在目标平面上，而是落在近似球面上，所以外围区域光斑会变大」[来源](https://www.rp-photonics.com/scanning_lenses.html)

**✅ 一手（本题关键否决项：真实 f=160 场镜的可用幅面上限）**：Thorlabs FTH160-1064（f=160 mm，1064 nm，3 片式）：**大扫描场 70×70 mm² 至 156.7×156.7 mm²**，f-θ 畸变 <1.3%[来源](https://www.govolition.com/product/V40-FTH160-1064)。⚠️ 注意：**156.7×156.7 mm 是 f=254 mm 的 FTH254-1064 的幅面**；FTH160-1064 的额定角是 **±28°**。

**⚠️ 我的算术（±100 mm 幅面所需角度）**：由 $y=f\theta$，覆盖 ±100 mm 需光学半角
$$\theta=100/160=0.625\ \text{rad}=\mathbf{35.8°}\quad(\text{机械镜面 } \pm17.9°)$$
而 FTH160-1064 额定 **±28°**（对应 $y=160\times0.4887=78.2$ mm，即 **≈110.6×110.6 mm 幅面**）。→ **±100 mm（200 mm 幅面）在 f=160 mm 下超出该镜头额定能力约 28%**，必须换更长焦距场镜或改用预聚焦（AXIALSCAN / FOCUSSHIFTER）架构。

**DOF / 瑞利长度公式与算例（λ=1064 nm，M²=1）**：
$$z_R=\frac{\pi w_0^2}{M^2\lambda},\qquad \mathrm{DOF}\approx 2z_R\ (\text{即}\ \pm z_R)$$
其中 $w_0$ = 焦斑**半径**，$\lambda$ = 波长，$M^2$ = 光束质量因子。

| 光斑直径 (1/e²) | w₀ | z_R | DOF ≈ ±z_R |
|---|---|---|---|
| 12 µm | 6 µm | 0.106 mm | ±0.11 mm |
| 20 µm | 10 µm | 0.295 mm | ±0.30 mm |
| 24 µm | 12 µm | 0.425 mm | ±0.43 mm |
| 30 µm | 15 µm | 0.664 mm | ±0.66 mm |
| 50 µm | 25 µm | 1.845 mm | ±1.85 mm |
| 100 µm | 50 µm | 7.382 mm | ±7.38 mm |

（校验：π×0.015²/1.064e−3 = 7.0686e−4/1.064e−3 = 0.6643 mm ✅）

**✅ 一手（残余场曲 vs 焦深的判据）**：Sill 与 RAYLASE 都给出「多数设计在整个扫描场上**衍射极限**」「f-θ 镜头在整个加工幅面上实现**极小的光斑变化**」[来源](https://www.silloptics.de/en/service/sill-technical-guide/laser-optics/f-theta-lenses)、[来源](https://www.raylase.de/_Resources/Persistent/5/1/8/9/5189d9ad9239901c83aa37b1738071904ed74596/2026-03-16_Datenblatt_FOCUSSHIFTER%20RD-14_EN_v2.0.pdf)

**⚠️ 我的推算（判据）**：
- 残余 0.2 mm 对 **50 µm 光斑**（DOF ±1.85 mm）只占 **11%** → **落在焦深内，Z 轴非必需**；
- 对 **30 µm 光斑**（±0.66 mm）占约 **30%** → 边缘吃紧；
- 对 **20 µm 光斑**（±0.30 mm）占约 **68%** → **超出/逼近焦深，必须做平场校正或 Z 轴动态聚焦**；
- 对 **12 µm 光斑**（±0.11 mm）→ **残余场曲是焦深的 1.8 倍，不做 Z 补偿必然边缘离焦**。

**❌ 未找到**：Sill Optics、Jenoptik、LINOS/Qioptiq、Ronar-Smith、Volition、Dayy、Wavelength Opto-Electronic、ULO Optics、II-VI/Coherent 的**数据表中均未给出「flat field deviation / focal plane flatness」的 mm 级数值**；也没有任何厂商给出「f=160 mm + 1064 nm + 200×200 mm 幅面」的公开平场或焦深规格。**不要用估算填补这个空白。**

**🟡 二手（工程经验值，供交叉验证）**：一支工业博客给出「标准 2D 光纤激光（f=160 mm）总工程 DOF 约 ±1.5～2.0 mm；f=254 mm 增至 ±3.5～5.0 mm」，并称「当表面深度变化超过 5～50 mm 时，动态 Z 轴补偿是强制性的」[来源](https://www.meenjet.net/news/laser-marking-curved-surfaces-dynamic-focal-depth.html)。原文把 f=160mm 误写为「F=160nm」，属二手来源，仅作量级参考。

---

## 2. 两种技术路线对比

### (a) 机械式 z-shifter（移动光学镜组改变系统焦距/发散度）

**✅ 一手（SCANLAB 原理原文）**：varioSCAN II「通过**移动光学元件**扩展入射激光束，然后由**固定光学元件**准直或聚焦」，因此有两种配置：**Type FT（配 F-Theta 物镜）或 Type PR（PRefocus，预聚焦）** —— 即「有或没有 F-Theta 物镜的系统配置都能用」[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)

**✅ 一手（SCANLAB 老款 varioSCAN 原理，更明确）**：「扫描过程中，varioSCAN 内的**发散光学元件**相对于**固定聚焦光学元件**沿光轴高动态定位，产生整个系统**总焦距的变化**，并与振镜运动同步」[来源](https://pdf.directindustry.com/pdf/scanlab-gmbh/varioscan-20-varioscan-40-varioscan-40flex/39164-169746.html)（🟡 DirectIndustry 转载的 SCANLAB 手册）

**✅ 一手（RAYLASE 原理原文）**：「在预聚焦偏转单元中，激光束先进入一个**移动镜头——Linear-Translator-Module**。移动镜头使光束迅速发散，随后通过一片或两片聚焦镜。**预聚焦单元的焦点补偿是通过在振镜把光束扫过工作场时，微调移动镜头与聚焦镜之间的距离来实现的，由第三个移动 Z 轴完成**」[来源](https://www.raylase.de/en/products/prefocusing-deflection-units.html)

**✅ 一手（FOCUSSHIFTER RD-14 原理）**：「它在 f-θ 镜头与偏转单元的组合上**增加了一套可调镜组（adjustable lens system）**，允许动态设定焦点的 z 位置。因此**逐层加工（2.5D）与空间加工（3D）都成为可能**」[来源](https://www.raylase.de/_Resources/Persistent/5/1/8/9/5189d9ad9239901c83aa37b1738071904ed74596/2026-03-16_Datenblatt_FOCUSSHIFTER%20RD-14_EN_v2.0.pdf)

**关键架构差异（✅ 一手）**：RAYLASE AXIALSCAN RD-14「与 F-Theta 方案不同，**激光在扫描振镜之前就被聚焦**，因此**偏转角可以被完全利用**，从而实现更大的加工场」[来源](https://www.raylase.de/en/products/prefocusing-deflection-units.html)。这正是「预聚焦架构 + 内置 Z 轴」与「场镜架构 + 外挂 z-shifter」的分野。

### (b) 扫描头内部的 Z 轴（一体式 3 轴头）

**✅ 一手**：Novanta LIGHTNING II 把 **DFM 做进扫描头内部**（模块化 z 轴一体式设计），「DFM 确保光斑在整个工作场保持聚焦」[来源](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf)
**✅ 一手**：SCANLAB excelliSHIFT 是外挂式但**基于振镜（galvanometer）技术**的 Z 轴，**只用反射光学元件**（无透射元件）→ 不同波长无色散、热透镜效应小[来源](https://www.scanlab.de/sites/default/files/2025-06/SCANLAB-excelliSHIFT-EN.pdf)

### (c) 路线对比小结

| 维度 | 外挂 z-shifter（varioSCAN / FOCUSSHIFTER DIGITAL II / excelliSHIFT） | 一体式 3 轴头（LIGHTNING II DFM） | 预聚焦单元（AXIALSCAN / FOCUSSHIFTER RD-14） |
|---|---|---|---|
| Z 轴位置 | 加在扫描头之外（场镜前） | 扫描头内部 | 振镜之前，与偏转单元一体 |
| 场镜 | 需要（FT 型）或不需要（PR 型） | 需要 | 可不要（PR 型），或配 f-θ / 远心镜 |
| 幅面能力 | 受场镜限制 | 受场镜限制 | **可达 600×600 乃至 2000×2000 mm²** |
| 升级现有设备 | 容易（模块化加装） | 需整头更换 | 需整单元更换 |

---

## 3. 关键指标与厂商参数表

### 3.1 SCANLAB excelliSHIFT —— ✅ 一手

| 指标 | 数值 |
|---|---|
| 孔径 Aperture | **14 mm** |
| 波长 | 515–532 nm、1030–1070 nm（其他波长可定制） |
| 光束扩束 | 1 倍 |
| **聚焦行程 Focus range / Focus stroke** | **±14 mm** |
| **聚焦速度（像场内）** | **最高 30 m/s**（配 f-θ 场镜 f=160 mm；更长焦距时更高） |
| **跟踪误差 Tracking error** | **0.1 ms** |
| 光束引导 | **反射式**（无透射元件） |
| 激光功率（带冷却） | 120 W（绿光）/ 200 W（红外） |
| 尺寸 / 重量 | 115 × 160 × 142 mm³ / 3.7 kg |
| 接口 | SL2-100、POWER IN |

[来源](https://www.scanlab.de/sites/default/files/2025-06/SCANLAB-excelliSHIFT-EN.pdf)；「Focus stroke: ±14 mm」另见 [PDF 目录页镜像](https://pdf.directindustry.com/pdf/scanlab-gmbh/excellishift/39164-992718.html)
**✅ 一手（官方页补充）**：「Z 扫描器不再是限制因素，因此**三个空间方向可以达到相同的加速度**」「仅使用反射光学元件，允许使用不同波长而无色散，并在高功率应用中减少热透镜效应」[来源](https://www.scanlab.de/en/products/z-axes-3d-add-ons/excellishift)

### 3.2 SCANLAB varioSCAN II / varioSCANde II —— ✅ 一手

**动态与电机**（手册明确：「以下规格仅针对电机本身，其对加工场/体积内实际光束定位的影响取决于具体光学配置」）

| 指标 | varioSCANde II 20i | varioSCANde II 40i (FLEX) |
|---|---|---|
| **跟踪误差** | **0.55 ms** | **0.70 ms** |
| **移动镜最大行程** | **±2 mm** | **±3 mm** |
| **移动镜典型速度** | **≤ 280 mm/s** | **≤ 140 mm/s** |
| **长期漂移（>8 h）** | **< 3 µm** | **< 3 µm** |
| **重复精度 Repeatability** | **< 0.5 µm** | **< 0.5 µm** |
| 共光路孔径 | 4–7 mm | 8–18 mm |
| 典型出射光束直径 | ≤ 20 mm | ≤ 40 mm |
| 扩束系数 | **2–5** | **1.4–3.8**（FLEX 2–2.5） |
| 最大连续功率 | 75 W(UV)/150 W(绿)/250 W(IR)/250 W(CO₂) | 1000 W(绿)/3000 W(IR)/2000 W(CO₂) |
| 重量 | 0.5–0.7 kg | ≈2.4 kg（FLEX ≈4.4 kg） |
| 接口 | **SL2-100、XY2-100 Enhanced** | **SL2-100、XY2-100 Enhanced** |

[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)

**整机配置示例（同页表格，含场镜 f 与聚焦行程的对应关系）**：

| 应用 | 激光打标 | 微加工 | 增材制造 | 纺织加工 |
|---|---|---|---|---|
| 典型扫描头孔径 | 10 mm | 14 mm | 30 mm | 30 mm |
| varioSCAN II 型号 | 20-20 FT | 20-133 FT | 40-116 PR | 40-89-PR (FLEX) |
| 孔径直径 | 5 mm | 7 mm | 16 mm | 16 mm |
| 扩束系数 | 2.8 | 2.0 | 2.0 | 2.0–2.5 |
| **物镜焦距 FT / 预聚焦后焦距 PR** | **f = 163 mm** | **f = 100 mm** | **PR 850 mm** | **PR 370–2015 mm** |
| **方形像场边长** | **95 mm** | **50 mm** | **500 mm** | **180–1400 mm** |
| **聚焦偏移 Focus shift** | **17.1 mm** | **2.2 mm** | **23.5 mm** | **11 – 600 mm** |
| **聚焦偏移（varioSCANde II）** | **±32 mm** | **±4 mm** | **±20 mm** | **±0 … ±300 mm** |
| 平均每次镜头行程的聚焦偏移 | 表头独立列项（原文 "Average focus shift per lens travel"） | ← | ← | ← |

⚠️ 最后一行的具体数值在 PDF 文本抽取中呈乱码，**未采信**；但可确认厂商把「**平均每次镜头行程的聚焦偏移**」作为**独立规格项**列出，说明该增益是选型核心参数。
[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)

**⚠️ 我的算术（聚焦增益 = 聚焦偏移 / 移动镜行程）**：

| 配置 | 场镜 f | 移动镜行程 | 聚焦偏移 | 增益 |
|---|---|---|---|---|
| 20i / 20-20 FT | 163 mm | ±2 mm | ±32 mm | **16.0×** |
| 20i / 20-133 FT | 100 mm | ±2 mm | ±4 mm | **2.0×** |
| 40i / 40-116 PR | PR 850 mm | ±3 mm | ±20 mm | **6.7×** |

→ **同一个 Z 轴电机，配不同光学配置时聚焦行程可差 8 倍**，选型必须按「整机配置」而非「电机行程」看。

**✅ 一手**：varioSCANde i「配备**数字线性编码器**」「最大行程是常规 varioSCAN 的**两倍**，跟踪误差**低得多**，聚焦偏移范围更大、光斑质量更好；精度、速度、分辨率与线性度也明显优于所有其他 varioSCAN，并大幅消除漂移影响」[来源](https://pdf.directindustry.com/pdf/scanlab-gmbh/3d-focusing-systems-varioscan-varioscande/39164-260795.html)（🟡 二手镜像）
**✅ 一手（iDRIVE 实时回读）**：「数字式 varioSCANde II 系统采用 iDRIVE 技术，**可实时回读实际位置**及其他状态」[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)
**✅ 一手（FLEX 的能力边界）**：「varioSCANFLEX 另外允许**连续调节幅面尺寸、工作距离与光斑尺寸**」；同时「**最大幅面尺寸配最小光斑**」（maximum image field size is achieved with the minimum spot size）—— 即幅面与光斑是**互斥权衡**[来源](https://pdf.directindustry.com/pdf/scanlab-gmbh/varioscan-20-varioscan-40-varioscan-40flex/39164-169746.html)

### 3.3 RAYLASE FOCUSSHIFTER RD-14（2026 v2.0，**当前主力型号**）—— ✅ 一手

| 指标 | FOCUSSHIFTER RD-14 SI | FOCUSSHIFTER RD-14 QU |
|---|---|---|
| 调谐 Tuning | MA / VC | MA / C |
| 写入速度（高/良 书写质量） | 650 / 800 cps（MA） | — |
| 加工速度 | 30 rad/s（MA）/ 50（VC） | 30（MA）/ 100（C） |
| 定位速度 | 90（MA）/ 50（VC） | 90（MA）/ 100（C） |
| 跟踪误差（偏转） | 0.16（MA）/ 0.20（VC）ms | 0.17（MA）/ 0.30（C）ms |
| 加速时间（近似） | 0.30 / 0.46 ms | 0.30 / 0.60 ms |
| 阶跃响应（1% 满量程） | 0.36 / 0.68 ms | 0.39 / 0.69 ms |
| **跟踪误差（聚焦单元）** | **0.9 ms** | **0.9 ms** |
| **移动镜速度（聚焦）** | **900 mm/s** | **900 mm/s** |

注：写入速度按 f-θ 镜头 f=163 mm、加工场 120×120 mm² 计；速度换算「加工场速度 = 场镜焦距 × 加工速度」，例：f=163 mm、MA 调谐 30 rad/s → v = 163/1000 × 30 = **4.8 m/s**。[来源](https://www.raylase.de/_Resources/Persistent/5/1/8/9/5189d9ad9239901c83aa37b1738071904ed74596/2026-03-16_Datenblatt_FOCUSSHIFTER%20RD-14_EN_v2.0.pdf)

**通用规格**

| 指标 | 数值 |
|---|---|
| 供电 | **+48 V**；4 A RMS，最大 8 A；纹波 ≤300 mVpp @20 MHz |
| 环境温度 | +15 … +35 °C |
| **分辨率 XY2-100 Enhanced（16 bit）** | **12 µrad** |
| **分辨率 RL3-100 / SL2-100（20 bit）** | **0.76 µrad** |
| 典型偏转（光学） | ±0.393 rad |
| 重复精度 RMS | < 2.0 µrad |
| 定位噪声 RMS | < 4.5 µrad |
| 增益漂移 / 偏置漂移 | ≤15 ppm/K / ≤10 µrad/K |
| **长期漂移 8 h** | **< 60 µrad** |
| 防护等级 | **IP64** |
| 限制输入孔径 / 最佳入射光束（全光束 / 1/e²） | **5.0 mm** / 4.7 mm / 3.1 mm |
| 光束位移 | 17.0 mm |
| 重量（不含场镜）/ 尺寸 | 5.5 kg / 330 × 105 × 134 mm |

[来源](https://www.raylase.de/_Resources/Persistent/5/1/8/9/5189d9ad9239901c83aa37b1738071904ed74596/2026-03-16_Datenblatt_FOCUSSHIFTER%20RD-14_EN_v2.0.pdf)

**配置举例（spot 与自由焦程随波长的关系 —— 这是最有价值的一张表）**

| 波长 | 355 nm | 532 nm | 1064 / 1070 nm |
|---|---|---|---|
| EFL 163 mm：**光斑 1/e²** | **8.7 µm** | **13.0 µm** | **26.1 µm** |
| EFL 163 mm：**自由焦程 Free focus range** | **−16.0 … +14.0 mm** | **−16.0 … +14.0 mm** | **−16.0 … +14.0 mm** |
| EFL 254 mm：**光斑 1/e²** | **13.6 µm** | **20.3 µm** | **40.7 µm** |
| EFL 254 mm：**自由焦程** | **−41.0 … +32.0 mm** | **−41.0 … +32.0 mm** | **−41.0 … +32.0 mm** |

（光束质量 M² = 1；最大允许功率：355 nm→100 W、532 nm→200 W、1064 nm→300 W、1070 nm→1000 W）
**→ 极重要工程事实：同一台 Z 轴，换 f=163 mm 场镜时自由焦程约 30 mm，换 f=254 mm 场镜时约 73 mm（焦程约 2.4 倍），但光斑也从 26.1 µm 放大到 40.7 µm。焦程与光斑、幅面是同一组权衡。**
[来源](https://www.raylase.de/_Resources/Persistent/5/1/8/9/5189d9ad9239901c83aa37b1738071904ed74596/2026-03-16_Datenblatt_FOCUSSHIFTER%20RD-14_EN_v2.0.pdf)

**✅ 一手（RAYVOLUTION DRIVE 的定性）**：「感谢 **RAYVOLUTION DRIVE 技术**，它能在加工过程中**实时调整焦点**。这确保激光始终在正确深度保持最优聚焦」「**确保 z 位置与穿透深度不受加工速度影响**」[来源](https://www.raylase.de/_Resources/Persistent/5/1/8/9/5189d9ad9239901c83aa37b1738071904ed74596/2026-03-16_Datenblatt_FOCUSSHIFTER%20RD-14_EN_v2.0.pdf)、[来源](https://www.raylase.de/en/products/focusshifter/focusshifter-rd-14.html)
**✅ 一手（接口与回读）**：「数字控制，支持 **XY2-100 或 SL2-100** 协议 —— 实现高精度控制，并**额外反馈位置与状态信号**用于过程监控与优化」[来源](https://www.raylase.de/_Resources/Persistent/5/1/8/9/5189d9ad9239901c83aa37b1738071904ed74596/2026-03-16_Datenblatt_FOCUSSHIFTER%20RD-14_EN_v2.0.pdf)
**❌ 未找到**：**RAYVOLUTION DRIVE 的行程/速度/精度独立规格数字**（该技术本身无独立数据手册；`/en/products/rayvolution-drive.html` 返回 **HTTP 404**）。只能通过搭载它的 FOCUSSHIFTER RD-14 指标间接获得（0.9 ms 跟踪误差、900 mm/s 移动镜速度）。
**⚠️ 型号代差提醒**：RAYLASE 现有**两代同名产品**，参数差异显著，引用时必须注明：

| | FOCUSSHIFTER DIGITAL II（v1.8，2021-07） | FOCUSSHIFTER RD-14（v2.0，2026-03） |
|---|---|---|
| 移动镜行程 / 速度 | **11 mm / 880 mm/s** | 未单列行程；速度 **900 mm/s** |
| 聚焦单元跟踪误差 | **1.3 ms** | **0.9 ms** |
| 自由焦程（f=160/163） | ±9 … ±19 mm（随型号） | **−16.0 … +14.0 mm** |
| 分辨率标注 | XY2-100-E **12 µrad** / SL2-100 **0.76 µrad** | XY2-100-E **12 µrad** / **RL3-100 或 SL2-100 0.76 µrad** |
| 防护 / 重量 | IP54 / ≈5.3 kg | **IP64** / 5.5 kg |
| 供电 | +30 V 或 +48 V | **+48 V** |

（DIGITAL II 来源 [此处](https://www.raylase.de/_Resources/Persistent/5/b/9/0/5b9058dcb0c4f361859551b86d9c55d6d35478d1/RAYLASE%20FOCUSSHIFTER%20DIGITAL%20II_en.pdf)）

### 3.4 Novanta（Cambridge Technology）LIGHTNING II 3 轴扫描头 + DFM —— ✅ 一手

| 指标 | 20 mm 孔径型 | 30 mm 孔径型 | 50 mm 孔径型 |
|---|---|---|---|
| 扫描角 | ±20° | ±22° | ±22° |
| 典型加工速度 | 50 rad/s | 50 rad/s | 18 rad/s |
| 场尺寸范围 | 200–2500 mm | 100–1200 mm | 100–1200 mm |
| **跟踪延迟 Tracking Delay** | **0.2 ms** | **0.2 ms** | **0.4 ms** |
| **指令分辨率 Command Resolution** | **24-bit** | **24-bit** | **24-bit** |
| 重复精度 | <2 µrad | <2 µrad | <2 µrad |
| 长期漂移（8 h） | <10 µrad | <10 µrad | <10 µrad |
| 热漂移 | <2 µrad/°C | <2 µrad/°C | <2 µrad/°C |

按波长的**跟踪误差**：CO₂ / 光纤 / UV 各表均为 **0.2 ms（30 mm 孔径）/ 0.4 ms（50 mm 孔径）**。[来源](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf)
**❌ 未找到**：LIGHTNING II 的 **DFM Z 轴行程（±mm）、Z 轴速度、Z 轴重复精度**在任何公开数据手册中均未列出（数据手册只给扫描头整体指标）。厂商页面同样只描述「DFM 提供动态焦点控制」[来源](https://novanta.com/precision-manufacturing/product/lightning-ii-3-axis-scan-head/)。

### 3.5 横向对比总表（含口径差异提醒）

| 方案 | 类型 | 聚焦行程 | 速度 / 重复精度 | 跟踪误差 | 分辨率 |
|---|---|---|---|---|---|
| SCANLAB excelliSHIFT | 外挂，反射式，振镜技术 | **±14 mm** | 像场内 **30 m/s** | **0.1 ms** | 未公布 |
| SCANLAB varioSCANde II 20i | 外挂，透射式 | **±32 mm**（配 f=163） | 移动镜 **≤280 mm/s**，重复 **<0.5 µm**，漂移 <3 µm/8h | **0.55 ms** | 未公布 |
| SCANLAB varioSCANde II 40i | 外挂，预聚焦 | **±20 mm**（配 PR 850） | 移动镜 **≤140 mm/s**，重复 **<0.5 µm**，漂移 <3 µm/8h | **0.70 ms** | 未公布 |
| RAYLASE FOCUSSHIFTER RD-14 | 一体式 3D 偏转单元 | **−16…+14 mm**（f=163）/ **−41…+32 mm**（f=254） | 移动镜 **900 mm/s** | **0.9 ms** | **16 bit = 12 µrad / 20 bit = 0.76 µrad** |
| RAYLASE FOCUSSHIFTER DIGITAL II | 一体式 3 轴偏转单元 | **±9 … ±19 mm** | 镜头行程 **11 mm**，聚焦镜 **880 mm/s** | **1.3 ms** | **16 bit = 12 µrad / 20 bit = 0.76 µrad** |
| Novanta LIGHTNING II DFM | 一体式 3 轴头 | ❌ 未公布 | ❌ 未公布 | **0.2 / 0.4 ms**（头整体） | **24-bit** |

**⚠️ 口径警告**：「跟踪误差 0.1 ms vs 1.3 ms」不是同一物理量的严格对比 —— SCANLAB 与 RAYLASE 都把它作为**跟随误差时间常数（servo lag / drag）**给出，**乘以扫描速度才是位置误差**。
**⚠️ 我的算术**：
- RAYLASE DIGITAL II：880 mm/s × 1.3 ms ≈ **1.14 mm** 滞后
- RAYLASE RD-14：900 mm/s × 0.9 ms ≈ **0.81 mm** 滞后
- excelliSHIFT：30 m/s × 0.1 ms = **3.0 mm** 滞后
→ **高速扫描时 Z 滞后可达毫米级，这是必须做延迟补偿的定量理由。**（速度换算依据：RAYLASE 手册「加工场速度 = 场镜焦距 × 定位速度」[来源](https://www.raylase.de/_Resources/Persistent/5/b/9/0/5b9058dcb0c4f361859551b86d9c55d6d35478d1/RAYLASE%20FOCUSSHIFTER%20DIGITAL%20II_en.pdf)）

---

## 4. 焦距变化对光斑的影响 /「in-focus zoom」

**✅ 一手（光斑尺寸公式）**：
- Thorlabs：$\text{Spot Size}=\dfrac{C\,\lambda f}{A}$，Spot Size 为 1/e² 直径，λ 波长，f 有效焦距，A 入射光束直径，**C = 1.83**（高斯光束在 1/e² 直径处截断时）[来源](https://www.govolition.com/product/V40-FTH160-1064)
- SCANLAB SCANpedia：$d = M^2 \cdot k(A,D)\cdot \dfrac{\lambda f}{D}$，**k 理想值 1.27，典型 1.5–2.0**（🟡 该页抓取时返回 404，数值来自次级引用，**建议复核**）
- 场尺寸：$L = f\cdot\theta$（L 为方形场对角线/边长，θ 为弧度）[来源](https://www.govolition.com/product/V40-FTH160-1064)
- RP Photonics：「**焦距与输入光束半径共同决定靶面光束半径：输入光束越大，光斑越小**」[来源](https://www.rp-photonics.com/scanning_lenses.html)

**⚠️ 我的推导（基于上面的一手公式 $d\propto f\lambda/A$）**：移动镜组改变系统焦距时：
- 若 **A 不变** → **光斑直径随 f 线性变化**；
- 若让 **A/f 保持恒定**（同步改变扩束比）→ **光斑直径不变**，这就是「in-focus zoom / 光学变焦」。
**⚠️ 我的算术校验**：C=1.83、λ=1064 nm、A=12 mm → f=100 得 16.2 µm（Thorlabs 规格 16 µm）、f=160 得 26.0 µm（规格 26 µm）、f=254/A=20 mm 得 24.7 µm（规格 25 µm）—— **完全吻合，公式可用**。

**✅ 一手（RAYLASE 明确区分「散焦放大」与「变焦放大」—— 本题最关键的厂商原文）**：
- **散焦放大（defocus）**：「最简单的动态放大光斑直径的方法是**把焦点移到加工面下方**（通过 Z 轴）。这会导致粉末中光斑直径增大。……但这导致**焦点外光束形状定义不良**，离焦光斑**不再保持原有能量分布，而是变得模糊**」。对单模激光束轮廓仍「类高斯」，但对**平顶或环形（ring mode）轮廓，光束形状直接丢失**。且「光斑内的功率分布强烈依赖离焦量，必须**对每个放大倍率实验测定**分布并专门开发工艺参数」[来源](https://www.raylase.de/en/applications/additive-manufacturing/in-focus-spot-magnificantion-in-additive-manufacturing.html)
- **光学变焦（zoom）**：「连续放大无法用标准偏转单元实现，**需要光路中额外的可动望远镜（telescope）**……因为**焦点处最小光斑直径也随光束直径变化**，这样的变焦光学让你**在不离开焦平面的前提下连续调整焦点直径**。这样原始光束轮廓仍被清晰成像，对平顶和环形这类特殊光束形状尤其重要」[来源](https://www.raylase.de/en/applications/additive-manufacturing/in-focus-spot-magnificantion-in-additive-manufacturing.html)
- **变焦的物理限制**：「放大倍率的限制因素包括光路中的**自由孔径**、偏转单元内的**可用空间**，以及反射镜与光学元件的**功率兼容性**」[来源](https://www.raylase.de/en/applications/additive-manufacturing/in-focus-spot-magnificantion-in-additive-manufacturing.html)

**⚠️ 重要概念澄清（我的归纳）**：所谓「保持光斑不变」有两种截然不同的诉求，**不要混为一谈**：
1. **Z 轴升降但光斑不变**（真正的 z-shifter 设计目标）：只改变入射到场镜的光束**发散度/波前曲率**，使焦点沿轴移动，而**场镜孔径上的光束直径 A 基本不变** → 光斑尺寸基本不变，f-θ 标定 $y=f\theta$ 也不变 → **场尺寸不变**。这正是 varioSCAN 型「移动发散镜 + 固定聚焦镜」架构的巧妙之处（原理见 [SCANLAB 手册](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)）。
2. **变焦放大但焦点不离面**（in-focus zoom）：同时改变 A 与 f 的比例，光斑直径改变但焦点始终在焦面上，需**额外的可动望远镜**（RAYLASE 原文）。

**⚠️ 若 Z 轴真的改变系统焦距 → 场尺寸随 f 缩放**：SCANLAB 把这类能力命名为 **varioSCAN II FLEX「可变调整像场尺寸与工作距离」**[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)，RAYLASE 也把「**改变工作距离、场和光斑尺寸**」列为预聚焦单元的能力[来源](https://www.raylase.de/en/products/prefocusing-deflection-units.html)。**这与「只移动焦点、场尺寸不变」是互斥的两种使用模式。** SCANLAB 更直接点明权衡：「**最大幅面尺寸配最小光斑**」[来源](https://pdf.directindustry.com/pdf/scanlab-gmbh/varioscan-20-varioscan-40-varioscan-40flex/39164-169746.html)。
**⚠️ 我的算术（耦合后果）**：f 从 160 → 100 mm 而 A 不变时，光斑 ×0.625、同角度幅面也 ×0.625（110.6 mm → 69.1 mm）；**要维持原光斑，A 必须缩到 12×100/160 = 7.5 mm。**

---

## 5. 驱动方式对比

**✅ 一手（厂商对自家执行机构的定性）**：

| 方案 | 执行机构 | 来源原文 |
|---|---|---|
| SCANLAB varioSCAN / 40FLEX | **高性能无倾斜直线电机（tilt-free linear motor）** | 「使用高性能、无倾斜的直线电机沿光轴快速精确移动激光焦点」[来源](https://pdf.directindustry.com/pdf/scanlab-gmbh/varioscan-20-varioscan-40-varioscan-40flex/39164-169746.html)（🟡 二手镜像） |
| SCANLAB varioSCAN II | **电机块（Motor block）** 驱动 moving optics | 结构图「Water-cooled entrance aperture / Motor block / Moving optics / Fixed optics」[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf) |
| SCANLAB varioSCANde i | **数字线性编码器（digital linear encoder）** | 「配备数字线性编码器」，支持实时查询实际位置[来源](https://pdf.directindustry.com/pdf/scanlab-gmbh/3d-focusing-systems-varioscan-varioscande/39164-260795.html)（🟡） |
| SCANLAB excelliSHIFT | **振镜（galvanometer）技术** | 「基于久经验证的振镜技术，全新设计大幅提升动态性能」[来源](https://www.scanlab.de/sites/default/files/2025-06/SCANLAB-excelliSHIFT-EN.pdf) |
| RAYLASE FOCUSSHIFTER | **Linear Translator Module（直线平移模块）** + 数字 PWM 输出级 | 「数字化控制高速 Z 轴」「数字 PWM 输出级大幅降低功率损耗与热发展」[来源](https://www.raylase.de/_Resources/Persistent/5/b/9/0/5b9058dcb0c4f361859551b86d9c55d6d35478d1/RAYLASE%20FOCUSSHIFTER%20DIGITAL%20II_en.pdf) |
| Novanta LIGHTNING II DFM | 未公开具体执行器类型（仅称 Dynamic Focusing Module） | [来源](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf) |

**🟡 二手（驱动方式的通用对比，各执行器族的行程/响应量级）**：

| 驱动 | 典型行程 | 响应 / 带宽 | 备注 |
|---|---|---|---|
| 压电堆栈（piezo stack） | **100 µm 级** | **微秒级** | 厂商原文：「在 100 µm 行程上提供纳米级分辨率，**微秒级响应时间**，封装非常紧凑」[来源](https://www.newport.com/p/NPA100)（✅ 一手，但为显微/纳米定位器件，非扫描头） |
| 压电（放大式/电机式） | 亚毫米～毫米 | 高刚度、高带宽 | 力/带宽/热负载对比[来源](https://thepiezodesk.com/technology/piezo-vs-voice-coil)（🟡） |
| 音圈（voice coil） | **数十 µm ～ 数 mm** | 高带宽、力中等 | [来源](https://xeryon.com/voice-coil-actuators-vs-linear-motor-vs-ultrasonic-piezo-actuators/)（🟡）；「行程从零点几毫米起…常选直驱：直线电机、压电电机或音圈」[来源](https://www.linearmotiontips.com/piezo-motors-voice-coil-actuators-micron-and-sub-micron-positioning/)（🟡） |
| 直线电机 | **数 mm ～ 数百 mm** | 高加速度、大力 | 「直线电机平台通常用于需要大力、行程超过几百毫米的场合」[来源](https://www.linearmotiontips.com/piezo-motors-voice-coil-actuators-micron-and-sub-micron-positioning/)（🟡） |
| 步进 | 大行程 | 慢、有离散步距 | ❌ **未找到**用于扫描头 Z 轴动态聚焦的公开实例 |

**⚠️ 与真实产品的对应关系（我的判断）**：
- **压电**行程太短（100 µm 级），**不适用于扫描头 Z 轴的 ±mm～±16 mm 级行程** —— ❌ 未找到任何扫描头厂商用压电堆栈做 Z 轴的公开证据。
- **音圈**是扫描头 Z 轴的常见选择（🟡 行业文章：「动态聚焦系统把高速**音圈或压电驱动**的光学元件置于 X-Y 振镜前」[来源](https://www.meenjet.net/news/laser-marking-curved-surfaces-dynamic-focal-depth.html)）—— ⚠️ 注意这是二手来源，与「厂商一手证据指向直线电机/振镜技术」**存在张力**，建议以厂商数据手册为准。
- **直线电机**是 SCANLAB varioSCAN 明确采用的方案（✅ 见上表）。
- **振镜技术**被 excelliSHIFT 明确采用（✅）。
- 有限行程 + mm 级精度 + 高速，三者共同把选择收敛到「无铁芯直线电机 / 音圈 / 振镜电机」这类直驱方案。

---

## 6. 控制与标定

### 6.1 Z 轴与 XY 同步 / 延迟补偿

**✅ 一手（3D 标定的官方工具）**：SCANLAB **laserDESK 3D Calibration Wizard** —— 「一个**对话驱动的工具，极大简化了原本高度复杂的 3 轴扫描系统标定**。智能助手引导用户完成整个复杂标定流程，最终**为整个系统生成个性化的 3D 校正文件（.ct5）**」，兼容 RTC5/RTC6 控制卡[来源](https://www.scanlab.de/en/products/calibration/hardware-configuration-and-control)
**✅ 一手**：RTC 校正文件用于「**补偿两镜扫描系统及其光学系统固有的像场畸变，确保在平面或工作体积内精确扫描**」[来源](https://www.scanlab.de/sites/default/files/2020-08/CalibrationSolutions.pdf)

**✅ 一手（标定精度分级，SCANLAB 官方，f=163 mm 典型值）**：

| 方案 | 工具 | 精度 | 工作量 |
|---|---|---|---|
| RTC 校正文件（标准） | 出厂预计算 *ctb/*ct5 | **< 150 µm** | 低 |
| CALsheet | 智能手机 / 数码相机 | **< 50 µm** | 中 |
| CALsheet | 平板扫描仪 | **< 30 µm** | 中 |
| correXion pro | 三坐标测量机（CMM） | **< 20 µm** | 高 |

[来源](https://www.scanlab.de/sites/default/files/2020-08/CalibrationSolutions.pdf)

**✅ 一手（correXion pro 定位）**：「额外的 correXion pro 标定用于**最小化个体制造公差与非线性**」[来源](https://www.scanlab.de/en/products/calibration/correxion-pro)

**✅ 一手（滞后补偿的厂商功能名）**：SCANLAB 控制/工艺控制页列出 **Sky Writing**（含「前导运动缩放的 sky writing」）、**SCANahead**、**SCAN motionControl**（「在存在 **drag delay** 的系统中通过优化轨迹实现生产率与质量」）[来源](https://www.scanlab.de/en/regulation-and-process-control)
**✅ 一手**：excelliSHIFT「现在还提供带 **SCANahead** 技术的版本」[来源](https://www.scanlab.de/sites/default/files/2025-06/SCANLAB-excelliSHIFT-EN.pdf)
**✅ 一手（RAYLASE 侧的同步机制）**：SP-ICE 3「**允许偏转单元、激光与外设的同步控制**，以及扫描器与传感器信号的**组合回读**」；FOCUSSHIFTER RD-14 数据手册把 SP-ICE 3 列为「**带反馈功能的控制卡**」[来源](https://www.raylase.de/_Resources/Persistent/5/1/8/9/5189d9ad9239901c83aa37b1738071904ed74596/2026-03-16_Datenblatt_FOCUSSHIFTER%20RD-14_EN_v2.0.pdf)、[来源](https://www.raylase.de/en/products/electronics-control-cards/sp-ice-3.html)
**✅ 一手（Z 稳定性的关键设计目标）**：FOCUSSHIFTER RD-14 把 RAYVOLUTION DRIVE 的卖点写成「**确保 z 位置与穿透深度不受加工速度影响**」—— 这句话本身就是「必须做 Z 延迟补偿」的厂商侧确认[来源](https://www.raylase.de/_Resources/Persistent/5/1/8/9/5189d9ad9239901c83aa37b1738071904ed74596/2026-03-16_Datenblatt_FOCUSSHIFTER%20RD-14_EN_v2.0.pdf)
**❌ 未找到**：SCANLAB / RAYLASE 公开文档中 Z 轴的**具体延迟补偿算法或参数**（如 z 前导量的计算公式）。RTC6 手册 PDF 在本环境多次抓取超时，未能读到命令级细节。

**⭐⭐ 以下为本次调研关于延迟补偿的「一手硬数字」（价值最高）**：

**(1) ✅ 一手：协议层不存在独立的 Z 时间戳队列。** RAYLASE 的 XY2-100-E 厂商文档把帧类型直接写作 `16Bit command position frame (X+, Y+, Z+ to deflection unit)` 与 18Bit 版本，正文写「**a 16- or 18-Bit target position is sent in each frame to each axis of the deflection unit**」。→ **Z 与 X/Y 同帧、同字长、同刷新率**，传输层不给 Z 任何额外延迟。[来源](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)
**(2) ✅ 一手：SP-ICE-3 固件所有矢量处理函数默认按 3D（XYZ）处理**，2D 函数等价于 Z=0；且「**Z 坐标可以在单条矢量加工过程中变化**」[来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/254aa48e-536e-4bbe-a569-fe200cc6a2ac.htm)
**(3) ✅ 一手：补偿总公式** —— **总定位延迟 = 传输延迟 + 跟踪误差（Lag）**；`LaserOnDelay` / `LaserOffDelay` 必须按该**总和**设置。其中 **TD_TX = T_K(13 µs) + T_C(20 µs) + T_Int，T_Int=0 时 = 14 µs**；**TD_RX = 36 µs（常数）**。可用 Enhanced Protocol 原始命令 **0x0556 / 0x0557** 读回[来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/7a6d305c-a5d1-4dfb-a1d2-3afc1768b87f.htm)
**(4) ✅ 一手：逐轴补偿的厂商证据** —— SP-ICE-3 数据表列出 **"Tracking Error compensation for all axes individually"**；`TrackingError` 是 **AxisParameterSet 的逐轴属性**[来源](https://www.raylase.de/en/products/electronics-control-cards/sp-ice-3.html)
**(5) ✅ 一手：SCANLAB 侧的对应物是「SCANahead 的 preview time t_p」，不是 "look-ahead"** —— RTC6 经 SL2-100 @100 kHz 下发 microvector，激光控制 64 MHz；SCANahead 使 **t_s = 0**，**excelliSCAN 实测 Tracking error = 0 ms**[来源](https://www.scanlab.de/sites/default/files/2024-11/scanahead_en_0.pdf)
**(6) ⚠️ 我的算术（为什么单一全局延迟不够）**：Z 的跟踪误差（**0.55 / 0.70 / 0.1 / 1.3 / 0.2–0.4 ms**）比同型 XY 振镜（**0.10–0.30 ms**）**大 2–13 倍**，excelliSCAN + SCANahead 更是 **0 ms**。→ **单一全局激光延迟无法同时对齐 XY 与 Z**，必须逐轴补偿。
**❌ 未找到**：SCANLAB / RAYLASE 均**未公开**「Z 字提前 N 个 microvector」的一手描述。
**⚠️ 引用纪律提醒**：`set_focus` / `set_z` / `z_offset` 这些 RTC 命令名在公开文档中**不存在**；「look-ahead」也不是 SCANLAB 的功能名。**不要把 RAYLASE 侧的真实对应物（`FieldTransform` 的 Z 分量 / FC3 的 `FieldOffset.Z`）与虚构的 RTC 命令名混用。**

### 6.2 分辨率不足（如 RTC4 只有 16 bit）的后果

**✅ 一手（RTC4 / RTC5 的位深与分辨率对比原文）**：
- RTC4：「每 **10 µs** 发送一次 **16-bit** 控制信号，执行微矢量化与像场校正」[来源](https://pdf.directindustry.com/pdf/scanlab-gmbh/rtc4/39164-694240.html)（🟡 二手镜像）；RTC4 规格页：「XY2-100 **enhanced** 协议，**16-bit 定位分辨率**，**10 µs 输出周期**」[来源](http://www.ainnotech.com/ainnotech/pdf/02/1_3/3SCAN-RTC4-Control%20And%20Versatility.pdf)（🟡 经销商镜像）
- RTC5：「通过新的 **SL2-100** 数据传输协议与扫描系统通信。该协议支持 **20-bit 控制信号**，因此与 RTC4 前代板相比**定位分辨率提高 16 倍**」[来源](https://www.scanlab.de/sites/default/files/2020-08/13_RTC5_control%20boards.pdf)（✅ 一手）
- SL2-100 由 SCANLAB 开发并推出，RTC5/RTC6 支持[来源](https://www.scanlab.de/en/applications/micromachining)（✅ 一手）
- Novanta 侧用 **24-bit** 指令分辨率[来源](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf)（✅ 一手）

**⚠️ 我的算术（位深 → LSB 尺寸，按不同聚焦行程）**：

| 位深 | 全行程 22 mm | 全行程 28 mm | 全行程 38 mm | 全行程 64 mm |
|---|---|---|---|---|
| **16 bit** | 0.336 µm | **0.427 µm** | 0.580 µm | **0.98 µm** |
| 18 bit | 0.084 µm | 0.107 µm | 0.145 µm | 0.244 µm |
| 20 bit | 0.021 µm | 0.027 µm | 0.036 µm | **0.061 µm** |
| 24 bit | 0.0013 µm | 0.0017 µm | 0.0023 µm | 0.0038 µm |

（算式：LSB = 全行程 / 2^bits；如 28 mm / 65536 = 0.427 µm，64 mm / 65536 = 0.98 µm）

**后果归纳（我的分析，非单一来源）**：
1. **量化台阶**：16 bit 在 ±14 mm 行程上每级约 0.43 µm。单看这个数字**远小于景深**（30 µm 光斑 DOF ≈ ±0.66 mm），**所以「16 bit 根本不足以定位焦点」这个说法不成立**。
2. **✅ 一手（「16 bit 是接口决定的硬上限」的最有力证据）**：**Novanta LIGHTNING II 的 2 轴数据手册原文** —— `Command Resolution: 24-bit (GSB) or 16-bit (XY2-100)`。即**16 bit 不是控制器算力问题，而是 XY2-100 接口本身的天花板**。⚠️ **注意标注矛盾**：同厂的 **3 轴**数据手册只写 `24-bit` 且不提 XY2-100 限制，**两表口径不一致**，引用时应点出[来源](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf)。
3. **✅ 一手（两组独立厂商标称值互相验证）**：RAYLASE 给出 XY2-100-E 16-Bit → **12 µrad**、SL2-100 20-Bit → **0.76 µrad**。⚠️ 我的算术：12 / 0.76 = **15.8 ≈ 2⁴**，正是 16 → 20 bit 的 4 个二进位 —— **两家独立厂商的数字自洽**，这个交叉验证很有说服力[来源](https://www.raylase.de/_Resources/Persistent/5/b/9/0/5b9058dcb0c4f361859551b86d9c55d6d35478d1/RAYLASE%20FOCUSSHIFTER%20DIGITAL%20II_en.pdf)。
4. **真正的问题在标定与增益**：3D 校正文件把 Z 指令映射到实际焦点位置；若中间还有机械/光学增益（见 §3.2 的 2×–16× 聚焦增益），**实际焦点分辨率 = LSB × 聚焦增益**。
5. **⚠️ 关键批判性结论（我的算术，可能是本节最有价值的判断）**：**升级 DAC 位宽并不自动改善聚焦精度。** varioSCANde II 的**长期漂移 < 3 µm / 8 h** 比 16 bit 在 ±14 mm 上的 **0.427 µm/LSB** 还**大约 7 倍** —— 也就是说，**在真实系统里，热漂移与重复性（<0.5 µm）比量化台阶更早成为瓶颈**。先解决漂移，再谈位宽。
6. ⚠️ **必带脚注**：SCANLAB 明确声明 varioSCAN II 的**全部规格「仅指电机本身」**，其对加工场/体积内实际光束定位的影响**取决于具体光学配置**[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)。**引用任何 µm 级指标时必须带这个限定。**
7. ❌ **未找到**任何公开文档把 RTC4 的 16 bit 明确指为 Z 轴精度瓶颈的定量分析。厂商的实际做法是用 **20/24 bit 的新协议绕开**：SL2-100（20 bit）、RL3-100（20 bit）、Novanta 24-bit 指令[来源](https://www.scanlab.de/sites/default/files/2020-08/13_RTC5_control%20boards.pdf)、[来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/48a53e4f-2a14-4518-ad32-d622848ab64a.htm)、[来源](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf)。

### 6.3 Z 轴位置标定方法

**✅ 一手（软件侧标定路径）**：SCANLAB laserDESK 3D Calibration Wizard 生成 **.ct5 三维校正文件**[来源](https://www.scanlab.de/en/products/calibration/hardware-configuration-and-control)；correXion pro 用**三坐标测量机**逐点测量网格实际位置后生成校正文件（< 20 µm）[来源](https://www.scanlab.de/sites/default/files/2020-08/CalibrationSolutions.pdf)
**✅ 一手（自动化标定仪器）**：RAYLASE 提供 **SCAN FIELD CALIBRATOR**、**RAYDIME**、**RAYSPECTOR** 图像处理与测量系统作为标定工具链[来源](https://www.raylase.de/en/products/prefocusing-deflection-units.html)
**✅ 一手（光束质量/焦斑位置的标准测量框架）**：**ISO 11146-1:2021** 是「激光束宽度、发散角和光束传播比的测试方法」国际标准，规定通过**焦散（caustic）扫描**测量束宽与 M² —— 这是「焦斑法」的国际标准依据[来源](https://www.iso.org/obp/ui/#!iso:std:77769:en)、[来源](https://cdn.standards.iteh.ai/samples/77769/8c3dd35c9da844e0b712dec7df96c53d/ISO-11146-1-2021.pdf)
**✅ 一手（色散共焦法，用于 Z 位置测量）**：Precitec 色散共焦传感器「使用高性能光学镜头**把白光聚焦在沿光轴的不同距离上**，而不是单一点」，具备「**极高的 Z 轴分辨率与精度**」「对反射面可达 **45°**、对漫射面 **>80°** 的斜率容限」[来源](https://www.precitec.com/optical-3d-metrology/technology/chromatic-confocal-sensors/)
**🟡 二手（共聚焦在机标定）**：学术文献用色散共焦传感器做在机测量，**同步采集传感器数据与运动轴实时位置**以降低传感器轴与主轴对准误差的负面影响[来源](https://www.sciencedirect.com/science/article/pii/S0141635921002956)
**❌ 未找到**：**刀口法（knife-edge）用于激光扫描头 Z 轴标定的厂商一手文档**。刀口法是 ISO 11146 焦散测量中常用的实现手段之一，但本次未找到任何扫描头厂商公开其 Z 标定采用刀口法的证据。⚠️ 另：**IEEE 刀口法不确定度论文摘要无具体数值、全文付费墙**，不宜引用具体数字。

**⭐⭐ 以下为各标定方法的「一手量化数字」（价值最高）**：

| 方法 | 一手数字 | 来源 |
|---|---|---|
| **焦斑法（烧纸/烧蚀）** | **Novanta 技术通报 AN00025** 给出判据：**烧纸最白的一格 = 焦点位置**；在**黑色阳极氧化铝**上（功率高到会烧穿纸时）则**较暗格**更佳，**最佳焦点在两个白格之间** —— 因为白化是激光汽化黑色氧化层，而更暗处激光侵入了金属、更接近真实 Z=0。CO₂ 焦深 ≈ **1 mm**；**1 kW 光纤激光焦深仅 100–200 µm**（焦点步进必须小于此）。实例：1 kW IPG YLR、**300 µm 步进**打点、显微镜读熔线宽，中心附近约 **80 µm**；推荐试片：黑色阳极氧化铝 **5005/5205**、不锈钢 **SS316/SS312** | ✅ 一手（[Novanta AN00025](https://novantaphotonics.com/wp-content/uploads/2022/03/AN00025_Finding-Focus-Plane-with-CalWizard-on-Black-Anodized-Sheet-Metal....pdf)）⚠️ **20 µm 是「理论预期焦斑」、80 µm 是「实测熔线宽」，二者都不可当作「标定精度」引用** |
| **共聚焦（色散共焦）** | **Precitec**：轴向分辨率 **2–4 nm**，线性度 30–400 nm；**Keyence CL-3000**：**0.003–0.1 µm**；**Micro-Epsilon IFS2405** 静态 **< 2 nm** | ✅ 一手（厂商数据手册） |
| **焦散扫描（caustic scan）** | **Cinogy CinSquare**：焦散扫描测量**精度典型 2–3%**，束腰尺寸/位置 **3–5%** | ✅ 一手（厂商） |
| **软件 3D 校正** | SCANLAB 分级见上表（RTC 校正文件 <150 µm→correXion pro <20 µm） | ✅ 一手 |

**⚠️ 三处引用陷阱（务必注意）**：
1. **ISO 11146-1 的免费预览只有 11 页、仅第 1–3 章**，测量流程细节（如「≥10 个 z 位置」「重复性 ±5%」等）**只能引二手，不能标注为「标准一手」**[来源](https://cdn.standards.iteh.ai/samples/77769/8c3dd35c9da844e0b712dec7df96c53d/ISO-11146-1-2021.pdf)
2. IEEE 刀口法论文**全文付费墙**（见上）
3. **SCANLAB 与 RAYLASE 均未公开焦点标定后的量化精度** —— 即「标完之后能保证多少 µm」这个问题，**厂商不给数字**。

**⚠️ 我的算术（与景深的对照）**：1 kW 光纤激光焦深仅 **100–200 µm**，而 RAYLASE 标定工具的精度是 **<20 µm（correXion pro）** —— 标定精度比焦深小 5–10 倍，**是够用的**；但这也说明**小焦深高功率场景对 Z 标定的要求远高于打标场景**。

---

## 7. Z 轴补偿的数学模型

**✅ 一手（基本关系，两套架构）**：
- **F-θ 场镜架构**：焦斑位置 $y=f\cdot\theta$（y 为距场中心距离，f 为有效焦距，θ 为扫描角）[来源](https://www.govolition.com/product/V40-FTH160-1064)
- **场尺寸**：$L=f\cdot\theta$，L 为方形场对角线[来源](https://www.govolition.com/product/V40-FTH160-1064)
- **预聚焦架构**：调整「移动镜与聚焦镜之间的距离」来补偿弧线焦面 → **Z 是 (x, y) 的函数**，因为弧面高度只取决于离场中心的径向距离[来源](https://www.raylase.de/en/products/prefocusing-deflection-units.html)

**⚠️ 我的数学模型（基于上述一手几何关系推导，非厂商公式）**：
1. **理想球面焦面的补偿量**（无限远共轭、镜间距忽略）：
   $$z_{\text{corr}}(x,y)=-\left(\sqrt{f^2+x^2+y^2}-f\right)\approx-\frac{x^2+y^2}{2f}$$
   **数值算例（f=160 mm，幅面 ±100 mm）**：
   - 角点 (100, 100)：$\sqrt{160^2+100^2+100^2}-160=\sqrt{45600}-160=213.54-160=$ **53.5 mm**
   - 边中点 (100, 0)：**28.7 mm**
   → **补偿量是二维抛物面；角点补偿量约为边中点的 1.86 倍**（按 r² 计为 2 倍；按严格矢高为 1.86 倍）。
2. **实测焦面校正（工程做法）**：用 $z_{\text{corr}}(x,y)=-\big(a_1 r^2+a_2 r^4+\cdots\big)$（$r^2=x^2+y^2$）做最小二乘拟合，系数由 3D 标定文件（.ct5）承载[来源](https://www.scanlab.de/en/products/calibration/hardware-configuration-and-control)。SCANLAB 建议「**把零曲率点放在扫描范围中段**以限制整个扫描过程中的场曲量」→ 拟合时应让残差在场上呈对称正负分布[来源](https://www.govolition.com/product/V40-FTH160-1064)。
3. **任意曲面工件（含法向补偿）**：
   $$z_{\text{focus}}(x,y)=Z_w(x,y)+\Delta_{\text{lens}}(x,y)$$
   其中 $Z_w$ 为工件面高度，$\Delta_{\text{lens}}$ 为镜组残余场曲修正量。
   **入射角修正**：若工件面法向与光束轴夹角为 $\varphi$，**光斑在表面上的椭圆长轴被拉长 $1/\cos\varphi$ 倍**，功率密度按 $\cos\varphi$ 下降。🟡 二手：多数 3D 动态聚焦系统可有效加工**表面法向角至 60°–75°**，超过 75° 后菲涅耳反射损失显著增大，需第四轴[来源](https://www.meenjet.net/news/laser-marking-curved-surfaces-dynamic-focal-depth.html)
4. **Z 与 XY 的时序关系**：三轴共用同一 10 µs 帧（见 §9），Z 指令与 XY 指令**同步下发**；但 Z 轴跟踪误差（0.1–1.3 ms）远大于 10 µs，**必须做前导/延迟补偿**，否则高速下 Z 滞后毫米级（§3.5 算例）。
5. **软件侧的实现证据**：EZCAD3 明确支持「**真正的三轴控制（X、Y、Z）**」，可导入 STL / IGES / STEP 做曲面打标[来源](https://www.ezcad.com/products/ezcad3-software/)（🟡 二手，但为软件厂商官方产品页）
6. **2.5D vs 3D 的区分（✅ 一手）**：RAYLASE 明确「**逐层加工（2.5D）与空间加工（3D）都成为可能**」[来源](https://www.raylase.de/_Resources/Persistent/5/1/8/9/5189d9ad9239901c83aa37b1738071904ed74596/2026-03-16_Datenblatt_FOCUSSHIFTER%20RD-14_EN_v2.0.pdf) —— 2.5D 只需 z 随层高变化（一维），3D 需 z=f(x,y)（二维面）。

---

## 8. 失效现象 → 原因对应

**❌ 未找到厂商一手的 Z 轴失效模式白皮书**。以下为**一手规格线索 + 🟡 二手故障排查指南**的交叉整理，**明确标注哪些是推断**：

| 现象 | 可能原因 | 依据 |
|---|---|---|
| **Z 轴卡死 / 自锁失效** | ① 电机自锁电路故障（连接线开路/短路、接线错误、保险丝熔断）；② 驱动器板故障；③ 机械卡滞 | 🟡「振镜电机不自锁：检查连接线是否开路或短路、接线是否正确、保险丝是否完好；确认无误后通电观察驱动板指示灯是绿还是黄。若不亮或红灯亮，拔下驱动板电源线，用万用表测输入端各端子电压是否 ±24 V」[来源](https://www.leadtech.ltd/solutions-to-common-faults-of-laser-marking-machine-galvanometer.html)；🟡「若无声音，用手稍加力轻推振镜镜片，若镜片不自锁…找一块确认完好的驱动板接上：若仍不自锁则电机损坏；反之则驱动板损坏」[来源](https://www.laserhome.com/Common-faults-and-treatment-methods-of-galvanometer-of-laser-marking-machine-id45739067.html) |
| **自锁但力矩不足** | 电机退磁 / 线圈局部短路 / 驱动级损坏 | 🟡「用确认完好的驱动板 + 好电机分别接到待测驱动板与振镜头…用手轻转振镜轴，若感觉『发硬』则镜电机损坏」[来源](https://www.leadtech.ltd/solutions-to-common-faults-of-laser-marking-machine-galvanometer.html) |
| **Z 轴异响 / 啸叫** | ① 调谐（tuning）与负载不匹配；② 伺服增益过高导致自激振荡；③ 接地/屏蔽不良引入干扰；④ 轴承磨损 | 🟡「若仍有啸叫，调试振镜驱动板滤波板上的电位器；若仍无法消除，需返厂精调。**注意：不要让振镜长时间处于啸叫状态，以免烧毁振镜电机**」[来源](https://www.leadtech.ltd/solutions-to-common-faults-of-laser-marking-machine-galvanometer.html)；🟡「标记出现波浪线且打标头有轻微噪声 → 驱动板发热偏高（产生干扰），检查地线是否正确连接（最佳方式：X 振镜信号地、Y 振镜信号地、屏蔽线、220 V 电源地、打标机外壳共地）」[来源](https://www.leadtech.ltd/solutions-to-common-faults-of-laser-marking-machine-galvanometer.html)；⚠️ **推断**：RAYLASE 提供 **MA/VC/C**（RD-14）与 **VC/W/H/M**（DIGITAL II）多种 tuning 曲线，说明调谐参数与负载/轨迹类型强相关，不匹配会有动态表现异常[来源](https://www.raylase.de/_Resources/Persistent/5/1/8/9/5189d9ad9239901c83aa37b1738071904ed74596/2026-03-16_Datenblatt_FOCUSSHIFTER%20RD-14_EN_v2.0.pdf) |
| **回零 / 参考位置丢失** | ① 编码器或位置反馈失效；② 限位/参考开关故障；③ 掉电后未执行回零流程 | ⚠️ **推断 + 一手旁证**：SCANLAB 把「**Read-back function 回读功能**」「**Better position stability 更好的位置稳定性**」列为 varioSCANde II 的**升级卖点**[来源](https://www.scanlab.de/en/products/z-axes-3d-add-ons/varioscan-ii)；varioSCANde i「配备**数字线性编码器**」[来源](https://pdf.directindustry.com/pdf/scanlab-gmbh/3d-focusing-systems-varioscan-varioscande/39164-260795.html)；RAYLASE 强调「**额外反馈位置与状态信号**」[来源](https://www.raylase.de/_Resources/Persistent/5/1/8/9/5189d9ad9239901c83aa37b1738071904ed74596/2026-03-16_Datenblatt_FOCUSSHIFTER%20RD-14_EN_v2.0.pdf) —— **说明位置可信度是 Z 轴的核心痛点，无编码器/无回读的型号无法自查** |
| **聚焦漂移（随时间的焦点偏移）** | ① **热漂移**：功率吸收导致热透镜效应；② 长期漂移；③ 冷却不足 | ✅ **一手定量**：varioSCANde II 长期漂移 **< 3 µm（>8 h）**[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)；FOCUSSHIFTER RD-14 长期漂移 **< 60 µrad（8 h）**、偏置漂移 ≤10 µrad/K、增益漂移 ≤15 ppm/K[来源](https://www.raylase.de/_Resources/Persistent/5/1/8/9/5189d9ad9239901c83aa37b1738071904ed74596/2026-03-16_Datenblatt_FOCUSSHIFTER%20RD-14_EN_v2.0.pdf)；excelliSHIFT 因**只用反射元件**而「减少热透镜效应」[来源](https://www.scanlab.de/sites/default/files/2025-06/SCANLAB-excelliSHIFT-EN.pdf)；✅ 光学侧原理：「高功率激光应用中，镜片材料与镀膜的吸收会导致**热透镜效应**，使**焦面发生位移（focal shift）**并劣化光束质量」[来源](https://www.rp-photonics.com/scanning_lenses.html)；✅ RAYLASE 水冷要求 22–28 °C、≥2 l/min，并注明「**不带温度控制运行时漂移值可能增大**」[来源](https://www.raylase.de/_Resources/Persistent/5/b/9/0/5b9058dcb0c4f361859551b86d9c55d6d35478d1/RAYLASE%20FOCUSSHIFTER%20DIGITAL%20II_en.pdf) |
| **加工面高度对但边缘虚焦** | 残余场曲 + 光斑太小（DOF < 残差）→ 需 Z 补偿或换长焦/预聚焦架构 | ✅ 见 §1.1（由 DOF 判据与厂商原文推出） |
| **Z 位置随加工速度变化** | 跟踪误差未补偿（drag） | ✅ **一手（厂商把「不随速度变化」当作卖点，反证这是常见故障）**：RD-14「**确保 z 位置与穿透深度不受加工速度影响**」[来源](https://www.raylase.de/_Resources/Persistent/5/1/8/9/5189d9ad9239901c83aa37b1738071904ed74596/2026-03-16_Datenblatt_FOCUSSHIFTER%20RD-14_EN_v2.0.pdf) |

⚠️ **重要提醒**：上表中**所有振镜故障排查内容均来自二手工业网站，且原文全部针对 XY 振镜电机**。3 轴系统的 Z 轴若是**透射镜组 + 直线电机/音圈**架构（varioSCAN、FOCUSSHIFTER），故障模式与 XY 振镜电机**并不相同**（无镜片，但有导轨与光学面污染问题）。**不要把 XY 振镜的排查流程直接套用到 Z 轴。❌ 未找到专门针对扫描头 Z 轴镜组的厂商故障文档。**

---

## 9. 接口：各协议怎么传 Z 轴

### 9.1 XY2-100 —— ✅ 一手（协议规格书原文）

**帧格式（20-bit 字，帧周期 10 µs = 100 kHz；CLK 2 MHz）**：
> 「XY2-100 接口用于把 X 和 Y 坐标从控制器发送到偏转系统。它是**串行接口，使用 20-bit 字，以 2 Mbit/s 或 100 kwords/s 的速度发送**。」「每个轴的数据由 **20-bit 字**组成。**前 3 bit 用作控制字（C2–C0）**，**接下来 16 bit 是数据信息（D15–D0，偏移二进制 offset binary）**，**最后 1 bit 是奇偶校验位（P，偶校验 even parity）**。」「SYNC 在第一个 bit 可发送时变高，**保持高电平 19 个 bit**，在奇偶校验位时变低。」「时钟频率 **2 MHz**：变高时数据位改变，变低时偏转系统采样数据位。」时序：tDS ≥ 50 ns，tDH ≥ 100 ns。
[来源](https://dvd.ilphotonics.com/Ray-Motion%20-%20galvanometers%20-%201D-2D-3D%20scanners/Motion%20Control%20-%20Optomechanics/Interface%20XY2-100.pdf)（Ray-Motion 官方技术数据表）

**⚠️ 必须纠正的一个常见说法：XY2-100 是 MSB-first，不是 LSB-first。** 位序为 `001` + **D15 → D0** + 偶校验；RAYLASE 手册原文「D0 是最低位、D15/D17 是最高位」；sigrok 解码器亦以 `bits[3]` 为 MSB。[来源](https://raw.githubusercontent.com/sigrokproject/libsigrokdecode/master/decoders/xy2-100/pd.py)

**XY2-100 的 Z 通道 —— ✅ 一手（多个独立来源交叉验证）**：
- **LasIA 官方规范信号图直接画出 X+ / Y+ / Z+**（LIA202001）[来源](https://www.aaronvose.net/Quantronix_Osprey/xy2_100_specification.pdf)（⚠️ 该镜像为第三方转载，lasia.org 原文本环境 401 不可达）
- **RAYLASE SS-III 的 XY2-100-E 手册**原文「每一轴（x、y 以及 z）都有去往振镜头的正向通道和回传通道」；DB25 引脚 **`5/18 = Z−/Z+`（聚焦轴）**、`7/20 = Z_stat`，状态字 bit13/5 = Z 轴跟踪窗口[来源](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)
- **RAYLASE SP-ICE 3** 的 `XY2_100` 头格式定义为 **"XY or XYZ"**[来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/45289f65-2556-4dff-8d27-7f5918253301.htm)
- **RAYLASE AXIALSCAN** 用词为 **`Z-DAC CHANNEL`**，引脚同为 5/18
- 开源实现用 **`Channel Z`** 命名第三路[来源](https://github.com/hyperchao0/qspi4xy2-100)
- **⚠️ 术语提醒：`CHANNELZ` 这个字面写法 ❌ 未找到一手出处。** 规范与厂商实际使用的命名是 `X+/Y+/Z+`（LasIA）、`Z−/Z+ (focus axis)`（RAYLASE SS-III）、`Z-DAC CHANNEL`（RAYLASE AXIALSCAN）。SCANLAB 转换器侧只标 `CHAN1/CHAN2`（**仅 2 路**）。
- **✅ 一手（物理连接）**：3D 配置「**至少需要两个差分线驱动器**」来支持三个通道 + SYNC + CLK；需 `AM26LS31` 之类差分驱动器（TIA/EIA-422 兼容，5 V 供电，接受 3.3 V TTL）；数据在**时钟下降沿**采样；**时钟默认高极性、SYNC 默认低极性**[来源](https://github.com/hyperchao0/qspi4xy2-100)

**✅ 一手（控制器侧）**：RTC4 支持 XY2-100 **enhanced** 协议，**16-bit 定位分辨率**，**10 µs 输出周期**[来源](http://www.ainnotech.com/ainnotech/pdf/02/1_3/3SCAN-RTC4-Control%20And%20Versatility.pdf)（🟡 经销商镜像）
**✅ 一手（增强模式的确切内容）**：**Standard 与 Enhanced 的更新率相同**（帧长都是 20 bit）。Enhanced 增加的是：**16 或 18 bit 模式（18 bit 用奇校验）**、**命令帧**（8 bit 命令 + 8 bit 参数；发命令帧的周期不发目标位置，**振镜头线性插值**）、可选回传格式。更新率由时钟决定 —— **RAYLASE SS-III 支持 CLK 最高 10 MHz、推荐 4 MHz**（4 MHz 变体即 sigrok 所称 **XY2-200**）[来源](http://www.alaser.com.tw/db/upload/webdata4/5alaser_201412422541519318.pdf)、[来源](https://sigrok.org/wiki/Protocol_decoder:Xy2-100)
**✅ 一手**：varioSCAN II eBox 明确「**SL2-100 与 XY2-100 变体可选**」[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)
**✅ 一手**：RAYLASE FOCUSSHIFTER DIGITAL II 兼容 **XY2-100（16 bit）** 与 **SL2-100（20 bit）**，对应分辨率 12 µrad / 0.76 µrad[来源](https://www.raylase.de/_Resources/Persistent/5/b/9/0/5b9058dcb0c4f361859551b86d9c55d6d35478d1/RAYLASE%20FOCUSSHIFTER%20DIGITAL%20II_en.pdf)

### 9.2 XY3-100 —— ✅ 一手（v1.1 官方 PDF 已取得并逐条核对）

**✅ 一手（定义方与商标）**：XY3-100 由 **LasIA e.V.** 定义并持有商标。LasIA 声明：「作为 XY3-100™ 协议与名称的版权与商标权所有者，LasIA 允许认为自己的 XY3-100 协议实现符合规范的厂商**把这些设备命名为『XY3-100 compatible』**」；要命名为「**XY3-100 certified**」或使用官方 logo、要保证与其他任何 XY3-100™ 认证设备的互操作性，**需要 LasIA 的正式许可**。[来源](https://sourceforge.net/p/lasia/blog/2023/07/xy3-100-digital-scanner-interface-version-11/)

**✅ 一手（规范版本与关键参数）**：

| 项 | 数值 |
|---|---|
| 版本 | **v1.0 = LIA202002**；**v1.1 = LIA202307** |
| 通道 | 核心 2 轴；可选 **Z / U / W → 最多 5 轴**（DB15 版为 3 轴） |
| **比特深度** | **可变 16 … 26 bit**（不是固定值！） |
| 更新率 | **100 kHz 典型**；24 bit 帧 → 2.4 MHz，32 bit 帧 → 3.2 MHz |
| **Z 轴引脚** | DB25 **`5/18 = Z−(E−) / Z+(E+)`**，与 X/Y **共用 SYNC / CLK** |

**⚠️ 最需警惕的工程陷阱：XY2-100 与 XY3-100 在同一条 DB25 上 CLK / SYNC 是互换的。**
- XY3-100：`1/14 = SYNC(A)`、`2/15 = CLK(B)`
- XY2-100：`1/14 = CLK`、`2/15 = SYNC`
规范里写的 "Same pinout as XY2-100(E)" **只在数据线上成立**。混用两种协议会导致帧同步失败。

### 9.3 SL2-100 —— ✅ 一手（SCANLAB RTC6 手册附录 F）

- **20-bit 控制信号**，由 **SCANLAB 开发并推出**；相比 RTC4 的 16-bit，**定位分辨率提高 16 倍**；RTC5 / RTC6 支持[来源](https://www.scanlab.de/sites/default/files/2020-08/13_RTC5_control%20boards.pdf)、[来源](https://www.scanlab.de/en/applications/micromachining)
- **✅ 一手（为什么「每连接器只能 2 轴」—— 这是帧结构决定的，不是随意限制）**：RTC6 手册附录 F 给出官方帧结构 = 1 block **192 帧**，**1 帧 = 2 子帧 / 10 µs**，**1 子帧 = 20 bit 载荷 + 12 bit 附加** → **每帧恰好 2 轴 × 20 bit**。[来源](https://raw.githubusercontent.com/labspiral/sirius3/main/doc/SCANLAB/RTC6_Manual.en.pdf)
- **✅ 一手（Z 轴的真实接法）**：RTC6 的 **"3D" 选件**明确要求 Z 接 **Connector for Second Scan Head（第二根电缆）** —— 即 **Z 不是帧内第 3 通道，而是走第 2 个 SCANHEAD 连接器**。RAYLASE 侧完全一致：**`SL2_Single3D` = "XY on X904, Z on X905"**，并标注 "SL 协议每连接器限 2 轴"[来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/48a53e4f-2a14-4518-ad32-d622848ab64a.htm)
- **❌ 未找到**：SL2-100 的**官方 bit/s 数据率**（官方从未公布；按附录 F 推算约 **6.4 Mbit/s**，属推算值）；6 bit 模式码表与校验算法的完整位域定义；官方连接器型号/引脚（第三方记为 9-pin D-SUB）。⚠️ 常被引用的「**2 Mbaud**」**❌ 未找到一手来源** —— 2 MHz 实际是 **XY2-100 的 CLK**，两者被混淆了。
- ⚠️ 一手矛盾：RAYLASE FOCUSSHIFTER RD-14 接口栏写「XY2-100 Enhanced 16 Bit / **SL2-100** 20 Bit」，分辨率栏却写「Resolution **RL3-100** / SL2-100 20-Bit = 0.76 µrad」—— **同一份数据手册两处表述不一致**，引用需注明[来源](https://www.raylase.de/_Resources/Persistent/5/1/8/9/5189d9ad9239901c83aa37b1738071904ed74596/2026-03-16_Datenblatt_FOCUSSHIFTER%20RD-14_EN_v2.0.pdf)

### 9.4 RL3-100 —— ✅ 一手（RAYLASE 官方手册）

> 「**RL3-100 协议，20 bit 位置分辨率，每个连接器最多 6 轴。**」
> 「SL2-100 协议，20 bit 位置分辨率，每个连接器最多 2 轴。」
> 「XY2-100 协议，16 bit 位置分辨率（需选配适配器）。」
[来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/48a53e4f-2a14-4518-ad32-d622848ab64a.htm)（RAYLASE SP-ICE 3 用户手册 §2.4 Interfaces）

**✅ 一手（SP-ICE 3 整体能力）**：「SP-ICE 3 通过 **SL2-100 或 RL3-100 协议控制最多 2 个偏转单元**，**20 bit 位置分辨率，10 µs 步进周期**；最多可记录来自偏转单元的 **2400 万条测量数据**」[来源](https://www.raylase.de/en/products/electronics-control-cards/sp-ice-3.html)
**✅ 一手（Z 位深与 XY 相同）**：SP-ICE 3 手册 §7.1.3 明确 `SL2-100 = 20 bits`、`XY2-100 = 16 bits`，且「**All X, Y, and Z ordinates fall within (-res/2)…(res/2)-1**」—— **Z 与 X/Y 使用同一分辨率与同一数值范围**。
**✅ 一手（单电缆）**：3D / 5 轴头的头格式全部标注 "**ALL axes provided on X904 Scanner1**"，即**一根电缆**内包含全部轴[来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/45289f65-2556-4dff-8d27-7f5918253301.htm)
**→ 关键结论（我的归纳）**：RAYLASE 的 **RL3-100 是本次调研中唯一原生支持「单连接器 6 轴」的协议**，因此 3 轴（含 Z）系统用 **1 个 RL3-100 连接器 / 1 根电缆**即可，而 SL2-100 的 3 轴必须拉**第二根电缆**。**20 bit 相比 XY2-100 的 16 bit，Z 与 XY 的分辨率同时提高 16 倍。**
**❌ 未找到**：RL3-100 的**帧级规范**（帧长、位序、校验方式、时钟频率）——RAYLASE 未公开其专有协议的完整规格书。
**✅ 一手（同一台硬件多协议可选）**：同一台 3 轴 AXIALSCAN-50 DIGITAL II 可任选 **RL3-100（20 bit）/ XY2-100（16 bit）/ SL2-100（20 bit）** 三种接口。

### 9.5 接口横向对比表

| 协议 | 定义方 | 通道数 | 比特深度 | 更新率 / 时钟 | Z 轴如何传 | 标注 |
|---|---|---|---|---|---|---|
| **XY2-100** | 无单一发明方；公开格式规范由 **LasIA** 发布（LIA202001） | 标配 2 轴；**Z 为可选第 3 路数据通道** | **16 bit**（偶校验） | 帧 20 bit / **10 µs = 100 kHz**；CLK **2 MHz** | **第 3 对差分线（DB25 `5/18 = Z−/Z+`）**，与 X/Y 共用 CLK/SYNC，同一 20 bit 帧结构 | ✅ 一手 |
| **XY2-100 Enhanced / XY2-200** | 同上 | 同上（X/Y/Z） | **16 或 18 bit**（18 bit 奇校验）+ 命令帧 | 帧长仍 20 bit；**CLK 最高 10 MHz、推荐 4 MHz**（4 MHz 变体 = XY2-200） | 与 XY2-100 相同（Z 在 `5/18`） | ✅ 一手 |
| **XY3-100** | **LasIA**（v1.0 = LIA202002，v1.1 = LIA202307） | 核心 2 轴；可选 Z/U/W → **最多 5 轴**（DB15 版 3 轴） | **可变 16 … 26 bit** | **100 kHz 典型**；24 bit 帧 → 2.4 MHz，32 bit 帧 → 3.2 MHz | DB25 `5/18 = Z−(E−) / Z+(E+)`，共用 SYNC/CLK。**⚠️ CLK/SYNC 引脚与 XY2-100 互换！** | ✅ 一手 |
| **SL2-100** | **SCANLAB** 自研 | **每连接器最多 2 轴**（帧结构决定）；3/4 轴靠第 2 连接器 | **20 bit**/子帧 | 1 帧 = 2 子帧 / **10 µs = 100 kHz**；**官方未公布 bit/s**（推算 ≈6.4 Mbit/s） | **不是帧内第 3 通道** —— Z 走**第 2 个 SCANHEAD 连接器（第二根电缆）** | ✅ 一手 |
| **RL3-100** | **RAYLASE** 自有 | **单连接器最多 6 轴** | **20 bit** | **10 µs 步进周期** | 与 X/Y **同一连接器、同一根电缆** | ✅ 一手（轴数/位深/周期）；帧级细节 ❌ |
| Novanta LIGHTNING II | Novanta / Cambridge | 3 轴（DFM 集成） | **24-bit 指令分辨率** | ❌ 未找到 | 头内部集成 | ✅ 一手（分辨率） |

---

## ⚠️ 常见误解

1. **误解：「f-θ 场镜焦面是平面的，所以不需要 Z 轴。」**
   场镜只是把焦面**近似**做平（残余 ≈0.2 mm）。厂商自己承认残差存在（Thorlabs/Sill：「真实镜头很少达到理论值，总会存在一定的畸变与场曲」[来源](https://www.govolition.com/product/V40-FTH160-1064)、[来源](https://www.silloptics.de/en/service/sill-technical-guide/laser-optics/f-theta-lenses)）。而且**曲面工件根本无法用平面焦面对应**——RAYLASE 原文描述不校正时焦点「在工作场上方形成一个球面」，场外「根本没有聚焦」[来源](https://www.raylase.de/en/products/prefocusing-deflection-units.html)。**Z 轴的第一需求是 3D 曲面，不是补场曲。**

2. **误解：「f=160 mm 场镜在 ±100 mm 上的场曲是 31 mm。」**
   错两层：① 精确值是 **28.68 mm**，31.25 mm 只是 y²/(2f) 近似；② **这两个数都不是 f-θ 场镜的真实残差**——它们是**未校正球面焦面**的几何矢高。真实 f-θ 场镜残差约 **0.2 mm**（Thorlabs 官方曲线读图值），**改善约 143 倍**。真正要比较的是**残差 vs 景深 $z_R=\pi w_0^2/(M^2\lambda)$**：λ=1064 nm、光斑 12 µm 时 DOF 仅 ±0.11 mm（残差是它的 1.8 倍，必须补偿）；光斑 50 µm 时 DOF 达 ±1.85 mm（残差只占 11%，可不补）（⚠️ 我的算术）。

3. **误解：「±100 mm 幅面用 f=160 mm 场镜就能做。」**
   由 $y=f\theta$，±100 mm 需光学半角 **35.8°**，而 Thorlabs FTH160-1064 额定仅 **±28°**（对应 ≈110.6×110.6 mm 幅面）[来源](https://www.govolition.com/product/V40-FTH160-1064)、[曲线图](https://www.thorlabs.com/f-theta-lenses-tutorial)。**别把 FTH254-1064 的 156.7 mm 幅面误记到 f=160 头上。** 200 mm 幅面要更长焦距场镜或预聚焦架构。

4. **误解：「Z 轴就是把整个场镜前后移动。」**
   主流方案**都不是移动场镜**：varioSCAN 移动的是**镜组内的一片发散镜**，相对**固定的聚焦镜**运动，从而改变**系统总焦距**与入射场镜的发散度[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)、[来源](https://pdf.directindustry.com/pdf/scanlab-gmbh/varioscan-20-varioscan-40-varioscan-40flex/39164-169746.html)；RAYLASE 移动的是**预聚焦模块内的 Linear-Translator 镜头**，微调其与聚焦镜的距离[来源](https://www.raylase.de/en/products/prefocusing-deflection-units.html)，RD-14 则是「在 f-θ 镜头与偏转单元的组合上**增加一套可调镜组**」[来源](https://www.raylase.de/_Resources/Persistent/5/1/8/9/5189d9ad9239901c83aa37b1738071904ed74596/2026-03-16_Datenblatt_FOCUSSHIFTER%20RD-14_EN_v2.0.pdf)。excelliSHIFT 甚至**只用反射元件**，完全没有透射光学件[来源](https://www.scanlab.de/sites/default/files/2025-06/SCANLAB-excelliSHIFT-EN.pdf)。

5. **误解：「用散焦（defocus）就能放大光斑，所以没必要做 in-focus zoom。」**
   RAYLASE 明确反驳：散焦放大使光斑**「定义不良」「变得模糊」**，**对平顶/环形光束轮廓直接丢失形状**，且功率分布随离焦量变化，**必须对每个倍率单独做实验标定工艺参数**。真正的 in-focus zoom 需要**光路中额外的可动望远镜**，才能在不离开焦平面的前提下连续调整焦点直径[来源](https://www.raylase.de/en/applications/additive-manufacturing/in-focus-spot-magnificantion-in-additive-manufacturing.html)。

6. **误解：「RTC4 只有 16 bit，所以 Z 轴精度不够。」**
   ⚠️ **未找到任何公开来源支持这个因果链**。16 bit 在 ±14 mm 行程上对应 **0.43 µm/LSB**（⚠️ 我的算术），远小于景深。16 bit 的真实短板是**带聚焦增益的大行程配置下余量变小**：±32 mm 聚焦行程 → **0.98 µm/LSB**。厂商的应对是升级到 SL2-100 / RL3-100 的 20 bit（**16 倍**改善）或 Novanta 的 24-bit 指令[来源](https://www.scanlab.de/sites/default/files/2020-08/13_RTC5_control%20boards.pdf)、[来源](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf)。

7. **误解：「excelliSHIFT 的 0.1 ms 与 FOCUSSHIFTER 的 0.9 ms 可以直接比大小。」**
   两者都是**跟随误差时间常数（拖曳）**，必须**乘以当时的 Z 向速度**才是位置误差。⚠️ 我的算术：RD-14 = 900 mm/s × 0.9 ms ≈ **0.81 mm**；DIGITAL II = 880 mm/s × 1.3 ms ≈ **1.14 mm**；excelliSHIFT = 30 m/s × 0.1 ms = **3.0 mm**。**跟踪误差小 9 倍，但因为速度快 33 倍，绝对滞后反而更大。** 选型必须带速度一起算。

8. **误解：「Z 轴 = 三轴同步，所以不用补偿延迟。」**
   三轴共用 10 µs 帧下发（XY2-100 / SL2-100 / RL3-100 均为 10 µs 周期）[来源](https://dvd.ilphotonics.com/Ray-Motion%20-%20galvanometers%20-%201D-2D-3D%20scanners/Motion%20Control%20-%20Optomechanics/Interface%20XY2-100.pdf)、[来源](https://www.raylase.de/en/products/electronics-control-cards/sp-ice-3.html)，但**Z 的机械跟踪误差是 0.1–1.3 ms**，比帧周期大 **10–130 倍**。所以**指令同步 ≠ 位置同步**，必须靠 sky writing / SCANahead / drag delay 优化等机制补偿[来源](https://www.scanlab.de/en/regulation-and-process-control)。

9. **误解：「XY3-100 是 XY2-100 的 3 轴版，规格公开可查。」**
   XY3-100 由 **LasIA e.V.** 持有协议与商标权，「XY3-100 certified」需正式许可[来源](https://sourceforge.net/p/lasia/blog/2023/07/xy3-100-digital-scanner-interface-version-11/)，**但其帧格式与 Z 通道细节在本次调研中 ❌ 未找到公开规范正文**。**不要把 XY3-100 当成免费公开的标准。**

10. **误解：「Novanta DFM 的参数和 SCANLAB/RAYLASE 一样可以列表比较。」**
    **❌ Novanta 公开数据手册完全没有 DFM 的 Z 轴行程、速度、重复精度**，只给出扫描头整体的 0.2/0.4 ms 跟踪延迟与 **24-bit 指令分辨率**[来源](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf)。**做选型表时 DFM 列必须留空，不能填推测值。**

11. **误解：「RAYLASE RAYVOLUTION DRIVE 有独立规格。」**
    **❌ 未找到**——该技术无独立数据手册或产品页（`/en/products/rayvolution-drive.html` 返回 **HTTP 404**）。只能用搭载它的 FOCUSSHIFTER RD-14 的指标（0.9 ms / 900 mm/s）间接说明，并注明是间接证据。

12. **误解：「把 XY 振镜的故障排查流程套用到 Z 轴就行。」**
    ⚠️ 网上所有振镜故障指南（不自锁、啸叫、波浪线）**都针对 XY 振镜电机**。3 轴系统的 Z 轴若是**透射镜组 + 直线电机/音圈**架构，故障模式完全不同（无振镜镜片，但有导轨、光学面污染、线性编码器）。**❌ 未找到专门针对扫描头 Z 轴镜组的厂商故障文档。**

13. **误解：「同一台 Z 轴的聚焦行程是固定的。」**
    错。⚠️ 我的算术：RAYLASE RD-14 配 f=163 mm 场镜时自由焦程 **−16…+14 mm（约 30 mm）**，配 f=254 mm 时 **−41…+32 mm（约 73 mm）**，**焦程约 2.4 倍**，但光斑同时从 26.1 µm 放大到 40.7 µm（1064 nm）[来源](https://www.raylase.de/_Resources/Persistent/5/1/8/9/5189d9ad9239901c83aa37b1738071904ed74596/2026-03-16_Datenblatt_FOCUSSHIFTER%20RD-14_EN_v2.0.pdf)。SCANLAB 侧同理：同一台 20i 电机配不同光学配置，聚焦偏移在 **±4 mm 到 ±32 mm** 之间变化（**8 倍**）[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)。**报规格必须带场镜焦距一起报。**

---

## 📋 来源可靠性清单（本次调研实际打开的文件）

| 状态 | 来源 | 类型 |
|---|---|---|
| ✅ 已读全文 | SCANLAB excelliSHIFT 数据手册 PDF（05/2025） | 厂商一手 |
| ✅ 已读全文 | SCANLAB varioSCAN II 手册 PDF（09/2025） | 厂商一手 |
| ✅ 已读全文 | **RAYLASE FOCUSSHIFTER RD-14 数据手册 PDF（v2.0，2026-03）** | 厂商一手 |
| ✅ 已读全文 | RAYLASE FOCUSSHIFTER DIGITAL II 数据手册 PDF（v1.8，2021-07） | 厂商一手 |
| ✅ 已读全文 | Novanta LIGHTNING II 数据手册 PDF | 厂商一手 |
| ✅ 已读全文 | RAYLASE SP-ICE 3 用户手册 §2.4 接口 | 厂商一手 |
| ✅ 已读全文 | Ray-Motion XY2-100 技术数据表 PDF | 协议规格书一手 |
| ✅ 已读全文 | SCANLAB Calibration Solutions PDF（标定精度分级） | 厂商一手 |
| ✅ 已读全文 | RAYLASE 预聚焦偏转单元页 / Spot Magnification 应用页 / RD-14 产品页 | 厂商一手 |
| ✅ 已读全文 | github.com/hyperchao0/qspi4xy2-100（CHANNELZ 证据） | 开源实现 |
| ✅ 已读全文 | govolition（Thorlabs FTH160-1064 + F-Theta 教程镜像） | 代理镜像 |
| ✅ **已直接读图核对** | Thorlabs FTH160-1064 / FTH100-1064 官方场曲曲线图 | 厂商一手（读图值） |
| ✅ 已读全文 | Sill Optics 技术指南 / RP Photonics 扫描镜百科 / ISO 11146-1 | 厂商一手 / 标准 |
| ✅ 已读全文 | Precitec 色散共焦传感器技术页 | 厂商一手 |
| ⚠️ 抓取超时/被拦 | Thorlabs 官网 f-theta 页面（反爬，返回空）、SCANLAB 3D Calibration Wizard PDF、RTC6 手册、SCANLAB SCANpedia 焦点直径页（404） | — |
| ❌ 404 / 不存在 | RAYLASE RAYVOLUTION DRIVE 独立页 | — |
| ❌ 工具报错 | `web_fetch` 工具在本会话对**所有**域名均返回 "resolves to a non-public IP address"；全部内容改由 shell（curl / python / node）获取 | — |

**⚠️ 环境提示（对复现者）**：本会话中 `web_fetch` 工具**完全不可用**（对所有域名报非公网 IP）。可行替代路径：用 `pwsh` 调用 `curl.exe`（**不要加 `--compressed`**，本机 libcurl 版本过旧）下载，再用 `pdftotext -layout`（MiKTeX 附带）或 Node.js 脚本转文本。工作目录含中文时，**Python 的 `sys.argv` 路径会被系统代码页破坏**，需改用 Node.js 或把脚本写到纯 ASCII 路径。
