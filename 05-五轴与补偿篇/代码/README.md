# 五轴振镜数字孪生与 5D 补偿平台

> [!info] 这份 README 在库里的位置
> 它是 **`05-五轴与补偿篇/代码/`** 这个可运行子项目的说明书。
> 想先看**讲解型笔记**（不是说明书），从 `../00-五轴补偿总览.md` 进 ——
> 那边按 `00 总览 → 01 正向 → 02 逆解 → 03 误差 → 04 标定 → 05 补偿矩阵 →
> 06 验证 → 07 4+1 架构 → 08 装配边界 → 09 落地路线` 组织。
> 本 README 是它们的**展开版**，适合查阅细节与跑代码。

## 当前主页：4+1 前置动态聚焦（2026-09-23）

根据选定方案，主页已切换为 **四个旋转振镜 + 一个独立直线调焦轴**。指令为四个镜角（rad）和 L1 负透镜位移（m），不再使用等效光程作为第五个实体执行轴。结构、薄透镜追迹、XYZ/AOI/RotZ 面板与补偿共用 `four_plus_one.py`。

使用主页的“调焦演示”观察 L1 位移改变焦点 Z，再点击“训练 4+1 仿真补偿”比较误差。细节与限制见 [4+1 模型说明](docs/4加1模型说明.md)。新接口位于 `/api/4p1/`。

旧页面保留在 `/legacy`，原 API 与实验功能保留。**下文为旧版模型和厂商资料的历史说明，不是当前 4+1 假设结构的内部设计依据。** 4+1 是本项目选定的替代研究架构，不宣称复原 precSYS 的内部五轴机构。

## 旧版等效模型（保留）

这是一个用于研究 `q=[q1,q2,q3,q4,qf]` 与光束位姿
`T=[X,Y,Z,alpha,beta]` 映射关系的最小可运行平台。

默认规格采用用户提供的 **515 nm (Standard)** 参数：4 mm 入射净口径、2 mm 典型入射光束、
10.2 μm 典型焦斑、±7.5° 最大入射角、75 mm 物镜焦距、25 mm 有效焦距、
±1 mm Z 向调焦范围、≤5 mm 标记视场。

当前模型采用四面可旋转平面镜。前四个控制量是各反射镜绕自身扫描轴的转角，
`qf` 是末级镜面交点到焦点的光程。`alpha`、`beta` 分别是出射方向相对 `-Z`
方向在 XZ、YZ 平面的倾角。所有长度单位为米、角度单位为弧度。

## 五轴的含义：五个振镜轴驱动 5D 输出

厂方手册明确写的是**五个振镜轴**，并且是「纯振镜式的五轴加工子系统」：

> `5-axis micro processing`
> "…by the system-**internal five galvo axes**."（Beam position measuring unit 一节）
> "…a stable, **purely galvo-based 5-axis** micromachining subsystem … realized for the first time."（Innovation 一节）
> "Due to precSYS's possibility to position the laser beam in **5 axis (x, y, z, a, b)**…"
> 图注：`1  Five galvo axes`

而且**入射角是被主动指定的控制量**，不是定位的副产品：

> "For any geometry, **the incidence angle will be controlled as specified** during trajectory motion."

| 输出自由度 | 手册的表述 |
|---|---|
| x、y 落点 | 五个振镜轴的合成转角 |
| z 焦深 | 同属 `5 axis (x, y, z, a, b)`；整机「不依赖任何旋转光学元件」（`works without any rotary optics`），未提及可动调焦镜组 |
| a、b 入射角（±7.5°） | 同属这五个轴，且沿轨迹逐点指定 |

手册没有写明这五个轴各自对应哪个输出量，也没有给出内部光学拓扑；上面的对应关系是本项目的解读。

但有一点是手册明说的：`q` 的 5 维与 `T=[X,Y,Z,α,β]` 的 5 维，是**五个振镜轴到 5D 输出的满映射**，
五个自由度都可独立指令，入射角不是定位的副产品。

