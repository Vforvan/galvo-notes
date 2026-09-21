"""
optics_calc.py -- 振镜光学系统计算器（教学 + 选型工具）

用途:
  1. 算聚焦光斑尺寸与焦深（含 M²）
  2. 由需要的幅面/光斑反推该选多大焦距的 F-θ 场镜
  3. 算扩束镜倍率、准直后光束参数
  4. 算功率密度（选镜片时判断损伤阈值够不够）
  5. 算焦面弯曲、扫描速度、伺服滞后距离
  6. 自检：用真实厂商数据反算，确认公式系数没记错

用法:
  python optics_calc.py selftest
  python optics_calc.py spot 1064 160 10                 # 波长nm 焦距mm 入射光斑mm
  python optics_calc.py spot 1064 160 10 --m2 1.5
  python optics_calc.py lens 1064 100 50                 # 反推场镜焦距：波长 幅面mm 要的光斑um
  python optics_calc.py expand 3 12                      # 输入光斑mm 需要的扩束倍率
  python optics_calc.py collimate 50 0.12 100            # 纤芯um 光纤NA 准直镜焦距mm
  python optics_calc.py power 1000 50                    # 功率W 光斑直径um
  python optics_calc.py curvature 160 200                # 球面焦面矢高（⚠️ 非场镜残差）
  python optics_calc.py speed 160 20 2.0                 # 场镜焦距mm 光学角deg 转速rad/s
  python optics_calc.py delay 160 2000 25                # 场镜焦距mm 扫描速度mm/s 滞后时间us
  python optics_calc.py table 1064                       # 打印常用场镜参数表

约定（重要，别搞错）:
  * 所有"角度"默认是【光学角】（= 2 × 机械角）
  * 场镜公式用 r = f × θ，θ 单位是弧度
  * 光斑默认用 d = 1.83·λ·f·M²/D —— 这是 Thorlabs / LINOS / Sill 等厂商标称口径
    （入瞳在 1/e² 处硬截断）。另一个式子 4λfM²/(πD) 差了 43.7%，两式结果【不可互相对照】，
    工具两个都打印，但看清楚标签再用
  * 焦深用瑞利长度定义 DOF = 2·z_R
"""

import math
import sys

# ---------------------------------------------------------------- 基础工具

def nm(x):   return x * 1e-6      # nm  -> mm
def um(x):   return x * 1e-3      # um  -> mm
def to_um(x): return x * 1e3      # mm  -> um
def deg2rad(d): return d * math.pi / 180.0


# ---------------------------------------------------------------- 光斑与焦深

def spot_size(wavelength_nm, f_mm, d_in_mm, m2=1.0):
    """
    衍射极限聚焦光斑直径。两种系数【不可混用】，差 44%！

    厂商标称值用（本工具默认，与 Thorlabs / LINOS / Sill 目录口径一致）:
        d = 1.83·λ·f·M² / D        D = 在 1/e² 处【被硬截断】的高斯入瞳直径
    未截断理想高斯:
        d = 4·λ·f·M² / (π·D)       D 同上，d 为 1/e² 直径

    两式 D 含义相同，系数不同（1.83 vs 4/π=1.273），比值 1.4373 -> 差 43.7%。
    来历: 入瞳边缘硬截断 -> 孔径衍射主瓣变宽 + 旁瓣，系数从 1.273 抬到 1.83。
    所以【不要】拿 1.83 算出的值和 4/π 算出的值互相对照，会以为哪里错了。

    返回 (d_vendor, d_ideal) 单位 mm。
    """
    lam = nm(wavelength_nm)
    d_vendor = 1.83 * lam * f_mm * m2 / d_in_mm
    d_ideal = 4.0 * lam * f_mm * m2 / (math.pi * d_in_mm)
    return d_vendor, d_ideal


def depth_of_focus(wavelength_nm, f_mm, d_in_mm, m2=1.0, mode="rayleigh"):
    """
    焦深。

    mode="rayleigh":  DOF = 2·Z_R = 2·λ·M²·f² / (π·(D/2)²)·... 这里用
                      DOF = 8·λ·M²·(f/D)² / π   （瑞利长度 ×2，常用定义）
    mode="spot":      工程判据 DOF ≈ ±d/2 / NA，NA = D/(2f)
    返回 mm。
    """
    lam = nm(wavelength_nm)
    if mode == "rayleigh":
        return 8.0 * lam * m2 * (f_mm / d_in_mm) ** 2 / math.pi
    # 工程判据：焦点前后光斑直径不超过焦斑的 √2 倍 -> 约 ±λ/(NA²)·...
    na = d_in_mm / (2.0 * f_mm)
    d_eng, _ = spot_size(wavelength_nm, f_mm, d_in_mm, m2)
    return 2.0 * d_eng / na


