# 偏振分光镜（PBS）、薄膜偏振器与法拉第光隔离器 — 光学事实核查报告

**范围**：偏振分光立方体（PBS cube）、平板式薄膜偏振器（plate / thin-film polarizer）、法拉第光隔离器（Faraday isolator）。
**方法**：全部数值均通过 `get.py` 抓取网页/PDF 原文后从**已下载文本**中读取；凡未在抓取文本中读到的数字，一律标注「❌ 未找到公开来源」。
**标注约定**：
- 「✅ 一手确认」= 本次实际抓取到该页面/PDF 正文，数字出现在抓取文本中
- 「🟡 二手转述」= 仅来自搜索摘要或二次转述，未读到原文
- 「❌ 未找到」= 未找到公开来源

> **关于 Thorlabs 的说明**：`thorlabs.com` / `thorlabs.de` / `thorlabs.co.jp` 在本环境下全部被反爬拦截（返回 JS 挑战页，`get.py` 报 `chars=0`）。本报告中的 Thorlabs 规格来自其**授权经销商镜像页 `govolition.com`（Volition）**，该页逐字转载 Thorlabs 官方页面文案，已实际读取正文，故标注 ✅ 并注明镜像来源。

---

## 1. PBS 立方体原理（MacNeille 设计）

MacNeille 偏振分光立方体由两个 45° 直角棱镜胶合而成，分光膜镀在其中一片棱镜的斜面上。