本项目用「四个转角 + `qf` 等效光程」实现这个 5D 映射，是**本项目的建模简化**，不是对实机内部结构的复刻：
它让 `alpha=atan2(d.x,−d.z)`、`beta=atan2(d.y,−d.z)` 与落点同源，因此在本模型里 α、β 表现为伴随量。
**不要把这条模型性质读成实机能力** —— 实机的 α、β 可独立指定并闭环控制。

工作域（手册）：±7.5° 入射角，φ2.5 mm 圆形加工视场，最大 φ5 mm 标记视场，2D 与 3D 轨迹均可。

> **第一次接触本项目？先看 [`导读.html`](导读.html)。**
> 它用可视化方式讲清了项目构造、数据流、补偿矩阵怎么生成，以及最容易搞错的五个点，
> 并带一个可拖动的工作域演示。双击即可用浏览器打开，不依赖网络。
> 本文档（README）是它的展开版，适合查阅细节。

## 等效物镜

镜头采用高斯光束等效模型，不虚构厂家镜片曲率或玻璃材料。以 515 nm、M²=1.2、
2 mm 入射光束和 25 mm 有效焦距计算，预测焦斑直径为 9.84 μm，与规格中的
10.2 μm 接近；按规格焦斑计算的瑞利长度为 0.132 mm。4 mm 入口口径用于
等效光学展示，目前未进行整个光束包络的通光裁切检查。动态焦点限制为名义 75 mm 光程的 ±1 mm。

> **这些是模型量，不是实测值。** 焦斑、瑞利长度、M² 在本项目里是输入或模型输出，
> 从未用仪器测过。可实测这些量的仪器（如多平面光束轮廓仪）记在
> [资料索引](docs/references.md)。

## 整机结构参考（2026-09 更新）

新增五镜假设光路追迹：从入口依次反射至 A1–A5，经固定折转镜到等效物镜，再显示会聚光束。支持逐段查看、聚焦特写及打偏提示；镜面初始法向按该假设光路重新定向。此演示与原四镜 + qf 补偿模型分开，不声称复原实机第五轴调焦机构。

新增按 precSYS 公开工程图建立的 303.5 × 263.5 × 271 mm 主箱体，以及五个旋转振镜执行器、上下分舱、独立冷却回路示意、侧挂检测模块、物镜外壳、保护玻璃抽屉、喷嘴和接口。可切换整机、剖视、电机特写与计算光路视图。

外部主尺寸有依据，内部电机尺寸和布局是工程假设。A1–A4 与计算转角联动，但结构坐标尚未用于光路计算；A5 仅装配预览，不把 qf 冒充第五电机角度。既有补偿算法和误差图保留。详见 [结构依据与建模边界](docs/assembly-reference.md)。

## 功能

- 理想机与带安装误差、轴倾斜、零偏、焦距误差的真实机模型
- 光线与旋转镜面的逐级求交、反射及光路有效性检查
- 4 mm 等效物镜、25 mm 有效焦距、高斯光束包络、焦斑和瑞利长度计算
- 有界非线性逆运动学和数值雅可比
- 标定样本生成、二阶多项式 5D 误差模型和迭代补偿
- 补偿前后位置/姿态 RMSE 验证
- FastAPI 接口与 Three.js 光路预览

## 项目构造

### 目录结构