# ---------------------------------------------------------------- 场镜 / 幅面

def field_size(f_mm, half_angle_deg):
    """
    扫描幅面边长 = 2·f·θ（θ 为半角，弧度）。返回 mm。
    注意：这是【光学角】半角。
    """
    return 2.0 * f_mm * deg2rad(half_angle_deg)


def curvature(f_mm, field_mm):
    """
    未校正【球面】焦面的矢高（⚠️ 不是 F-θ 场镜的残余场曲！）:

        Δz = √(f² + r²) − f  ≈  r²/(2f)      （精确式与近似式都返回）

    ⚠️ 重要边界（本工具最容易误用的地方）:
      这个式子的含义是「假如完全没有做平场校正，焦面会弯多少」，
      典型用途是分析**预聚焦（pre-scan）架构**为什么需要动态调焦。

      **它不能用来评估 F-θ 场镜的残余场曲。**
      F-θ 场镜是专门为平场设计的多片系统，真实残差比这个值小约 143 倍
      （f=160、y=100：矢高 28.68 mm vs 真实残差约 0.2 mm）。
      真实残差要从场镜的 "Field Curvature vs Deflection Angle" 曲线读。

    因此本函数返回 dict，两个值都给，并在调用处明确标注口径。
    """
    r = field_mm / 2.0
    return {
        "sag_exact": math.sqrt(f_mm ** 2 + r ** 2) - f_mm,
        "sag_approx": r * r / (2.0 * f_mm),
        "r": r,
    }


def pick_lens(wavelength_nm, field_mm, target_spot_um, d_in_mm, m2=1.0,
              half_angle_deg=20.0, max_f_mm=1000.0):
    """
    反推：要在 field_mm 幅面上得到 target_spot_um 的光斑，需要多大焦距？
        f = 1.83·λ·f/D  ->  f = d·D / (1.83·λ)
    同时受扫描角限制: f >= field/(2·θ)
    返回 dict。
    """
    lam = nm(wavelength_nm)
    d_target = um(target_spot_um)
    f_by_spot = d_target * d_in_mm / (1.83 * lam * m2)
    f_by_angle = field_mm / (2.0 * deg2rad(half_angle_deg))
    f_need = max(f_by_spot, f_by_angle)
    return {
        "f_by_spot": f_by_spot,
        "f_by_angle": f_by_angle,
        "f_recommend": f_need,
        "binding": "光斑要求" if f_by_spot >= f_by_angle else "扫描角要求",
        "actual_spot_um": to_um(spot_size(wavelength_nm, f_need, d_in_mm, m2)[0]),
    }


# ---------------------------------------------------------------- 扩束 / 准直

def expander_mag(d_in_mm, d_need_mm):
    """需要多大扩束倍率。"""
    return d_need_mm / d_in_mm


def collimate(core_um, na, f_mm):
    """
    光纤输出准直：
      准直后光斑直径 D ≈ 2·f·NA
      准直后发散角 θ_div ≈ 光纤纤芯直径 / f
      光束参数积 BPP = (core/2)·NA  （不变量）
    返回 dict，长度单位 mm、角度单位 mrad。
    """
    d_out = 2.0 * f_mm * na
    div = um(core_um) / f_mm           # rad
    bpp = (um(core_um) / 2.0) * na     # mm·rad
    return {
        "d_out_mm": d_out,
        "divergence_mrad": div * 1e3,
        "bpp_mm_mrad": bpp * 1e3,
        "d_over_f_ratio": d_out / f_mm,
    }


# ---------------------------------------------------------------- 功率密度

def power_density(power_w, spot_dia_um, shape="tophat", absorption=1.0):
    """
    功率密度 (W/cm²)。
      tophat:  P / (π·(d/2)²)
      gauss:   2P / (π·(d/2)²)   （高斯峰值是平均值 2 倍）
    """
    d_cm = um(spot_dia_um) / 10.0      # mm -> cm
    area = math.pi * (d_cm / 2.0) ** 2
    base = power_w * absorption / area
    return base * (2.0 if shape == "gauss" else 1.0)


# ---------------------------------------------------------------- 运动学

