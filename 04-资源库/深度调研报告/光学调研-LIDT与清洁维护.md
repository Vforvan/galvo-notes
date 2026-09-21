# 振镜系统光学元件调研素材：保护镜 / 窗口片 / 分光取样镜 / 光阑 / LIDT / 清洁维护

> 说明：本文是**调研素材 + 来源清单**，不是成品文章。每条结论后紧跟来源链接与来源类型。
> 可信度标记：**✅ 一手确认**（标准原文、厂商官网/数据手册原文，我已直接读取正文）｜**🟡 二手转述**（转销商/行业博客/新闻页，或我仅见到摘要）｜**❌ 未找到**。
> 采集方式说明：本次调研中 `web_fetch` 对多数厂商域名（thorlabs.com、edmundoptics.com、layertec.de、lasercomponents.com 等）返回 "resolves to a non-public IP address"，因此对这类页面改用 PowerShell `Invoke-WebRequest` 直取 HTML 正文并去标签后阅读，所有引文均来自实际抓取到的页面文本。

---

## 1. 保护镜（protective window / cover slide / debris shield）

### 1.1 为什么需要、装在哪个位置

- 保护镜是**装在光路中、位于工件侧最外层**的平板保护元件，用来挡住飞溅、颗粒与工艺蒸气，从而保护昂贵的聚焦镜与准直镜。原文："Laser protection windows are flat protective elements positioned in the beam path. They shield sensitive focusing and collimation optics from spatter, particles and process vapors." [来源](https://www.svs-schweisstechnik.de/en/products/laser-protection-windows/) — 厂商官网（SVS，激光焊接保护镜厂商）✅
- RP Photonics 的术语体系里这一类元件叫 **sacrificial window（牺牲窗）**，别名 **debris shield**：设计成"坏了就便宜地换掉"，以保护更贵的元件；并建议用专门支架便于快速更换。原文："a sacrificial window, also called a debris shield, is a protective window used in harsh environments like laser material processing. It is designed to be easily and inexpensively replaced when damaged." [来源](https://www.rp-photonics.com/optical_windows.html) — 行业技术百科（RP Photonics，作者 Dr. Rüdiger Paschotta，有编辑中立政策）✅
- 飞溅确实会打到保护镜上并导致停机更换：伊尔梅瑙工业大学的研究明确指出熔池飞溅液滴会沉积在激光头保护窗上、必须更换、造成停机。原文："The spatter can also deposit on the protective window of the laser optic which then needs to be replaced causing downtime." [来源](https://www.cavitar.com/library/spatter-behavior-in-laser-beam-welding-process/) — 应用论文（Ilmenau University of Technology 作者署名，Cavitar 刊载）✅
- ⚠️ 注意：**"保护镜"这个词在中文/英文里都有歧义**。同一英文 "laser protective window" 也指**激光安全防护观察窗**（按 OD 值衰减激光、保护人眼，装在设备外罩上）[来源](https://optlasers.com/laser-safety-window)。采购/写文档时必须区分，见第 8 节。

### 1.2 材质选择

| 材质 | 适用波段 | 关键数据 | 来源 |
|---|---|---|---|
| 熔融石英 Fused Silica（含 JGS1 合成石英） | UV / VIS / NIR（1064、1070nm） | 厂商明确列为"高功率激光器的标准基材（standard substrate）"；可耐 500°C | [SVS](https://www.svs-schweisstechnik.de/en/products/laser-protection-windows/) ✅ |
| 硼硅玻璃 Borosilicate | VIS / NIR 低功率 | 在同一厂商标准配置表中与熔石英、蓝宝石并列 | [SVS](https://www.svs-schweisstechnik.de/en/products/laser-protection-windows/) ✅ |
| 蓝宝石 Sapphire | VIS / NIR，耐磨环境 | 同表列为可选；文献对比指出蓝宝石用于"耐刮擦与户外耐候优先"的场合 | [SVS](https://www.svs-schweisstechnik.de/en/products/laser-protection-windows/)、[对比文](https://m.felixglass.com/blog/Fused-Silica-vs-Sapphire-Optical-Window-Full-Performance-Comparison_b30529) 🟡 |
| ZnSe | CO2 10.6μm（及 9.35μm） | 数据手册：总吸收 标准 <0.25%（≤9mm 厚）、低吸收选项 <0.15%；AR/AR@10.6μm 总透射 T>99.4%，单面反射 R<0.25%；楔角 <3 arcmin | [LASER COMPONENTS ZnSe 数据手册 PDF](https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/diverse-laser-optics/co2-laseroptics/znse-windows.pdf) ✅ |
| 光学玻璃 N-BK7 | VIS/NIR 低功率 | RP Photonics：VIS/NIR 窗常用熔石英与 BK7 | [RP Photonics](https://www.rp-photonics.com/optical_windows.html) ✅ |

- ❌ **未找到公开来源**：一份把"熔石英 vs 蓝宝石 vs ZnSe vs 光学玻璃"四者 LIDT 直接横向对比的**厂商一手数据表**（ZnSe 之外）。目前能拿到的只有分项数据和二手对比文。
- ZnSe 额外注意：ISO 21254-1 把 ZnSe 列入**有毒材料**警示清单（与 GaAs、CdTe、ThF4、硫系材料、Be 并列），涉及损伤测试后的样品处置。原文："In the case of toxic materials (e.g. ZnSe, GaAs, CdTe, ThF4, chalcogenides, Be…" [来源](https://cdn.standards.iteh.ai/samples/43001/82e64c00f69642a3914423945df39eec/ISO-21254-1-2011.pdf) — 标准样本 PDF ✅

### 1.3 镀膜与厚度

- AR 增透：厂商数据为**双面 AR、透射 >99%、反射 <0.2%**（SVS，1064nm 光纤激光典型值）[来源](https://www.svs-schweisstechnik.de/en/products/laser-protection-windows/) ✅；另一家工业件厂商给出**双面 AR，单面反射率 <0.1%，1064nm 总透射 >99.5%**，并声明支持到 30,000W [来源](https://lasvio.com/product/protective-window-for-fiber-laser-cutting-head/) 🟡（转销商产品页，非原厂）
- **无镀膜 vs 镀膜**：RP Photonics 指出未镀膜窗仅靠菲涅尔反射即有约 4% 单面损耗量级，且"未镀膜窗也作为商品出售，由用户自行镀膜"；AR 膜"只在有限波段有效"，宽带膜抑制反射的能力弱于窄带激光线膜。[来源](https://www.rp-photonics.com/optical_windows.html) ✅
  - 一条二手数值：未镀膜熔石英约 96% 透射，"≤3kW 可接受，6kW+ 不推荐"。[来源](https://lasercoppernozzle.com/protection-lens-ar-coating-damage-threshold-guide/) 🟡（转销商博客，**未在原厂处得到证实，谨慎引用**）
- **厚度**：SVS 标准品表里出现 **1.5 / 1.6 / 2.0 / 3.0 mm**，对应不同直径（19→3.0、26.8→2.0、27→2.0、30→1.5、38→2.0 或 3.0、50→1.5）[来源](https://www.svs-schweisstechnik.de/en/products/laser-protection-windows/) ✅；另一转销商列出常见厚度 1.5/2/3/4/5/6.35mm，并强调"厚度改变会改变安装位置与光学条件，不能因为直径相同就换厚度"[来源](https://www.linkmetalcnc.com/blogs/news/how-to-choose-protective-lens-for-fiber-laser-cutting-heads) 🟡
- ❌ **未找到公开来源**：任何厂商给出"何时必须用 1mm、何时必须用 3mm"的**定量判据**（例如按气压载荷或热梯度给出的选型公式）。目前只找到"厚度必须与刀架/抽屉匹配"的定性要求。

### 1.4 更换判据（**没有找到公认的百分比阈值**）

- **可按现象判定的清单（多源一致）**：
  - 雾状白斑、黑色烧坑、黄/褐色膜（常见于辅助气体污染）→ 立即更换。[来源](https://lasvio.com/how-to-tell-when-your-fiber-laser-protective-window-needs-replacing/) 🟡
  - 涂层损伤、裂纹、清洁后仍复现的热点 → **更换，不要反复清洁**。原文："Replace, do not over-clean: A window with coating damage, cracks or persistent hot spots should be replaced."（同上）🟡
  - 深色或彩虹色热痕、束内划伤/涂层缺陷、按规程清洁后仍残留的污染、反复出现激光头温度或保护窗报警 → 更换。[来源](https://machinistsvault.com/blogs/news/fiber-laser-consumable-replacement-intervals) 🟡（转销商维护指南，其中引用 TRUMPF/Bystronic 的做法但未见原厂原文）
  - 检测方法：拆抽屉 → 暗背景 + 强光**低角度斜照**（flashlight test）看雾斑/烧坑/色膜。[来源](https://lasvio.com/how-to-tell-when-your-fiber-laser-protective-window-needs-replacing/) 🟡
  - "烧坑不能擦"——涂层一旦损伤不可恢复。原文："Do not attempt to wipe off burn pits"（同上）🟡
- **机理（一手、可引用）**：污染物吸收激光能量 → 局部过热 → **热透镜效应（thermal lensing）** → 功率损耗、焦点位置漂移、涂层提前损伤，最终元件损坏。原文："Thermal lensing caused by high absorption of laser lens due to contamination can lead to many problems. It can cause irreversible thermal stress in the lens substrate, power loss when the beam passes through the lens, deviation of the focal point position, premature damage to the coating layer, and eventually damage to the lens." [来源](https://www.scanneroptics.com/how-to-avoid-secondary-contamination-of-lens.html) — **振镜厂商官网**（Scanner Optics）✅
- ❌ **未找到公开来源**：任何**一手厂商**给出的"功率下降 X% 即更换"的定量判据。我专门检索了 Precitec / TRUMPF / Bystronic / Raytools / WSX 的口径，找到的全部是**条件判定**（按现象、按报警、按切缝质量），没有任何一家给出百分比阈值。**建议在文档中明确写成"无公开统一阈值，由设备厂商维护手册规定"**，不要编造 5%/10% 这类数字。
  - 仅能找到的相关二手说法：中文行业文称"功率波动超过 5% 就可能使焊接良率下降 20% 以上"，但这是**工艺良率**论述，不是保护镜更换阈值。[来源](https://wh-dyzz.com/newsinfo/8667830.html) 🟡
- 检查周期（一手性存疑，但可作工程参考）：每班次检查喷嘴与保护窗；陶瓷环每周及每次碰撞后检查；每次打开抽屉/卡匣检查密封圈。[来源](https://machinistsvault.com/blogs/news/fiber-laser-consumable-replacement-intervals) 🟡

### 1.5 带气帘（air knife / cross-jet）的保护镜座

- 厂商方案：Bergmann Steffen 的 Tornadoblade 鼓风机式风刀——"在飞溅产生点就把焊接飞溅偏转开，保持光学件与工艺区之间的空间洁净，从而提高保护玻璃寿命，同时**大幅减少压缩空气消耗**"。原文："The Tornadoblade® deflects weld spatter from the point of origin, keeps the space between the optics and the process clean and thus increases the lifetime of the protective glass while drastically reducing the amount of compressed air required." [来源](https://www.bergmann-steffen.de/en/solutions/tornadoblade/) — 厂商官网 ✅
- 相关工艺侧证据（飞溅抑制的物理机制）：叠加二极管激光可扩大熔池、降低熔池流动动力学，从而**显著减少飞溅**。[来源](https://www.cavitar.com/library/spatter-behavior-in-laser-beam-welding-process/) — 论文（Ilmenau）✅
- ⚠️ **未找到公开来源**：横向对比"有/无气帘时保护镜寿命提升倍数"的定量数据。
- 附带一手事实：现代振镜扫描头普遍采用**密封壳体**防尘防水（SCANLAB SCANcube III 系列宣传"robust, sealed housing for protection against water and dust"）。[来源](https://pdf.directindustry.com/pdf/scanlab-gmbh/scancube-iii-scan-heads/39164-400637.html) 🟡（产品目录转载页）

---

## 2. 窗口片 vs 保护镜；光路里还有哪些窗口

- **定义差异（一手）**：光学窗口的功能是"把光学系统或元件与外界环境影响隔离开"——保护敏感件免受灰尘、湿气、腐蚀与机械损伤，同时让光通过。原文："used for isolating optical systems or components against detrimental influences from the environment." [来源](https://www.rp-photonics.com/optical_windows.html) ✅
  - 因此：**窗口片是通用功能名**（隔离环境），**保护镜 = 窗口片的一个子集**，特指处于工艺污染最前线、被设计成定期更换的**牺牲窗/debris shield**。
  - 同一页给出关键工程理由：在恶劣环境中单设一片窗更划算，因为**换窗比换高质量光学元件既容易又便宜**。✅
- **振镜/激光头光路里的窗口清单**：
  1. **激光器输出窗（output window）**：RP Photonics 指出输出耦合镜若有显著透射，**基片后表面的反射会造成寄生标准具效应（etalon）或鬼光束**，解决办法是后表面镀优质 AR 膜，并且**基片通常做轻微楔角（例如 30 arcmin）**把鬼反射在空间上分离，避免反馈回谐振腔。原文："the substrate is often slightly wedged (e.g. by 30 arcminutes) to spatially separate the ghost reflection from the main beam, preventing it from feeding back into the laser resonator." [来源](https://www.rp-photonics.com/laser_mirrors.html) ✅
  2. **激光器壳体窗**："housings of lasers are often protected with optical windows to keep the housing free of any dust." [来源](https://www.rp-photonics.com/optical_windows.html) ✅
  3. **扫描头密封窗 / 场镜后保护窗**：见第 1 节；振镜厂商要求密封以防尘防水 [来源](https://pdf.directindustry.com/pdf/scanlab-gmbh/scancube-iii-scan-heads/39164-400637.html) 🟡
  4. **激光安全观察窗（外罩上）**：按 OD（光密度）选型，与上述光学窗完全不是一回事。OD 6 对应理论透射 ≤ 1×10⁻⁶；且"OD 额定值必须对应实际激光波长"，OD 6+@190–540nm 的产品对 1064nm **不提供**该额定防护。[来源](https://optlasers.com/laser-safety-window) 🟡（厂商页面，但技术陈述自洽）
- 平行窗 vs 楔形窗（工程要点）：平行窗只产生轻微光束位移、不偏折，通常无需精密对准；楔形窗有确定楔角，会产生光束偏折，用于消除两表面寄生反射之间的干涉（标准具）效应。[来源](https://www.rp-photonics.com/optical_windows.html) ✅

---

## 3. 分光取样镜（beam sampler / pickoff mirror / partial reflector）

### 3.1 原理与分光比

- **未镀膜表面菲涅尔反射取样**：Thorlabs 的 beam sampler 用未镀膜光学面的菲涅尔反射"拾取入射光的 1–10%，比例取决于入射光的偏振态"。原文："utilize the Fresnel reflection from an uncoated optical surface … to pick off 1-10% of an incident beam, depending on the incident light's polarization." [来源](https://www.thorlabs.com/beam-samplers) ✅
  - 工程含义：**菲涅尔取样的分光比随偏振变化**，若激光偏振态在传输中变化（如经过振镜镜面反射后 s/p 比例改变），取样比会漂移 → 影响功率监测精度。这是一条重要但常被忽略的事实。
- 后表面处理：取样镜"后表面做成楔形以避免内部条纹（internal fringes），并镀 AR 膜以消除鬼像"。原文："The back surface is wedged to avoid internal fringes and is anti-reflection coated to remove ghost images." [来源](https://www.holmarc.com/beam_samplers.php) 🟡（厂商页面）
- 介质膜部分反射镜/分光镜可用于更宽的分光比范围："A wide range of power splitting ratios can be achieved via different designs of the dielectric coating." [来源](https://www.rp-photonics.com/beam_splitters.html) ✅
- ⚠️ 注意介质膜分光镜的**偏振敏感性**：反射率"强烈依赖偏振态"，近正入射时最容易做到非偏振。[来源](https://www.rp-photonics.com/beam_splitters.html) ✅
- 关于 0.1% / 1% / 4% 这类具体分光比：**1%（乃至 1–10%）有厂商一手确认**（Thorlabs，见上）✅；**0.1% 与 4% 未找到对应的厂商一手规格**（❌）——不要凭空写这两个数字，除非能在具体型号数据手册上核到。

### 3.2 取样位置：振镜前 vs 振镜后

- **可引用的专利一手描述**：CN121261196A《高功率振镜焊接的外部激光功率闭环监测系统及监测方法》（申请人：北京正时精控科技有限公司，申请日 2025-12-04，公开日 2026-01-02）公开了**级联分光取样**结构：反射镜安装壳内倾斜安装**一级反射镜**，其透过的激光再由**二级反射镜**反射，最后由集成式驱动采集模块采集功率信号；目的是"提高监测精度、响应速度"。原文摘要："分光取样模块，包括倾斜安装于所述反射镜安装壳内的一级反射镜……还包括倾斜安装于所述反射镜安装壳内的二级反射镜……用于反射所述一级反射镜透过的激光；集成式驱动采集模块，位于所述二级反射镜反射激光的方向上，用于采集激光功率信号。" [来源](https://www.imaibj.cn/patent/details/202511817087) — 专利（已公开待审）✅
  - 该专利名里的"**外部**"是关键：**取样点在激光进入振镜之前/之外**。这类"外部监测"测到的是**进入扫描头的功率**，不含振镜镜片、场镜、保护镜的损耗。
- **为什么"振镜后（更靠近工件）取样才能看到实际到工件的功率"——这里的证据链**：
  1. **振镜后各元件确实会显著改变到工件的功率**：保护镜污染造成吸收↑ → 热透镜 → **功率损耗 + 焦点位置漂移 + 涂层提前损伤** [来源](https://www.scanneroptics.com/how-to-avoid-secondary-contamination-of-lens.html) ✅
  2. 工艺侧的诊断共识也是"**工件处的功率损失 ≠ 激光器输出功率损失**"，且应按"从最靠近工件的元件开始、逐级向光源回溯"的顺序排查。原文："Output power loss at the workpiece and output power loss at the laser source are not the same thing…trace the path of light backward, beginning with the component nearest the workpiece." [来源](https://whcstec.com/what-to-check-when-your-fiber-laser-source-output-drops/) 🟡（厂商技术文，非原厂手册）
  3. 结论（**这是推论，不是引文**）：把取样点放在振镜/场镜之后、保护镜附近，采样光路里包含了这些"会劣化"的元件，因此该信号能反映真实到工件的功率下降；而振镜前取样对保护镜污染、场镜热透镜不敏感，只能反映光源输出。⚠️ **未找到**任何厂商/论文以对照实验数据（振镜前 vs 振镜后取样读数差异）证明这一点，故以上机制链中"取样位置决定监测准确性"这句**属于机理论证，不是文献直证**。
- 楔形镜（wedge）的两条作用（一手）：
  1. **消除标准具条纹**：平行平板内部多次反射干涉会产生随波长/角度变化的周期性透射纹波，楔角把谐振"在整个孔径上去调谐（de-tune）"，把条纹洗掉。[来源](https://www.nandioptics.com/wedge-window) 🟡（厂商技术页）
  2. **抑制回光**："By angling the two surfaces relative to each other, a wedge window deflects the front-surface and back-surface reflections in different directions, both away from the original beam axis — preventing reflected light from coupling back into a laser cavity or interfering with the primary measurement beam."（同上）🟡
  - 一手佐证：RP Photonics 明确"wedged window 通常楔角极小（几角分或不到 1°），**主要目的不是偏折光束，而是抑制平行平板的标准具效应，或避免面反射返回激光光源**"；激光镜基片常用 30 arcmin 楔角分离鬼反射。[来源](https://www.rp-photonics.com/wedge_prisms.html)、[来源](https://www.rp-photonics.com/laser_mirrors.html) ✅
  - 楔角与偏折量的关系（公式，一手）：小楔角 α 时偏折角 δ ≈ (n−1)·α，n 为折射率；普通玻璃 n≈1.5 时偏折角约为楔角的一半。[来源](https://www.rp-photonics.com/wedge_prisms.html) ✅
  - 楔角选型区间（二手）：light wedge 2–10 arcmin（最小束偏折）／标准 0.5°–2°（通用回光消除）／steep 3°–10°（强分离，用于分光取样与高隔离度场合）。[来源](https://www.nandioptics.com/wedge-window) 🟡
- **功率闭环怎么用这个信号**：找到的直接证据较弱。
  - 可引用：扫描头本身有闭环（振镜位置环，实时光束指向反馈），且"检测到异常 10ms 内自动关光"。[来源](https://www.scanneroptics.com/galvo-laser-welding.html) 🟡
  - 专利宣称其分光取样 + 集成驱动采集模块可"提高监测精度、响应速度"，用于**功率闭环监测**。[来源](https://www.imaibj.cn/patent/details/202511817087) ✅
  - ❌ **未找到公开来源**：闭环控制律本身（比例/积分、带宽、如何用取样功率去调节激光器输出）、以及闭环精度指标。这类内容属厂商专有技术，公开资料几乎没有。

---

## 4. 光阑 / 空间滤波（aperture / spatial filter）

### 4.1 光阑与空间滤波的常规作用

- **空间滤波器的构成与作用（一手）**：由显微物镜 + 针孔光阑 + 定位机构组成，等效于开普勒望远镜的第一片透镜，针孔置于焦点处；作用是"去除不需要的多阶能量峰、只通过衍射图的中心极大"，从而得到干净的高斯光束；同时**去除光路中灰尘/元件表面造成的散射光**——"This scattered light can leave unwanted ring patterns in the beam profile. The spatial filter removes this additional spatial noise." [来源](https://www.edmundoptics.com/knowledge-center/application-notes/lasers/understanding-spatial-filters/) ✅
- **针孔直径怎么定（一手）**：Edmund Optics 给出透射功率百分比 p 与针孔直径 D、物镜焦距 f 的关系式，并给出经验规则——**约 99.3% 功率透射时的 D 被普遍接受为最优针孔尺寸**（即工程上常用的 D ≈ 1.83·λ·f/D_beam 形式）。原文："A good rule of thumb is that approximately 99.3% of power is transmitted when: … The diameter found using Equation 2 is commonly accepted as the optimal size for a spatial filter."（同上）✅
  - 关键取舍（同页）：针孔**变小**→ 触到衍射极限，光束向各方向散射，**得到与目标相反的结果**；针孔**变大**→ 放过更多杂散光。多数情况下宁可选大一点。✅
- **等价术语**：spatial filter 也叫 **mode cleaner**，用于"通过去除强度与相位分布中的畸变来改善激光光束质量"。[来源](https://www.rp-photonics.com/mode_cleaners.html) ✅

### 4.2 空间滤波在振镜系统里的应用——**很少见，原因是结构性的**

- ⚠️ **未找到公开来源**：任何厂商/论文描述在**振镜扫描头内部或之后**使用针孔空间滤波器。检索无果。
- 我给出的机理解释（**属推论，明确标注**）：空间滤波要求针孔精确位于**会聚焦点**处。而振镜系统里，焦点是由 f-theta 场镜在**扫描平面上随扫描角移动**的——焦点位置随振镜偏转在工件面上移动（这正是扫描的目的）。针孔若放在该焦点处，会随扫描位置偏离针孔，把"扫描"直接破坏掉。因此针孔空间滤波与"扫描"这一功能在原理上冲突，只能放在**扫描前**的准直光路里（此时它并不改善场镜之后的像差/污染问题）。
- 实践中振镜系统抑制杂散光/高阶模更常用的是别的手段（**部分有来源**）：
  - **密封壳体 + 正压/气帘**防尘（避免散射源）[来源](https://pdf.directindustry.com/pdf/scanlab-gmbh/scancube-iii-scan-heads/39164-400637.html) 🟡、[来源](https://www.bergmann-steffen.de/en/solutions/tornadoblade/) ✅
  - **光阑限制光束直径/挡边缘光**：RP Photonics 把 optical apertures 单列为光学元件类别，但**未找到**其在振镜系统中的定量设计数据。❌
  - 环形/点环光斑通常是**主动整形**（衍射光学元件 DOE、涡旋光）而不是滤波残留。[来源](https://laser.hust.edu.cn/info/1107/1143.htm) 🟡

### 4.3 杂散光 / 回光对振镜的危害与遮挡设计

- **最强的证据是一篇同行评议论文**：《Investigation of Galvanometer Scanner Failure During the Laser Processing of High Reflectivity Materials and Concrete Composite Materials》（Int. J. Precision Engineering and Manufacturing, 2024）。摘要明确：加工电池电芯与混凝土复合材料会产生大量副产物，包括**污染物与回光（back reflection）**；扫描头的**光学元件因这些副产物引起的激光辐照而遭受热损伤**；论文还讨论了**回光如何在污染物存在的情况下加剧损伤、导致镜片热损伤**。原文："It is found that the processing of battery cells and concrete composites produces a lot of byproducts such as contaminants and back reflection. The optical component of the scanner suffers thermal damage due to the laser irradiation of the byproducts…how the back reflection aggravates this damage in the presence of the contaminants causing thermal damage to the mirror was also discussed." [来源](https://link.springer.com/article/10.1007/s12541-024-01133-1) — 论文（Springer，同行评议）✅
  - 关键词（论文自带）：Galvanometer scanner / Byproducts / Contaminants / Back reflection / Thermal damage。✅
- 回光到达光源侧的链路（一手、分步）：工件反射 → 光学系统收集 → 反向耦合进传输光纤 → 纤芯/包层传播 → 防护 → 监测 → 继续/降额/报警/关断。原文："Workpiece reflection → optical collection → reverse fiber coupling → core/cladding propagation → protection → monitoring → continue, derate, alarm, or shut down." [来源](https://whcstec.com/fiber-laser-back-reflection-damage-protection/) 🟡
  - 同时给出一个重要概念区分：**材料反射率 ≠ 实际回到激光器的回光功率**。[来源](https://whcstec.com/fiber-laser-back-reflection-damage-protection/) 🟡
- **遮挡/抑制设计的可引用手段**：
  - 楔形输出窗（30 arcmin 级）把鬼反射从主光路空间分离，防止反馈回谐振腔 [来源](https://www.rp-photonics.com/laser_mirrors.html) ✅
  - 光隔离器（Faraday isolator）用于抑制回光——但**未找到**振镜系统专用的隔离设计参数。❌
  - 光纤激光器在铜/黄铜等高反材料加工时的回光报警/热保护跳闸，是"事件触发的失效模式"。[来源](https://whcstec.com/what-to-check-when-your-fiber-laser-source-output-drops/) 🟡

---

## 5. 损伤阈值 LIDT

### 5.1 定义与单位（**CW 的单位有一个必须知道的坑**）

- **定义（标准原文）**：ISO 21254-1 把 threshold 定义为"入射到光学元件上的、其外推损伤概率为零的**最高**激光辐射量"，该量可表示为能量密度 Hth、**功率密度 Eth** 或**线功率密度 Fth**。原文："highest quantity of laser radiation incident upon the optical component for which the extrapolated probability of damage is zero, where the quantity of laser radiation may be expressed as energy density Hth, power density Eth, or linear power density Fth" [来源](https://cdn.standards.iteh.ai/samples/43001/82e64c00f69642a3914423945df39eec/ISO-21254-1-2011.pdf) ✅
- **单位（标准原文）**：
  - 脉冲激光："Damage thresholds of pulsed lasers are usually expressed in units of energy density (J/cm²). The pulse duration of the test laser shall be documented in the test report."
  - 连续激光："Damage thresholds of cw-lasers are usually expressed in terms of units of **linear power density (W/cm)**."
  - 线的定义："linear power density threshold, expressed in **watts per centimetre (W/cm)**, above which damage might occur"，且注明**线功率密度适用于 CW 与长脉冲**；"长脉冲"的判据是热扩散长度 (2Dτ_eff)^½（D 为热扩散率）与测试光斑直径 d_T,eff 同量级。
  - 符号表：Emax [W/cm²]、Hmax [J/cm²]、Fmax [W/cm]、Eth [W/cm²]、Hth [J/cm²]、Fth [W/cm]。
  （以上均出自 [ISO 21254-1:2011 样本 PDF](https://cdn.standards.iteh.ai/samples/43001/82e64c00f69642a3914423945df39eec/ISO-21254-1-2011.pdf)）✅
  - ⚠️ **实务含义**：标准体系给 CW 的规范单位是 **W/cm（线功率密度）**，而厂商目录与科普材料给 CW 的规格普遍是 **W/cm²（功率密度）**。二者不可混用；比较时务必确认口径。
- **术语现状**：该文件版本为 ISO 21254-1:2011。ISO 现行目录显示已有 **ISO 21254-1:2025**（同一标准号、同一标题"Lasers and laser-related equipment — Test methods for laser-induced damage threshold — Part 1: Definitions and general principles"）。[来源](https://www.iso.org/standard/83937.html) 🟡（我仅见到 ISO 目录页标题，未取得 2025 版正文；2011 版定义见上方样本 PDF）
- **"损伤"的判定极严（一手）**：按 ISO 21254，"元件在曝光后**任何可检测的变化**都算损伤"；但"ISO 定义的损伤**不必然意味着性能退化**"，因为性能影响是应用相关的。原文："According to ISO 21254:2011, any detectable change in an optic after exposure to a laser is considered damage." / "what ISO defines as 'damage' does not necessarily imply performance degradation because it is application-dependent." [来源](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/understanding-and-specifying-lidt-of-laser-components/)、[来源](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/laser-damage-threshold-testing/) ✅
- **概率性质**：LIDT "不能被认为低于该通量就绝不会损伤"，而是损伤概率低于临界风险水平；风险水平取决于光斑直径、每样品测试点数、样品数。[来源](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/understanding-and-specifying-lidt-of-laser-components/) ✅

### 5.2 CW 与脉冲的机理差异

- **CW（及长脉冲）→ 热效应主导**：损伤源于"涂层或基片中的吸收导致的热效应"；胶合元件（如消色差镜）因胶层吸收/散射而 CW 阈值更低。[来源](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/understanding-and-specifying-lidt-of-laser-components/) ✅
  - 温度升高 ΔT 与热学参数（k 热导率、κ 热扩散率）、表面吸收 β_s、**光束直径 w** 相关；当辐照时间 t_I 远长于特征热扩散时间 w²/κ 时，公式可化简为渐近形式。[来源](https://www.laseroptik.com/en/customer-service/lidt) ✅
  - **吸收主导下的标定律（厂商一手）**：短脉冲 LIDT ∝ P/w²；长辐照或 CW 时 **LIDT ∝ P/w（与光束直径成线性，即线功率密度概念）**。原文："short pulses: LIDT ~ power density P/w²；long irradiation times or cw: LIDT ~ linear power density P/w"。**这条直接解释了为什么 ISO 用 W/cm 给 CW 定标**。[来源](https://www.laseroptik.com/en/customer-service/lidt) ✅
  - 延迟：热过程"从开始辐照到损伤出现往往有几十秒量级的延迟，必须计入"。（同上）✅
- **脉冲 → 缺陷主导 + 电子过程**：
  - 现代 VIS/NIR 镀膜吸收极低，损伤"由嵌入膜层结构中的缺陷主导"——缺陷吸收远高于周围膜材，受照后快速升温爆裂，掀掉上层膜系，形成小坑。[来源](https://www.laseroptik.com/en/customer-service/lidt) ✅
  - 脉宽定标（厂商一手，方根律）：**LIDT ∝ τ^x，x = 0.5**，适用 0.1–10 ns；在 ms 量级可把指数换成 0.5–2 之间；但**主要适用于热损伤过程**，跨一个数量级以上的外推要极度小心；**低于约 20 ps 时由热过程转向电子效应，τ^x 标定律可能不再适用**。[来源](https://www.laseroptik.com/en/customer-service/lidt) ✅
  - 另一厂商给出的经验式：LIDT ~ 2^(-lg(rep-rate))；LIDT ~ τ^(1/2)（τ > 0.1 ns）；LIDT ~ τ^(1/3)（τ < 20 ps）；"从 ns 降到 ps，损伤机制改变，方根律不再适用"。[来源](https://www.laseroptik.com/en/coating-guide/thin-film-basics/hr-standards) ✅
  - 超快（fs）机制（一手）：能量先被基态电子吸收、数 fs 内占据激发态（"热"电子），再经 ps 量级声子-电子/声子-声子散射弛豫、重分布能量；可用双温模型描述。给出的算例：**0.2 J/cm²、10 fs、800nm、光斑直径 120μm** 照在 200nm 金纳米膜（铜基）上，电子温度可瞬时达 13,000K，晶格温度升至约 1,300K，已接近金的熔点 1,337K。[来源](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/lidt-for-ultrafast-lasers/) ✅
  - 波长趋势："对多数材料和多数工况，**LIDT 随波长减小而降低**"；且"波长标定始终有损伤机制随波长改变的风险，尤其接近吸收带时"。[来源](https://www.laseroptik.com/en/customer-service/lidt) ✅

### 5.3 光斑直径对 LIDT 的影响（面积效应）

- **机理（一手）**：光斑越大，越可能覆盖低阈值缺陷。原文："When the beam size of a laser used for LIDT testing is significantly larger than the density of defects on the optic, the likelihood of triggering scarce damage mechanisms is high… If the beam size is too small, low defect densities are not always detectable and parts appear more resistant to damage than they actually are." [来源](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/importance-of-beam-diameter-on-laser-damage-threshold/) ✅
- **ISO 下限**：LIDT 测试允许的**最小光斑直径为 0.2 mm**；很多供应商倾向用尽可能小的光斑（因为容易做到高通量），但这会造成表面缺陷的"欠采样（under-sampling）"。（同上）✅
- **量级示例（同页简化模型）**：存在两类缺陷，多数阈值 10 J、少数阈值 1 J。0.2mm 光束几乎测不到 1J 缺陷 → 阈值读到接近 10J；放大到 2mm，1J 处损伤概率陡增；放大到 10mm，1J 处几乎必然损伤。**"光斑从 0.2mm 放大到 10mm，LIDT 下降一个数量级（factor of 10）。"**（同上）✅
- **标定公式（一手，注意这是"近似"）**：
  LIDT(λ₂, τ₂, ∅₂) ≈ LIDT(λ₁, τ₁, ∅₁) × (λ₂/λ₁) × √(τ₂/τ₁) × (∅₁/∅₂)²
  同页文字说明："For small changes in beam diameter, this scaling can be approximated by multiplying the original LIDT value by the square of the ratio of the original diameter to the new diameter."
  **适用边界（明确写出）**："This scaling should not be applied over large wavelength or pulse duration ranges. For example, Equation 5 would be adequate for a wavelength shift from 1064nm to 1030nm, but should not be applied for scaling an LIDT value at 1064nm to a drastically different wavelength, such as 355nm."
  [来源](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/understanding-and-specifying-lidt-of-laser-components/) ✅（同式也见[面积效应专页](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/importance-of-beam-diameter-on-laser-damage-threshold/)）
- **厂商侧独立佐证（一手）**："关于 LIDT 随光束直径的变化，大量研究表明**阈值随光束直径增大而下降**"；缺陷主导击穿时，若光束尺寸小于可致损缺陷的平均间距，问到临界缺陷的概率低、阈值高；随光束直径增大该概率渐近趋于 1，LIDT 趋近较小的缺陷损伤阈值。[来源](https://www.laseroptik.com/en/customer-service/lidt) ✅
- Layertec 的表述（我未取得正文，仅见搜索摘要）："LIDT is usually normalized to beam spot area, but a larger beam will likely illuminate more defects. This may result in a smaller damage threshold." [来源](https://www.layertec.de/en/knowledge/knowhow-LIDT/) 🟡（仅摘要，正文被网络策略拦截）
- **测试协议对数值的影响（一手）**：1-on-1（每点单脉冲）与 S-on-1（每点 S 个脉冲）结果不同；1-on-1 阈值"如今主要只有学术意义、对实际应用价值有限"，却仍被大量厂商目录列为主打；S-on-1 更贴近实际，并可把特征损伤曲线外推到 10⁹–10¹² 脉冲量级以粗估元件寿命。[来源](https://www.laseroptik.com/en/customer-service/lidt) ✅
- **规格类型（一手）**：LIDT 有 Certified（厂商自测认证）／Reference（对批量样品按 ISO 21254 测试以保证性能）／By Design（未测试，依设计推断）三类，比较元件时不可混用。[来源](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/different-types-of-lidt-specifications/) ✅
- **不确定度（一手）**：LIDT 是二项分布的损伤概率函数，置信区间用 Wilson score interval 计算；**在每通量级 10 个测试点的条件下，损伤概率只能确定到约 ±25%**（若 10 点全无损伤，则第 11 点发生损伤的最坏概率约 25%）；要优于 ±5% 需要在每个通量级打 **100 发以上**。[来源](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/uncertainty-in-lidt-specifications/) ✅
- **安全系数（一手）**：行业通行做法是用**2 倍或 3 倍**安全系数；但因应用与激光类型差异很大，"**没有普适的安全系数**"。原文："Common industry practice is to use a safety factor of two of three. However… no general safety factor works for all situations." [来源](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/laser-damage-threshold-testing/) ✅

### 5.4 算例：1000W 连续激光、光斑直径 50μm 的功率密度

**公式（写清符号与单位）**

- 光斑面积（按圆直径 d 定义）：A = π (d/2)²，A [cm²]，d [cm]
- 平均功率密度（平顶光束）：E = P / A，E [W/cm²]，P [W]
- 高斯光束**峰值**功率密度：E_peak = 2P / A（同功率下高斯束峰值是平顶的 2 倍）——一手依据："The peak fluence of a Gaussian beam is twice as large as that of a flat top beam with the same optical power." [来源](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/understanding-and-specifying-lidt-of-laser-components/) ✅

**数值代入**

d = 50 μm = 50 × 10⁻⁴ cm = 5.0 × 10⁻³ cm
A = π × (5.0×10⁻³ / 2)² = π × (2.5×10⁻³)² = π × 6.25×10⁻⁶ = **1.963×10⁻⁵ cm²**
E = 1000 W / 1.963×10⁻⁵ cm² = **5.09×10⁷ W/cm²** = **50.9 MW/cm²** = **50.9 kW/mm²**
E_peak（高斯）= 2 × 50.9 = **约 102 MW/cm²**

**怎么用它选元件**

1. 用**与元件规格同一口径**的单位和定义比对：厂商若给 W/cm²，就用上面的 E（若光束是高斯，取峰值 E_peak）；厂商若按 ISO 给 W/cm（线功率密度），要换算成"每单位长度上的功率"——`F = P/d = 1000 W / (5.0×10⁻³ cm) = 2.0×10⁵ W/cm = 200 kW/cm`，而不是 50.9 MW/cm²。**这是最容易搞错的地方。**
2. 确认规格的**测试条件**（波长、光斑直径、脉宽或 CW、1-on-1 还是 S-on-1、Certified/Reference/By Design）。[来源](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/different-types-of-lidt-specifications/) ✅
3. 若规格的测试光斑与应用光斑不同，用面积效应公式折算，并记住它只是**近似**、且 50μm 远小于 ISO 允许的最小测试光斑 0.2mm，**外推到 50μm 属于大幅外推，风险高**。[来源](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/importance-of-beam-diameter-on-laser-damage-threshold/) ✅
4. 留 **2–3 倍**安全系数（无普适值），并考虑热点、功率波动。[来源](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/laser-damage-threshold-testing/) ✅
5. 注意统计不确定度（10 点测试 → ±25%）。（来源同上）

- 📌 **交叉核对（已验证）**：Edmund Optics 同页给出的 CW 算例是"5 mW、532nm、平顶、光斑直径 1mm → 功率密度 0.64 W/cm²"，并提示"高斯束需再加 2 倍系数"。[来源](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/understanding-and-specifying-lidt-of-laser-components/) ✅
  我用同一公式复算该算例：A = π(0.05)² = 7.854×10⁻³ cm²，E = 0.005/7.854×10⁻³ = **0.637 W/cm² ≈ 0.64 W/cm²**，与厂商值一致 → 说明本文 50.9 MW/cm² 所用的公式与圆直径约定与厂商口径一致。
- ⚠️ **必须同时声明光斑直径的定义**：光斑直径有 FWHM、1/e²、D4σ 三种常用定义，彼此不等价（1/e² 对应峰值强度的 13.5% 处；D4σ 为二阶矩定义，见 ISO 11146）。[来源](https://zhuanlan.zhihu.com/p/601284014) 🟡。上面算例按"几何圆直径"处理，若厂商规格按 1/e² 或 D4σ 标注，代入的 d 不同，结果会明显不同——**比对前必须先统一口径**（尤其 ZnSe 手册明确写的是 "1/e²"）。

### 5.5 镀膜 vs 基材：谁先坏？（**结论明确：镀膜是短板**）

- **厂商一手、直述**：历史上光学材料本身的体质量与功率承受能力已被优化到很好，"因此在过去几十年里，激光损伤问题**从体材料转移到了元件表面**"；而"**沉积在光学表面、用于调整反射/透射的薄膜涂层体系，对 LIDT 降低贡献最大。它被认为是高功率激光元件开发中最关键的环节**"。原文："the problem of laser induced damage shifted from the bulk to the surface of the optical component during the last decades… the thin film coating system… contributes predominantly to the reduction of the LIDT-values. It is considered the most critical element in the development of high power laser components." [来源](https://www.laseroptik.com/en/customer-service/lidt) — 镀膜厂商官网 ✅
- **同一厂商的另一条关键权衡**："**通常 LIDT 最高的镀膜并不是反射率最高的镀膜**"。原文："Normally coatings with the highest LIDT will not have the highest reflection." [来源](https://www.laseroptik.com/en/coating-guide/thin-film-basics/hr-standards) ✅
  - 同页还给出 1064nm 高反膜的常规损耗水平：**标准 EBE 镀膜吸收 <20 ppm、散射 <150 ppm；IBS 可做到 <10 ppm**；标准 HR 1064nm/45° 的反射为 Rs>99.9%、Ru>99.8%、Rp>99.7%。✅
- **基材侧数据**：ISO 21254-1 明确"**前表面与后表面的损伤阈值可能不同**"，且"损伤可发生在前表面或后表面"。原文："The damage threshold value for the front surface may differ from that for the rear surface." [来源](https://cdn.standards.iteh.ai/samples/43001/82e64c00f69642a3914423945df39eec/ISO-21254-1-2011.pdf) ✅
- **第三方学术佐证**：Ristau, Jupé & Starke, "Laser damage thresholds of optical coatings", Thin Solid Films 518(5), 1607–1613 (2009) —— 光学镀膜 LIDT 的权威综述，被上述 Springer 论文引用。[文献条目见 Springer 参考文献列表](https://link.springer.com/article/10.1007/s12541-024-01133-1) 🟡（我仅见到该参考文献条目，未取得全文）
- **被引用的相关文献线索（可用于进一步查证）**：
  - Han, K., Song, R., Xu, X., "Influence of the contaminant size on the thermal damage of optical mirrors used in high energy laser system", SPIE 9952, 99520M (2016), doi:10.1117/12.2236773 —— 直接研究**污染物尺寸**对镜面热损伤的影响。🟡
  - Han, Song & Xu, "The thermal damage process of the contaminated optical element used in high energy laser system", SPIE 10173, 101730G (2017), doi:10.1117/12.2267510。🟡
  - Palmier et al., "Laser damage to optical components induced by surface chromium particles", SPIE 5647, 156 (2005), doi:10.1117/12.585248 —— 表面金属颗粒诱发损伤。🟡
  （以上条目均见 [Springer 论文参考文献列表](https://link.springer.com/article/10.1007/s12541-024-01133-1)）
- **1064nm HR / AR 膜的典型 LIDT 数值**：见第 5.6 节（含厂商一手实测表）。

### 5.6 可核到的 LIDT 数值（截至本次调研）

#### 5.6.1 厂商一手实测数据集（**本调研最有价值的一条**）

OPTOMAN（立陶宛，IBS 镀膜厂）在官网公开了**按 ISO 标准或客户现场实测得到的 LIDT 测试值表**，并明确标注"这些值可信，但**不等于最终产品规格，必须考虑安全系数**"。原文："Values are the result of LIDT test procedure according to ISO standards or based on the measurements done at customer sites. While the values are trustworthy, it doesn't mean that they can be transferred to final product specifications as the safety factor should be considered." [来源：OPTOMAN LIDT Capabilities](https://www.optoman.com/technology/lidt-capabilities/) — 厂商官网技术页 ✅

| 镀膜类型 | 波长 (nm) | 脉宽 | 重频 | 光束直径 | **LIDT (J/cm²)** |
|---|---|---|---|---|---|
| HR | 1030 | 500.9 fs | 10 kHz | 185 μm | 0.78 |
| HR | 1030 | 499.7 fs | 100 kHz | 121 μm | 1.084 |
| HR | 1030 | 201.6 fs | 500 kHz | 58.2 μm | 0.941 |
| HR | 515 | 202.8 fs | 1 kHz | 127.9 μm | 0.546 |
| HR | 343 | 300.8 fs | 200 kHz | 40.9 μm | 0.376 |
| HR | 258 | 305.4 fs | 200 kHz | 34.4 μm | 0.306 |
| HR+HT | 258 | 299.9 fs | 200 kHz | 17.3 μm | 0.359 |
| Polarizer | 1030 | 504.6 fs | 10 kHz | 173.6 μm | 0.77 |
| HR | **1064** | **370 ps** | 20 Hz | **2.4 mm** | **2.58** |
| HR | 532 | 350 ps | 20 Hz | 2.1 mm | 1.64 |
| HR | 1030 | 10 ps | 1000 Hz | 0.154 mm | 8.313 |
| **AR** | **1064** | **370 ps** | 20 Hz | **2.3 mm** | **5.5** |
| AR | 532 | 350 ps | 20 Hz | 2.1 mm | 2.1 |
| AR | 343 | 1 ps | 20 Hz | 1 mm | 0.39 |
| Polarizer | 1030 | 10.1 ps | 10 kHz | 0.113 mm | 2.7 |
| **HR** | **1064** | **9.8 ns** | 100 Hz | **223.5 μm** | **168** |
| HR | 532 | 10 ns | 100 Hz | 219.7 μm | 38.18 |
| HR | 193 | 9.6 ns | 30 Hz | 549 μm | 0.3 |
| **AR** | **1064** | **10.2 ns** | 100 Hz | **231.7 μm** | **96.1** |
| AR | 532 | 10 ns | 10 Hz | 421 μm | 10 |
| AR | 532 | 10 ns | 100 Hz | 217.8 μm | 35.0 |
| AR | 355 | 5.3 ns | 100 Hz | 225.5 μm | 15.9 |
| HR+HT | 532 | 5.8 ns | 100 Hz | 403.7 μm | 12 |
| HR+HT | 355 | 10 ns | 100 Hz | 218.4 μm | 14.81 |
| Polarizer | 1064 | 10.4 ns | 100 Hz | 206.2 μm | 49.4 |
| Polarizer | 1064 | 10.48 ns | 20 Hz | 410 μm | 44.96 |
| Polarizer | 532 | 10 ns | 100 Hz | 216.7 μm | 8.9 |

（整表出自 [OPTOMAN LIDT Capabilities](https://www.optoman.com/technology/lidt-capabilities/)）✅

**这张表能直接支撑的结论（都是可验证的趋势，不是我的猜测）：**

1. **1064nm、ns 量级的典型 LIDT 量级**：HR 膜 **168 J/cm²**（9.8ns, 100Hz, 223.5μm）、AR 膜 **96.1 J/cm²**（10.2ns, 100Hz, 231.7μm）。→ **HR 膜阈值高于 AR 膜**（此数据集内约 1.7 倍），且二者**都在百 J/cm² 量级**。这可以替换任何"常见数值"的模糊说法。
2. **脉宽效应极大**：同为 HR@1030nm，fs（≈0.94 J/cm²，58μm）→ ps（8.3 J/cm²，10ps）→ ns 量级。fs 与 ns 之间相差**两个数量级以上**。→ 引用 LIDT 数值时**不写脉宽等于没说**。
3. **重频效应（同一镀膜体系内可比）**：HR@1030nm/500fs 从 10 kHz 的 0.78 J/cm² → 100 kHz 的 1.084 J/cm²（此处阈值上升）；而 AR@532nm/10ns 从 10 Hz 的 10 J/cm² → 100 Hz 的 35.0 J/cm²（**更高**），Polarizer@1064nm 从 20 Hz 的 44.96 → 100 Hz 的 49.4 J/cm²（**更高**）。→ ⚠️ **本数据集并不单调地支持"重频越高阈值越低"**，说明重频与阈值的关系还强烈依赖光束直径与镀膜体系，不能当作简单规律引用。**不要写"重频越高 LIDT 越低"这种简化结论。**
4. **波长效应**：1064nm→532nm→355nm→193nm，HR 膜阈值从 168 → 38.18 → （193nm）0.3 J/cm²，**单调急剧下降**。→ 一手印证了 Laseroptik 的"LIDT 随波长减小而降低"。✅
5. **光斑直径效应（同厂商同工艺，最有说服力的一组对照）**：ps 段的 HR 测试用了 **2.4mm** 光斑（2.58 J/cm²），而 fs 段用 **58–185μm** 小光斑（0.78–1.084 J/cm²）、ns 段用 **≈220–550μm**（168 J/cm²）。ps 那组脉冲更长，**按理应比 fs 组阈值高**，却只测到 2.58 J/cm²——与"大光斑探到更多低阈值缺陷、阈值下降"一致。⚠️ 这是**跨脉宽+跨光斑的混合对照，不能作为面积效应的纯净证据**，只能作趋势旁证；纯净的面积效应证据仍以 Edmund Optics 的模型（0.2mm→10mm 降一个数量级）[来源](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/importance-of-beam-diameter-on-laser-damage-threshold/) 与 Laseroptik 的"阈值随光束直径增大而下降"表述为准 [来源](https://www.laseroptik.com/en/customer-service/lidt) ✅。

#### 5.6.2 一份完整的 S-on-1 实测报告（可直接引用为 S-on-1 与 1-on-1 差异的铁证）

OPTOMAN 公开了样品 CAM71-opt（**fs 高反膜 fsHR1030**）的完整 LIDT 测试报告 PDF：

- **测试条件**：波长 1030 nm；脉宽（FWHM）499.7 fs；重频 100 kHz；AOI 45.0°；偏振 线偏振 S；**光束直径（1/e²）= (121.0 ± 0.6) μm**。
- **特征损伤曲线（Catastrophic 阈值，拟合模型估计值，Table 1）**：

| 测试模式 | 阈值（Catastrophic, J/cm²） | 阈值（Color mode, J/cm²） |
|---|---|---|
| 1-on-1 | 1.612 (+0.056 / −0.055) | — |
| 10-on-1 | 1.332 (+0.068 / −0.067) | — |
| 10²-on-1 | 1.241 (+0.056 / −0.055) | — |
| 10³-on-1 | 1.193 (+0.025 / −0.025) | — |
| 10⁴-on-1 | 1.183 (+0.032 / −0.032) | — |
| 10⁵-on-1 | 1.181 (+0.030 / −0.030) | — |
| **10⁶-on-1** | **1.181 (+0.030 / −0.030)** | **1.084 (+0.037 / −0.037)** |

[来源：OPTOMAN LIDT TEST RESULTS PDF](https://www.optoman.com/wp-content/uploads/2024/10/fsHR1030_5-4.pdf) — 厂商一手测试报告 ✅

**这张表能支撑的结论：**
- **单脉冲阈值 ≠ 多脉冲阈值**：1-on-1 为 1.612 J/cm²，累积到 10⁶ 脉冲后降至 **1.181 J/cm²**，即**下降约 27%**（我用表中数值计算：1 − 1.181/1.612 = 0.267）。→ 直接证明"用 1-on-1 阈值去评估实际多脉冲工况会高估寿命"。厂商也说 1-on-1 阈值"如今主要只有学术意义、对实际应用价值有限" [来源](https://www.laseroptik.com/en/customer-service/lidt) ✅。
- **收敛性**：阈值在 10³–10⁶ 区间基本持平（1.193→1.181），且**损伤曲线趋于平坦**，而非按 1/S 继续下降。→ 可支持"把特征损伤曲线外推到 10⁹–10¹² 脉冲以粗估寿命"这一做法的合理性 [来源](https://www.laseroptik.com/en/customer-service/lidt) ✅。
- **两种损伤判据给出不同阈值**：Catastrophic（灾难性）1.181 J/cm² vs **Color mode（变色/色变）1.084 J/cm²**。→ **变色模式阈值更低**，印证厂商关于超快波段"**color-change effect 是 LIDT 的限制因素**，必须消除它才能提高元件寿命、降低总拥有成本"的说法。[OPTOMAN LIDT Capabilities](https://www.optoman.com/technology/lidt-capabilities/) ✅
- ⚠️ 注意此报告的**光束直径只有 121 μm**，远小于 ISO 允许的最小测试光斑 0.2 mm（见 5.3）。OPTOMAN 自己提示这些值"不能直接当作产品规格"。

#### 5.6.3 另一份 UV AR 膜的一手 R&D 报告

- OPTOMAN《High LIDT IBS Anti-Reflective and High Transmittance coatings at UV spectral range》（日期 2022-04-01，Rev V.1.00）：**实测 LIDT >12.66 J/cm² @ 355nm, 6ns, 100Hz（在线检测）**；目标 LIDT >20 J/cm² @ 355nm, 6ns, 100Hz；镀膜：AR @ 355nm，AOI=0°。[来源：报告 PDF（第三方网站托管，内容为 OPTOMAN 原始 R&D 报告）](http://www.sun-ins.com/pickup/ibs-uv/CAM_108%20High%20LIDT%20AR%20UV.pdf) ✅（内容一手，托管方非原厂）
  - 与 5.6.1 表中"AR @355nm, 5.3ns, 100Hz, 225.5μm → 15.9 J/cm²"互相印证，量级一致。

#### 5.6.4 其它来源（可信度较低，仅作旁证）

| 元件 / 镀膜 | 数值 | 测试条件（源文所载） | 来源 | 类型 |
|---|---|---|---|---|
| ZnSe AR/AR@10.6μm 窗（CO2） | 典型 **3000 W/mm**（"3 kW per mm of beam dia. 1/e²"） | CW CO2 激光；源文注明"取决于光束直径" | [LASER COMPONENTS ZnSe 数据手册](https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/diverse-laser-optics/co2-laseroptics/znse-windows.pdf) | 厂商数据手册 ✅ |
| 高功率激光镜（介质膜） | **20 J/cm²** | @1064nm, 10ns, 10Hz | [RP Photonics 激光镜页（含供应商内容）](https://www.rp-photonics.com/laser_mirrors.html) | 供应商内容，非原厂直证 🟡 |
| 高功率偏振分光棱镜（光学接触、无胶） | **>15 J/cm²** | @1064nm, 20ns, 20Hz | [RP Photonics 分光镜页（含供应商内容）](https://www.rp-photonics.com/beam_splitters.html) | 供应商内容，非原厂直证 🟡 |
| 介质膜分光镜/AR（IBS） | **>20 J/cm²** | 源文未给脉宽/波长细节 | [RP Photonics 分光镜页](https://www.rp-photonics.com/beam_splitters.html) | 供应商内容 🟡 |
| 保护镜（工业件，转销商自述） | Series A **>15 J/cm²**（10ns）；Series C **24 J/cm²** | 源文称 10ns | [lasercoppernozzle](https://lasercoppernozzle.com/protection-lens-ar-coating-damage-threshold-guide/) | ⚠️ 转销商博客，**无第三方印证，建议不采用** 🟡 |

- 📌 **旁证一致性检查**：上表"介质膜镜 20 J/cm² @1064nm/10ns"与 OPTOMAN 实测"HR 168 J/cm² @1064nm/9.8ns"**相差近一个数量级**。这不矛盾——两者是不同的镀膜材料体系与工艺，且**光斑直径也不同**（前者未标注，后者 223.5μm）。**结论：跨厂商直接比 LIDT 数值没有意义**，必须以同一供应商、同一工艺、同一测试条件的数据为准。此点也印证 Laseroptik 的"LIDT 强烈依赖镀膜材料与制备方法"。[来源](https://www.laseroptik.com/en/coating-guide/thin-film-basics/hr-standards) ✅
- ❌ **仍未找到**：以 **W/cm² 或 kW/cm²** 标注的**裸基材 vs 镀膜 CW LIDT 对照表**；以及熔石英保护镜的 CW 允许功率 vs 光斑直径曲线。这类数据通常只在厂商询价后的确认书上给出。

---

## 6. 清洁与维护

### 6.1 正确方法（**TWI 的规程最完整，可作主引用**）

- **适用前提**：高功率 Nd:YAG 用的**硬膜熔石英**镀膜非常耐用，通常比基材本身还硬。原文："The coatings on the silica optics commonly used with high power Nd:YAG lasers are very durable and usually harder than the substrates themselves." [来源](https://www.twi-global.com/technical-knowledge/faqs/faq-how-should-i-clean-laser-optics) — TWI Ltd（英国焊接研究所）技术 FAQ ✅
- **步骤（一手，逐步照录要点）**：
  1. **预清洁**（并非总是必要）：用温肥皂水+温和液体洗涤剂，或用丙酮，彻底去除过量油、脂、污物；**轻柔冲洗，避免磨损表面**；顽固痕迹可用戴乳胶手套的手指辅助；完成后用洁净白纸巾擦拭。
  2. **终清洁 —— "drop and drag"（滴-拖）法**：推荐用**丙酮**。始终**持元件边缘**，或把它放在洁净干燥工作面上的镜头纸上。取一张镜头纸**悬在元件上方**，在纸上滴几滴丙酮，把纸**放下贴到元件上、单向拖过表面**；**纸的干燥部分有助于带走丙酮残留**。重复到干净为止。**镜头纸不得重复使用。**
  3. **溶剂替代**：可用乙基或甲基酒精代替丙酮；但**注意溶剂不要接触手指**（会溶解手上油脂并沉积到元件上）；且酒精挥发比丙酮慢，**一般留下更多残留**。
  4. **ZnSe 聚焦镜**：先用**带单向阀的橡胶吹气球**吹掉表面灰尘颗粒，再按上述 drop-and-drag 用丙酮+洁净镜头纸；顽固附着颗粒可用**蘸丙酮的棉签**局部处理；小元件用乳胶手套或指套拿取；**生物性污渍（呼吸、喷嚏）不能用丙酮去除**，应先用蒸馏水处理并干燥。
  （以上均出自 [TWI FAQ](https://www.twi-global.com/technical-knowledge/faqs/faq-how-should-i-clean-laser-optics)）✅
- **金属镜与金属膜镜的例外（一手）**：
  - **软金膜镜**："表面非常娇气，不应使用上述技法清洁"；推荐**非接触方法**——用丙酮冲洗，再用喷罐干氮吹干。✅
  - **硬金膜镜**：较坚韧，可用熔石英那一套方法。✅
  - **相位延迟镜（Cu 或 Si 基）与硅平面镜**含介质层，"**不应让该层接触水**，否则可能导致膜层剥离"；清洁时改用 ZnSe 那一套流程。✅
  - 裸金属镜（通常为铜）极脏时可用市售液体金属抛光剂，之后必须用丙酮洗掉抛光剂残留，再用镜头纸擦拭。✅
  （均出自 [TWI FAQ](https://www.twi-global.com/technical-knowledge/faqs/faq-how-should-i-clean-laser-optics)）
- **通用擦拭方向（一手）**：用软镜头纸加少量合适溶剂（清洁酒精或丙酮）擦拭可及的表面；"**应避免来回擦**——那只是把污物摊开；应**有系统地单向擦拭**，把污物带出敏感区域"；同时注意勿用硬物接触光学面。原文："One should avoid wiping back and forth, only distributing dirt; instead, one should systematically wipe in one direction, getting any dirt outside the sensitive area." [来源](https://www.rp-photonics.com/optical_windows.html) ✅
- **振镜厂商的清洁要求（一手）**：只能用指定材料——**光学擦拭纸、棉签、试剂级乙醇**；清洁/拆装时**必须戴指套或医用手套**，减少指纹、唾液等人为污染；"清洁、拆装任何镜片时走捷径，都会缩短寿命甚至造成不可逆损伤"。[来源](https://www.scanneroptics.com/how-to-avoid-secondary-contamination-of-lens.html) ✅
- **Newport 的规范流程**：先吹尘，再用"drop and drag"——把展开的镜头纸铺在元件上、滴溶剂、缓慢拖过。原文："After blowing off the dust using compressed air or nitrogen, lay a piece of unfolded lens tissue over the optic, drop on some solvent, and slowly drag the soaked tissue…" [来源](https://www.newport.com/n/how-to-clean-optics) 🟡（页面返回 403，我仅见搜索摘要中的引文）

### 6.2 绝对不能做的事（**每条都有来源，或明确标为未证实**）

| 禁止项 | 依据 | 可信度 |
|---|---|---|
| **干擦**（无溶剂的擦拭） | 需先吹尘再"drop and drag"；预清洁须"轻柔冲洗以免磨损表面" | ✅ [TWI](https://www.twi-global.com/technical-knowledge/faqs/faq-how-should-i-clean-laser-optics)、🟡 [Newport](https://www.newport.com/n/how-to-clean-optics) |
| **来回擦** | "避免来回擦，那只是把污物摊开" | ✅ [RP Photonics](https://www.rp-photonics.com/optical_windows.html) |
| **重复使用镜头纸** | "Do not re-use the lens tissue." | ✅ [TWI](https://www.twi-global.com/technical-knowledge/faqs/faq-how-should-i-clean-laser-optics) |
| **软金膜镜用擦拭法** | "不应使用上述技法" | ✅ [TWI](https://www.twi-global.com/technical-knowledge/faqs/faq-how-should-i-clean-laser-optics) |
| **相位延迟镜/硅镜接触水** | 可导致介质层剥离 | ✅ [TWI](https://www.twi-global.com/technical-knowledge/faqs/faq-how-should-i-clean-laser-optics) |
| **溶剂接触手指/裸手操作** | 溶剂溶解手油并沉积到元件；应戴手套/指套 | ✅ [TWI](https://www.twi-global.com/technical-knowledge/faqs/faq-how-should-i-clean-laser-optics)、[Scanner Optics](https://www.scanneroptics.com/how-to-avoid-secondary-contamination-of-lens.html) |
| **试图擦掉烧坑** | "Do not attempt to wipe off burn pits — once the optical coating is damaged, the glass cannot be restored." | 🟡 [lasvio](https://lasvio.com/how-to-tell-when-your-fiber-laser-protective-window-needs-replacing/)（二手，但机理与 ✅ 的"涂层是 LIDT 短板"一致） |
| **反复清洁已损坏的保护镜** | "Replace, do not over-clean" | 🟡 [lasvio](https://lasvio.com/how-to-tell-when-your-fiber-laser-protective-window-needs-replacing/)、[machinistsvault](https://machinistsvault.com/blogs/news/fiber-laser-consumable-replacement-intervals) |
| **用嘴吹** | ❌ **未找到公开来源**给出"用嘴吹光学元件"的直接禁令原文。可间接支持：TWI 指出"生物性污渍（呼吸、喷嚏等）不能用丙酮去除"——反证呼出气会污染光学面；且标准做法是用**带单向阀的吹气球或干氮**而非口吹。 | ❌ 无直接来源，建议按"间接证据 + 行业惯例"表述 |
| **用普通纸巾/面巾纸** | ❌ **未找到公开来源**直接对比普通纸巾与镜头纸。可间接支持：TWI 用"clean white tissue / lens tissue"，Scanner Optics 规定"仅使用指定材料：光学擦拭纸、棉签、试剂级乙醇"。 | ❌ 无直接来源，同上 |

### 6.3 洁净度等级与环境

- ❌ **未找到公开来源**：光学元件装配/激光头维护所要求的**具体 ISO 14644-1 等级**（如 ISO Class 7 / Class 8）。我确认了 ISO 14644-1:2015 是现行洁净室分级标准本体（[ISO 目录](https://www.iso.org/obp/ui/#!iso:std:53394:en)），但未找到任何光学或激光厂商文件把它作为装配环境要求引用。**不要在文档里写"应满足 ISO Class X"，除非能拿到具体厂商文件。**
- 可引用的一手替代要求（工程层面的"洁净"表述）：
  - 应"在清洁、无尘环境中"取出保护窗抽屉，以防二次污染 [来源](https://lasvio.com/how-to-tell-when-your-fiber-laser-protective-window-needs-replacing/) 🟡
  - 保护镜应"保存在清洁、干燥环境，远离灰尘、湿气与不必要的手工接触" [来源](https://www.linkmetalcnc.com/blogs/news/how-to-choose-protective-lens-for-fiber-laser-cutting-heads) 🟡
  - 振镜/激光头采用密封壳体防尘防水 [来源](https://pdf.directindustry.com/pdf/scanlab-gmbh/scancube-iii-scan-heads/39164-400637.html) 🟡
  - 环境决定清洁频次："激光光学件可以且应当按需清洁，清洁量通常取决于元件所处环境" [来源](https://www.twi-global.com/technical-knowledge/faqs/faq-how-should-i-clean-laser-optics) ✅

### 6.4 常见污染源与防护

- **飞溅（spatter）**：熔池液滴离开熔池后沉积在工件表面（降低表面质量）**并沉积到保护窗上**，需更换、造成停机。[来源](https://www.cavitar.com/library/spatter-behavior-in-laser-beam-welding-process/) — 论文 ✅
- **辅助气体不纯**：压缩空气或氧气管路中的**油或水分**会立刻在镜片下表面形成覆盖层。[来源](https://lasvio.com/how-to-tell-when-your-fiber-laser-protective-window-needs-replacing/) 🟡
- **穿孔（piercing）参数不当**：穿孔过快或离材料过近，会把大量熔融金属反向喷到玻璃上。（同上）🟡
- **灰尘/颗粒**：光路中或元件上的灰尘会扰动光束并产生散射光，**在光束剖面里留下不需要的环形花纹（ring patterns）**。[来源](https://www.edmundoptics.com/knowledge-center/application-notes/lasers/understanding-spatial-filters/) ✅
  - 另注：强脉冲下"灰尘和其他污物可能被**烧进**表面，之后很难去除"。[来源](https://www.rp-photonics.com/optical_windows.html) ✅
- **防护手段**：气帘/风刀（把飞溅在源头偏转）[来源](https://www.bergmann-steffen.de/en/solutions/tornadoblade/) ✅；密封壳体 [来源](https://pdf.directindustry.com/pdf/scanlab-gmbh/scancube-iii-scan-heads/39164-400637.html) 🟡；定期检查密封圈与抽屉 [来源](https://machinistsvault.com/blogs/news/fiber-laser-consumable-replacement-intervals) 🟡；加盖/加管状防护结构 [来源](https://www.rp-photonics.com/optical_windows.html) ✅

---

## 7. 失效现象对照表

> ⚠️ 重要前提：下表把"现象 → 最可能元件"做成对照，**但公开来源中没有任何一份文档给出这一整张表**。各行的依据强度不同，我在"依据"列逐一标注。**这是整理的工程推理框架，不是引文。**

| 现象 | 最可能的元件/原因 | 机理与依据 |
|---|---|---|
| **功率下降**（到工件处） | 保护镜污染/吸收；其次喷嘴、气路、冷却降额 | 污染→吸收↑→热透镜→功率损耗 [来源](https://www.scanneroptics.com/how-to-avoid-secondary-contamination-of-lens.html) ✅；"工件处功率损失 ≠ 光源功率损失"，应按由近及远顺序排查 [来源](https://whcstec.com/what-to-check-when-your-fiber-laser-source-output-drops/) 🟡 |
| **功率下降（光源侧）** | 光源退化、回光报警/热保护、供电故障 | 突然下降且与某事件同时发生（铜/黄铜切割回光报警、热保护停机）= 事件触发型失效 [来源](https://whcstec.com/what-to-check-when-your-fiber-laser-source-output-drops/) 🟡 |
| **光斑变形 / 功率分布不均** | 保护镜或场镜污染（热透镜） | 高吸收元件上"中心温度高、边缘温度低"，折射率变化导致功率分布不均 [来源](https://www.scanneroptics.com/how-to-avoid-secondary-contamination-of-lens.html) ✅ |
| **环形光斑 / 同心环** | ① 光路中灰尘或元件表面污染造成的散射（环状花纹）；② **主动整形**（DOE / 涡旋光产生的点环光斑），属设计而非故障 | ① 散射光"在光束剖面里留下不需要的环形花纹"，正是空间滤波器要解决的问题 [来源](https://www.edmundoptics.com/knowledge-center/application-notes/lasers/understanding-spatial-filters/) ✅；② [DOE 点环光斑论文](https://www.docin.com/p-4816208557.html)、[华科环光斑焊接研究](https://laser.hust.edu.cn/info/1107/1143.htm) 🟡 |
| **散斑 / 散射噪声** | 元件表面粗糙度、污染、膜层散射 | 膜层散射是 HR 膜损耗来源之一（标准 EBE <150 ppm，IBS 更低）[来源](https://www.laseroptik.com/en/coating-guide/thin-film-basics/hr-standards) ✅；表面非理想导致散射与光束剖面变形 [来源](https://www.rp-photonics.com/optical_windows.html) ✅ |
| **焦漂 / 焦点位置漂移** | 保护镜或透镜污染造成热透镜；焦面光斑变化 | "deviation of the focal point position"是热透镜的直接后果 [来源](https://www.scanneroptics.com/how-to-avoid-secondary-contamination-of-lens.html) ✅ |
| **保护镜发热 / 激光头温度报警** | 污染吸收 → 局部过热；也可能是回光异常或安装不当 | "不要因为机器没报警就继续切"；应检查雾斑、烧痕、涂层变色、飞溅、指纹 [来源](https://lasvio.com/how-to-tell-when-your-fiber-laser-protective-window-needs-replacing/) 🟡 |
| **振镜镜片热损伤 / 扫描头失效** | 污染物 + **回光**共同作用 | 论文结论：高反材料与混凝土加工产生污染物与回光，回光在污染物存在下**加剧**镜片热损伤 [来源](https://link.springer.com/article/10.1007/s12541-024-01133-1) ✅ |
| **切缝质量突然变差（挂渣、条纹、切不透）** | 保护镜为**首要嫌疑**（参数未变时） | "If your machine parameters haven't changed but your cut quality suddenly declines, the protective window should be your first suspect." [来源](https://lasvio.com/how-to-tell-when-your-fiber-laser-protective-window-needs-replacing/) 🟡 |
| **电容报警 / 随动高度异常** | 陶瓷环、喷嘴（**不是**光学件） | 环破损/污染导致随动不稳、误判板材、Z 轴故障 [来源](https://machinistsvault.com/blogs/news/fiber-laser-consumable-replacement-intervals) 🟡 |

- ⚠️ 诊断顺序的一条强建议（有来源）：**按"从最靠近工件的元件开始、向光源回溯"的顺序排查**，因为污染光学件、耗材退化、气路问题、冷却降额各自都比"光源真退化"更常见。[来源](https://whcstec.com/what-to-check-when-your-fiber-laser-source-output-drops/) 🟡

---

## 8. ⚠️ 常见误解

1. **❌ "保护镜的更换有公认的功率下降百分比阈值（比如掉 5%/10% 就换）。"**
   → **未找到任何一手厂商给出这类阈值。** Precitec / TRUMPF / Bystronic / Raytools / WSX 口径一致，都是**按现象与报警判定**（雾斑、烧坑、彩虹热痕、涂层变色、清洁后复现的热点、反复温度报警）。[来源](https://machinistsvault.com/blogs/news/fiber-laser-consumable-replacement-intervals) 🟡。写文档时请写成"由设备厂商维护手册规定"，不要发明百分数。

2. **❌ "CW 的 LIDT 就是 W/cm²。"**
   → **ISO 21254 体系给 CW 的规范单位是线功率密度 W/cm**，并明确线功率密度"适用于 CW 与长脉冲"；功率密度 W/cm² 才是给短脉冲/一般情形的另一口径。[来源（标准原文）](https://cdn.standards.iteh.ai/samples/43001/82e64c00f69642a3914423945df39eec/ISO-21254-1-2011.pdf) ✅。厂商目录普遍用 W/cm²，两者混用会差一个光斑直径因子（本例中 50.9 MW/cm² 对应 200 kW/cm，看似"相差 250 倍"，实为不同物理量）。

3. **❌ "LIDT 是绝对安全线，低于它就绝不会坏。"**
   → LIDT 是**外推损伤概率为零的统计量**，存在置信区间；10 点/通量级的测试只能把概率确定到 ±25%；且 ISO 把"任何可检测变化"都算损伤，而这不必然等于性能退化。行业惯例要留 2–3 倍安全系数，且**没有普适安全系数**。[来源](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/uncertainty-in-lidt-specifications/)、[来源](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/laser-damage-threshold-testing/) ✅

4. **❌ "小光斑测出来的 LIDT 可以直接用在大光斑/实际光斑上。"**
   → 光斑越小越"欠采样"缺陷，测出的阈值**偏乐观**；0.2mm→10mm 可使 LIDT **下降一个数量级**；ISO 规定测试最小光斑 0.2mm，而工业振镜聚焦光斑常在 50μm 量级，**把 0.2mm 的规格外推到 50μm 属大幅外推**，必须自己复测或向厂商索取应用条件下的数据。[来源](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/importance-of-beam-diameter-on-laser-damage-threshold/) ✅

5. **❌ "基材先坏，膜只是附带的。"**
   → 恰恰相反：厂商明确表示损伤问题**已从体材料转移到表面**，**薄膜涂层对 LIDT 的降低贡献最大**、是高功率元件开发中最关键的一环；并且"**LIDT 最高的镀膜通常不是反射率最高的镀膜**"——追求高反射会牺牲阈值。[来源](https://www.laseroptik.com/en/customer-service/lidt)、[来源](https://www.laseroptik.com/en/coating-guide/thin-film-basics/hr-standards) ✅
   → 另有反直觉实验证据：NASA 报告称商用镀膜的 ps 阈值最高约 12–14 J/cm²，**比裸熔石英低约 50%**，且部分镀膜与裸面存在明显"预处理效应"（阈值提升 1.2–1.8 倍）。[来源](https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19930009583.pdf) 🟡（我仅见摘要）

6. **❌ "'1064nm HR 膜的 LIDT 大约 20 J/cm²'——可以拿一个数字到处用。"**
   → 同一个波长、同一种膜系，LIDT 随**脉宽**变化可达**两个数量级以上**：OPTOMAN 实测 HR@1064nm 在 **9.8ns** 为 **168 J/cm²**，而 HR@1030nm 在 **500fs** 只有 **0.78–1.084 J/cm²**；AR@1064nm 在 10.2ns 为 **96.1 J/cm²**，AR@343nm 在 1ps 仅 **0.39 J/cm²**。[来源](https://www.optoman.com/technology/lidt-capabilities/) ✅
   → 而且**跨厂商比数值是无意义的**：同为"1064nm 介质膜镜"，供应商目录值 20 J/cm²@10ns 与 OPTOMAN 实测 168 J/cm²@9.8ns 差近一个数量级，因为**镀膜材料体系、工艺（EBE vs IBS）与光斑直径都不同**。[来源](https://www.rp-photonics.com/laser_mirrors.html)、[来源](https://www.laseroptik.com/en/coating-guide/thin-film-basics/hr-standards) ✅
   → **正确表述**：引用 LIDT 必须同时给出「波长 + 脉宽（或 CW）+ 重频 + 光斑直径 + 测试模式（1-on-1/S-on-1, S=?）」。

7. **❌ "1-on-1 测出来的阈值就是元件的真实承受能力。"**
   → OPTOMAN 同一片 fs 高反膜（fsHR1030）实测：**1-on-1 = 1.612 J/cm²，10⁶-on-1 = 1.181 J/cm²，下降约 27%**；且该厂商直言 1-on-1 阈值"如今主要只有学术意义、对实际应用价值有限"，却仍被大量厂商目录列为主打。[报告 PDF](https://www.optoman.com/wp-content/uploads/2024/10/fsHR1030_5-4.pdf) ✅、[Laseroptik](https://www.laseroptik.com/en/customer-service/lidt) ✅
   → 附带一个易忽略点：该报告里**"变色（color mode）"损伤的阈值（1.084 J/cm²）低于"灾难性"损伤阈值（1.181 J/cm²）**——先"变色"、后"崩坏"，超快波段尤其如此。[来源](https://www.optoman.com/technology/lidt-capabilities/) ✅

8. **❌ "保护镜 = 激光安全防护窗。"**
   → 完全不同的两类件。前者在**光路内部**保护下游光学件（要 AR 增透、要低吸收）；后者在**设备外罩上**保护人眼（要**高** OD 衰减）。且安全窗的 OD 额定值**只在标定波段有效**——OD 6+@190–540nm 的窗对 1064nm **不提供**该额定防护。[来源](https://optlasers.com/laser-safety-window) 🟡

9. **❌ "在振镜后加个针孔做空间滤波，就能改善到工件的光斑质量。"**
   → 未找到任何公开案例，且原理上冲突：针孔必须精确位于会聚焦点，而振镜系统中焦点随扫描角在工件面上移动，针孔会被扫描"扫出"焦点。空间滤波只能放在**扫描前的准直段**，因而管不到场镜之后的像差与污染。[空间滤波器原理来源](https://www.edmundoptics.com/knowledge-center/application-notes/lasers/understanding-spatial-filters/) ✅ + 本文机理论证 ⚠️

10. **❌ "取样镜的分光比是固定值。"**
    → 菲涅尔取样镜的分光比**取决于入射光偏振态**（厂商原文："1-10%, depending on the incident light's polarization"）；介质膜分光镜的反射率也强烈依赖偏振，且中心波长随入射角增大**向短波移动**（HR 1064nm/0° 在 AOI=45° 时偏移约 10%，AOI<13° 时 <1%）。所以振镜前的取样读数会随偏振/角度变化而漂移，这直接影响功率监测的准确性。[来源](https://www.thorlabs.com/beam-samplers) ✅、[来源](https://www.laseroptik.com/en/coating-guide/thin-film-basics/hr-standards) ✅

11. **❌ "振镜前取样就等于到工件功率。"**
    → 不等。振镜镜片、场镜、保护镜的损耗与热透镜都不在取样光路内。论文级别证据表明污染物 + 回光会造成扫描头光学件热损伤与性能劣化。[来源](https://link.springer.com/article/10.1007/s12541-024-01133-1) ✅。**但"振镜后取样更准"这一比较本身未找到对照实验数据**，属机理论证。

12. **❌ "镀膜镜片可以用酒精棉片随便擦。"**
    → 溶剂不得接触手指；不得来回擦；镜头纸不得复用；ZnSe 需先吹尘；软金膜镜**禁止**擦拭法；相位延迟镜/硅镜**禁止**接触水。指定材料是光学擦拭纸、棉签、试剂级乙醇/丙酮。[来源](https://www.twi-global.com/technical-knowledge/faqs/faq-how-should-i-clean-laser-optics) ✅、[来源](https://www.scanneroptics.com/how-to-avoid-secondary-contamination-of-lens.html) ✅

13. **❌ "普通纸巾/嘴吹一下没事。"**
    → 我**未找到**直接的公开禁令原文，因此不应把这两条写成"标准规定"。可按下列**有来源的替代表述**来写：标准做法是用**带单向阀的吹气球或干氮**除尘（TWI 对 ZnSe 的规定）、只用**指定材料**（Scanner Optics）、且**呼出气属于会污染光学面的生物性污渍**（TWI）。[TWI](https://www.twi-global.com/technical-knowledge/faqs/faq-how-should-i-clean-laser-optics) ✅

---

## 9. 来源总表（按类型）

**标准 / 规范**
- ISO 21254-1:2011 样本 PDF（定义、单位、1-on-1/S-on-1、0.2mm 限制、毒性警示）— [cdn.standards.iteh.ai](https://cdn.standards.iteh.ai/samples/43001/82e64c00f69642a3914423945df39eec/ISO-21254-1-2011.pdf)（非官方样本；正式购买入口 [ISO 83937](https://www.iso.org/standard/83937.html)）
- ISO 14644-1:2015（洁净室分级，**未能取得内容**）— [ISO OBP](https://www.iso.org/obp/ui/#!iso:std:53394:en)

**厂商官网 / 数据手册（一手）**
- **OPTOMAN LIDT Capabilities（核心：跨脉宽/重频/光斑/波长的 LIDT 实测值表）** — [optoman.com/technology/lidt-capabilities](https://www.optoman.com/technology/lidt-capabilities/)
- **OPTOMAN 完整 S-on-1 测试报告 fsHR1030（1-on-1 → 10⁶-on-1 特征损伤曲线）** — [PDF](https://www.optoman.com/wp-content/uploads/2024/10/fsHR1030_5-4.pdf)
- OPTOMAN UV AR 膜 R&D 报告（实测 >12.66 J/cm² @355nm,6ns,100Hz）— [PDF](http://www.sun-ins.com/pickup/ibs-uv/CAM_108%20High%20LIDT%20AR%20UV.pdf)（第三方托管，内容为原厂报告）
- LASER COMPONENTS ZnSe 窗数据手册 — [PDF](https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/diverse-laser-optics/co2-laseroptics/znse-windows.pdf)
- LASEROPTIK LIDT 知识页 — [laseroptik.com/en/customer-service/lidt](https://www.laseroptik.com/en/customer-service/lidt)
- LASEROPTIK HR 标准（LIDT 经验式、损耗、偏振、AOI 漂移）— [HR standards](https://www.laseroptik.com/en/coating-guide/thin-film-basics/hr-standards)
- SVS 激光保护窗 — [svs-schweisstechnik.de](https://www.svs-schweisstechnik.de/en/products/laser-protection-windows/)
- Thorlabs 分光取样镜（菲涅尔 1–10%）— [thorlabs.com/beam-samplers](https://www.thorlabs.com/beam-samplers)
- Bergmann Steffen Tornadoblade 风刀 — [bergmann-steffen.de](https://www.bergmann-steffen.de/en/solutions/tornadoblade/)
- Scanner Optics（振镜厂商）：热透镜后果 — [污染文](https://www.scanneroptics.com/how-to-avoid-secondary-contamination-of-lens.html)；振镜焊接闭环/10ms 关光 — [焊接页](https://www.scanneroptics.com/galvo-laser-welding.html)
- TWI Ltd 激光光学清洁 FAQ — [twi-global.com](https://www.twi-global.com/technical-knowledge/faqs/faq-how-should-i-clean-laser-optics)

**技术百科（有作者与编辑政策）**
- RP Photonics：光学窗口 — [optical_windows](https://www.rp-photonics.com/optical_windows.html)；激光镜 — [laser_mirrors](https://www.rp-photonics.com/laser_mirrors.html)；分光镜 — [beam_splitters](https://www.rp-photonics.com/beam_splitters.html)；楔形棱镜/楔形窗 — [wedge_prisms](https://www.rp-photonics.com/wedge_prisms.html)；模式清洁器/空间滤波 — [mode_cleaners](https://www.rp-photonics.com/mode_cleaners.html)

**应用笔记（厂商技术文档，一手）**
- Edmund Optics：LIDT 理解与规格 — [EU 页](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/understanding-and-specifying-lidt-of-laser-components/)；光斑直径影响 — [EU 页](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/importance-of-beam-diameter-on-laser-damage-threshold/)；LIDT 测试 — [EU 页](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/laser-damage-threshold-testing/)；不确定度 — [EU 页](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/uncertainty-in-lidt-specifications/)；规格类型 — [EU 页](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/different-types-of-lidt-specifications/)；超快 LIDT — [EU 页](https://www.edmundoptics.eu/knowledge-center/application-notes/lasers/lidt-for-ultrafast-lasers/)；空间滤波器 — [US 页](https://www.edmundoptics.com/knowledge-center/application-notes/lasers/understanding-spatial-filters/)

**论文**
- Lian, Baek & Lee, *Investigation of Galvanometer Scanner Failure During the Laser Processing of High Reflectivity Materials and Concrete Composite Materials*, Int. J. Precis. Eng. Manuf. (2024) — [Springer](https://link.springer.com/article/10.1007/s12541-024-01133-1)
- Nagel & Bergmann（Ilmenau）, *Spatter Behavior in Laser Beam Welding Process* — [Cavitar](https://www.cavitar.com/library/spatter-behavior-in-laser-beam-welding-process/)
- NASA NTRS, *Laser damage of HR, AR-coatings, monolayers and bare surfaces at 1064 nm* — [PDF](https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19930009583.pdf) 🟡（仅摘要）
- Ristau, Jupé & Starke, *Laser damage thresholds of optical coatings*, Thin Solid Films 518(5) 1607–1613 (2009) — 🟡（仅见参考文献条目）

**专利**
- CN121261196A《高功率振镜焊接的外部激光功率闭环监测系统及监测方法》，北京正时精控科技有限公司，申请日 2025-12-04，公开日 2026-01-02 — [转果果专利库](https://www.imaibj.cn/patent/details/202511817087)（[Google Patents 可按公开号检索](https://patents.google.com/?q=CN121261196A)）

**转销商 / 行业博客（二手，仅作交叉参考，不宜作主引用）**
- Lasvio：[更换判据](https://lasvio.com/how-to-tell-when-your-fiber-laser-protective-window-needs-replacing/)、[选型](https://lasvio.com/choose-fiber-laser-protective-window/)、[产品页](https://lasvio.com/product/protective-window-for-fiber-laser-cutting-head/)
- Machinist's Vault：[耗材更换周期](https://machinistsvault.com/blogs/news/fiber-laser-consumable-replacement-intervals)
- LinkMetal：[保护镜选型](https://www.linkmetalcnc.com/blogs/news/how-to-choose-protective-lens-for-fiber-laser-cutting-heads)
- lasercoppernozzle：[AR 膜与损伤阈值（数值未获印证）](https://lasercoppernozzle.com/protection-lens-ar-coating-damage-threshold-guide/)
- whcstec：[回光损伤与防护](https://whcstec.com/fiber-laser-back-reflection-damage-protection/)、[功率下降排查](https://whcstec.com/what-to-check-when-your-fiber-laser-source-output-drops/)
- Holmarc：[分光取样镜](https://www.holmarc.com/beam_samplers.php)；NaNdi：[楔形窗](https://www.nandioptics.com/wedge-window)；Opt Lasers：[激光安全窗](https://optlasers.com/laser-safety-window)

---

## 10. 尚缺的关键数据（建议后续向厂商索取，而非网搜）

1. 熔石英 / 蓝宝石 / ZnSe / 光学玻璃四类保护镜在 **1064nm CW** 下的 LIDT 对照（**统一口径：W/cm 还是 W/cm²**）。
2. ✅ **已找到**（OPTOMAN，见 5.6.1/5.6.2）：1064nm AR 膜与 HR 膜的厂商一手脉冲 LIDT（含脉宽、重频、光斑直径、1-on-1/S-on-1）。**仍需补充**：熔融石英保护镜这一具体品类（而非镀膜镜）的同等数据。
3. 具体保护镜型号的**允许最大 CW 功率 vs 光斑直径**曲线（ZnSe 有 3000 W/mm@1/e² 这一条，熔石英我没找到对等的一手曲线）。
4. 保护镜**更换的定量触发条件**（透过率下降百分比、温升阈值）——设备厂商维护手册内部资料。
5. **振镜前 vs 振镜后取样**的对照实验数据（监测误差、响应时间）。
6. 光学件装配/维护的**洁净度等级要求**（是否真有厂商引用 ISO 14644 某等级）。
7. 以 **W/cm² / kW/cm²** 标注的**裸基材 vs 镀膜 CW LIDT 对照表**。