```
05-五轴与补偿篇/代码/              ← 本子项目根目录（下文相对此目录）
├── 启动网页.bat                     一键启动（双击运行）
├── 导读.html                        可视化项目导读（双击打开，建议先看这个）
├── pyproject.toml                   依赖、入口点 five-axis-galvo = api:main
├── docs/
│   ├── 4加1模型说明.md              4+1 前置动态聚焦模型：光路、参数、边界
│   ├── assembly-reference.md        整机结构依据、坐标约定与建模边界
│   ├── references.md                资料来源索引：本地副本、链接与未核实项
│   └── 英文项目技术方案.md          项目最初的任务书（英文原稿，历史文档）
├── src/five_axis_galvo/
│   ├── specifications.py            515 nm 光学规格常量表 STANDARD_515_NM
│   ├── geometry.py                  向量数学：旋转、镜面求交、反射、方向→角度
│   ├── optics.py                    高斯光束等效物镜、光斑包络、瑞利长度
│   ├── model.py                     ★ 机器模型与正向解算 forward()
│   ├── kinematics.py                数值雅可比、有界非线性逆解 least_squares
│   ├── calibration.py               ★ 标定样本生成 generate_calibration_data()
│   ├── compensation.py              ★ 5D 补偿矩阵 PolynomialCompensator
│   ├── verification.py              独立验证集上的补偿前后 RMSE
│   ├── four_plus_one.py             4+1 前置动态聚焦模型（当前主页）
│   ├── assembly.py                  箱体包络、五执行器装配假设、五镜假设追迹
│   ├── readout.py                   固定 +Z 面坐标系下的焦点读数与 AOI / RotZ
│   ├── api.py                       旧版 FastAPI 接口与启动入口
│   ├── api_4p1.py                   4+1 版接口（/api/4p1/）
│   └── static/                      index_4p1.html + app_4p1.js（当前主页）
│                                    index.html + app.js + assembly.js（旧版 /legacy）
└── tests/                           契约测试（.venv\Scripts\python -m pytest）
```

> **厂商参考资料不在本仓库里。** 本库只收录原创内容：
> `SCANLAB-precSYS-EN.pdf`、`CalWizard_Manual.pdf`、`dataray-beammap2-whitepaper.pdf`
> 与 precSYS 手册截图已按库的既有约定放到 `99-附件与下载/pdf/`（**该目录被 `.gitignore` 忽略**），
> 来源、许可证与获取途径登记在库根目录的 `THIRD-PARTY.md`。
> 需要离线核对时按那份文档取回即可。

带 ★ 的三个模块是补偿链路的核心。回环关系：

```
标定数据  →  补偿矩阵  →  逆运动学
calibration   compensation   kinematics
     ↑                            │
     └──────  model.forward()  ───┘   （正向解算，被反复调用）
```

### 分层职责

| 层 | 模块 | 职责 | 关键约束 |
|---|---|---|---|
| 常量 | `specifications.py` | 515 nm 规格表 | 单一数据源，模型与镜头都从它取值 |
| 数学 | `geometry.py` | 旋转、求交、反射 | 全部抛 `GeometryError`，由上层捕获 |
| 光学 | `optics.py` | 高斯光束等效物镜 | 不虚构镜片曲率/玻璃材料 |
| 模型 | `model.py` | 四面镜光路正向解算 | `q∈[−3.75°,3.75°]⁴×[0.074,0.076]`，越界即抛错 |
| 反解 | `kinematics.py` | 5→5 有界非线性求解 | 数值雅可比，标称点秩为 5 |
| 标定 | `calibration.py` | 随机采样 + 工作域过滤 | 拒绝采样，上限 `30×n` 次尝试 |
| 补偿 | `compensation.py` | 二阶多项式 5D 误差模型 | 21×5 系数矩阵 |
| 验证 | `verification.py` | 独立验证集 RMSE | 只统计逆解成功的样本 |
| **4+1** | `four_plus_one.py` | 前置动态聚焦：薄透镜近轴追迹、Z5 位移、遮挡校核 | 假设架构，不是厂家处方；不参与原补偿求解 |
| 装配 | `assembly.py` | 箱体包络、五执行器假设、五镜演示追迹 | 尺寸分「公开/推导/假设」三级；不参与补偿求解 |
| 读数 | `readout.py` | XYZ / AOI / RotZ 焦点读数 | 单一固定 +Z 面坐标系，横向方向量 ≤1e−10 时方位角为 `None` |
| 接口 | `api.py` | HTTP + 静态页（旧版 `/legacy`） | 进程内持有全局已拟合模型 |
| 接口 | `api_4p1.py` | 4+1 版 HTTP 接口（`/api/4p1/`） | 含手动目标逆解 `POST /api/4p1/inverse` |