def scan_speed(f_mm, half_angle_deg, omega_rad_s):
    """
    正弦扫描时焦平面上的最大线速度:
       r = f·θ, θ = A·sin(ωt)  ->  v_max = f·A·ω
    返回 mm/s。
    """
    return f_mm * deg2rad(half_angle_deg) * omega_rad_s


def servo_lag(f_mm, speed_mm_s, lag_us):
    """伺服滞后距离 (mm) = 速度 × 滞后时间。"""
    return speed_mm_s * (lag_us * 1e-6)


# ---------------------------------------------------------------- 输出

def cmd_spot(a):
    wl, f, d = float(a[0]), float(a[1]), float(a[2])
    m2 = 1.0
    if "--m2" in a:
        m2 = float(a[a.index("--m2") + 1])
    de, dr = spot_size(wl, f, d, m2)
    dz = depth_of_focus(wl, f, d, m2)
    na = d / (2 * f)
    print(f"输入: λ={wl:g} nm  f={f:g} mm  D={d:g} mm  M²={m2:g}")
    print(f"  D/f 比        = {d/f:.4f}")
    print(f"  数值孔径 NA   = {na:.4f}")
    print(f"  光斑 d (1.83λf/D) = {to_um(de):8.2f} μm   ← 厂商标称口径（1/e² 硬截断）")
    print(f"  光斑 d (4λf/πD)   = {to_um(dr):8.2f} μm   ← 未截断理想高斯，比上面小 {to_um(de)/to_um(dr):.3f}×")
    print(f"  焦深 DOF (瑞利)   = {dz:8.4f} mm = {dz*1000:.0f} μm")
    print(f"  焦深 DOF (工程)   = {depth_of_focus(wl,f,d,m2,'spot'):8.4f} mm")
    print()
    print(f"  ⚠️ 两个光斑系数差 {(to_um(de)/to_um(dr)-1)*100:.1f}%，【不要混用】——")
    print(f"     和厂商目录对比时用 1.83 口径，别拿 4/π 的结果去质疑手册。")
    print(f"  ⚠️ 实际光斑通常比理论值大 10%~30%（波前误差、装调、镜面粗糙度）")


def cmd_lens(a):
    wl, field, target = float(a[0]), float(a[1]), float(a[2])
    d = float(a[3]) if len(a) > 3 else 10.0
    ha = float(a[4]) if len(a) > 4 else 20.0
    r = pick_lens(wl, field, target, d, half_angle_deg=ha)
    print(f"目标: λ={wl:g} nm  幅面={field:g} mm  目标光斑={target:g} μm")
    print(f"      入射光斑 D={d:g} mm  最大半角={ha:g}°(光学角)")
    print(f"  → 光斑要求 f ≥ {r['f_by_spot']:8.1f} mm")
    print(f"  → 扫描角要求 f ≥ {r['f_by_angle']:8.1f} mm")
    print(f"  → 推荐焦距 f = {r['f_recommend']:8.1f} mm（由「{r['binding']}」决定）")
    print(f"  → 该焦距下光斑 = {r['actual_spot_um']:.1f} μm")
    print()
    for cand in (100, 160, 210, 254, 330, 420, 500):
        if cand < r["f_recommend"]:
            continue
        s = to_um(spot_size(wl, cand, d)[0])
        fs = field_size(cand, ha)
        print(f"  候选 f={cand:4d} mm → 光斑 {s:6.1f} μm, ±{ha:g}° 幅面 {fs:7.1f} mm")


def cmd_expand(a):
    d_in, d_need = float(a[0]), float(a[1])
    m = expander_mag(d_in, d_need)
    print(f"输入光斑 {d_in:g} mm → 需要 {d_need:g} mm")
    print(f"  扩束倍率 M = {m:.2f}×")
    print(f"  ⚠️ 扩束后光斑必须 ≤ 场镜入瞳直径，否则边缘会被切光（渐晕）")
    for cand in (1, 1.5, 2, 2.5, 3, 4, 6, 8, 10):
        if d_in * cand >= d_need:
            print(f"  最接近的标准倍率: {cand}× → 输出 {d_in*cand:.2f} mm")
            break


