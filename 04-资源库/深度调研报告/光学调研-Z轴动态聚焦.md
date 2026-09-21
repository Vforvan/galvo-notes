# Z 轴动态聚焦镜组（dynamic focusing / z-shifter / focus shifter）调研素材

> 标注约定：**✅ 一手确认** = 厂商官网/数据手册/协议规格书/规范原文，或已读全文的论文；**🟡 二手转述** = 代理商、博客、论坛、行业文章；**❌ 未找到** = 未找到公开来源。
> 所有数值均标注来源；自行算术推导的部分明确写「⚠️ 我的算术」。

---

## 1. 为什么需要动态聚焦（Z 轴）？

**✅ 一手：场镜不是「理想平面」，Z 轴有两个完全不同的使命。**

厂商给的官方理由（一手原文）：

- SCANLAB：varioSCAN II 的 z 轴「使 2D 扫描系统能够执行 3D 加工，或**替代昂贵的物镜以提供平面聚焦面**」[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)
- SCANLAB：excelliSHIFT「把 2D 扫描头扩展为高动态 3D 系统」，卖点是**三个轴加速度完全一致**，且**光路只用反射元件**（无透射元件 → 不同波长无色散、高功率下热透镜效应小）[来源](https://www.scanlab.de/sites/default/files/2025-06/SCANLAB-excelliSHIFT-EN.pdf)
- RAYLASE：预聚焦偏转单元（AXIALSCAN 系列）的存在理由写得很直白：「**在不做焦点校正的偏转单元中，场中心聚焦光斑在任一轴移动时都描出一条弧线，在工作场上方形成一个球面**；在场中心以外，由于镜到工件距离增加，光束**根本没有聚焦**」[来源](https://www.raylase.de/en/products/prefocusing-deflection-units.html)
- RAYLASE 预聚焦单元还解决「输出镜的成本与尺寸限制、2 轴单元的光束孔径限制」，并允许**同一台单元改变工作距离、场尺寸和光斑尺寸** [来源](https://www.raylase.de/en/products/prefocusing-deflection-units.html)
- Novanta LIGHTNING II：DFM（Dynamic Focusing Module）「使光斑在整个工作场保持聚焦」，并「**可适应不同的工作距离和有效场尺寸**，以配合不同的待加工零件」[来源](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf)

**归纳 4 类需求**：① 3D 曲面/异形面加工（焦面必须跟随工件面，不可能靠平面场镜）；② 大幅面残余场曲 + 小光斑（UV/小光斑时景深小于场曲残差）；③ 同一台设备切换工作距离/场尺寸/焦距（免更换场镜）；④ 预热焦（pre-focus）架构下补偿球面焦面。

### 1.1 定量：f=160 mm 场镜在 ±100 mm 幅面上的焦面弯曲量

**⚠️ 我的算术（几何推导，非厂商数据）**：若焦面是球面（普通球面镜/未校正系统的极限情形），矢高
$$\Delta z=\sqrt{f^2+y^2}-f\approx\frac{y^2}{2f}$$

| 场镜 f | 幅面半宽 y | 严格值 √(f²+y²)−f | 近似 y²/(2f) |
|---|---|---|---|
| 100 mm | 100 mm | 41.42 mm | 50.0 mm |
| **160 mm** | **100 mm** | **28.68 mm** | **31.25 mm** |
| 254 mm | 100 mm | 18.98 mm | 19.69 mm |
| 420 mm | 100 mm | 11.74 mm | 11.91 mm |

**但这个 28.7 mm 不是真实场镜的答案** —— f-θ 场镜是专门为平场设计的多片空气间隔系统，把场曲校正到远小于此的残差：

**✅ 一手（定性，厂商明确承认存在残差）**：Thorlabs（原厂 F-Theta 教程，经代理镜像转载）：「f-θ 场镜被很好地设计为提供平坦像面，但**真实镜头很少达到理论值，总会存在一定的畸变与场曲**」，并给出 **FTH100-1064（f=100 mm，最大偏转角 28°）的场曲（单位 mm）随扫描角变化曲线**，建议「把零曲率点放在扫描范围中段以限制整个扫描过程中的场曲量」[来源](https://www.govolition.com/product/V40-FTH160-1064)
**❌ 未找到**：该曲线的**具体数值**在网页上以图片呈现，未给出数字表；Thorlabs 官网 `/f-theta-lenses-tutorial` 与产品页在本次环境中被反爬拦截（返回空内容），未能读到原始数字。
**✅ 一手**：Sill Optics 技术指南同样定性确认：「标准镜头把光束聚焦在**球面**上，而非理想的平场；使用 f-θ 镜头可提供**平面聚焦面**，并在整个 XY 像面上获得**几乎恒定的光斑尺寸**」[来源](https://www.silloptics.de/en/service/sill-technical-guide/laser-optics/f-theta-lenses)
**🟡 二手**：RP Photonics（行业百科）：「用简单球面镜时，焦点并不是都落在目标平面上，而是落在近似球面上，所以外围区域光斑会变大。平场扫描镜…提供近似恒定的光斑尺寸」[来源](https://www.rp-photonics.com/scanning_lenses.html)

**✅ 一手（真实 f=160 场镜的可用幅面上限）**：Thorlabs FTH160-1064（f=160 mm，1064 nm，M85×1.0，3 片式）：**大扫描场 70×70 mm² 至 156.7×156.7 mm²**，f-θ 畸变 <1.3%[来源](https://www.govolition.com/product/V40-FTH160-1064)。**即 ±100 mm（200 mm 幅面）已超出一支典型 f=160 mm 场镜的标称幅面**，需要更长的 f 或预聚焦（AXIALSCAN/FOCUSSHIFTER）架构。

**结论（工程判据）**：真实场镜的**残余**场曲通常只有零点几毫米量级，是否可用取决于它相对景深（DOF）的大小。

**DOF / 瑞利长度公式与算例（λ=1064 nm，M²=1）**：
$$z_R=\frac{\pi w_0^2}{M^2\lambda},\qquad \mathrm{DOF}\approx 2z_R$$
其中 $w_0$ = 焦斑**半径**，$\lambda$ = 波长，$M^2$ = 光束质量因子。

| 光斑直径 (1/e²) | w₀ | z_R | DOF ≈ 2z_R |
|---|---|---|---|
| 12 µm | 6 µm | 0.106 mm | 0.21 mm |
| 20 µm | 10 µm | 0.295 mm | 0.59 mm |
| 24 µm | 12 µm | 0.425 mm | 0.85 mm |
| 30 µm | 15 µm | 0.664 mm | 1.33 mm |
| 50 µm | 25 µm | 1.845 mm | 3.69 mm |

**判据**：12 µm 光斑的 DOF 仅 ±0.11 mm —— 若场曲残差 >0.1 mm，边缘就必然离焦；而 50 µm 光斑容忍 ±1.8 mm。**这就是「小光斑/UV/大幅面必须做 Z 补偿，而 1064 nm 粗光斑可以只靠场镜」的物理原因。**

**🟡 二手（工程经验值，供交叉验证）**：一支工业博客给出「标准 2D 光纤激光（f=160 mm）总工程 DOF 约 ±1.5～2.0 mm；f=254 mm 增至 ±3.5～5.0 mm」，并称「当表面深度变化超过 5～50 mm 时，动态 Z 轴补偿是强制性的」[来源](https://www.meenjet.net/news/laser-marking-curved-surfaces-dynamic-focal-depth.html)。原文把 f=160mm 误写为「F=160nm」，属二手来源，仅作量级参考。

**关于动态聚焦的定位（🟡 二手）**：该文称「动态聚焦系统把高速**音圈或压电驱动**的光学元件置于 X-Y 振镜之前」，可标记表面法向角至 60°–75°[来源](https://www.meenjet.net/news/laser-marking-curved-surfaces-dynamic-focal-depth.html)。

---

## 2. 两种技术路线对比

### (a) 机械式 z-shifter（移动光学镜组改变系统焦距）

**✅ 一手（SCANLAB 原理原文）**：varioSCAN II「通过**移动光学元件**扩展入射激光束，然后由**固定光学元件**准直或聚焦」，因此有两种配置：**Type FT（配 F-Theta 物镜）或 Type PR（PRefocus，预聚焦）** —— 即「有或没有 F-Theta 物镜的系统配置都能用」[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)

**✅ 一手（SCANLAB 老款 varioSCAN 的工作原理，更明确）**：「扫描过程中，varioSCAN 内的**发散光学元件**相对于**固定聚焦光学元件**沿光轴高动态定位，产生整个系统**总焦距的变化**，并与振镜运动同步」[来源](https://pdf.directindustry.com/pdf/scanlab-gmbh/varioscan-20-varioscan-40-varioscan-40flex/39164-169746.html)（🟡 该页为 DirectIndustry 转载的 SCANLAB 手册，属二手镜像）

**✅ 一手（RAYLASE 原理原文）**：「在预聚焦偏转单元中，激光束先进入一个**移动镜头——Linear-Translator-Module**。移动镜头使光束迅速发散，随后通过一片或两片聚焦镜。**预聚焦单元的焦点补偿是通过在振镜把光束扫过工作场时，微调移动镜头与聚焦镜之间的距离来实现的，由第三个移动 Z 轴完成**」[来源](https://www.raylase.de/en/products/prefocusing-deflection-units.html)

**关键架构差异（✅ 一手）**：RAYLASE AXIALSCAN RD-14「与 F-Theta 方案不同，**激光在扫描振镜之前就被聚焦**，因此**偏转角可以被完全利用**，从而实现更大的加工场」[来源](https://www.raylase.de/en/products/prefocusing-deflection-units.html)。这正是「预聚焦架构 + 内置 Z 轴」与「场镜架构 + 外挂 z-shifter」的分野。

### (b) 扫描头内部的 Z 轴（一体式 3 轴头）

**✅ 一手**：Novanta LIGHTNING II 把 **DFM 做进扫描头内部**（模块化 z 轴一体式设计），「DFM 确保光斑在整个工作场保持聚焦」[来源](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf)
**✅ 一手**：SCANLAB excelliSHIFT 是**外挂式但基于振镜技术**的 Z 轴，**只用反射光学元件**（无透射元件）→ 不同波长无色散、热透镜效应小[来源](https://www.scanlab.de/sites/default/files/2025-06/SCANLAB-excelliSHIFT-EN.pdf)

---

## 3. 关键指标与厂商参数表

### 3.1 SCANLAB excelliSHIFT —— ✅ 一手

| 指标 | 数值 |
|---|---|
| 孔径 Aperture | **14 mm** |
| 波长 | 515–532 nm、1030–1070 nm（其他波长可定制） |
| 光束扩束 | 1 倍 |
| **聚焦行程 Focus range** | **±14 mm** |
| **聚焦速度（像场内）** | **最高 30 m/s**（配 f-θ 场镜 f=160 mm；更长焦距时更高） |
| **跟踪误差 Tracking error** | **0.1 ms** |
| 光束引导 | **反射式**（无透射元件） |
| 激光功率（带冷却） | 120 W（绿光）/ 200 W（红外） |
| 尺寸 / 重量 | 115 × 160 × 142 mm³ / 3.7 kg |
| 接口 | SL2-100、POWER IN |

[来源](https://www.scanlab.de/sites/default/files/2025-06/SCANLAB-excelliSHIFT-EN.pdf)（页面上同时列出「Focus stroke ±14 mm」，见 [PDF 目录页](https://pdf.directindustry.com/pdf/scanlab-gmbh/excellishift/39164-992718.html)）
**✅ 一手**：官方页面补充「Z 扫描器不再是限制因素，因此**三个空间方向可以达到相同的加速度**」「仅使用反射光学元件，允许使用不同波长而无色散，并在高功率应用中减少热透镜效应」[来源](https://www.scanlab.de/en/products/z-axes-3d-add-ons/excellishift)

### 3.2 SCANLAB varioSCAN II / varioSCANde II —— ✅ 一手

**动态与电机（注意：手册明确「以下规格仅针对电机本身，其对加工场/体积内实际光束定位的影响取决于具体光学配置」）**

| 指标 | varioSCANde II 20i | varioSCANde II 40i (FLEX) |
|---|---|---|
| **跟踪误差** | **0.55 ms** | **0.70 ms** |
| **移动镜最大行程** | **±2 mm** | **±3 mm** |
| **移动镜典型速度** | **≤ 280 mm/s** | **≤ 140 mm/s** |
| **长期漂移（>8 h）** | **< 3 µm** | **< 3 µm** |
| **重复精度 Repeatability** | **< 0.5 µm** | **< 0.5 µm** |
| 共光路孔径 | 4–7 mm | 8–18 mm |
| 典型出射光束直径 | ≤ 20 mm | ≤ 40 mm |
| 扩束系数 | 2–5 | 1.4–3.8 |
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

[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)
**⚠️ 我的算术（聚焦增益）**：把上表换算成「聚焦偏移 / 移动镜行程」的放大倍数：

| 配置 | 场镜 f | 移动镜行程 | 聚焦偏移 | 增益 |
|---|---|---|---|---|
| 20i / 20-20 FT | 163 mm | ±2 mm | ±32 mm | **16.0×** |
| 20i / 20-133 FT | 100 mm | ±2 mm | ±4 mm | **2.0×** |
| 40i / 40-116 PR | PR 850 mm | ±3 mm | ±20 mm | **6.7×** |

→ **同一个 Z 轴电机，配不同光学配置时聚焦行程可差 8 倍**，选型必须按「整机配置」而非「电机行程」看。

**✅ 一手（iDRIVE 实时回读）**：「数字式 varioSCANde II 系统采用 iDRIVE 技术，**可实时回读实际位置**及其他状态」[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)
**✅ 一手（老款对比）**：「varioSCANde i 的最大行程是常规 varioSCAN 的**两倍**，跟踪误差**低得多**，因此聚焦偏移范围更大、光斑质量更好；精度、速度、分辨率与线性度也明显优于所有其他 varioSCAN，并大幅消除漂移影响」[来源](https://pdf.directindustry.com/pdf/scanlab-gmbh/3d-focusing-systems-varioscan-varioscande/39164-260795.html)（🟡 二手镜像）

### 3.3 RAYLASE FOCUSSHIFTER DIGITAL II —— ✅ 一手

**Linear Translator Module（即 Z 轴执行机构）**

| 指标 | LT-II-F2-05 [TY] | LT-II-F3-05 [DY] V4 | LT-II-F3-05 [Y] V4 | LT-II-F1.5-10 [C] |
|---|---|---|---|---|
| **镜头行程 Lens travel** | **11 mm** | **11 mm** | **11 mm** | **11 mm** |
| 波长 | 355 nm | 532 nm | 1064 nm | 10600 nm |
| 输入孔径 | 5 mm | 5 mm | 5 mm | 10 mm |
| 扩束系数 | 2 | 3 | 3 | 1.5 |
| **聚焦范围 Focus range** | **±19.0 mm** | **±17.0 mm** | **±16.0 mm** | **±9.0 mm** |
| 场尺寸示例 | ≈67×67 mm² | ≈75×75 mm² | ≈66×66 mm² | ≈145×145 mm² |
| 工作距离 | 345 mm ± 聚焦范围 | 228 mm ± | 222 mm ± | 264 mm ± |
| **光斑直径 1/e²** | **12 µm** | **12 µm** | **24 µm** | **360 µm** |
| 最大连续功率 | 100 W | 500 W | 1000 W | 500 W |

注：场尺寸与焦距按 **f-θ 场镜 f = 160 mm**（[C] 型为 f = 250 mm）计；输入光束质量 M² = 1.0。[来源](https://www.raylase.de/_Resources/Persistent/5/b/9/0/5b9058dcb0c4f361859551b86d9c55d6d35478d1/RAYLASE%20FOCUSSHIFTER%20DIGITAL%20II_en.pdf)

**通用规格与偏转单元**

| 指标 | 数值 |
|---|---|
| 供电 | +30 V 或 +48 V；4 A RMS，最大 8 A |
| 环境温度 | +15 … +35 °C |
| **分辨率 XY2-100-E（16 bit）** | **12 µrad** |
| **分辨率 SL2-100（20 bit）** | **0.76 µrad** |
| **跟踪误差 LT-II-F** | **1.3 ms** |
| **聚焦镜加工速度 Processing speed focus lens** | **880 mm/s** |
| 偏转单元孔径 | 10 mm（SS-IV-10 SI [TY]）/ 15 mm（SS-IV-15、SS-V-15 系列） |
| 偏转典型角度 | ±0.393 rad |
| 重复精度 RMS | < 2.0 µrad（IV 系列）/ < 0.4 µrad（V 系列） |
| 位置噪声 RMS | < 4.5 µrad（IV）/ < 2.0 µrad（V） |
| 长期漂移 8 h（无水冷） | < 60 µrad（IV）/ < 50 µrad（V） |
| 长期漂移 8 h（带水冷 22 °C） | < 40 µrad（IV）/ < 30 µrad（V） |
| 防护等级 | IP 54 |
| 接口 | **XY2-100-Enhanced 与 SL2-100 双协议兼容**，由 SP-ICE-3 / SP-ICE-1 PCIe PRO 等控制卡驱动 |

[来源](https://www.raylase.de/_Resources/Persistent/5/b/9/0/5b9058dcb0c4f361859551b86d9c55d6d35478d1/RAYLASE%20FOCUSSHIFTER%20DIGITAL%20II_en.pdf)

**✅ 一手（分辨率与功率级的卖点）**：「FOCUSSHIFTER DIGITAL II 偏转单元可实现小光斑、软件控制的 Z 向灵活聚焦、高偏转速度、长期稳定性和极低的漂移值，**位置分辨率 20 bit**」；由于采用数字 PWM 输出级，**热发展最小化**；模块化设计适配 10 mm 与 15 mm 孔径[来源](https://www.raylase.de/en/products/focusshifter/focusshifter-digital-ii.html)

**✅ 一手（AXIALSCAN RD-14）**：3D 偏转单元，「借助预聚焦光学做平场校正，可**利用最大加工场**，并借助 **RAYVOLUTION DRIVE 技术**仍能非常动态地调整焦点 Z 位置」；面向中功率、中大加工场，`600×600 mm²` [来源](https://www.raylase.de/en/products/prefocusing-deflection-units/axialscan-rd-14.html)、[新闻稿](https://www.raylase.de/en/products/prefocusing-deflection-units.html)
**❌ 未找到**：RAYLASE「RAYVOLUTION DRIVE」独立产品页（`/en/products/rayvolution-drive.html` 返回 **HTTP 404**）与 **FOCUSSHIFTER II / FOCUSSHIFTER RD-14 的独立数据手册**（相关 URL 抓取到的都是站点导航/404 页面），因此**没有拿到 RAYVOLUTION DRIVE 的行程/速度/精度数字**。可确认的只有：它是 AXIALSCAN/FOCUSSHIFTER 系列使用的 RAYLASE 自有 Z 轴驱动技术名称。

### 3.4 Novanta（Cambridge Technology）LIGHTNING II 3 轴扫描头 + DFM —— ✅ 一手

| 指标 | 20 mm 孔径型 | 30 mm 孔径型 | 50 mm 孔径型 |
|---|---|---|---|
| 扫描角 | ±20° | ±22° | ±22° |
| 典型加工速度 | 50 rad/s | 50 rad/s | 18 rad/s |
| 场尺寸范围 | 200–2500 mm | 100–1200 mm | 100–1200 mm |
| 输入光束 | 1–3 mm \| 2–3 mm | 10 mm \| 17 mm | 20 mm \| 17 mm |
| **跟踪延迟 Tracking Delay** | **0.2 ms** | **0.2 ms** | **0.4 ms** |
| **指令分辨率 Command Resolution** | **24-bit** | **24-bit** | **24-bit** |
| 重复精度 | <2 µrad | <2 µrad | <2 µrad |
| 长期漂移（8 h） | <10 µrad | <10 µrad | <10 µrad |
| 热漂移 | <2 µrad/°C | <2 µrad/°C | <2 µrad/°C |

另外按波长给出**跟踪误差**：CO₂/光纤/UV 各表均为 **0.2 ms（30 mm 孔径）/ 0.4 ms（50 mm 孔径）**[来源](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf)
**❌ 未找到**：LIGHTNING II 的 **DFM Z 轴行程（±mm）、Z 轴速度、Z 轴重复精度**在任何公开数据手册中均未列出（数据手册只给扫描头整体指标）。厂商页面同样只描述「DFM 提供动态焦点控制」[来源](https://novanta.com/precision-manufacturing/product/lightning-ii-3-axis-scan-head/)。

### 3.5 横向对比（汇总，含口径差异提醒）

| 方案 | 类型 | 聚焦行程 | 行程/速度/精度口径 | 跟踪误差 | 分辨率 |
|---|---|---|---|---|---|
| SCANLAB excelliSHIFT | 外挂，反射式，振镜技术 | **±14 mm** | 像场内 **30 m/s** | **0.1 ms** | 未公布（控制器侧） |
| SCANLAB varioSCANde II 20i | 外挂，透射式 | ±32 mm（配 f=163） | 移动镜 **≤280 mm/s**，重复 **<0.5 µm**，漂移 <3 µm/8h | **0.55 ms** | 未公布 |
| SCANLAB varioSCANde II 40i | 外挂，预聚焦 | ±20 mm（配 PR 850） | 移动镜 **≤140 mm/s**，重复 **<0.5 µm**，漂移 <3 µm/8h | **0.70 ms** | 未公布 |
| RAYLASE FOCUSSHIFTER DIGITAL II | 一体式 3 轴偏转单元 | **±9 … ±19 mm** | 镜头行程 **11 mm**，聚焦镜 **880 mm/s** | **1.3 ms** | **16 bit = 12 µrad / 20 bit = 0.76 µrad** |
| Novanta LIGHTNING II DFM | 一体式 3 轴头 | ❌ 未公布 | ❌ 未公布 | **0.2 / 0.4 ms**（头整体） | **24-bit** |

**⚠️ 口径警告**：「跟踪误差 0.1 ms vs 1.3 ms」不是同一物理量的严格对比 —— SCANLAB 与 RAYLASE 都把它作为**跟随误差时间常数（servo lag / drag）**给出，乘以扫描速度才是位置误差。**⚠️ 我的算术**：RAYLASE 聚焦镜 880 mm/s × 1.3 ms ≈ **1.14 mm** 滞后；excelliSHIFT 29.6 m/s（= 0.185 rad × 160 mm） × 0.1 ms ≈ **2.96 mm** 滞后。→ **高速扫描时 Z 滞后可达毫米级，这是必须做延迟补偿的定量理由。**（速度换算：RAYLASE 手册给出「加工场速度 = 场镜焦距 × 定位速度」，例：f=254 mm、40 rad/s → 10.1 m/s[来源](https://www.raylase.de/_Resources/Persistent/5/b/9/0/5b9058dcb0c4f361859551b86d9c55d6d35478d1/RAYLASE%20FOCUSSHIFTER%20DIGITAL%20II_en.pdf)）

---

## 4. 焦距变化对光斑的影响 /「in-focus zoom」

**✅ 一手（光斑尺寸公式，Thorlabs F-Theta 教程）**：衍射极限扫描镜的光斑尺寸
$$\text{Spot Size}=\frac{C\,\lambda f}{A}$$
其中 Spot Size 为 1/e² 光束直径，λ 波长，$f$ 有效焦距，$A$ 入射光束直径，$C$ 为与光瞳填充/截断程度相关的常数（高斯光束在 1/e² 处截断时 **C = 1.83**）。场尺寸 $L = f\cdot\theta$（L 为方形场对角线，θ 为最大偏转角）[来源](https://www.govolition.com/product/V40-FTH160-1064)
**✅ 一手（RP Photonics 同义表述）**：「焦距与输入光束半径（假定准直）共同决定靶面光束半径：**输入光束越大，光斑越小**」[来源](https://www.rp-photonics.com/scanning_lenses.html)

**⚠️ 我的推导（基于上面的一手公式）**：$d\propto f\cdot\lambda/A$。移动镜组改变系统焦距时：
- 若 **A 不变**（典型 z-shifter）→ **光斑直径随 f 线性变化**；
- 若让 **A/f 保持恒定**（即同步改变扩束比）→ **光斑直径不变**，这就是「in-focus zoom / 光学变焦」。

**✅ 一手（RAYLASE 明确区分「散焦放大」与「变焦放大」——这是本题最关键的厂商原文）**：
- **散焦放大（defocus）**：「最简单的动态放大光斑直径的方法是**把焦点移到加工面下方**（通过 Z 轴）。这会导致粉末中光斑直径增大。……但这导致**焦点外光束形状定义不良**，离焦光斑**不再保持原有能量分布，而是变得模糊**」。对单模激光束轮廓仍「类高斯」，但对**平顶或环形（ring mode）轮廓，光束形状直接丢失**。且「光斑内的功率分布强烈依赖离焦量，必须**对每个放大倍率实验测定**分布并专门开发工艺参数」[来源](https://www.raylase.de/en/applications/additive-manufacturing/in-focus-spot-magnificantion-in-additive-manufacturing.html)
- **光学变焦（zoom）**：「连续放大无法用标准偏转单元实现，**需要光路中额外的可动望远镜（telescope）**，用于扩展预聚焦偏转单元。因为**焦点处最小光斑直径也随光束直径变化**，这样的变焦光学让你**在不离开焦平面的前提下连续调整焦点直径**。这样原始光束轮廓仍被清晰成像，对平顶和环形这类特殊光束形状尤其重要」[来源](https://www.raylase.de/en/applications/additive-manufacturing/in-focus-spot-magnificantion-in-additive-manufacturing.html)
- **变焦的物理限制**：「放大倍率的限制因素包括光路中的自由孔径、偏转单元内的可用空间，以及反射镜与光学元件的功率兼容性」[来源](https://www.raylase.de/en/applications/additive-manufacturing/in-focus-spot-magnificantion-in-additive-manufacturing.html)

**✅ 一手（in-focus zoom 的独立卖点）**：RAYLASE 把 "IN-FOCUS SPOT MAGNIFICATION IN ADDITIVE MANUFACTURING" 作为独立应用页，理由是「用散焦做传统光斑放大**会对焦斑轮廓产生负面影响**」；「通过变焦光学，焦点直径可**连续调整而不牺牲成像质量**，即使环形或平顶等复杂光斑轮廓也能**无质量损失地放大**」[来源](https://www.raylase.de/en/applications/additive-manufacturing/in-focus-spot-magnificantion-in-additive-manufacturing.html)

**⚠️ 重要概念澄清（我的归纳）**：所谓「保持光斑不变」有两种截然不同的诉求，**不要混为一谈**：
1. **Z 轴升降但光斑不变**（真正的 z-shifter 设计目标）：只改变入射到场镜的光束**发散度/波前曲率**，使焦点沿轴移动，而**场镜孔径上的光束直径 A 基本不变** → 光斑尺寸基本不变，f-θ 标定 $y=f\theta$ 也不变 → **场尺寸不变**。这正是 varioSCAN 型「移动发散镜 + 固定聚焦镜」架构的巧妙之处（原理见 [SCANLAB 手册](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)）。
2. **变焦放大但焦点不离面**（in-focus zoom）：同时改变 A 与 f 的比例，光斑直径改变但焦点始终在焦面上，需**额外的可动望远镜**（RAYLASE 原文）。

**⚠️ 若 Z 轴真的改变系统焦距（i.e. 改变了入射到 X-Y 振镜的准直度），则 $y=f\theta$ 关系随之改变 → 场尺寸随 f 缩放**。SCANLAB 把这类能力明确命名为 **varioSCAN II FLEX「可变调整像场尺寸与工作距离」**[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)，RAYLASE 也把「**改变工作距离、场和光斑尺寸**」列为预聚焦单元的能力[来源](https://www.raylase.de/en/products/prefocusing-deflection-units.html)。**这与「只移动焦点、场尺寸不变」是互斥的两种使用模式。**

---

## 5. 驱动方式对比

**✅ 一手（厂商对自己执行机构的定性）**：

| 方案 | 执行机构 | 来源原文 |
|---|---|---|
| SCANLAB varioSCAN / 40FLEX | **高性能无倾斜直线电机（tilt-free linear motor）** | 「使用高性能、无倾斜的直线电机沿光轴快速精确移动激光焦点」[来源](https://pdf.directindustry.com/pdf/scanlab-gmbh/varioscan-20-varioscan-40-varioscan-40flex/39164-169746.html)（🟡 二手镜像） |
| SCANLAB varioSCAN II | **电机块（Motor block）** 驱动 moving optics | 「Watercooled entrance aperture / Motor block / Moving optics / Fixed optics」结构图 [来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf) |
| SCANLAB excelliSHIFT | **振镜（galvanometer）技术** | 「基于久经验证的振镜技术，全新设计大幅提升动态性能」[来源](https://www.scanlab.de/sites/default/files/2025-06/SCANLAB-excelliSHIFT-EN.pdf) |
| RAYLASE FOCUSSHIFTER | **Linear Translator Module（直线平移模块）**，数字 PWM 输出级 | 「数字化控制高速 Z 轴」「数字 PWM 输出级大幅降低功率损耗与热发展」[来源](https://www.raylase.de/_Resources/Persistent/5/b/9/0/5b9058dcb0c4f361859551b86d9c55d6d35478d1/RAYLASE%20FOCUSSHIFTER%20DIGITAL%20II_en.pdf) |
| Novanta LIGHTNING II DFM | 未公开具体执行器类型（仅称 Dynamic Focusing Module） | [来源](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf) |

**🟡 二手（驱动方式的通用对比，各执行器族的行程/响应量级）**：

| 驱动 | 典型行程 | 响应/带宽 | 备注 |
|---|---|---|---|
| 压电堆栈（piezo stack） | **100 µm 级** | **微秒级响应** | 厂商原文：「在 100 µm 行程上提供纳米级分辨率，**微秒级响应时间**，封装非常紧凑」[来源](https://www.newport.com/p/NPA100)（一手，但是显微镜用器件，非扫描头） |
| 压电（放大式/电机式） | 亚毫米～毫米 | 高刚度、高带宽 | 力/带宽/热负载对比[来源](https://thepiezodesk.com/technology/piezo-vs-voice-coil)（🟡） |
| 音圈（voice coil） | **数十 µm ～ 数 mm** | 高带宽、力中等 | 「音圈、直线电机与超声压电三类执行器对比」[来源](https://xeryon.com/voice-coil-actuators-vs-linear-motor-vs-ultrasonic-piezo-actuators/)（🟡）；「行程从零点几毫米起…常选直驱：直线电机、压电电机或音圈」[来源](https://www.linearmotiontips.com/piezo-motors-voice-coil-actuators-micron-and-sub-micron-positioning/)（🟡） |
| 直线电机 | **数 mm ～ 数百 mm** | 高加速度、大力 | 「直线电机平台通常用于需要大力、行程超过几百毫米的场合」[来源](https://www.linearmotiontips.com/piezo-motors-voice-coil-actuators-micron-and-sub-micron-positioning/)（🟡） |
| 步进 | 大行程 | 慢、有离散步距 | ❌ **未找到**用于扫描头 Z 轴动态聚焦的公开实例 |

**⚠️ 与真实产品的对应关系（我的判断）**：
- **压电**行程太短（100 µm 级），**不适用于扫描头 Z 轴的 ±mm 级行程**——❌ 未找到任何扫描头厂商用压电堆栈做 Z 轴的公开证据。
- **音圈**是扫描头 Z 轴的常见选择（🟡 行业文章：「动态聚焦系统把高速音圈或压电驱动的光学元件置于 X-Y 振镜前」[来源](https://www.meenjet.net/news/laser-marking-curved-surfaces-dynamic-focal-depth.html)）。
- **直线电机**是 SCANLAB varioSCAN 明确采用的方案（✅ 见上表）。
- **有限行程 + 需要 mm 级精度 + 需要高速**这三者共同把选择收敛到「无铁芯直线电机 / 音圈」这一类直驱方案。

---

## 6. 控制与标定

### 6.1 Z 轴与 XY 同步 / 延迟补偿

**✅ 一手（3D 标定的官方工具）**：SCANLAB **laserDESK 3D Calibration Wizard** —— 「一个**对话驱动的工具，极大简化了原本高度复杂的 3 轴扫描系统标定**。智能助手引导用户完成整个复杂标定流程，最终**为整个系统生成个性化的 3D 校正文件（.ct5）**」，兼容 RTC5/RTC6 控制卡[来源](https://www.scanlab.de/en/products/calibration/hardware-configuration-and-control)
**✅ 一手**：RTC 校正文件用于「**补偿两镜扫描系统及其光学系统固有的像场畸变，确保在平面或工作体积内精确扫描**」[来源](https://www.scanlab.de/sites/default/files/2020-08/CalibrationSolutions.pdf)

**✅ 一手（标定精度分级，SCANLAB 官方，f=163 mm 典型值）**：

| 方案 | 工具 | 精度 | 工作量 |
|---|---|---|---|
| RTC 校正文件（标准） | 出厂预计算 *ctb/*ct5 | **< 150 µm** | 低 |
| CALsheet | 智能手机/数码相机 | **< 50 µm** | 中 |
| CALsheet | 平板扫描仪 | **< 30 µm** | 中 |
| correXion pro | 三坐标测量机 | **< 20 µm** | 高 |

[来源](https://www.scanlab.de/sites/default/files/2020-08/CalibrationSolutions.pdf)

**✅ 一手（correXion pro 的定位）**：「额外的 correXion pro 标定用于**最小化个体制造公差与非线性**」[来源](https://www.scanlab.de/en/products/calibration/correxion-pro)

**✅ 一手（滞后补偿的厂商功能名）**：SCANLAB 控制/工艺控制页列出 **Sky Writing（含前导运动缩放的 sky writing）**、**SCANahead**、**SCAN motionControl**（「在存在 drag delay 的系统中通过优化轨迹实现生产率与质量」）[来源](https://www.scanlab.de/en/regulation-and-process-control)
**✅ 一手**：excelliSHIFT「现在还提供带 **SCANahead** 技术的版本」[来源](https://www.scanlab.de/sites/default/files/2025-06/SCANLAB-excelliSHIFT-EN.pdf)
**❌ 未找到**：SCANLAB 公开文档中 Z 轴的**具体延迟补偿算法/参数**（如 z 前导量计算公式）。RTC6 手册 PDF 在本次环境多次抓取超时，未能读到命令级细节。

### 6.2 分辨率不足（RTC4 只有 16 bit）的后果

**✅ 一手（RTC4 / RTC5 的位深与分辨率对比原文）**：
- RTC4：「每 **10 µs** 发送一次 **16-bit** 控制信号，执行微矢量化与像场校正」[来源](https://pdf.directindustry.com/pdf/scanlab-gmbh/rtc4/39164-694240.html)（🟡 二手镜像）；RTC4 规格页：「XY2-100 **enhanced** 协议，**16-bit 定位分辨率**，**10 µs 输出周期**」[来源](http://www.ainnotech.com/ainnotech/pdf/02/1_3/3SCAN-RTC4-Control%20And%20Versatility.pdf)（🟡 经销商镜像）
- RTC5：「通过新的 **SL2-100** 数据传输协议与扫描系统通信。该协议支持 **20-bit 控制信号**，因此与 RTC4 前代板相比**定位分辨率提高 16 倍**」[来源](https://www.scanlab.de/sites/default/files/2020-08/13_RTC5_control%20boards.pdf)
- SL2-100 由 SCANLAB 开发并推出，RTC5/RTC6 支持[来源](https://www.scanlab.de/en/applications/micromachining)

**⚠️ 我的算术（位深 → LSB 尺寸，按不同聚焦行程）**：

| 位深 | 全行程 22 mm | 全行程 28 mm | 全行程 38 mm |
|---|---|---|---|
| **16 bit** | 0.336 µm/LSB | **0.427 µm/LSB** | 0.580 µm/LSB |
| 18 bit | 0.084 µm/LSB | 0.107 µm/LSB | 0.145 µm/LSB |
| 20 bit | 0.021 µm/LSB | 0.027 µm/LSB | 0.036 µm/LSB |
| 24 bit | 0.0013 µm/LSB | 0.0017 µm/LSB | 0.0023 µm/LSB |

（算式：LSB = 全行程 / 2^bits，如 28 mm / 65536 = 0.427 µm）

**后果归纳（我的分析，非单一来源）**：
1. **量化台阶**：16 bit 在 ±14 mm 行程上每级约 0.43 µm。单看这个数字远小于景深（30 µm 光斑 DOF ≈ ±0.66 mm），**所以「16 bit 不足以定位焦点」这个说法不成立**。
2. **真正的问题是标定与增益**：3D 校正文件把 Z 指令映射到实际焦点位置，若中间还有机械/光学增益（见 §3.2 的 2×–16× 聚焦增益），**实际焦点分辨率 = LSB × 聚焦增益**。⚠️ 我的算术：16 bit、±32 mm 聚焦行程（20i 配置）→ 64 mm/65536 = **0.98 µm/LSB**；20 bit → **0.061 µm/LSB**（16 倍改善）。
3. **与 XY 不同量纲**：XY 的 16 bit 覆盖 ±0.393 rad 全角，1 LSB ≈ 12 µrad（RAYLASE 数据手册给的正是这个换算）[来源](https://www.raylase.de/_Resources/Persistent/5/b/9/0/5b9058dcb0c4f361859551b86d9c55d6d35478d1/RAYLASE%20FOCUSSHIFTER%20DIGITAL%20II_en.pdf)；同一份手册里 **20 bit 给出 0.76 µrad**，正好是 **16 倍**改善，与分析一致。
4. **低速爬行/抖动**：分辨率不足在低速精修时会表现为**台阶式跳动**，而不是误差累积；这在高倍显微加工中才可见。
5. ❌ **未找到**任何公开文档把 RTC4 的 16 bit 明确指为 Z 轴精度瓶颈的定量分析。厂商的实际做法是**用 20/24 bit 的新协议（SL2-100 / RL3-100 / 24-bit 指令）绕开这个问题**。

### 6.3 Z 轴位置标定方法

**✅ 一手（软件侧标定路径）**：SCANLAB laserDESK 3D Calibration Wizard 生成 **.ct5 三维校正文件**[来源](https://www.scanlab.de/en/products/calibration/hardware-configuration-and-control)；correXion pro 用**三坐标测量机**逐点测量网格实际位置后生成校正文件（< 20 µm）[来源](https://www.scanlab.de/sites/default/files/2020-08/CalibrationSolutions.pdf)
**✅ 一手（自动化标定仪器）**：RAYLASE 提供 **SCAN FIELD CALIBRATOR** 与 **RAYDIME / RAYSPECTOR** 图像处理与测量系统作为标定工具链[来源](https://www.raylase.de/en/products/prefocusing-deflection-units.html)
**❌ 未找到（本环境）**：刀口法（knife-edge）、焦斑法（burn paper / ablation）、共聚焦/色散共焦传感器用于**激光扫描头 Z 轴**标定的厂商一手文档。文献侧仅在加工测量领域找到色散共焦传感器的应用（如「基于色散共焦传感器的在机测量系统，同步采集传感器数据与运动轴实时位置」[来源](https://www.sciencedirect.com/science/article/pii/S0141635921002956)，🟡 摘要级）。

---

## 7. Z 轴补偿的数学模型

**✅ 一手（基本关系，平场/预聚焦两套公式）**：
- **F-θ 场镜架构**：焦斑位置 $y=f\cdot\theta$（y 为距场中心距离，f 为有效焦距，θ 为扫描角）[来源](https://www.govolition.com/product/V40-FTH160-1064)
- **预聚焦架构**：调整「移动镜与聚焦镜之间的距离」来补偿弧线焦面 → Z 是 **(x, y) 的函数**，因为弧面高度只取决于离场中心的径向距离[来源](https://www.raylase.de/en/products/prefocusing-deflection-units.html)
- **场尺寸**：$L=f\cdot\theta$，L 为方形场对角线[来源](https://www.govolition.com/product/V40-FTH160-1064)

**⚠️ 我的数学模型（基于上述一手几何关系推导，非厂商公式）**：
1. **理想球面焦面的补偿量**（无限远共轭、镜间距忽略）：
   $$z_{\text{corr}}(x,y)=-\left(\sqrt{f^2+x^2+y^2}-f\right)\approx-\frac{x^2+y^2}{2f}$$
   数值算例（f=160 mm，幅面 ±100 mm）：角点 $(100,100)$ → $\sqrt{160^2+100^2+100^2}-160=200-160=$ **40.0 mm**；边中点 $(100,0)$ → **28.7 mm**。→ **补偿量是二维抛物面，角点约为边中点的 1.4 倍**。
2. **实测焦面校正（工程做法）**：用 $z_{\text{corr}}(x,y)=-\big(a_1 r^2+a_2 r^4+\cdots\big)$（$r^2=x^2+y^2$）做最小二乘拟合，系数 $a_1,a_2$ 由 3D 标定文件（.ct5）承载[来源](https://www.scanlab.de/en/products/calibration/hardware-configuration-and-control)。SCANLAB 明确建议「**把零曲率点放在扫描范围中段**以限制整个扫描过程中的场曲量」→ 即拟合时应让残差在场上呈对称正负分布[来源](https://www.govolition.com/product/V40-FTH160-1064)。
3. **任意曲面工件（含法向补偿）**：工件面 $z_w=Z(x,y)$，则
   $$z_{\text{focus}}(x,y)=Z(x,y)+\Delta_{\text{lens}}(x,y)$$
   其中 $\Delta_{\text{lens}}$ 为镜组残余场曲修正量。**法向入射/入射角修正**：若工件面法向与光束轴夹角为 $\varphi$，则**光斑在表面上的椭圆长轴被拉长 $1/\cos\varphi$ 倍**，功率密度按 $\cos\varphi$ 下降；$\varphi$ 超过某阈值后需改用旋转轴。🟡 二手：行业文章称多数 3D 动态聚焦系统可有效加工**表面法向角至 60°–75°**，超过 75° 后菲涅耳反射损失显著增大，需第四轴[来源](https://www.meenjet.net/news/laser-marking-curved-surfaces-dynamic-focal-depth.html)
4. **Z 与 XY 的时序关系**：因为三轴共用同一 10 µs 帧（见 §9），Z 指令与 XY 指令是**同步下发**的；但由于 Z 轴跟踪误差（0.1–1.3 ms）远大于 10 µs，**必须做前导/延迟补偿**，否则高速下 Z 滞后毫米级（§3.5 算例）。
5. **软件侧的实现证据**：EZCAD3 明确支持「真正的三轴控制（X、Y、Z）」，可导入 STL / IGES / STEP 做曲面打标[来源](https://www.ezcad.com/products/ezcad3-software/)（🟡 二手，但为软件厂商官方产品页）

---

## 8. 失效现象 → 原因对应

**❌ 未找到厂商一手的 Z 轴失效模式白皮书**。以下为可用的一手规格线索 **+ 🟡 二手故障排查指南**的交叉整理，**明确标注哪些是推断**：

| 现象 | 可能原因 | 依据 |
|---|---|---|
| **Z 轴卡死 / 自锁失效** | ① 电机自锁电路故障（连接线开路/短路、接线错误、保险丝熔断）；② 驱动器板故障；③ 机械卡滞 | 🟡「振镜电机不自锁：检查连接线是否开路或短路、接线是否正确、保险丝是否完好；确认无误后通电观察驱动板指示灯是绿还是黄」[来源](https://www.leadtech.ltd/solutions-to-common-faults-of-laser-marking-machine-galvanometer.html)；🟡「无声时用手轻推振镜镜片，若镜片不自锁…换一块确认完好的驱动板接上不自锁的电机」[来源](https://www.laserhome.com/Common-faults-and-treatment-methods-of-galvanometer-of-laser-marking-machine-id45739067.html) |
| **Z 轴异响 / 啸叫** | ① 调谐（tuning）与负载不匹配；② 伺服增益过高导致自激振荡；③ 轴承磨损；④ 共振 | 🟡 故障指南把「whistling sounds」与「motor self-lock issues」「lack of swing」「no laser output」并列为常见问题[来源](https://www.scanneroptics.com/common-issues-and-solutions-for-laser-scanner-galvanometer.html)；⚠️ **推断**：RAYLASE 数据手册提供 VC / W / H / M 四种 tuning 曲线（矢量/晶圆/影线/微加工），说明调谐参数与负载/轨迹类型强相关，不匹配会有动态表现异常[来源](https://www.raylase.de/_Resources/Persistent/5/b/9/0/5b9058dcb0c4f361859551b86d9c55d6d35478d1/RAYLASE%20FOCUSSHIFTER%20DIGITAL%20II_en.pdf) |
| **回零 / 参考位置丢失** | ① 编码器或位置反馈失效（varioSCANde 的 iDRIVE 支持实时回读实际位置——**没有回读的型号无法自查**）；② 限位/参考开关故障；③ 掉电后未做回零流程 | ⚠️ **推断 + 一手旁证**：SCANLAB 明确把「**Read-back function 回读功能**」和「**Better position stability 更好的位置稳定性**」列为 varioSCANde II 相对普通 varioSCAN 的**升级卖点**[来源](https://www.scanlab.de/en/products/z-axes-3d-add-ons/varioscan-ii)、[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf) —— 说明**位置可信度确实是 Z 轴的核心痛点** |
| **聚焦漂移（随时间的焦点偏移）** | ① **热漂移**：功率吸收导致热透镜效应；② 长期漂移（长期稳定性）；③ 冷却不足 | ✅ **一手定量**：varioSCANde II 长期漂移 **< 3 µm（>8 h）**[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)；excelliSHIFT 因**只用反射元件**而「减少热透镜效应」[来源](https://www.scanlab.de/sites/default/files/2025-06/SCANLAB-excelliSHIFT-EN.pdf)；✅ 光学侧原理：「高功率激光应用中，镜片材料与镀膜的吸收会导致**热透镜效应**，使**焦面发生位移（focal shift）**并劣化光束质量」[来源](https://www.rp-photonics.com/scanning_lenses.html)；✅ RAYLASE 水冷要求 22–28 °C、≥2 l/min，并注明「不带温度控制运行时**漂移值可能增大**」[来源](https://www.raylase.de/_Resources/Persistent/5/b/9/0/5b9058dcb0c4f361859551b86d9c55d6d35478d1/RAYLASE%20FOCUSSHIFTER%20DIGITAL%20II_en.pdf) |
| **加工面高度对但边缘虚焦** | 残余场曲 + 光斑太小（DOF < 残差）→ 需要 Z 补偿或换长焦/预聚焦架构 | ✅ 见 §1.1（由 DOF 判据与厂商原文推出） |

---

## 9. 接口：各协议怎么传 Z 轴

### 9.1 XY2-100 —— ✅ 一手（协议规格书原文）

**帧格式（20-bit 字，2 Mbit/s / 100 kwords/s / 帧周期 10 µs）**：
> 「XY2-100 接口用于把 X 和 Y 坐标从控制器发送到偏转系统。它是**串行接口，使用 20-bit 字，以 2 Mbit/s 或 100 kwords/s 的速度发送**。」「每个轴的数据由 **20-bit 字**组成。**前 3 bit 用作控制字（C2–C0）**，**接下来 16 bit 是数据信息（D15–D0，偏移二进制 offset binary）**，**最后 1 bit 是奇偶校验位（P，偶校验 even parity）**。」「SYNC 在第一个 bit 可发送时变高，**保持高电平 19 个 bit**，在奇偶校验位时变低。」「时钟频率 **2 MHz**：变高时数据位改变，变低时偏转系统采样数据位。」时序：data-in setup time tDS ≥ 50 ns，data-in hold time tDH ≥ 100 ns。
[来源](https://dvd.ilphotonics.com/Ray-Motion%20-%20galvanometers%20-%201D-2D-3D%20scanners/Motion%20Control%20-%20Optomechanics/Interface%20XY2-100.pdf)（Ray-Motion 官方技术数据表）

**✅ 一手：CHANNELZ 确实存在**：
> 「IO3 | **Channel Z** | + | Channel Z data. **如果 XY2-100 设备配置为 2D 传感器，此引脚不使用。**」「注意：**如果 XY2-100 设备配置为 3D 传感器，至少需要两个差分线驱动器**来支持**三个通道 + 同步信号 + 时钟信号**。」
[来源](https://github.com/hyperchao0/qspi4xy2-100)（开源实现，✅ 一手代码/文档级，但非标准组织）

**✅ 一手（控制器侧）**：RTC4 支持 XY2-100 **enhanced** 协议，**16-bit 定位分辨率**，**10 µs 输出周期**[来源](http://www.ainnotech.com/ainnotech/pdf/02/1_3/3SCAN-RTC4-Control%20And%20Versatility.pdf)（🟡 经销商镜像）
**✅ 一手（协议增强模式）**：XY2-100 标准模式**16-bit** 数据 + 偶校验；**增强模式（Enhanced）18-bit** 数据 + **奇校验**[来源](https://www.scribd.com/document/941573319/Xy2-100-Specification)（🟡 Scribd 上的规格书扫描件，未拿到原始 PDF）
**✅ 一手**：varioSCAN II eBox 明确「**SL2-100 与 XY2-100 变体可选**」[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)
**✅ 一手**：RAYLASE FOCUSSHIFTER DIGITAL II 兼容 **XY2-100（16 bit）** 与 **SL2-100（20 bit）**，并给出对应分辨率 12 µrad / 0.76 µrad[来源](https://www.raylase.de/_Resources/Persistent/5/b/9/0/5b9058dcb0c4f361859551b86d9c55d6d35478d1/RAYLASE%20FOCUSSHIFTER%20DIGITAL%20II_en.pdf)
**✅ 一手（XY2-100E）**：sigrok 协议解码器文档称「**XY2-100E 与 XY2-200E 是增强变体**，提供向扫描器发送额外命令的可能，用户可影响状态通道的格式；协议主要功能是**向扫描器提交 16-bit 有符号整数控制振镜位置，0 为中心**」[来源](https://sigrok.org/wiki/Protocol_decoder:Xy2-100)（🟡 开源项目 wiki）

### 9.2 XY3-100 —— 部分找到

**✅ 一手（定义方与商标）**：XY3-100 由 **LasIA e.V.** 定义与持有商标。LasIA 声明：「作为 XY3-100™ 协议与名称的版权与商标权所有者，LasIA 允许认为自己的 XY3-100 协议实现符合规范的厂商**把这些设备命名为『XY3-100 compatible』**」；要命名为「**XY3-100 certified**」或使用官方 logo、要保证与其他任何 XY3-100™ 认证设备的互操作性，**需要 LasIA 的正式许可**。[来源](https://sourceforge.net/p/lasia/blog/2023/07/xy3-100-digital-scanner-interface-version-11/)
**规范版本**：**XY3-100 Digital Scanner Interface version 1.1**（2023-07 发布公告）[来源](https://sourceforge.net/p/lasia/blog/2023/07/xy3-100-digital-scanner-interface-version-11/)
**❌ 未找到**：XY3-100 的**帧格式、第三轴（Z）具体传法、比特深度、时钟频率**的公开规范正文。可检索到的规格书资源为 Scribd 上传件（标题含 "Bit Rate"）[来源](https://www.scribd.com/document/951428348/xy3-100-specification-1)，未能取得原始文本。**本环境无法核实 XY3-100 的 Z 通道细节。**

### 9.3 SL2-100 —— ✅ 一手（厂商原文）

- **20-bit 控制信号**，由 **SCANLAB 开发并推出**；相比 RTC4 的 16-bit，**定位分辨率提高 16 倍**；RTC5 / RTC6 支持[来源](https://www.scanlab.de/sites/default/files/2020-08/13_RTC5_control%20boards.pdf)、[来源](https://www.scanlab.de/en/applications/micromachining)
- RAYLASE 侧规格：**SL2-100 协议，20 bit 位置分辨率，每个连接器最多 2 轴**[来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/48a53e4f-2a14-4518-ad32-d622848ab64a.htm)（✅ RAYLASE 官方用户手册）
- **Z 轴如何传**：SL2-100 的每个连接器最多承载 **2 轴**；3 轴系统通过**多个连接器/通道组**实现 —— 即 Z 作为**独立通道**与该连接器配对的另一轴共用一条链路。⚠️ **我的推断**（基于「最多 2 轴/连接器」这一手规格 + FOCUSSHIFTER 为 3 轴单元需同时接 X/Y 与 Z）：3 轴系统需要 **2 个连接器**。
- ✅ 一手：varioSCAN II eBox 有「**SL2-100 和 XY2-100 变体**」[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)
- 🟡 二手（物理层）：SL2-100 只有 **DataIn± 与 DataOut± 四条线**，支持 20 bit 扫描器分辨率，长距离传输比 XY2-100 更可靠[来源](https://www.photonlexicon.com/forums/showthread.php/28608-SL2-100-Protocol-for-scanner)（论坛，仅供参考）

### 9.4 RL3-100 —— ✅ 一手（RAYLASE 官方手册）

> 「**RL3-100 协议，20 bit 位置分辨率，每个连接器最多 6 轴。**」
> 「SL2-100 协议，20 bit 位置分辨率，每个连接器最多 2 轴。」
> 「XY2-100 协议，16 bit 位置分辨率（需选配适配器）。」
[来源](https://software.raylase.de/rpi/RAYLASE/spice3/usersmanual/html/48a53e4f-2a14-4518-ad32-d622848ab64a.htm)（RAYLASE SP-ICE 3 用户手册 §2.4 Interfaces）

**✅ 一手（SP-ICE 3 整体能力）**：「SP-ICE 3 通过 **SL2-100 或 RL3-100 协议控制最多 2 个偏转单元**，**20 bit 位置分辨率，10 µs 步进周期**；最多可记录来自偏转单元的 **2400 万条测量数据**」[来源](https://www.raylase.de/en/products/electronics-control-cards/sp-ice-3.html)

**→ 关键结论（我的归纳）**：RAYLASE 的 **RL3-100 是三者中唯一原生支持「单连接器 6 轴」的协议**，因此 3 轴（含 Z）系统用 **1 个 RL3-100 连接器**即可，比 SL2-100（2 轴/连接器，需 2 个连接器）更简洁。**20 bit = 相比 XY2-100 的 16 bit，Z 与 XY 的分辨率同时提高 16 倍。**
**❌ 未找到**：RL3-100 的电气层细节（差分对数量、帧结构、时钟频率、编码方式）——RAYLASE 未公开其专有协议的完整规格书。

### 9.5 接口横向对比表

| 协议 | 定义方 | 位数 | 更新率 / 步进周期 | 每连接器通道数 | Z 轴如何传 | 标注 |
|---|---|---|---|---|---|---|
| **XY2-100** | 早期行业事实标准（Precitec/SCANLAB 生态） | 标准 **16 bit** / 增强 **18 bit**；字长 20 bit | **时钟 2 MHz，帧周期 10 µs**（100 kwords/s） | **3 个数据通道（X / Y / Z）**+ SYNC + CLK，Z 通道在 2D 配置下不用 | **CHANNELZ 专用差分通道** | ✅ 一手 |
| **XY2-100 Enhanced** | 同上 | **18 bit** + 奇校验 | 10 µs | 同上 | 同上 | 🟡 二手 |
| **XY3-100** | **LasIA e.V.**（v1.1） | ❌ 未找到 | ❌ 未找到 | ❌ 未找到（预期 ≥3） | ❌ 未找到 | 定义方 ✅ / 细节 ❌ |
| **SL2-100** | **SCANLAB** | **20 bit** | 10 µs | **最多 2 轴** | Z 占用通道；3 轴需 2 个连接器（⚠️ 推断） | ✅ 一手 |
| **RL3-100** | **RAYLASE**（专有） | **20 bit** | **10 µs 步进周期** | **最多 6 轴** | **单连接器内即含 Z** | ✅ 一手 |
| Novanta LIGHTNING II | Novanta/Cambridge | **24-bit 指令分辨率** | ❌ 未找到 | 3 轴（DFM 集成） | 头内部集成 | ✅ 一手（分辨率） |

---

## ⚠️ 常见误解

1. **误解：「f-θ 场镜焦面是平面的，所以不需要 Z 轴。」**
   场镜只是把焦面**近似**做平。厂商自己承认残差存在（Thorlabs/Sill：「真实镜头很少达到理论值，总会存在一定的畸变与场曲」[来源](https://www.govolition.com/product/V40-FTH160-1064)、[来源](https://www.silloptics.de/en/service/sill-technical-guide/laser-optics/f-theta-lenses)）。而且**曲面工件根本无法用平面焦面对应**——RAYLASE 原文描述不校正时焦点「在工作场上方形成一个球面」，场外「根本没有聚焦」[来源](https://www.raylase.de/en/products/prefocusing-deflection-units.html)。**Z 轴的第一需求是 3D 曲面，不是补场曲。**

2. **误解：「f=160 mm 场镜在 ±100 mm 上的场曲是 28.7 mm / 31 mm。」**
   这是**未校正球面焦面**的几何矢高 $\sqrt{f^2+y^2}-f$，**不是 f-θ 场镜的真实残差**。场镜是多片平场设计，残差小得多。真正要比较的量是**残差 vs 景深 z_R = πw₀²/(M²λ)**：λ=1064 nm、光斑 12 µm 时 DOF 仅 ±0.106 mm，光斑 50 µm 时 DOF 达 ±1.85 mm（⚠️ 我的算术）。**❌ 未找到**公开的 f=160 mm 场镜「场曲残差 vs 扫描角」数字表（Thorlabs 的曲线是图片形式）。

3. **误解：「Z 轴就是把整个场镜前后移动。」**
   主流方案（varioSCAN / FOCUSSHIFTER / excelliSHIFT）**不是移动场镜**：varioSCAN 移动的是**镜组内的一片发散镜**，相对**固定的聚焦镜**运动，从而改变**系统总焦距**与入射场镜的发散度[来源](https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-varioSCANII-eBox-EN.pdf)、[来源](https://pdf.directindustry.com/pdf/scanlab-gmbh/varioscan-20-varioscan-40-varioscan-40flex/39164-169746.html)；RAYLASE 移动的是**预聚焦模块内的 Linear-Translator 镜头**，与「工作场之外的聚焦镜」距离微调[来源](https://www.raylase.de/en/products/prefocusing-deflection-units.html)。excelliSHIFT 甚至**只用反射元件**，完全没有透射光学件[来源](https://www.scanlab.de/sites/default/files/2025-06/SCANLAB-excelliSHIFT-EN.pdf)。

4. **误解：「用散焦（defocus）就能放大光斑，所以没必要做 in-focus zoom。」**
   RAYLASE 明确反驳：散焦放大使光斑**「定义不良」「变得模糊」**，**对平顶/环形光束轮廓直接丢失形状**，且功率分布随离焦量变化，**必须对每个倍率单独做实验标定工艺参数**。真正的 in-focus zoom 需要**光路中额外的可动望远镜**，才能在不离开焦平面的前提下连续调整焦点直径[来源](https://www.raylase.de/en/applications/additive-manufacturing/in-focus-spot-magnificantion-in-additive-manufacturing.html)。

5. **误解：「RTC4 只有 16 bit，所以 Z 轴精度不够。」**
   ⚠️ **未找到任何公开来源支持这个因果链**。16 bit 在 ±14 mm 行程上对应 **0.43 µm/LSB**（⚠️ 我的算术），远小于景深。16 bit 的真实短板是**相对 XY 同步通道的位深一致性**与**长距离传输可靠性**，厂商的应对是升级到 SL2-100/RL3-100 的 20 bit 或 24-bit 指令[来源](https://www.scanlab.de/sites/default/files/2020-08/13_RTC5_control%20boards.pdf)。**说「16 bit 不够」应改为「16 bit 在带聚焦增益的大行程配置下余量变小」**（±32 mm 聚焦行程 → 0.98 µm/LSB，⚠️ 我的算术）。

6. **误解：「excelliSHIFT 的 0.1 ms 与 FOCUSSHIFTER 的 1.3 ms 可以直接比。」**
   两者都是**跟随误差时间常数（拖曳）**，必须**乘以当时的 Z 向扫描速度**才是位置误差。⚠️ 我的算术：FOCUSSHIFTER 聚焦镜 880 mm/s × 1.3 ms ≈ **1.14 mm**；excelliSHIFT ≈29.6 m/s × 0.1 ms ≈ **2.96 mm**。**跟踪误差小 13 倍，但因为速度快 33 倍，绝对滞后反而更大。** 选型必须带速度一起算。

7. **误解：「Z 轴 = 三轴同步，所以不用补偿延迟。」**
   三轴共用 10 µs 帧下发（XY2-100 / SL2-100 / RL3-100 均为 10 µs 周期）[来源](https://dvd.ilphotonics.com/Ray-Motion%20-%20galvanometers%20-%201D-2D-3D%20scanners/Motion%20Control%20-%20Optomechanics/Interface%20XY2-100.pdf)、[来源](https://www.raylase.de/en/products/electronics-control-cards/sp-ice-3.html)，但**Z 的机械跟踪误差是 0.1–1.3 ms**，比帧周期大 **10–130 倍**。所以**指令同步 ≠ 位置同步**，必须靠 sky writing / SCANahead / drag delay 优化等机制补偿[来源](https://www.scanlab.de/en/regulation-and-process-control)。

8. **误解：「XY3-100 是 XY2-100 的 3 轴版，规格公开可查。」**
   XY3-100 由 **LasIA e.V.** 持有协议与商标权，「XY3-100 certified」需正式许可[来源](https://sourceforge.net/p/lasia/blog/2023/07/xy3-100-digital-scanner-interface-version-11/)，**但其帧格式与 Z 通道细节在本次调研中 ❌ 未找到公开规范正文**。**不要把 XY3-100 当成有公开标准的免费协议。**

9. **误解：「Novanta DFM 的参数和 SCANLAB/RAYLASE 一样可以列表比较。」**
   **❌ Novanta 公开数据手册完全没有 DFM 的 Z 轴行程、速度、重复精度**，只给出扫描头整体的 0.2/0.4 ms 跟踪延迟与 **24-bit 指令分辨率**[来源](https://novantaphotonics.com/wp-content/uploads/2021/11/datasheet_3_axis_scan_head_lightningII.pdf)。**做选型表时 DFM 列必须留空，不能填推测值。**

10. **误解：「场镜标称 70×70 到 156.7×156.7 mm，所以 f=160 能打 ±100 mm。」**
    Thorlabs FTH160-1064 的标称最大场是 **156.7 × 156.7 mm²**（对角线），**±100 mm（200 mm 幅面）超出该镜标称范围**[来源](https://www.govolition.com/product/V40-FTH160-1064)。要 200 mm 幅面必须换更长焦距场镜或改用预聚焦（AXIALSCAN / FOCUSSHIFTER）架构 —— 后者的场可以做到 600×600 mm² 甚至 2000×2000 mm²[来源](https://www.raylase.de/en/products/prefocusing-deflection-units.html)。

---

## 📋 来源可靠性清单（本次调研实际打开的文件）

| 状态 | 来源 | 类型 |
|---|---|---|
| ✅ 已读全文 | SCANLAB excelliSHIFT 数据手册 PDF | 厂商一手 |
| ✅ 已读全文 | SCANLAB varioSCAN II 手册 PDF | 厂商一手 |
| ✅ 已读全文 | RAYLASE FOCUSSHIFTER DIGITAL II 数据手册 PDF | 厂商一手 |
| ✅ 已读全文 | Novanta LIGHTNING II 数据手册 PDF | 厂商一手 |
| ✅ 已读全文 | RAYLASE SP-ICE 3 用户手册 §2.4 接口 | 厂商一手 |
| ✅ 已读全文 | Ray-Motion XY2-100 技术数据表 PDF | 协议规格书一手 |
| ✅ 已读全文 | SCANLAB Calibration Solutions PDF（标定精度分级） | 厂商一手 |
| ✅ 已读全文 | RAYLASE 预聚焦偏转单元页 / Spot Magnification 应用页 | 厂商一手 |
| ✅ 已读全文 | github.com/hyperchao0/qspi4xy2-100（CHANNELZ 证据） | 开源实现 |
| ✅ 已读全文 | govolition（Thorlabs FTH160-1064 + F-Theta 教程镜像） | 代理镜像 |
| ✅ 已读全文 | Sill Optics / RP Photonics 技术指南 | 厂商一手 / 行业百科 |
| ⚠️ 抓取超时/被拦 | Thorlabs 官网 f-theta 页面（反爬）、SCANLAB 3D Calibration Wizard PDF、RTC6 手册 | — |
| ❌ 404 / 不存在 | RAYLASE RAYVOLUTION DRIVE 独立页、FOCUSSHIFTER II 独立数据手册页 | — |
| ❌ 报错 | `web_fetch` 工具在本会话对**所有**域名均返回 "resolves to a non-public IP address"，全部内容改由 shell（curl/python，非 UTF-8 路径需用 `$D` 绝对路径变量）获取 | — |