### 核心数据结构

| 名称 | 形状 | 含义 |
|---|---|---|
| `q` 指令 | 5 | `[q1,q2,q3,q4,qf]`，前四项为转角（rad），`qf` 为末级镜面到焦点的光程（m） |
| `T` 位姿 | 5 | `[X,Y,Z,alpha,beta]`，焦点位置（m）+ 相对 `−Z` 的 XZ/YZ 倾角（rad） |
| 标定样本 | 400×5 | 每行一条指令 |
| 误差矩阵 | 400×5 | `real_poses − ideal_poses`，角分量已做 ±π 回绕 |
| **补偿矩阵** | **21×5** | 二阶多项式系数，`Cᵀ · features((T−center)/scale) = 5D 误差预测` |
| 雅可比 | 5×5 | 中心差分（`q±δ`，δ=1e-6，遇边界自动截断），标称点秩 5 |

## 数据流

### 正向：指令 → 位姿

`MachineModel.forward(q)` 是唯一的真值来源，逆解、标定、补偿全部依赖它：

```
q[5]
 │
 ├─ 逐级遍历 M1..M4（i = 0..3）
 │    center ← mirror.center + errors.position_offsets[i]      安装位置偏置
 │    axis   ← mirror.rotation_axis + errors.axis_tilts[i]     轴倾斜（再归一化）
 │    normal ← rotate(mirror.normal, axis, q[i] + errors.zero_offsets[i])
 │                                                            零偏叠加在转角上
 │    hit    ← intersect_ray_plane(origin, direction, center, normal)
 │    ├─ 命中点离镜心 > 镜面孔径(5 mm) → GeometryError「Ray misses mirror i」
 │    ├─ 光线与镜面平行 → GeometryError
 │    ├─ 交点在光线反方向 → GeometryError
 │    direction ← reflect(direction, normal)
 │    origin    ← hit
 │
 ├─ focus_distance ← q[4] * errors.focal_scale + errors.focal_offset
 ├─ focus ← origin + focus_distance * direction
 ├─ alpha, beta ← direction_to_angles(direction)
 │    alpha = atan2(d.x, −d.z)，beta = atan2(d.y, −d.z)
 │    d.z ≥ 0 时抛错（出射光必须朝 −Z 半空间）
 │
 └─ ForwardResult{ pose, focus, direction, intersections, segments, objective }
```

`errors` 为空时即理想机；`create_seeded_real_machine(seed=2026)` 注入的真实机误差：

| 误差项 | 分布 | 实测 RMS |
|---|---|---|
| `position_offsets` | N(0, 20 μm)，4×3 | 16.15 μm |
| `axis_tilts` | N(0, 100 μrad)，4×3 | 54.15 μrad |
| `zero_offsets` | N(0, 50 μrad)，4 | 61.58 μrad |
| `focal_scale` / `focal_offset` | 常数 | 1.0002 / 20 μm |

### 逆向：位姿 → 指令

`inverse_kinematics()` 用 `scipy.optimize.least_squares` 在边界内解：

```
目标 T ──> 残差 = pose_residual(forward(q), T) / 尺度
              │  角分量经 atan2(sin,cos) 回绕，避免 ±π 跳变
              │  位置尺度 max(pos_tol,1e-5)，角度尺度 max(ang_tol,1e-5)
              │  几何失败时返回常数 1e6，把解推回可行域
              └── least_squares(bounds=[lower,upper], max_nfev=150, xtol/ftol/gtol=1e-12)
                   └── success = 求解器成功 且 位置残差≤tol 且 角度残差≤tol
```