def cmd_collimate(a):
    core, na_, f = float(a[0]), float(a[1]), float(a[2])
    r = collimate(core, na_, f)
    print(f"光纤: 纤芯 {core:g} μm, NA {na_:g}   准直镜 f={f:g} mm")
    print(f"  准直后光斑直径 D = 2·f·NA = {r['d_out_mm']:.2f} mm")
    print(f"  准直后发散角     = core/f = {r['divergence_mrad']:.2f} mrad")
    print(f"  光束参数积 BPP   = {r['bpp_mm_mrad']:.3f} mm·mrad  ← 系统不变量，选镜片的硬约束")
    print(f"  D/f              = {r['d_over_f_ratio']:.4f}")
    print()
    print("  💡 把这个 D 当作后续扩束镜的输入光斑，再去算焦斑")


def cmd_power(a):
    p, d = float(a[0]), float(a[1])
    print(f"{p:g} W 激光, 光斑直径 {d:g} μm")
    print(f"  平顶分布 平均功率密度 = {power_density(p, d, 'tophat'):.3e} W/cm²")
    print(f"  高斯分布 峰值功率密度 = {power_density(p, d, 'gauss'):.3e} W/cm²")
    print(f"  = {power_density(p,d,'gauss')/1e6:.2f} MW/cm² (高斯峰值)")
    print()
    print("  ⚠️ 连续激光选镜片时，按【峰值】而不是平均值去比 LIDT，并留 2~3 倍余量")


def cmd_curvature(a):
    f, field = float(a[0]), float(a[1])
    c = curvature(f, field)
    print(f"场镜 f={f:g} mm, 幅面 {field:g} mm")
    print(f"  半幅面 r = {c['r']:g} mm")
    print()
    print("  【未校正球面焦面】—— 不是 F-θ 场镜的真实残差！")
    print(f"    精确矢高 √(f²+r²)−f = {c['sag_exact']:.2f} mm")
    print(f"    近似式    r²/(2f)    = {c['sag_approx']:.2f} mm"
          f"   （偏高 {(c['sag_approx']/c['sag_exact']-1)*100:.0f}%）")
    print()
    print("  【F-θ 场镜真实残余场曲】")
    print(f"    ≈ 0.2 mm 量级（f=160~254 档，读厂商 Field Curvature 曲线）")
    print(f"    → 比上面的球面矢高小约 {c['sag_exact']/0.2:.0f} 倍")
    print()
    dof = depth_of_focus(1064, f, 10)
    print(f"  判据：残余场曲 0.2 mm  vs  焦深 DOF（D=10 mm 时 = {dof:.3f} mm）")
    verdict = "落在焦深内 → 不需要 Z 轴" if 0.2 < dof else "超出焦深 → 需要 Z 轴补偿"
    print(f"    → 0.2 mm {'<' if 0.2 < dof else '>'} {dof:.3f} mm：{verdict}")
    print()
    print("  ⚠️ 但光斑越小焦深越短：50 µm 光斑 DOF≈±1.85 mm（不需要），")
    print("     12 µm 光斑 DOF≈±0.11 mm（0.2 mm 残差是它的 1.8 倍，必须补偿）")
    print("  ⚠️ 还有一条否决项：先算 θ = r/f，别超场镜额定角")
    print(f"     本例 f={f:g}、r={c['r']:g} → θ = {math.degrees(c['r']/f):.1f}°"
          f"（FTH160-1064 额定仅 ±28°）")


def cmd_speed(a):
    f, ang, omega = float(a[0]), float(a[1]), float(a[2])
    v = scan_speed(f, ang, omega)
    print(f"场镜 f={f:g} mm, 半角 {ang:g}°(光学角), 角频率 {omega:g} rad/s")
    print(f"  边缘最大线速度 v = f·θ·ω = {v/1000:.3f} m/s = {v:.1f} mm/s")
    freq = omega / (2 * math.pi)
    print(f"  对应扫描频率 = {freq:.1f} Hz")
    print(f"  ⚠️ 若这超过振镜带宽，边缘图形就会失真（见 02-硬件实现篇/05）")


def cmd_delay(a):
    f, v, lag = float(a[0]), float(a[1]), float(a[2])
    d = servo_lag(f, v, lag)
    print(f"场镜 f={f:g} mm, 扫描速度 {v:g} mm/s, 伺服滞后 {lag:g} μs")
    print(f"  滞后距离 = v·t = {d*1000:.1f} μm")
    print(f"  换算成角度 = {d/f*1000:.3f} mrad")
    print(f"  💡 这就是激光开关需要提前/延后的量级（laser on/off delay）")