**核心设计思想**：让所有内部界面的入射角都等于布儒斯特角，从而使 p 偏振光的反射为零；在此基础上用简单的布拉格反射镜堆叠即可获得 s 偏振的高反射，而不会给 p 偏振引入明显反射。[来源](https://www.rp-photonics.com/rp_coating_demo_polarizing_cube.html)「✅ 一手确认」

原文（RP Photonics，RP Coating 官方演示文件）：
> "The basic idea of the common MacNeille cube design is to eliminate the reflection for p polarization by having Brewster's angle at all internal interfaces. It is then easy to obtain high reflectivity for s polarization with a simple Bragg mirror design without introducing a significant reflection for p polarization. The Brewster angle condition requires that a substrate material with suitable refractive index (for given coating materials) is chosen. For the outer interfaces, one requires anti-reflection coatings."
[来源](https://www.rp-photonics.com/rp_coating_demo_polarizing_cube.html)「✅ 一手确认」

**膜系设计与内部角度的定量关系**：该演示文件给出最优基片折射率的解析式 `n_S_opt := n_H * n_L / sqrt(n_H^2 + n_L^2) / sin(theta)`（其中 H 层为 TiO₂、L 层为 SiO₂，theta 为内部 45° 角），并指出对 TiO₂/SiO₂ 膜系而言 **Schott SF11 玻璃**的折射率最接近该最优值；工作波长取 1064 nm，设计波段 900–1200 nm，布拉格对数为 4 对（`N_Bragg := 4`）。[来源](https://www.rp-photonics.com/rp_coating_demo_polarizing_cube.html)「✅ 一手确认」

**内部角度/入射角敏感度**：RP Photonics 在该演示中专门做了角度扫描（±2°，步长 0.5°），并给出明确结论：
> "We see that a good performance is obtained only in a relatively narrow range of angles, which is typical for such designs."
[来源](https://www.rp-photonics.com/rp_coating_demo_polarizing_cube.html)「✅ 一手确认」

**膜层位置与胶合工艺**（Thorlabs 原文，经 Volition 镜像读取）：
> "The dielectric beamsplitting coating is applied to the hypotenuse of one of the two prisms that make up the cube. Then, cement is used to bind the two prism halves together (refer to Figure 1.1). The engraved dot on the top of the cube indicates the prism with the beamsplitting coating."
[来源](https://www.govolition.com/product/V40-PBS052)「✅ 一手确认（经销商镜像 Thorlabs 原页面文案）」

**偏振分离方式分类**（Laser Components 官方 PDF，已抓取）：
- **I 型**：偏振分离由**镀膜**实现（即 PBS 立方体、薄膜偏振器）
- **II 型**：偏振分离由**双折射**实现（如 Glan-Taylor / Glan-Laser 偏振棱镜）
原文："In general, two different types of polarization optics are used, depending on the application. Polarization separation of type I is the result of a coating whereas polarization separation of type II is the result of birefringency."
并以 "Dot indicates prism with coating on the hypothenuse. For best performance the beam has to enter through this side."（圆点标记镀膜棱镜，为获得最佳性能光束须从此面入射）作为使用要点。
[来源](https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/diverse-laser-optics/polarizers/polarizing_beam_splitter_cubes.pdf)「✅ 一手确认」

**s 反射 / p 透射的几何关系**：Thorlabs 原文 "Polarizing beamsplitters are designed such that upon incidence the s-polarized light will be reflected at a 45° angle while the p-polarized light is transmitted. Therefore, these beamsplitters can be thought of as a 45° high reflector with the two reflection bands offset to allow high transmission of the p-polarized component and simultaneous high reflectance of the s-polarized component."
[来源](https://www.govolition.com/product/V40-PBSW-808)「✅ 一手确认（经销商镜像 Thorlabs 原页面文案）」

---

## 2. 平板式偏振分光镜（Plate / Thin-Film Polarizer）

**定义与工作角**：平板式偏振分光镜是在**平行平板的前表面**镀窄带分光膜的透射式偏振器，s 偏振以 45° 反射、p 偏振透射。关键区别是它按 **45° 入射角（AOI）** 设计，而**不是**按布儒斯特角设计。
Thorlabs 原文：
> "Thorlabs' polarizing plate beamsplitters are offered with narrowband beamsplitting coatings deposited on the front surface ... designed for various laser wavelengths. Unlike traditional polarizing beamsplitters, which are designed for use at Brewster's angle, these optics are meant to be used at a 45° AOI, which allows for easier mounting. Although the optics can be angle tuned, doing so will result in a degradation of the attainable extinction ratio."
[来源](https://www.govolition.com/product/V40-PBSW-808)「✅ 一手确认（经销商镜像 Thorlabs 原页面文案）」

**优势一：更高的损伤阈值（无胶层）**——Thorlabs 原文：
> "The hard coating deposited onto the surface of these plate beamsplitters offers a higher damage threshold than typically obtained with conventional coatings. For applications where high extinction ratio, transmission, or damage threshold is necessary, these optics are the preferred option over Polarizing Beamsplitter Cubes."
即 Thorlabs 官方明确表示：在需要高消光比、高透射或高损伤阈值时，**平板式偏振分光镜优于 PBS 立方体**。[来源](https://www.govolition.com/product/V40-PBSW-808)「✅ 一手确认」

**优势二 / 对比点：立方体无横向位移，平板有横向位移**——Laser Components 官方 PDF 在「高功率偏振分光立方体」一节明确写道：
> "The separation of polarization occurs at 90°. Compared to thin film polarizers, there is no offset of the transmitted p-pol beam (see drawing)."
（偏振分离在 90° 方向进行；**与薄膜偏振器相比，透射的 p 偏振光束没有偏移**。）[来源](https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/diverse-laser-optics/polarizers/polarizing_beam_splitter_cubes.pdf)「✅ 一手确认」

**平板式的代价（横向位移、鬼像、色散）**——第三方技术文章（Giai Photonics）系统性对比：
- "A plate introduces lateral beam displacement when a transmitted ray passes through an angled parallel substrate."（平板在斜入射时使透射光产生横向位移）[来源](https://www.giaiphotonics.com/cube-beamsplitter-vs-plate-beamsplitter/)「✅ 一手确认」
- "For a plane-parallel plate, the lateral displacement increases with substrate thickness and depends on incidence angle and refractive index."（横向位移随基片厚度增大，并依赖入射角与折射率）[来源](https://www.giaiphotonics.com/cube-beamsplitter-vs-plate-beamsplitter/)「✅ 一手确认」
- "A plate, however, has another optical surface behind it. Any residual reflection from that rear surface can travel along a slightly different path and appear as a weak secondary beam or ghost image."（平板背面残余反射会形成弱二次光束/鬼像）[来源](https://www.giaiphotonics.com/cube-beamsplitter-vs-plate-beamsplitter/)「✅ 一手确认」
- "The trade-off is optical path length. The light travels through significantly more substrate than it would in a thin plate. Substrate dispersion, thermal behavior, assembly construction and wavefront requirements can therefore become important."（立方体的代价是光程长：光束穿过的基片远多于薄平板，因此基片色散、热行为、装配结构与波前要求变得重要）[来源](https://www.giaiphotonics.com/cube-beamsplitter-vs-plate-beamsplitter/)「✅ 一手确认」
- 总结句："A cube usually simplifies mechanical alignment and, in its normal-entry geometry, avoids the lateral displacement associated with transmitting through an angled parallel plate. A plate uses less bulk optical material, can be lighter and may be easier to scale to larger apertures, but rear-surface reflections and transmitted-beam displacement must be controlled."（立方体简化机械对准且无横向位移；平板用料少、更轻、更易做大口径，但必须控制背面反射与透射光束位移）[来源](https://www.giaiphotonics.com/cube-beamsplitter-vs-plate-beamsplitter/)「✅ 一手确认」

**平板式偏振器的 AOI 公差（厂商实测规格）**：EKSMA Optics 官方 PDF 给出 45° 型薄膜偏振器的入射角规格为 **AOI = 45 ± 2°**，基片 UV FS，通光孔径 >90% 直径，平行度 <30 arcsec，表面质量 20–10。
[来源](https://cdn.eksmaoptics.com/rails/active_storage/blobs/proxy/eyJfcmFpbHMiOnsiZGF0YSI6MzE5NCwicHVyIjoiYmxvYl9pZCJ9fQ==--ddb76d618214c5a3567cf803f51c42db1db40990/EKSMA_Optics_Thin_Film_Polarizers-45.pdf?disposition=attachment)「✅ 一手确认」

> ⚠️ **关于「平板式无色散/无玻璃光程」的说法**：未找到任何厂商公开文字直接宣称平板式「无玻璃光程」或「无色散」。已确认的**可引用表述**是：立方体因光程长而带来基片色散/热效应/波前问题（Giai，见上），以及平板式因**无胶层**而 LIDT 更高（Thorlabs / Laser Components）。把「无色散」写成平板的绝对优势**缺乏公开来源支持**。「❌ 未找到公开来源」

---

## 3. 消光比（Extinction Ratio）实测规格

### 3.1 立方体：透射臂 vs 反射臂（关键结论）

Thorlabs 官方原文（经 Volition 镜像读取，已确认数字在抓取文本中）：
> "Thorlabs' Polarizing Beamsplitting Cubes are offered in six sizes and with five beamsplitting coating ranges. These cubes separate the s- and p-polarization components by reflecting the s component with the dielectric beamsplitter coating, while allowing the p component to pass. **These cubes are designed to be used with the transmitted beam, which offers an extinction ratio of TP:TS > 1000:1**, except the PBS519 2" 420 - 680 nm cube, which offers an average extinction ratio of > 1000:1 over the wavelength range. **The reflected beam will only have an extinction ratio of roughly 20:1 to 100:1, depending on the beamsplitter.**"
[来源](https://www.govolition.com/product/V40-PBS052)「✅ 一手确认（经销商镜像 Thorlabs 原页面文案）」

同一页面另给出：
- 激光线（laser line）PBS 立方体消光比为 **3000:1 (TP:TS)**："We also offer polarizing beamsplitter cubes at laser line wavelengths, which have an extinction ratio of 3000:1 (TP:TS)."「✅ 一手确认」
- 宽带 Polyhedron 偏振分光镜消光比**最高可达 100 000:1**："Polyhedron broadband polarizing beamsplitters with high extinction ratios up to 100 000:1, high damage thresholds, and low-GDD are also available."「✅ 一手确认」
[来源](https://www.govolition.com/product/V40-PBS052)「✅ 一手确认」

> ✅ **核查结论**：您此前看到的「宽带立方体反射臂仅 ~20:1–100:1，激光线立方体与高消光平板可达 1000:1 / 10 000:1 / 最高 100 000:1」**全部得到一手文本验证**，且条件（透射臂 TP:TS / 反射臂 / 46 AOI 45°）已明确。

### 3.2 平板式偏振器消光比

Thorlabs PBSW 系列平板偏振器（Volition 镜像，文字确认）：
> "**Extinction Ratio: TP:TS > 10 000:1 at 45° Angle of Incidence (AOI)**"，九个设计波长覆盖 405 nm–1550 nm，UV 熔融石英基片，两种尺寸 Ø1" 与 25.0 mm × 36.0 mm。
[来源](https://www.govolition.com/product/V40-PBSW-808)「✅ 一手确认」；同规格亦见 [PBSW-1064R 页面](https://www.govolition.com/product/V40-PBSW-1064R)「✅ 一手确认」

EKSMA Optics 薄膜偏振器（官方 PDF，两档）：
- **标准型**：Rs / Tp > 99.5 / 95.0%，透射光消光比 **Tp/Ts > 200:1**
- **高消光比型（HE）**：**Tp > 98%，Ts < 0.1%，透射光消光比 Tp/Ts > 1000:1**
[来源](https://cdn.eksmaoptics.com/rails/active_storage/blobs/proxy/eyJfcmFpbHMiOnsiZGF0YSI6MzE5NCwicHVyIjoiYmxvYl9pZCJ9fQ==--ddb76d618214c5a3567cf803f51c42db1db40990/EKSMA_Optics_Thin_Film_Polarizers-45.pdf?disposition=attachment)「✅ 一手确认」

### 3.3 立方体：胶合型 vs 光学接触型（重要反直觉结论）

Laser Components 官方 PDF 显示：**为了换取高损伤阈值而改用「光学接触」工艺后，消光比反而下降**——从胶合窄带的 >1000:1 降到 >200:1。详见下表与第 4 节。这三档规格同页并列，可直接对比。[来源](https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/diverse-laser-optics/polarizers/polarizing_beam_splitter_cubes.pdf)「✅ 一手确认」

### 3.4 其他厂商立方体

Real Optec YG-PBS251 规格图（PDF 原文）：材料 H-ZF3，设计波长 420–680 nm，通光孔径 >20.32 × 20.32 mm，波前 <λ/4 @633 nm，表面质量 40-20；PBS 膜层 S5 面：**Tp > 90% @420–680 nm，Rs_avg > 95%，AOI = 45°，消光比 > 1000:1**；AR 膜 Ravg < 0.5%；透射光束偏差 0° ± 5′，反射光束偏差 90° ± 5′。
[来源](https://www.realoptec.com/uploads/20241126/YG-PBS251.pdf)「✅ 一手确认」

---

## 4. 激光损伤阈值（LIDT）

### 4.1 立方体：胶合是 LIDT 的瓶颈（一手明确证据）

Laser Components 官方 PDF 对**胶合（cemented）**偏振立方体给出：
> "**Extinction ratio: Tp/Ts > 1000:1 with Tp > 95%, Rs > 99.8%**"；"**Damage threshold: ca. 1 kW/cm² (cw), ca. 0.5 J/cm² (10 ns)**"；特性描述为 "Cemented surfaces / Applicable at up to medium power levels"。

同 PDF 对其**宽带**胶合偏振立方体明确加了一句免责声明：
> "**The mentioned LDT values can not be guaranteed for cemented cubes, these are expected values.**"（胶合立方体的 LDT 数值不能保证，仅为期望值）
[来源](https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/diverse-laser-optics/polarizers/polarizing_beam_splitter_cubes.pdf)「✅ 一手确认」

**光学接触（optically contacted）高功率立方体**则完全不同：
> "These cubes are optically contacted and specially designed for use in high power lasers. **The characteristics possible in respect of damage threshold correspond to that of thin film polarizers.**"
> "**Damage threshold: ca. 10 J/cm² (10 ns) for Vis, NIR; ca. 5 J/cm² (10 ns) for UV**"
> 但同时："**Extinction ratio: Tp/Ts > 200:1** whereas TpUV > 90.0%, TpVIS/NIR > 95.0%, **Rs > 99.0%**"
[来源](https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/diverse-laser-optics/polarizers/polarizing_beam_splitter_cubes.pdf)「✅ 一手确认」

> ✅ **核查结论**：**胶合层/胶合工艺确实是 PBS 立方体 LIDT 的瓶颈**——同一厂商同一 PDF 内，胶合型 0.5 J/cm²（10 ns），光学接触型 10 J/cm²（10 ns），相差 **20 倍**。且厂商自认胶合件 LDT 不可保证。代价是消光比从 >1000:1 掉到 >200:1。

**胶合降低 CW 阈值的机理**（Thorlabs 原文）：
> "While many optics can handle high power CW lasers, **cemented (e.g., achromatic doublets) or highly absorptive (e.g., ND filters) optics tend to have lower CW damage thresholds. These lower thresholds are due to absorption or scattering in the cement or metal coating.**"
[来源](https://www.govolition.com/product/V40-PBS052)「✅ 一手确认」

### 4.2 平板式偏振器 LIDT

EKSMA Optics 官方 PDF（平板薄膜偏振器）：
> "Polarizers are made from UV FS and feature **high laser damage threshold reaching 10 J/cm² at 1064 nm**."，并明确其定位是 "used as an alternative to Glan laser polarizing prisms or cube polarizing beamsplitters"，典型应用为 "intracavity Q-switch hold-off polarizers or extracavity attenuators for Nd:YAG lasers"。
[来源](https://cdn.eksmaoptics.com/rails/active_storage/blobs/proxy/eyJfcmFpbHMiOnsiZGF0YSI6MzE5NCwicHVyIjoiYmxvYl9pZCJ9fQ==--ddb76d618214c5a3567cf803f51c42db1db40990/EKSMA_Optics_Thin_Film_Polarizers-45.pdf?disposition=attachment)「✅ 一手确认」

> 注：该官方 PDF 只写 "10 J/cm² at 1064 nm"，**未标注脉宽**。EKSMA 的 directindustry 目录页写 "10 J/cm² @ 1064 nm 8 ns"，但该页本次未抓取成功，故脉宽 8 ns 标注 🟡 二手转述。[来源](https://pdf.directindustry.com/pdf/eksma-optics/polarizing-optics-eksma-optics/57692-593432.html)「🟡 二手转述」

> ✅ **核查结论**：平板偏振器 LIDT（10 J/cm² @1064 nm）**远高于胶合立方体**（0.5 J/cm² @10 ns），与光学接触型立方体相当——这与 Laser Components「光学接触立方体的损伤阈值特性等同于薄膜偏振器」的表述互相印证。

### 4.3 LIDT 定义与测量标准

EKSMA 与 Thorlabs 均把 LIDT 描述为统计外推量而非绝对硬阈值。Thorlabs 原文对 LIDT 的测法与换算给出方法学说明（10 点曝光、显微镜 ~100× 检查、CW 用线功率密度 W/cm 可适用于任意光束直径、脉冲用 J/cm²、脉冲 <1 ns 时数据不可靠、波长缩放经验规则：CW 随波长线性、脉冲随波长平方根反比，例如 1064 nm 的 1 J/cm² 折算到 532 nm 约 0.7 J/cm²）。[来源](https://www.govolition.com/product/V40-PBS052)「✅ 一手确认」

> ⚠️ Thorlabs 页面对立方体的**具体 LIDT 数值表（Table 3.1）以图片/JS 形式给出，抓取文本中不含数值**，故**未获得 Thorlabs 立方体的具体 J/cm² 数值**。「❌ 未找到（本次抓取）」

---

## 5. 半波片 + PBS 连续可调衰减器（Variable Beam Splitter / Attenuator）

### 5.1 原理（厂商原文，一手）

Wavelength Opto-Electronic 官方 Application Note《Variable Beam Splitter: Precision Control by The Principle of Polarization》原文：
> "The key optics involved include a **half-wave plate** and **polarization beam splitter (PBS)**. The half-wave plate is usually made of birefringent crystal cut parallel to the optical axis. It is used to change the polarization direction of the incident beam. The surfaces of the waveplate and the beamsplitter cube are coated with an AR-coating over the designed wavelength range. **The PBS placed after the half-wave plate reflects s-polarized light while transmitting p-polarized light. The intensity ratio of s-polarized to p-polarized beams may be continuously varied by rotating the wave plate.** The intensity of either the exit beam or their intensity ratio can be controlled over a wide dynamic range. P-polarization can be selected for maximum transmission. **A full range of intensity variation between the two beams from maximum to minimum can be achieved by rotating the half-wave plate from 0 to 45 degrees.**"
[来源](https://wavelength-oe.com/variable-beam-splitter/)「✅ 一手确认」；同文亦见其官方 PDF [来源](https://wavelength-oe.com/wp-content/uploads/2020/02/Variable-Beam-Splitter.pdf)「✅ 一手确认」

**该产品的实测规格**（同一页面 Table 1，原文）：
| 项目 | 数值 |
|---|---|
| 波长 | 355 / 532 / 1064 nm |
| 类型 | Transmission Mode |
| 通光孔径 | 14 mm |
| 光束位移 Beam Shift | 0.5 mm |
| 消光比 | **> 200:1** |
| 功率变化范围 | **0.5% – 95%** |
| 损伤阈值 | **> 5 J/cm² @ 1064 nm, 20 ns, 20 Hz** |
| 重量 | < 300 g |

另注："Using a suitable type of polarizer, this principle can be realized at very high-power levels."（选用合适的偏振器，该原理可用于很高功率）[来源](https://wavelength-oe.com/variable-beam-splitter/)「✅ 一手确认」

### 5.2 余弦平方（Malus）定律的厂商表述

Thorlabs 在讨论隔离器调谐时明确写出 Malus 定律形式与量值：`I = I0·cos²θ`，θ 为法拉第旋光后偏振方向与偏振器透光轴夹角；示例中 θ = 2.6° 时 I = 0.998 I0。[来源](https://www.govolition.com/product/V40-IO-5-1064-HP)「✅ 一手确认（经销商镜像 Thorlabs 原页面文案）」

> 注意：Thorlabs 此段是**隔离器波长调谐**语境，不是可变衰减器语境；但 cos² 关系与衰减器完全同源。**未找到** Thorlabs 或 Edmund 官方针对「半波片+PBS 可变衰减器」的专门应用笔记（thorlabs.com 的 VOA 应用笔记 PDF `catalogpages/V21/1077.PDF` 抓取失败）。「❌ 未找到」

### 5.3 电动化商用衰减器实测规格（可作为「电机化 HWP+PBS」的一手规格）

Optogama **Motorized laser power attenuators LPA** 官方规格：
- 损伤阈值 **up to 10 J/cm² (10 ns @ 1064 nm)**
- 可调偏振器角度 **±2 deg**
- 通光孔径 **18 mm**
- 全旋转 **175,543 steps**
- 功率精度 **±0.05%**
- 调节时间 **< 0.2 s（min → max）**
[来源](https://www.optogama.com/products/beam-delivery-devices/motorized-laser-power-attenuators-lpa)「✅ 一手确认」

EKSMA Optics 紧凑型可变衰减器 990-0077 / 990-0078 官方规格：
- **透射光束衰减范围：典型 0.1% – 98%**（257 nm 与 266 nm 型号为 1% – 94%）
- **反射光束衰减范围：典型 2% – 99.9%**
[来源](https://www.eksmaoptics.com/c/variable-attenuators/83)「✅ 一手确认」

EKSMA 另一款 990-0076 的产品描述原文："This Variable Attenuator incorporates a high-performance **Polarizing Cube Beamsplitter which reflects s-polarized light at 90° while transmitting p-polarized light**."（内置高性能 PBS 立方体，s 偏振 90° 反射、p 偏振透射）[来源](https://www.eksmaoptics.com/c/variable-attenuators/83)「✅ 一手确认」

### 5.4 实用极限（已在原文中确认的部分 + 明确标注的推论）

**（a）最小可达消光受 PBS 消光比限制 / 透射臂与反射臂差异极大** —— 这是本主题最关键的实际限制，且已有**硬数据支撑**：
- Thorlabs PBS 立方体：**透射臂 TP:TS > 1000:1，反射臂仅 ~20:1 至 100:1**。[来源](https://www.govolition.com/product/V40-PBS052)「✅ 一手确认」
- EKSMA 官方规格也体现同一不对称：**透射臂**衰减范围 0.1%–98%，**反射臂** 2%–99.9%（下限差了 20 倍）。[来源](https://www.eksmaoptics.com/c/variable-attenuators/83)「✅ 一手确认」
- **推论（非原文）**：若把 PBS 的**反射臂**作为输出做衰减器，则出射光的偏振纯度受 20:1–100:1 限制；若用**透射臂**，则受 >1000:1 限制。因此「衰减器最小可达消光比 ≈ PBS 该臂的消光比」是**由上述厂商数据直接推出的工程结论**，本报告标注为**推论**，未找到厂商以这句话的原话表述。「❌ 未找到公开来源（原话）」

**（b）热负载去向** —— 未找到任何可变衰减器厂商页面明确描述「被挡住的光去哪里/如何做 beam dump」。仅找到**隔离器**领域的等价表述（RP Photonics）：
> "**High-power devices usually have exit ports for the rejected light, rather than internal absorbers, to avoid the associated heating inside the device.**"（高功率器件通常为被拒绝的光设置出射端口，而非内部吸收器，以避免器件内部发热）
[来源](https://www.rp-photonics.com/faraday_isolators.html)「✅ 一手确认」
> 可变衰减器的热负载处理「❌ 未找到公开来源」；可引用的最接近表述为 Wavelength OE 的 "Using a suitable type of polarizer, this principle can be realized at very high-power levels."（须配合适偏振器）[来源](https://wavelength-oe.com/variable-beam-splitter/)「✅ 一手确认」

---

## 6. 法拉第光隔离器（Faraday Isolator）

### 6.1 原理（非互易 45° 旋光 + 两个偏振器）

RP Photonics 官方百科原文：
> "The simplest (and quite common) type of Faraday isolator is **polarization-sensitive** in the sense that it works only when the input beam has a prescribed direction of linear polarization. Here, a properly polarized and collimated input beam passes a first polarizer (pol 1), then a **45° Faraday rotator**, and finally another polarizer (pol 2) with its transmitting axis being rotated by 45°, such that the transmission losses are small."
> "When light is reflected back to the output port of the isolator with an unchanged polarization state, it can fully transmit the output polarizer (pol 2). Then, however, **its polarization direction is rotated by another 45° in the Faraday rotator, so that this light will be blocked at the input polarizer**."
[来源](https://www.rp-photonics.com/faraday_isolators.html)「✅ 一手确认」

Wikipedia（作为非互易性的补充说明，已抓取正文）：
> "the Faraday rotator provides **non-reciprocal rotation** while maintaining linear polarization. That is, the polarization rotation due to the Faraday rotator is always in the same relative direction. So in the forward direction, the rotation is positive 45°. In the reverse direction, the rotation is −45°... This then adds to a total of 90° when the light travels in the forward direction and then the negative direction."
并指出最常用旋光材料：700–1100 nm 用掺铽硼硅酸盐玻璃与 **TGG（铽镓石榴石）**晶体，1310/1550 nm 用 YIG；"Commercial YIG based Faraday isolators reach isolations higher than 30 dB."
[来源](https://en.wikipedia.org/wiki/Optical_isolator)「✅ 一手确认」

**为什么高功率必须用**（RP Photonics）："In many cases, they are used to **protect some laser or amplifier against back-reflected light**. Amplifier chains sometimes require several isolators between the different amplifier stages, preventing not only back-reflected light but also amplified spontaneous emission in the backward direction from having detrimental effects."
[来源](https://www.rp-photonics.com/faraday_isolators.html)「✅ 一手确认」

### 6.2 典型隔离度与插损（多厂商一手数据）

**RP Photonics（权威综述）**：
> "Typical Faraday isolators achieve an isolation of the order of **30 to 40 dB** (in a limited wavelength range). A high degree of isolation is generally more difficult to achieve for high-power devices, where the beam in the Faraday medium covers a larger area and is thus more sensitive to field inhomogeneities. The quality and alignment of the polarizers used is also important. A lower degree of isolation may result from operation at a non-optimized wavelength, from improper alignment or large divergence of the input, or from **thermal effects when the isolator is operated with a high optical average power**."
[来源](https://www.rp-photonics.com/faraday_isolators.html)「✅ 一手确认」

### 6.3 两级（Dual-stage / Tandem）隔离器

- **RP Photonics**："If the return loss achievable with a single isolator is insufficient, a combination of two (or even more) isolators may be used. There are devices available where two isolators are packaged into one housing. One may then reach e.g. **60 dB isolation**, but the insertion loss will typically be somewhat higher with a dual-stage device." [来源](https://www.rp-photonics.com/faraday_isolators.html)「✅ 一手确认」
- **Thorlabs**："The third type, **Tandem Narrowband Isolators**, consists of **two Faraday rotators in series, boosting the isolation to at least 55 dB** at the expense of lower transmission." [来源](https://www.govolition.com/product/V40-IO-5-1064-HP)「✅ 一手确认」
- **Excelitas / LINOS**："Our **two-stage Isolators deliver over 60 dB of isolation**, making them among the best on the market." [来源](https://www.excelitas.com/product-category/linos-faraday-isolators)「✅ 一手确认」
- **TOPTICA 官方 PDF**：单级 >35 dB 隔离 / 85% 最小、92% 平均透射；**双级 >60 dB 隔离 / 80% 最小、90% 平均透射**。产品线还标称 "Power densities up to 4 kW/cm²"。[来源](https://www.toptica.com/fileadmin/Editors_English/11_brochures_datasheets/02_datasheets/toptica_BR_isolators.pdf)「✅ 一手确认」

> 两级提升隔离度、同时降低透射 —— 三个独立厂商（RP Photonics、Thorlabs、TOPTICA）数据一致，为可靠结论。

### 6.4 AOI / 波长 / 温度敏感性（有真实数字）

**Thorlabs 官方给出的波长敏感性定量示例**（原文）：
> "The magnitude of the rotation caused by the Faraday rotator is wavelength dependent. ... For example, **if 1064 nm light is rotated by 45° (that is, 1064 nm is the design wavelength), then 1054 nm light is rotated by 46.3°.** If 1054 nm light is sent backward through an isolator designed for 1064 nm without any tweaking, it will have a net polarization of 45° + 46.3° = 91.3° ... the isolation will therefore be significantly reduced."
> "For example, if the 1064 nm isolator shown in Figures 3.1 and 3.2 were used at **1044 nm without tuning, the transmission would be 92.2% (instead of 92.0%), but the isolation would be only 26 dB (instead of 42 dB)**."
[来源](https://www.govolition.com/product/V40-IO-5-1064-HP)「✅ 一手确认（经销商镜像 Thorlabs 原页面文案）」

→ 即：**偏离设计波长 20 nm，隔离度从 42 dB 崩到 26 dB，而透射率几乎不变（92.0%→92.2%）**。这是「隔离度对波长/角度极敏感、而透射率不敏感」的极佳定量证据。

**温度敏感性**：
- EOT TORNOS Compact 官方 PDF 把「Tunable Temperature」列为独立规格项，全部型号为 **10 °C to 30 °C**，并注明隔离度/透射率数值是 "At specified wavelength and temperature"（在指定波长与温度下）。[来源](https://www.japanlaser.co.jp/wp-content/uploads/2020/03/eot_TORNOS_Compact.pdf)「✅ 一手确认」
- RP Photonics："a lower degree of isolation may result from ... **thermal effects** when the isolator is operated with a high optical average power"；并解释机理为「热致退偏（thermally induced depolarization）」与「寄生吸收导致热透镜」。高功率器件的隔离度"generally more difficult to achieve"[来源](https://www.rp-photonics.com/faraday_isolators.html)「✅ 一手确认」
- DK Photonics 规格表把工作温度标为 **0 ~ +70 °C**，并在参数表中单列 "Min. Isolation in Band (**at 25℃**)"，暗示温度对隔离度的影响。[来源](https://www.dkphotonics.com/product/1064nm-high-power-isolator.html)「✅ 一手确认」

**AOI（入射角）敏感性**：厂商规格普遍要求准直、正入射平行光束（RP Photonics："Common Faraday isolators need a correctly polarized, **collimated** beam"）。**未找到**任何厂商给出隔离度随 AOI 变化的定量曲线/数值。「❌ 未找到公开来源」

### 6.5 高功率隔离器的能力边界（回答第 7 问的关键）

**RP Photonics（权威上限陈述）**：
> "Commercially available high-power Faraday isolators can handle **optical average powers up to the order of 100 W** with not too strong beam distortions. Particularly some applications in combination with high-power fiber lasers and amplifiers demand higher powers, and **more advanced devices for powers of the order of 1 kW are being developed**. For fiber-coupled devices, the power levels are more limited, **usually to well below 100 W**."
并列出高功率三大限制：热致退偏（影响隔离度）、寄生吸收导致热透镜（畸变光束）、高峰值功率下的激光损伤与自聚焦；"To prevent this, a sufficiently large beam area and thus a large input aperture is required."
[来源](https://www.rp-photonics.com/faraday_isolators.html)「✅ 一手确认」

**Agiltron 1 kW 自由空间隔离器（存在，但代价明确）**：
> "The OIHF series optical isolators are engineered for kilowatt-class, single-polarization laser systems and feature Agiltron's proprietary configuration with advanced compensation technologies for **thermal lensing and wavelength shifts** under high optical radiation. These isolators offer broadband performance, delivering **>40 dB isolation over 100 nm and >30 dB over 300 nm**, with **power handling proportional to aperture size — requiring beam expansion and collimation to match the aperture to reduce power density**. ... For a 1550 nm laser, the largest aperture size is **10 mm**, while for 1060 and 980 nm short wavelength laser, the max beam size is **30 mm**."
产品页规格项另列出：Forward Power **1 kW**，Backward Power 可选 **5 W / 10 W / 20 W / 100 W**，孔径可选 1 cm / 3 cm / 10 cm / 30 mm，标配热补偿器（Compensator: Yes/Non）。
[来源](https://agiltron.com/product/high-power-broadband-free-space-isolators/)「✅ 一手确认」

→ 即 **kW 级隔离器确实存在，但必须把光束扩束到 10–30 mm 口径以降低功率密度**，且反向承受功率仅 5–100 W 量级。

---

## 7. 工业高功率光纤激光器是否在激光器与振镜之间加自由空间隔离器？

### 7.1 结论：**通常不加**。回光防护做在激光器内部 / QBH 输出头 / 控制逻辑，而不是外置自由空间法拉第隔离器。

**（1）隔离器本身在 kW 级就不实用（见 6.5）**：商用高功率隔离器上限约 100 W，kW 级仍在研发；光纤耦合型通常远低于 100 W。[来源](https://www.rp-photonics.com/faraday_isolators.html)「✅ 一手确认」。而工业光纤激光器主力功率为 1.5–15 kW —— 差 1–2 个数量级。

**（2）厂商把回光防护做成激光器内部功能（一手厂商证据）**：

- **nLIGHT（官方）**："**Legacy fiber lasers often employ software isolation which shuts off the laser when back-reflection is detected.** This solution requires users to reset the system costing them valuable processing time. **nLIGHT's hardware isolation converts the back-reflected power to heat which dissipates before it can damage the laser**, keeping your operation running."
  [来源](https://www.nlight.net/back-reflection-protection)「✅ 一手确认」
  → 明确把回光防护分为「软件隔离（检测到回光就关机）」与「硬件隔离（把回光转成热耗散）」，**两者都在激光器内部**，均未涉及外置隔离器。

- **Raycus（锐科，官方英文站）**：针对铜/铝等高反材料，"Raycus Laser designed a **new QBH fiber output head**, which can effectively **convert the uncontrollable return light into light and heat that can be absorbed**, and at the same time improve the heat absorption and heat dissipation capabilities of the output head, thereby avoiding it to the greatest extent the effect of returning light on internal components."
  并给出实测：RFL-A1500D（1.5 kW）在铜面 90° 垂直全功率连续出光 **1200 min**，"the temperature of each part of the laser ... tends to be stable, and there is no significant increase or change. After the high-reverse test, the detected laser power is not attenuated." 各核心器件温度维持在 **30–40 °C** 区间（器件 1：33.9–39.3 °C；器件 2：30–35 °C；器件 3：35–40 °C；器件 4：33.3–38.8 °C）。
  [来源](https://en.raycuslaser.com/view/1818.html)「✅ 一手确认」

- **Raycus 四级防护体系（第三方技术文，已抓取正文）**："The foundation of the system is a **four-stage physical barrier** that absorbs and diverts reflected light before it can reach sensitive internal modules. **Output Head Protection**: Optimized QBH/QD connectors and integrated cooling systems efficiently dissipate heat and strip off initial reflected light. ... **Beam Combiner Module**: Dual-stage protection inside the combiner absorbs and neutralizes any remaining reflected energy through specialized absorbers."
  [来源](https://www.xc-laser.com/Raycus-Anti-High-Reflection-Technology-Core-Principles-id40786065.html)「✅ 一手确认（第三方转述 Raycus 技术）」

- **Coherent QBH 官方 datasheet**：QBH 被定义为 "the **industry-standard interface** for high-power industrial fiber lasers"，其防护手段完全是**被动热管理**而非隔离器：
  - 特性含 "**AR-coated end cap**"、"Superior power loss handling"、水冷
  - 规格：最大 CW 功率 **15 kW**；**Power Loss Capability 2.0 kW (10 s) / 1.0 kW (10 min.) / 0.5 kW (continuously)**（RQB 风冷型 0.1 kW / 0.05 kW / 0.01 kW）；传输损耗 <3%
  - 配件含 "**QB Protection Window, Input Side / Output Side**, 1030 to 1090 nm"（型号 1412500 / 1412501）
  [来源](https://www.coherent.com/resources/datasheet/components-and-accessories/qbh-fiber-optic-cable-1030-1090nm-ds.pdf)「✅ 一手确认」

- **深圳博科斯（BOX Optronics）QBH 产品页（中文一手）**：
  > "**我司光束输出头QBH有效吸收由工作界面反射回的背向反射光。**采用紧凑化设计以及内部的高效水冷结构。"
  规格表明确列出**反射功率耐受**：**@10 s = 1.5 kW；@50 s = 1 kW；长期 = 0.6 kW**；平均功率 5 kW；峰值功率 8 kW@1 ms / 40 kW@50 ns；透射率 ≥98%。
  [来源](https://www.box-optical.com/high-power-components/optical-fiber-laser-optical-cable(qbh).html)「✅ 一手确认」

- **思创激光（STR Laser）QBH 产品页（中文一手）**：
  > "思创激光自主研发的激光输出头（QBH），**减小激光出口的能量密度，防止设备烧毁**。"
  功率范围 200–12000 W，水冷/自然冷却。
  [来源](https://www.strlaser.com/productinfo/693478827153686528.html)「✅ 一手确认」

- **IPG 相关工程页**：把回光防护列为「保护逻辑（Protection logic）」的一部分——"Back-reflection, temperature, cover, fiber, and emergency-stop interlocks"，交付光纤为 "QBH/QCS connector options"。
  [来源](https://www.ipgfactory.com/)「🟡 二手转述」——⚠️ **该页域名为 `ipgfactory.com`，并非 `ipgphotonics.com`**，无法确认其为 IPG Photonics 官方站点，故降级标注。**未在 IPG 官方域名上读到关于「是否外置隔离器」的直接表述。**「❌ 未找到（IPG 官方）」
  > 补充：搜索结果显示 `ipgphotonics.com` 上存在 YLR 系列用户手册，但本次未成功抓取其正文。「❌ 未找到公开来源（本次）」

**（3）第三方技术综述（整合商视角）**：现代高功率光纤激光器对回光的防护手段被总结为七类，**全部为内部/被动/软件手段，无一条是外置法拉第隔离器**：① 实时主动保护（光电探测器监测回光，超阈值自动降功率/暂停/报警/关机）；② 抗反射（AR）光学镀膜（保护窗、准直镜、聚焦镜、输出光纤端帽）；③ QBH 连接器设计优化（高损伤阈值材料、端面抛光、水冷结构、抗反射几何）；④ 智能控制算法；⑤ 模场优化；⑥ 保护窗与耗材防护；⑦ （高反材料用）激光器本身的设计裕量。
[来源](https://www.superstarlaser.com/what-technologies-are-used-for-anti-reflection-protection-in-fiber-lasers/)「✅ 一手确认（第三方整合商技术文）」

**（4）「可选外置隔离器」的情形**：本次**未找到**任何光纤激光器厂商（IPG / Raycus / Maxphotonics / nLIGHT / Coherent）明确声明「隔离器为选配项」的官方原文。「❌ 未找到公开来源」
已确认的相关事实是：激光器侧的保护被表述为**内置功能**（nLIGHT 硬件隔离）、**输出头功能**（Raycus iHQB、Coherent QBH 保护窗）、**控制逻辑**（IPG 互锁），而非下游光路中的外置器件。

> **给振镜应用的直接含义**：在 XY2-100 振镜这条链路里，**不要假设激光器与振镜之间存在外置法拉第隔离器**。若需要回光防护，应按厂商实际做法考虑：激光器内置防护能力（需向厂商确认具体机制与耐受阈值）、QBH 输出头的反射功率耐受（如 BOX 的长期 0.6 kW / Coherent 的连续 0.5 kW）、以及振镜前端的保护窗与功率监测。若确需外置隔离，须注意商用高功率隔离器上限约 100 W，kW 级需大孔径（10–30 mm）扩束方案。

---

## 8. 规格汇总表（全部为已抓取文本中的真实数字）

### 8.1 消光比 / 透射 / 反射

| 器件类型 | 型号 / 系列 | 消光比 ER | Tp / Rs | 波长 / AOI | 来源标注 |
|---|---|---|---|---|---|
| PBS 立方体（胶合窄带，BK7） | Laser Components **PBS-xxx** | **Tp/Ts > 1000:1** | **Tp > 95%，Rs > 99.8%** | 单波长，440–1550 nm | ✅ [LC PDF](https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/diverse-laser-optics/polarizers/polarizing_beam_splitter_cubes.pdf) |
| PBS 立方体（胶合宽带，BK7/SF2） | Laser Components **PBSH-xxx** | **Tp/Ts > 500:1** | Tp > 90%（平均），Rs > 99.8%（平均） | 440–680 / 650–1000 / 900–1400 / 1200–1600 nm | ✅ [LC PDF](https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/diverse-laser-optics/polarizers/polarizing_beam_splitter_cubes.pdf) |
| PBS 立方体（**光学接触**高功率） | Laser Components **PBSC-xxx** | **Tp/Ts > 200:1** | Tp_UV > 90%，Tp_VIS/NIR > 95%，Rs > 99.0% | 248–1550 nm | ✅ [LC PDF](https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/diverse-laser-optics/polarizers/polarizing_beam_splitter_cubes.pdf) |
| PBS 立方体（Thorlabs，**透射臂**） | Thorlabs PBS 系列（6 种尺寸，5 种膜系） | **TP:TS > 1000:1** | — | 420–680 nm 等 | ✅ [Volition/PBS052](https://www.govolition.com/product/V40-PBS052) |
| PBS 立方体（Thorlabs，**反射臂**） | 同上 | **仅 ~20:1 至 100:1** | — | 同上 | ✅ [Volition/PBS052](https://www.govolition.com/product/V40-PBS052) |
| PBS 立方体（激光线） | Thorlabs laser line 系列 | **3000:1 (TP:TS)** | — | 激光线波长 | ✅ [Volition/PBS052](https://www.govolition.com/product/V40-PBS052) |
| 宽带 Polyhedron 偏振分光镜 | Thorlabs Polyhedron | **最高 100 000:1** | — | 宽带 | ✅ [Volition/PBS052](https://www.govolition.com/product/V40-PBS052) |
| **平板**偏振分光镜 | Thorlabs **PBSW-808 / PBSW-1064R** 等 | **TP:TS > 10 000:1 @ 45° AOI** | UV 熔融石英 | 405–1550 nm，9 个设计波长 | ✅ [Volition/PBSW-808](https://www.govolition.com/product/V40-PBSW-808) |
| **平板**薄膜偏振器（标准型） | EKSMA **420-xxxxi45** | **Tp/Ts > 200:1**（透射光） | **Rs/Tp > 99.5 / 95.0%** | 343–1064 nm，45 ± 2° | ✅ [EKSMA PDF](https://cdn.eksmaoptics.com/rails/active_storage/blobs/proxy/eyJfcmFpbHMiOnsiZGF0YSI6MzE5NCwicHVyIjoiYmxvYl9pZCJ9fQ==--ddb76d618214c5a3567cf803f51c42db1db40990/EKSMA_Optics_Thin_Film_Polarizers-45.pdf?disposition=attachment) |
| **平板**薄膜偏振器（高消光 HE 型） | EKSMA **420-xxxxi45HE** | **Tp/Ts > 1000:1**（透射光） | **Tp > 98%，Ts < 0.1%** | 343–1064 nm，45 ± 2° | ✅ [EKSMA PDF](https://cdn.eksmaoptics.com/rails/active_storage/blobs/proxy/eyJfcmFpbHMiOnsiZGF0YSI6MzE5NCwicHVyIjoiYmxvYl9pZCJ9fQ==--ddb76d618214c5a3567cf803f51c42db1db40990/EKSMA_Optics_Thin_Film_Polarizers-45.pdf?disposition=attachment) |
| PBS 立方体 | Real Optec **YG-PBS251** | **> 1000:1** | Tp > 90%，Rs_avg > 95% | 420–680 nm，AOI 45° | ✅ [RealOptec PDF](https://www.realoptec.com/uploads/20241126/YG-PBS251.pdf) |

### 8.2 激光损伤阈值 LIDT

| 器件类型 | 型号 / 系列 | CW LIDT | 脉冲 LIDT | 来源标注 |
|---|---|---|---|---|
| PBS 立方体（**胶合**窄带） | Laser Components **PBS-xxx** | **约 1 kW/cm² (CW)** | **约 0.5 J/cm² (10 ns)** | ✅ [LC PDF](https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/diverse-laser-optics/polarizers/polarizing_beam_splitter_cubes.pdf) |
| PBS 立方体（胶合宽带） | Laser Components **PBSH-xxx** | 约 100 W/cm² (CW) | 约 0.5 J/cm² (10 ns) | ✅ [LC PDF](https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/diverse-laser-optics/polarizers/polarizing_beam_splitter_cubes.pdf) |
| PBS 立方体（**光学接触**高功率） | Laser Components **PBSC-xxx** | ❌ 未找到公开来源 | **约 10 J/cm² (10 ns) Vis/NIR；约 5 J/cm² (10 ns) UV** | ✅ [LC PDF](https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/diverse-laser-optics/polarizers/polarizing_beam_splitter_cubes.pdf) |
| 普通分光立方体（胶合，对照） | Laser Components **PCB/CBS** | 约 100 W/cm² (CW) | 约 0.5 J/cm² (10 ns) | ✅ [LC PDF](https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/diverse-laser-optics/polarizers/beam_splitter_cubes.pdf) |
| **平板**薄膜偏振器 | EKSMA **420-xxxxi45 / i45HE** | ❌ 未找到公开来源 | **10 J/cm² @ 1064 nm**（PDF 未标脉宽；目录页标 8 ns 🟡） | ✅ [EKSMA PDF](https://cdn.eksmaoptics.com/rails/active_storage/blobs/proxy/eyJfcmFpbHMiOnsiZGF0YSI6MzE5NCwicHVyIjoiYmxvYl9pZCJ9fQ==--ddb76d618214c5a3567cf803f51c42db1db40990/EKSMA_Optics_Thin_Film_Polarizers-45.pdf?disposition=attachment) |
| 电机化 HWP+PBS 可变衰减器 | Optogama **LPA** | ❌ 未找到公开来源 | **up to 10 J/cm² (10 ns @ 1064 nm)** | ✅ [Optogama](https://www.optogama.com/products/beam-delivery-devices/motorized-laser-power-attenuators-lpa) |
| 可变衰减器（HWP+PBS） | Wavelength OE **VBS** | ❌ 未找到公开来源 | **> 5 J/cm² @ 1064 nm, 20 ns, 20 Hz** | ✅ [Wavelength OE](https://wavelength-oe.com/variable-beam-splitter/) |
| Thorlabs PBS 立方体 / PBSW 平板 | Thorlabs | ❌ 未找到公开来源（表格为图片，抓取文本无数值） | ❌ 未找到公开来源 | ❌ 未找到 |
| 高功率法拉第隔离器 | Newport **ISO-FRDY** 系列 | 1 MW/cm² (CW) | 10 J/cm² @ 10 ns；1 J/cm² @ 8 ps | 🟡 仅搜索摘要（newport.com 返回 403） |

### 8.3 法拉第隔离器隔离度 / 插损 / 功率

| 厂商 / 型号 | 隔离度 | 透射 / 插损 | 功率能力 | 其他 | 来源标注 |
|---|---|---|---|---|---|
| — （综述范围） | **典型 30–40 dB** | — | 商用高功率可达 ~100 W；kW 级在研 | 光纤耦合型通常远低于 100 W | ✅ [RP Photonics](https://www.rp-photonics.com/faraday_isolators.html) |
| — （两级） | **约 60 dB** | 插损略增 | — | 两只隔离器封装于同一壳体 | ✅ [RP Photonics](https://www.rp-photonics.com/faraday_isolators.html) |
| Thorlabs **Nd:YAG 自由空间隔离器**（如 IO-5-1064-HP） | **25 – 55 dB**（中心波长处） | — | **最大 CW 200 mW – 200 W**；功率密度 **最高 20 kW/cm²** | 可调窄带型可在 45 nm 范围调谐 | ✅ [Volition/IO-5-1064-HP](https://www.govolition.com/product/V40-IO-5-1064-HP) |
| Thorlabs **Tandem（两级）** | **≥ 55 dB** | 低于单级 | — | 两个法拉第旋光器串联 | ✅ [Volition/IO-5-1064-HP](https://www.govolition.com/product/V40-IO-5-1064-HP) |
| TOPTICA **单级** | **≥ 35 dB** | 最小 **85%** / 平均 **92%** | 功率密度 **可达 4 kW/cm²** | 波长 395–425 nm、630–1400 nm | ✅ [TOPTICA PDF](https://www.toptica.com/fileadmin/Editors_English/11_brochures_datasheets/02_datasheets/toptica_BR_isolators.pdf) |
| TOPTICA **双级** | **≥ 60 dB**（平均 67 dB） | 最小 **80%** / 平均 **90%** | 功率密度 可达 4 kW/cm² | — | ✅ [TOPTICA PDF](https://www.toptica.com/fileadmin/Editors_English/11_brochures_datasheets/02_datasheets/toptica_BR_isolators.pdf) |
| EOT **TORNOS Compact**（1064 nm） | **> 33 dB** | 前向透射 **> 95%**（405 nm 为 >90%） | **5 W** | 可调温度 **10–30 °C**；材料为光学接触 PBS 立方体 | ✅ [EOT PDF](https://www.japanlaser.co.jp/wp-content/uploads/2020/03/eot_TORNOS_Compact.pdf) |
| Excelitas / LINOS **两级** | **> 60 dB** | — | — | XP 系列高功率型 CW > 50 W | ✅ [Excelitas](https://www.excelitas.com/product-category/linos-faraday-isolators) |
| Qioptiq **SC 系列** | **> 30 dB，典型 38–42 dB** | — | — | TGG 晶体，稀土磁体，可选 Brewster 片 | ✅ [RITM/Qioptiq](https://www.ritmindustry.com/catalog/fiber-optic-signal-processing/faraday-isolator/) |
| DK Photonics **1064 nm 高功率在线型** | 典型峰值 **35 dB**；带内最小 **28 dB**（@25 °C） | 典型插损 **0.6 dB**；最大 **1.0 dB**；最小回损 45 dB | **CW 10 / 20 / 30 W**；ns 脉冲峰值 **5 / 10 / 20 kW** | TGG；工作温度 0~+70 °C | ✅ [DK Photonics](https://www.dkphotonics.com/product/1064nm-high-power-isolator.html) |
| BOX Photonics **1064 nm 高功率** | 典型峰值 **30 dB**；最小 **25 dB** | — | 平均 **10 W**；ns 脉冲峰值 **10 kW** | PM 与非 PM 可选 | ✅ [BOX Photonics](https://www.boxphotonics.com/1064nm-high-power-optical-isolator.html) |
| Agiltron **OIHF（1 kW 级）** | **> 40 dB / 100 nm**；**> 30 dB / 300 nm** | 低损耗（具体值未列） | 前向 **1 kW**；反向 5 / 10 / 20 / 100 W；孔径 1 cm – 30 mm | 需扩束准直以匹配孔径、降低功率密度；带热透镜补偿 | ✅ [Agiltron](https://agiltron.com/product/high-power-broadband-free-space-isolators/) |

### 8.4 高功率光纤激光器回光防护（QBH / 内部）

| 厂商 | 机制 | 关键数字 | 来源标注 |
|---|---|---|---|
| nLIGHT | 硬件隔离，把回光转为热耗散（对比：旧式为软件隔离直接关机） | ❌ 未给出具体功率/温度数值 | ✅ [nLIGHT](https://www.nlight.net/back-reflection-protection) |
| Raycus（锐科） | 新型 QBH 输出头（iHQB）把不可控回光转为可吸收的光与热 | RFL-A1500D 全功率 1.5 kW 对铜面 90° 垂直连续 1200 min，核心器件温度维持 30–40 °C，功率无衰减 | ✅ [Raycus](https://en.raycuslaser.com/view/1818.html) |
| Raycus（四级防护，第三方转述） | 输出头 → 合束器 → 内部模块的物理屏障 + 吸收体 | ❌ 未给出具体数值 | ✅ [xc-laser](https://www.xc-laser.com/Raycus-Anti-High-Reflection-Technology-Core-Principles-id40786065.html) |
| Coherent | QBH 被动热管理 + AR 端帽 + 保护窗 | 最大 **15 kW CW**；功率损耗承受 **2.0 kW(10 s) / 1.0 kW(10 min) / 0.5 kW(连续)**；传输损耗 <3%；保护窗型号 1412500（输入）/ 1412501（输出） | ✅ [Coherent PDF](https://www.coherent.com/resources/datasheet/components-and-accessories/qbh-fiber-optic-cable-1030-1090nm-ds.pdf) |
| 深圳博科斯 | QBH 输出头吸收背向反射光 + 内部水冷 | 反射功率耐受 **@10 s 1.5 kW / @50 s 1 kW / 长期 0.6 kW**；平均功率 5 kW；透射率 ≥98% | ✅ [BOX Optical](https://www.box-optical.com/high-power-components/optical-fiber-laser-optical-cable(qbh).html) |
| 思创激光 | QBH 输出头降低出口能量密度，防止设备烧毁 | 功率范围 **200–12000 W** | ✅ [STR Laser](https://www.strlaser.com/productinfo/693478827153686528.html) |
| IPG（存疑域名） | 保护逻辑包含回光互锁；交付光纤 QBH/QCS | ❌ 未给出数值；**域名为 ipgfactory.com，非官方站** | 🟡 [ipgfactory.com](https://www.ipgfactory.com/) |

---

## 9. 明确未找到公开来源的项目（不猜测）

1. **Thorlabs PBS 立方体的具体 LIDT 数值**（Table 3.1 为图片，抓取文本无数值）「❌ 未找到公开来源」
2. **Thorlabs PBSW 平板偏振器的具体 LIDT 数值**「❌ 未找到公开来源」
3. **法拉第隔离器隔离度随入射角（AOI）变化的定量曲线/数值**「❌ 未找到公开来源」
4. **可变衰减器中被拒绝光束的热负载处理方式的厂商明文描述**（仅在隔离器语境找到 "exit ports for the rejected light"）「❌ 未找到公开来源」
5. **「最小可达消光比受 PBS 消光比限制」的厂商原话**（该结论由厂商 ER 数据直接推得，本报告标注为推论）「❌ 未找到公开来源（原话）」
6. **IPG Photonics 官方关于「是否外置隔离器」的表述**（`ipgfactory.com` 非官方域名，已降级为 🟡）「❌ 未找到公开来源」
7. **任何光纤激光器厂商明确声明「隔离器为选配项」的官方原文**「❌ 未找到公开来源」
8. **「平板式偏振器无色散 / 无玻璃光程」的厂商宣称**（仅确认「立方体光程长带来色散/热/波前问题」）「❌ 未找到公开来源」
9. **Newport ISO-FRDY-08-1064-N 的完整规格表**（newport.com 与 globalspec 均返回 403 / 未抓取成功）「❌ 未找到（本次抓取）」

---

## 10. 抓取结果清单（成功 vs 失败）

**✅ 成功抓取并读取正文（用于本报告的一手数据）**
1. https://www.rp-photonics.com/rp_coating_demo_polarizing_cube.html
2. https://www.rp-photonics.com/faraday_isolators.html
3. https://wavelength-oe.com/variable-beam-splitter/
4. https://wavelength-oe.com/wp-content/uploads/2020/02/Variable-Beam-Splitter.pdf
5. https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/diverse-laser-optics/polarizers/polarizing_beam_splitter_cubes.pdf
6. https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/diverse-laser-optics/polarizers/beam_splitter_cubes.pdf
7. https://www.govolition.com/product/V40-PBS052 （Thorlabs 立方体镜像）
8. https://www.govolition.com/product/V40-PBSW-808 （Thorlabs 平板镜像）
9. https://www.govolition.com/product/V40-PBSW-1064R （Thorlabs 平板镜像）
10. https://www.govolition.com/product/V40-IO-5-1064-HP （Thorlabs 隔离器镜像）
11. https://www.japanlaser.co.jp/wp-content/uploads/2020/03/eot_TORNOS_Compact.pdf （EOT）
12. https://www.excelitas.com/product-category/linos-faraday-isolators
13. https://www.ritmindustry.com/catalog/fiber-optic-signal-processing/faraday-isolator/ （Qioptiq）
14. https://www.nlight.net/back-reflection-protection
15. https://www.coherent.com/resources/datasheet/components-and-accessories/qbh-fiber-optic-cable-1030-1090nm-ds.pdf
16. https://www.box-optical.com/high-power-components/optical-fiber-laser-optical-cable(qbh).html
17. https://www.strlaser.com/productinfo/693478827153686528.html
18. https://en.raycuslaser.com/view/1818.html
19. https://www.xc-laser.com/Raycus-Anti-High-Reflection-Technology-Core-Principles-id40786065.html
20. https://www.boxphotonics.com/1064nm-high-power-optical-isolator.html
21. https://www.dkphotonics.com/product/1064nm-high-power-isolator.html
22. https://www.eksmaoptics.com/c/variable-attenuators/83
23. EKSMA 薄膜偏振器 PDF（cdn.eksmaoptics.com 代理链接，见上表）
24. https://www.optogama.com/products/beam-delivery-devices/motorized-laser-power-attenuators-lpa
25. https://www.giaiphotonics.com/cube-beamsplitter-vs-plate-beamsplitter/
26. https://www.realoptec.com/uploads/20241126/YG-PBS251.pdf
27. https://agiltron.com/product/high-power-broadband-free-space-isolators/
28. https://www.toptica.com/fileadmin/Editors_English/11_brochures_datasheets/02_datasheets/toptica_BR_isolators.pdf
29. https://www.superstarlaser.com/what-technologies-are-used-for-anti-reflection-protection-in-fiber-lasers/
30. https://en.wikipedia.org/wiki/Optical_isolator
31. https://www.ipgfactory.com/ （⚠️ 非官方域名，数据降级为 🟡）

**❌ 抓取失败**
- `thorlabs.com`（全站，含 `/newgrouppage9.cfm`、`/item/`、`/catalogpages/V21/855.pdf`、`/catalogpages/V21/1077.PDF`、`/catalogpages/Obsolete/2016/CM1-PBS251.pdf`、`/catalogpages/Obsolete/2016/CM1-PBS25-1064-HP.pdf`）— 返回 JS 反爬挑战页，`chars=0`
- `thorlabs.de`、`thorlabs.co.jp` — 同上
- `newport.com`（`/p/ISO-FRDY-08-1064-N`、`/p/10FC16PB.3`、`/f/high-power-faraday-optical-isolators`）— HTTP 403
- `datasheets.globalspec.com`（Newport ISO-FRDY 数据表）— 403
- `meetoptics.com`（UFPBS053 / PBS251 / PBSW-1064R）— 返回空内容
- `edmundoptics.com`（宽带 PBS 立方体、高能量 PBS 立方体、LIDT 换算工具）— 仅返回 SPA 外壳与导航，正文无规格数值
- `pdf.directindustry.com/pdf/union-optic-inc/...` — HTTP 403
- `www.u-optic.com/product/detail/beamsplitter-cube` — 空内容
- `r.jina.ai`（用作代理抓 Thorlabs）— HTTP 403
- `researchgate.net`（Khazanov 热致退偏论文）— 未抓取成功

**🔁 变通方案（对后续核查有用）**：`govolition.com`（Volition，Thorlabs 授权经销商）逐字镜像 Thorlabs 官方页面文案，URL 模式为 `https://www.govolition.com/product/V40-<PARTNUMBER>`，可绕过 Thorlabs 的反爬；`lasercomponents.com` 的 PDF 直链可正常抓取。