标称点 `q=[0,0,0,0,0.075]` 处雅可比奇异值为 `[2.6994, 2.1889, 1.0007, 0.0504, 0.0429]`，全部非零，秩 5 —— 这是五维可解的前提，也是 `tests/test_kinematics.py::test_jacobian_is_full_rank` 把守的契约。

## 5D 补偿矩阵是怎么生成的

### 它到底是什么

补偿矩阵是一张 **21×5 的线性系数表**，不是几何矩阵。它把「真实机相对理想机的位姿偏差」表达为目标位姿的二次函数：

```
C            : 21 × 5
x            = (T − center) / scale        逐维标准化后的位姿
features(x)  : 21                          基函数向量
errors(T)    = features(x) @ C  ∈ R⁵       ← 预测的 [ΔX,ΔY,ΔZ,Δα,Δβ]
```

21 项基函数 = 1 个常数项 + 5 个一次项 + 15 个二次项：

```
1, x0, x1, x2, x3, x4,
x0², x0x1, x0x2, x0x3, x0x4, x1², x1x2, x1x3, x1x4, x2², x2x3, x2x4, x3², x3x4, x4²
```

其中 `x = (T − center) / scale` 是逐维标准化后的位姿，项数展开式
`(n+1)(n+2)/2 = 21`（n=5）。第 j 列（j=0..4）是第 j 个误差分量 `[ΔX,ΔY,ΔZ,Δα,Δβ]`
对应的 21 个系数。

### 生成流程：离线标定

```
① 随机采样指令
   q[0:4] ~ U(−angle_limit×0.55, +angle_limit×0.55)   angle_limit=3.75° → ±2.06°
   q[4]   ~ U(0.074, 0.076)
        │
② 同一指令喂给两台机器，得到「同一输入下的位姿差」
   ideal_pose = ideal.forward(q).pose
   real_pose  = real .forward(q).pose
        │
③ 过滤无效样本
   几何失败（打不到镜面/孔径外）→ 丢弃
   理想位姿超出工作域 → 丢弃
   有效样本不足 sample_count 且尝试次数 < 30×sample_count → 继续采样
        │
④ 组装标定数据 CalibrationData
   commands 400×5 | ideal_poses 400×5 | real_poses 400×5
   errors = real_poses − ideal_poses     ← 400×5，角分量做 ±π 回绕
        │
⑤ 标准化（防止量级失衡）
   center = mean(ideal_poses, axis=0)          5 维
   scale  = std(ideal_poses, axis=0)，<1e-12 时置 1
   x = (ideal_poses − center) / scale
        │
⑥ 构造特征并最小二乘求解
   A = _quadratic_features(x)                  400×21
   C, *_ = np.linalg.lstsq(A, errors, rcond=None)    →  21×5
        │
⑦ 独立验证（不同 seed，独立采样命令）
   verify_compensation(...) → 补偿前后位置/姿态 RMSE
```

`np.linalg.lstsq` 解的是超定方程 `A·C = errors`：400 个方程 > 21 个未知数，
得到唯一的最小二乘解。

### 使用流程：在线推理

```
目标位姿 T
   │
① 用补偿矩阵迭代反推「理想机应该走到哪」
   p ← T
   重复 3 次:  p ← T − predict(p)          predict(p) = features((p−center)/scale) @ C
   corrected ← p
   │
② 让理想机逆解出能到 corrected 的指令
   inverse_kinematics(ideal_machine, corrected,
                      initial_command = 当前滑块指令,
                      position_tolerance = 2e-6, angle_tolerance = 2e-6)
   │
③ 把这条指令交给真实机执行
   after = real_machine.forward(corrected_command)
   │
④ 与目标比较
   errors_after = pose_residual(after.pose, T)
```