def cmd_table(a):
    wl = float(a[0]) if a else 1064.0
    print(f"常用 F-θ 场镜参数表（λ={wl:g} nm, 入射光斑 D=10 mm, 半角 ±20°）")
    print(f"{'f (mm)':>8} {'幅面 (mm)':>12} {'光斑 (μm)':>11} {'焦深 (mm)':>11} {'NA':>8}")
    print("-" * 54)
    for f in (100, 160, 210, 254, 330, 420, 500, 800):
        d10 = to_um(spot_size(wl, f, 10)[0])
        dof = depth_of_focus(wl, f, 10)
        print(f"{f:>8} {field_size(f,20):>12.1f} {d10:>11.1f} {dof:>11.4f} {10/(2*f):>8.4f}")
    print()
    print("  ⚠️ 光斑随 D 反比变化：D 减半，光斑翻倍。所以扩束镜倍率直接决定光斑。")
    print("  ⚠️ 幅面按 ±20° 光学角算；实际振镜可能只有 ±10~±15°，幅面要按实测算。")


# ---------------------------------------------------------------- 自检

def selftest():
    ok = True
    print("=" * 62)
    print("optics_calc.py 自检")
    print("=" * 62)

    def check(name, got, want, tol, unit=""):
        nonlocal ok
        good = abs(got - want) <= tol
        ok = ok and good
        print(f"  [{'PASS' if good else 'FAIL'}] {name}: got {got:.4f}{unit}, "
              f"want {want:.4f}±{tol:.4f}{unit}")

    # 1. 经典校验：JHC 金海创经验数据
    #    "10 mm 光斑 + F160 场镜 → 光斑约 33 μm"
    d, _ = spot_size(1064, 160, 10)
    print("\n1) 厂商经验数据反算（JHC 金海创：10 mm 光斑 + F160 → 约 33 μm）")
    check("F160 光斑", to_um(d), 33.0, 3.0, " μm")

    #    "F254 → 光斑约 52 μm"
    d2, _ = spot_size(1064, 254, 10)
    print("   （JHC：F254 → 约 52 μm）")
    check("F254 光斑", to_um(d2), 52.0, 3.0, " μm")

    # 2. 两种光斑系数差 1.83/(4/π) = 1.4373
    print("\n2) 两种光斑系数之比应为 1.83/(4/π) = 1.4373（差 43.7%，不可混用）")
    de, dr = spot_size(1064, 160, 10)
    check("系数比 de/dr", de / dr, 1.83 / (4.0 / math.pi), 1e-9)

    # 3. 场镜基本关系 r = f·θ
    print("\n3) 场镜线性关系 r = f·θ")
    check("f=160, θ=20° → r", field_size(160, 20) / 2, 160 * deg2rad(20), 1e-9, " mm")

    # 4. 幅面数值校验：f=160, ±20° → ±55.85 mm → 111.7 mm
    print("\n4) 幅面数值（f=160 mm, ±20° 光学角）")
    check("满幅面", field_size(160, 20), 111.70, 0.05, " mm")

    # 5. 普适性：光斑 ∝ f
    print("\n5) 光斑应正比于焦距")
    a1, _ = spot_size(1064, 100, 10)
    a2, _ = spot_size(1064, 200, 10)
    check("f 翻倍光斑翻倍", a2 / a1, 2.0, 1e-9)

    # 6. 光斑应反比于入射光斑 D
    print("\n6) 光斑应反比于入射光斑直径 D")
    b1, _ = spot_size(1064, 160, 10)
    b2, _ = spot_size(1064, 160, 20)
    check("D 翻倍光斑减半", b1 / b2, 2.0, 1e-9)

    # 7. 光纤准直：NA 0.12, f=100 → D = 24 mm；纤芯 50 μm → 发散角 0.5 mrad
    print("\n7) 光纤准直（纤芯 50 μm, NA 0.12, f=100 mm）")
    c = collimate(50, 0.12, 100)
    check("准直光斑 D", c["d_out_mm"], 24.0, 1e-9, " mm")
    check("发散角", c["divergence_mrad"], 0.5, 1e-9, " mrad")
    check("BPP", c["bpp_mm_mrad"], 3.0, 1e-9, " mm·mrad")

    # 8. BPP 不变量：扩束后 BPP 不变
    print("\n8) 光束参数积 BPP 在扩束前后应不变")
    D1, th1 = 10.0, 2.0          # mm, mrad
    M = 3.0
    D2, th2 = D1 * M, th1 / M
    check("BPP 守恒", D2 * th2, D1 * th1, 1e-9, " mm·mrad")

    # 9. 功率密度：1000 W / 50 μm 平顶
    print("\n9) 功率密度（1000 W, 光斑 50 μm, 平顶）")
    #  d=50μm=0.005cm, r=0.0025cm, A=π·r²=1.9635e-5 cm²
    #  P/A = 1000/1.9635e-5 = 5.093e7 W/cm²
    check("功率密度", power_density(1000, 50) / 1e6, 50.93, 0.05, " MW/cm²")

    # 10. 高斯峰值 = 平顶的 2 倍
    print("\n10) 高斯峰值应为平顶的 2 倍")
    check("峰值/平均", power_density(1000, 50, "gauss") / power_density(1000, 50), 2.0, 1e-9)

    # 11. 扫描速度：f=160, ±20°, ω=2π·100 Hz
    print("\n11) 扫描速度 v = f·θ·ω")
    v = scan_speed(160, 20, 2 * math.pi * 100)
    want = 160 * deg2rad(20) * 2 * math.pi * 100
    check("v_edge", v, want, 1e-9, " mm/s")
    print(f"         = {v/1000:.2f} m/s  ← 大步长低频扫描速度量级")

    # 12. 焦深 ∝ (f/D)²
    print("\n12) 焦深应正比于 (f/D)²")
    z1 = depth_of_focus(1064, 160, 10)
    z2 = depth_of_focus(1064, 320, 10)
    check("f 翻倍焦深 4 倍", z2 / z1, 4.0, 1e-9)

    # 13. 未校正球面焦面矢高：f=160, r=100 → √35600 − 160 = 28.68；近似 31.25
    print("\n13) 未校正球面焦面矢高（注意：不是 F-θ 场镜残差）")
    c = curvature(160, 200)
    check("精确矢高 √(f²+r²)−f", c["sag_exact"], 28.68, 0.01, " mm")
    check("近似值 r²/(2f)", c["sag_approx"], 31.25, 0.01, " mm")
    print(f"         近似值偏高 {(c['sag_approx']/c['sag_exact']-1)*100:.0f}%，"
          f"引用时用精确值 {c['sag_exact']:.2f} mm")

    # 14. 反推场镜：要 50 μm @ D=10mm, λ=1064 → f = 0.05·10/(1.83·1.064e-3)
    print("\n14) 反推场镜焦距（目标 50 μm, D=10 mm, λ=1064 nm）")
    r = pick_lens(1064, 100, 50, 10)
    want_f = 0.050 * 10 / (1.83 * 1.064e-3)
    check("f_by_spot", r["f_by_spot"], want_f, 1e-6, " mm")
    print(f"         光斑要求 f≥{r['f_by_spot']:.1f} mm, "
          f"扫描角(±20°,100mm)要求 f≥{r['f_by_angle']:.1f} mm")
    print(f"         → 由「{r['binding']}」决定，推荐 f={r['f_recommend']:.1f} mm")

    print("\n" + "=" * 62)
    print("✅ 全部检查通过" if ok else "❌ 有检查未通过")
    print("=" * 62)
    return 0 if ok else 1