第 ① 步的迭代是必要的：`predict` 的自变量是**理想机应当到达的位置**，
而不是最终目标，所以需要不动点迭代。实测在前 2 轮内即收敛（残差变化 < 1e-7）。

### 为什么这样设计

| 设计选择 | 理由 |
|---|---|
| 对**系数**线性 | 最小二乘一步求解，不需要非线性优化，快且无初值敏感 |
| 只到二阶 | 21 参数配几百样本，超定充分；参数少，不易过拟合 |
| 输入标准化 | 5 个位姿分量量级差异巨大（`scale` 实测 `[1.2e-3,1.2e-3,5.4e-4,1.5e-2,1.5e-2]`），不标准化会让大分量主导拟合 |
| 角分量回绕 | 位姿与残差的角分量都做 `atan2(sin,cos)`，避免 ±π 跳变污染训练 |
| 训练与验证分离 | `seed` 与 `seed+1`，验证命令独立采样，报告成功/失败数 |
| 只在标定域内有效 | 超出工作域时 `compare` 直接停用补偿，不给出虚假改善 |

### 实测数据

标定 400 样本（`seed=42`，页面首次加载用的就是这组参数）：

| 项 | 数值 |
|---|---|
| 采样角度范围 | ±2.062°（`angle_fraction=0.55`） |
| `qf` 采样范围 | 0.074006 ~ 0.075998 m |
| 理想位姿径向偏移 | 最大 2.4964 mm（视场半径 2.5 mm），均值 1.5734 mm |
| 工作域内占比 | 400/400 |
| 系数矩阵 | 21×5 |
| `center` | `[9.83e-3, −5.60e-5, 3.79e-6, −1.25e-3, −5.76e-4]` |
| `scale` | `[1.21e-3, 1.16e-3, 5.43e-4, 1.51e-2, 1.54e-2]` |

补偿效果（独立验证集 80 点，由 `seed+1=43` 单独采样，全部成功、0 失败）：

| 指标 | 补偿前 | 补偿后 | 改善 |
|---|---|---|---|
| 位置 RMSE | 64.87 μm | 0.002 μm | 99.997% |
| 姿态 RMSE | 230.6 μrad | 0.003 μrad | 99.999% |

标定规模的边际效应（固定验证集：`seed=999`、60 点、与训练同域）：

| 标定规模 | 位置 RMSE（补偿后） | 姿态 RMSE（补偿后） |
|---|---|---|
| 400 样本 | 0.011106 μm | 0.002475 μrad |
| 800 样本 | 0.011107 μm | 0.002650 μrad |

两者系数矩阵相对差仅 **0.06%**，位置残差在小数点后第 5 位才有区别，姿态残差差
0.000175 μrad；说明 400 样本对该模型已接近饱和 —— 加倍样本不会带来可见改善。

### 工作域：真实约束比机械行程紧得多

这是文档里最容易误解的一点。`angle_limit` 是 3.75°，但**能用的范围小一个量级**：

| 约束 | 来源 | 数值 |
|---|---|---|
| 机械行程 | `MachineModel.angle_limit` | ±3.75° |
| **标记视场** | `marking_field_diameter_m` | 半径 2.5 mm ← 实际卡口 |
| Z 向调焦 | `maximum_focus_range_z_m` | ±1 mm |
| 最大入射角 | `maximum_incidence_angle_rad` | ±7.5° |

实测单轴扫描（其余轴归零）在**工作域内**的最大转角：

| 轴 | 工作域内上限 |
|---|---|
| q1 | 0.6° |
| q2 | 0.7° |
| q3 | 0.7° |
| q4 | 1.1° |

转角与径向偏移近似线性。单轴速率约 **1.309 mm/°**（由 75 mm 焦距决定：
`0.075 × π/180`）；上表 q1、q2 各转 a 度时两轴叠加，故约为 2 倍即 5.03 mm/°。
所以转角超过约 0.5°（单轴）就会因径向偏移突破 2.5 mm 视场半径而离开工作域；再大则
光线直接打不到 M4 镜面（实测 2.0° 时抛 `Ray misses mirror 4 aperture`）。
`tests/test_kinematics.py` 里的
`test_default_profile_matches_515_nm_standard_workspace` 断言了这条边界。