# ---------------------------------------------------------------- main

COMMANDS = {
    "selftest": ("自检全部公式", None),
    "spot":     ("算聚焦光斑与焦深", cmd_spot),
    "lens":     ("反推该选多大焦距场镜", cmd_lens),
    "expand":   ("算需要的扩束倍率", cmd_expand),
    "collimate":("算光纤准直后的光束参数", cmd_collimate),
    "power":    ("算功率密度", cmd_power),
    "curvature":("未校正球面焦面矢高（非场镜残差）", cmd_curvature),
    "speed":    ("算扫描线速度", cmd_speed),
    "delay":    ("算伺服滞后距离", cmd_delay),
    "table":    ("打印常用场镜参数表", cmd_table),
}


def usage():
    print(__doc__)
    print("可用命令:")
    for k, (d, _) in COMMANDS.items():
        print(f"  {k:<10} {d}")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "help"):
        usage()
        return 0
    cmd = args[0]
    if cmd not in COMMANDS:
        print(f"未知命令: {cmd}\n")
        usage()
        return 1
    if cmd == "selftest":
        return selftest()
    try:
        COMMANDS[cmd][1](args[1:])
    except (IndexError, ValueError) as e:
        print(f"❌ 参数错误: {e}\n")
        print(f"用法见: python optics_calc.py {cmd} ...")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