这解释了页面上的两个现象：滑块拖到较大转角后会提示「当前目标超出标定工作域，补偿对比已停用」；
以及为什么标定采样要把角度收到 ±2.06°。

需要强调：`angle_fraction=0.55` 这个采样范围**仍然远大于**可用工作域，全靠过滤器兜住。
实测 4000 条候选指令的存活情况：

| 结果 | 数量 | 占比 |
|---|---|---|
| 几何失败（打不到镜面/孔径外） | 217 | 5.4% |
| 超出标记视场工作域 | 3555 | 88.9% |
| **有效** | **228** | **5.7%** |

即**约 17.5 条候选才留下 1 条**。这直接解释了 `generate_calibration_data` 里
`maximum_attempts = sample_count × 30` 这个 30 倍余量的来历；也解释了为什么
`angle_fraction=0.9` + `sample_count=1000` 会抛
`Only 409 of 1000 valid calibration samples could be generated` —— 采样域越大，
工作域过滤器存活率越低，30 倍尝试次数也不够用。

前述「400/400 全在域内」是**过滤之后**的结果，不是采样天然落在域内。

## 观察补偿效果

页面显示 M1–M4 四面振镜、转轴、入射光阑和等效聚焦镜组，可切换理想、未补偿、补偿后镜片状态。
镜片厚度与支架为显示示意；位置、镜面法向和转轴取自各自计算状态。焦点用固定 4 px 点标记。

首次打开时自动训练 400 个标定点。滑块指定理想指令及对应目标；三条光路分别为理想机、
真实机执行原指令、真实机执行补偿后的修正指令。XY / XZ 位置误差和 αβ 姿态误差图以
目标为零点，位置单位 μm、角度单位 μrad，可选“补偿残差特写”。被刻度裁切的点会明确提示。
表格给出五个误差分量及范数；小残差以科学计数法显示。

超出标定工作域或逆解失败时，不显示补偿后结果。验证样本独立采样且限制在标定工作域内，
报告成功数与失败数。模型仅包含确定性误差，仿真残差不能当作设备实际精度。

## 安装与运行

### 一键启动（推荐）

双击本目录（`05-五轴与补偿篇/代码/`）下的 `启动网页.bat`。脚本会自动完成以下工作：

1. 切换到脚本所在目录，因此双击即可，不依赖当前工作目录
2. 缺少 `.venv` 时自动创建并安装依赖；依赖缺失时自动补装
3. 端口被占用时自动顺延到下一个可用端口，并在窗口中提示
4. 等接口真正就绪后再打开默认浏览器，避免出现空白页

指定端口：`启动网页.bat 8010`。此时若端口被占用，脚本会报错并列出占用进程，
不会静默换端口。关闭黑窗口即停止服务。

### 手动启动

```powershell
cd 05-五轴与补偿篇/代码
py -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev]"
.\.venv\Scripts\python -m pytest
.\.venv\Scripts\five-axis-galvo
```

浏览器打开 <http://127.0.0.1:8000>。API 文档位于
<http://127.0.0.1:8000/docs>。

注意 `api.py` 的 `main()` 中 `reload=False` 是硬编码的，修改 Python 代码后需要
重启服务；修改 `static/` 下的前端文件只需刷新浏览器。

## 研究边界

镜面中心、初始法向和旋转轴未包含在规格表中，因此默认值是为保证五维雅可比满秩而设置的
紧凑型虚拟光路，不代表厂商内部结构。接入真实设备时，
应替换镜面中心、法向、旋转轴、行程和焦距范围，并使用实测标定数据训练补偿模型。
