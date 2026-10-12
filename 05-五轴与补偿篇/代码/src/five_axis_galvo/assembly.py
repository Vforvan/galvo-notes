"""Public exterior dimensions and explicitly provisional internal packaging (SI units)."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np

from .geometry import GeometryError, intersect_ray_plane, normalize, reflect, rotate
from .readout import focus_readout


@dataclass(frozen=True)
class AssemblyDimensions:
    depth: float = 0.2635
    width: float = 0.3035
    height: float = 0.271
    handle_rise: float = 0.055
    exit_drop: float = 0.0557
    exit_flange_diameter: float = 0.090
    exit_neck_diameter: float = 0.080
    exit_axis_x: float = 0.31108
    exit_axis_y: float = -0.04028
    entrance_y: float = 0.05975
    entrance_z: float = 0.0494
    side_extension: float = 0.209
    panel_thickness: float = 0.004
    compartment_split_z: float = 0.133
    motor_radius: float = 0.011
    motor_length: float = 0.030
    encoder_length: float = 0.008
    mirror_radius: float = 0.005


# Modelling constants rather than drawing dimensions: they describe the beam this layout has to
# live with, not anything measured off the reference drawing.
COLLIMATED_BEAM_RADIUS = 0.001
# Radius of the drive stub the front end draws on the rotation axis.
STUB_DIAMETER = 0.0024
# Installation gap demanded between a barrel surface and the beam envelope. This is a packaging
# target, not a drawing dimension: the measured gap in ``_cylinder_clearance`` is already corrected
# for the beam radius, so a barrel that merely grazes the envelope reads as clipping on screen and
# leaves nothing for the steering swing. The layout keeps a visible air gap instead.
BARREL_CLEARANCE_MARGIN = 0.010


def _barrel_solids(shaft_length: float) -> tuple[tuple[float, float, float], ...]:
    """Coaxial (radius, near, far) barrel solids, measured along +axis from the mirror centre.

    The mirror disk is modelled separately as an actuator part, so the barrel starts at the shaft
    length rather than flush against the mirror face.
    """
    d = DIMENSIONS
    back = shaft_length + d.motor_length
    return (
        (d.motor_radius, shaft_length, back),
        (d.motor_radius * 0.91, back, back + d.encoder_length),
    )


def _stub_solid(shaft_length: float) -> tuple[float, float]:
    """(near, far) axial span for the drive stub, and the stub radius, as the front end draws it.

    The stub runs along the rotation axis towards the barrel. It may not start at the mirror: the
    beam crosses the rotation axis at the mirror centre by definition, so anything co-axial there is
    inside the beam. It starts one stub diameter before the barrel instead, and the caller keeps
    ``shaft_length`` clear of the beam, so the whole stub is clear as a consequence.
    """
    return (shaft_length - STUB_DIAMETER, shaft_length)


def _segment_distance(origin: np.ndarray, target: np.ndarray, point: np.ndarray) -> float:
    """Distance from a point to a ray segment."""
    along = target - origin
    squared = float(along @ along)
    if squared < 1e-18:
        return float(np.linalg.norm(point - origin))
    station = float(np.clip((point - origin) @ along / squared, 0.0, 1.0))
    return float(np.linalg.norm(point - (origin + along * station)))


def _cylinder_clearance(origin: np.ndarray, target: np.ndarray, anchor: np.ndarray, axis: np.ndarray,
                        radius: float, axial_bounds: tuple[float, float]) -> float:
    """Distance from a ray segment to a capped cylinder, in metres (negative means overlap).

    The barrel is a solid, so the gap is the true 3-D distance to its lateral surface *or* to either
    end cap, whichever is smaller. Measuring only the lateral surface is not enough: a ray that sits
    radially close but axially far away is nowhere near the barrel, and clamping it onto the lateral
    surface would report a collision that does not exist. Both ends are caps here because a beam that
    enters the open mirror end is just as much a conflict as one that clips the side.
    """
    along = target - origin
    if float(along @ along) < 1e-18:
        return float("inf")
    near, far = axial_bounds
    best = float("inf")

    # lateral surface of the finite cylinder
    unit = along / np.linalg.norm(along)
    length = float(np.linalg.norm(along))
    skew = unit - axis * float(unit @ axis)
    quadratic = float(skew @ skew)
    if quadratic > 1e-12:
        station = float(np.clip(-float((origin - anchor) @ skew) / quadratic, 0.0, length))
        point = origin + unit * station
        axial = float(np.clip((point - anchor) @ axis, near, far))
        radial = float(np.linalg.norm(point - anchor - axis * axial))
        best = min(best, radial - radius)

    # the two end caps
    for cap in (near, far):
        best = min(best, _segment_distance(origin, target, anchor + axis * cap) - radius)
    return best


def _barrel_gap(start: np.ndarray, end: np.ndarray, mirror_center: np.ndarray, axis: np.ndarray,
                shaft: float) -> float:
    """Worst gap between one beam envelope and the barrel that starts at ``shaft``.

    The beam radius is added to the barrel radius, so the returned gap is measured from the barrel
    surface to the outside of the beam rather than to its centreline.
    """
    return min(_cylinder_clearance(start, end, mirror_center, axis, radius + COLLIMATED_BEAM_RADIUS,
                                   (near, far))
               for radius, near, far in _barrel_solids(shaft))


def barrel_gap(mirror_center: np.ndarray, axis: np.ndarray, shaft: float,
               segments: list[list[tuple[np.ndarray, np.ndarray]]]) -> float:
    """Worst gap between one barrel and the beam envelope, in metres.

    EVERY leg is measured, with no exclusions. The two legs that meet at this mirror are the ones
    that matter most: a beam arriving at the mirror centre leaves the centre at one mirror radius
    from the shaft axis and then runs *along* the barrel, so it is precisely the leg that flies into
    that mirror's own actuator. Skipping it is what let an earlier revision report a clear layout
    while the barrel swallowed the beam. ``_clip_at_mirror`` trims the shared mirror-centre point,
    which is the only place any ray touches every candidate axis equally.
    """
    worst = float("inf")
    for leg in segments:
        for start, end in leg:
            clipped = _clip_at_mirror(start, end, mirror_center)
            if clipped is None:
                continue
            worst = min(worst, _barrel_gap(clipped, end, mirror_center, axis, shaft))
    return worst


def beam_bundle(waypoints: np.ndarray, samples: int = 8) -> list[list[tuple[np.ndarray, np.ndarray]]]:
    """Chief ray plus edge rays of the collimated bundle, grouped by leg.

    The steering bundle travels along the assumed waypoint polyline and stays parallel to each leg,
    so the envelope about every leg is that leg offset by the beam radius. Sizing a barrel against
    the chief ray alone leaves it sitting on the edge rays, and those are what actually draw it.
    """
    bundle = []
    for j in range(len(waypoints) - 1):
        start, end = np.asarray(waypoints[j]), np.asarray(waypoints[j + 1])
        unit = normalize(end - start)
        reference = np.array([0.0, 0.0, 1.0]) if abs(unit[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
        first = normalize(np.cross(unit, reference))
        second = np.cross(unit, first)
        leg = [(start, end)]
        for k in range(samples):
            angle = 2 * np.pi * k / samples
            offset = (first * np.cos(angle) + second * np.sin(angle)) * COLLIMATED_BEAM_RADIUS
            leg.append((start + offset, end + offset))
        bundle.append(leg)
    return bundle


def required_shaft_length(mirror_center: np.ndarray, axis: np.ndarray,
                          segments: list[list[tuple[np.ndarray, np.ndarray]]]) -> tuple[float, float]:
    """Pick the (shaft length, gap) for one mounting direction.

    A barrel that clears the margin wins over one that merely clears zero, because a graze reads as
    clipping on screen; among those, the shortest shaft wins so the actuator stays compact. The scan
    is coarse and then refined, so the answer is the shortest workable length without measuring every
    step, and it is reported as unusable when no length works.
    """
    d = DIMENSIONS
    limit = 0.10   # beyond this the barrel cannot fit the optical compartment anyway

    def candidate(shaft: float) -> tuple[float, float] | None:
        if not _fits_optical_compartment(mirror_center, axis, shaft):
            return None
        return float(shaft), barrel_gap(mirror_center, axis, shaft, segments)

    def scan(low: float, high: float, step: float, want_margin: bool) -> tuple[float, float]:
        """Pick the smallest shaft in the range, or the widest gap if none clears the margin."""
        best = (float("nan"), float("-inf"))
        for k in range(int((high - low) / step) + 1):
            found = candidate(d.motor_radius + low + k * step)
            if found is None:
                continue
            gap = found[1]
            if want_margin and gap <= BARREL_CLEARANCE_MARGIN:
                continue
            if np.isnan(best[0]) or (found[0], -gap) < (best[0], -best[1]):
                best = found
        return best

    coarse = scan(0.0, limit, 0.005, want_margin=True)
    if not np.isnan(coarse[0]):
        return scan(max(coarse[0] - 0.005, 0.0), coarse[0], 0.0005, want_margin=True)
    # Nothing clears the margin over the whole range, so the barrel is boxed in: report the widest
    # gap the compartment allows rather than a length that only just survives.
    return scan(0.0, limit, 0.005, want_margin=False)


def _clip_at_mirror(start: np.ndarray, end: np.ndarray, mirror_center: np.ndarray) -> np.ndarray | None:
    """Start of a beam segment once the mirror disk is removed from its end.

    The incoming and outgoing rays meet at the mirror centre by definition, which is the one point
    every candidate shaft direction shares. Leaving it in would mask the real geometry.
    """
    along = end - start
    length = float(np.linalg.norm(along))
    if length < 1e-12:
        return None
    unit = along / length
    lateral = float(np.linalg.norm(mirror_center - start))
    reach = float(np.sqrt(max(lateral ** 2 - DIMENSIONS.mirror_radius ** 2, 0.0)))
    if length <= reach:
        return None
    return start + unit * reach


def _fits_optical_compartment(mirror_center: np.ndarray, axis: np.ndarray, shaft: float) -> bool:
    """Whether the actuator barrel and encoder can sit in the lower optical compartment."""
    d = DIMENSIONS
    lower = np.array([d.panel_thickness, -d.width / 2 + d.panel_thickness, d.panel_thickness])
    upper = np.array([d.depth - d.panel_thickness, d.width / 2 - d.panel_thickness,
                      d.compartment_split_z - d.panel_thickness])
    for radius, near, far in _barrel_solids(shaft):
        center = mirror_center + axis * (near + far) / 2
        extent = np.abs(axis) * (far - near) / 2 + radius * np.sqrt(1 - axis ** 2)
        if not (np.all(center - extent > lower) and np.all(center + extent < upper)):
            return False
    return True


def _clearance(candidates: list[np.ndarray], mirror_center: np.ndarray,
               bundle: list[list[tuple[np.ndarray, np.ndarray]]]) -> list[tuple[float, float]]:
    """(gap, shaft length) per candidate shaft direction, each sized on its own measured clearance."""
    return [tuple(reversed(required_shaft_length(mirror_center, axis, bundle)))
            for axis in candidates]


def rendered_solids(motor: dict[str, object]) -> tuple[tuple[str, float, float, float], ...]:
    """Every co-axial solid the front end draws, as (name, radius, near, far) along +axis.

    The front end may only draw these; anything else it invents is unverified. Kept in one place so
    the render and the clearance check cannot drift apart again.
    """
    d = DIMENSIONS
    shaft = motor["shaft_length"]
    stub_near, stub_far = _stub_solid(shaft)
    cap = d.motor_radius * 1.1
    back = shaft + d.motor_length
    solids = []
    for radius, near, far in _barrel_solids(shaft):
        solids.append(("barrel" if radius == d.motor_radius else "encoder", radius, near, far))
    solids += [
        ("cap-near", cap, shaft - 0.0015, shaft + 0.0015),
        ("cap-far", cap, back - 0.0015, back + 0.0015),
        ("stub", STUB_DIAMETER / 2, stub_near, stub_far),
    ]
    return tuple(solids)


def verify_actuator_clearance(config: dict[str, object] | None = None) -> float:
    """Smallest gap between any rendered actuator solid and any beam leg. Nothing is skipped.

    Runs the nominal five-mirror trace and measures the chief ray plus the eight marginal rays
    against every solid ``rendered_solids`` lists: barrel, encoder can, bearing caps and drive stub.
    The two legs that meet at each mirror are included on purpose: a beam arriving at a mirror centre
    leaves it one mirror radius from that shaft axis and then runs along the barrel, so it is the leg
    most likely to be inside the motor. Negative means the beam passes through something drawn.
    The beam radius is folded into the traced rays, so this is a surface-to-surface gap.
    """
    config = config if config is not None else assembly_configuration()
    trace = trace_assembly([0.0] * 5, config=config)
    rays = [[(np.asarray(segment["start"]), np.asarray(segment["end"])) for segment in ray["segments"]]
            for ray in (trace["chief"], *trace["marginal"])]
    worst = float("inf")
    for motor in config["motors"]:
        axis = np.asarray(motor["axis"])
        center = np.asarray(motor["mirror_center"])
        for _name, radius, near, far in rendered_solids(motor):
            for segments in rays:
                for start, end in segments:
                    clipped = _clip_at_mirror(start, end, center)
                    if clipped is None:
                        continue
                    worst = min(worst, _cylinder_clearance(clipped, end, center, axis,
                                                           radius + COLLIMATED_BEAM_RADIUS,
                                                           (near, far)))
    return worst


DIMENSIONS = AssemblyDimensions()
SOURCE_URL = "https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-precSYS-EN.pdf"


def assembly_configuration() -> dict[str, object]:
    d = DIMENSIONS
    centers = [
        [0.042, d.entrance_y, d.entrance_z],
        [0.092, 0.020, 0.062],
        [0.147, 0.050, 0.0494],
        [0.204, d.exit_axis_y, 0.0494],
        [0.238, d.exit_axis_y, 0.087],
    ]
    source = [-0.025, d.entrance_y, d.entrance_z]
    fold = [d.exit_axis_x, d.exit_axis_y, d.entrance_z]
    lens = [d.exit_axis_x, d.exit_axis_y, -0.040]
    waypoints = np.asarray([source, *centers, fold, lens])
    bundle = beam_bundle(waypoints)
    motors = []
    for i, center in enumerate(centers):
        incoming = normalize(waypoints[i + 1] - waypoints[i])
        outgoing = normalize(waypoints[i + 2] - waypoints[i + 1])
        normal = normalize(incoming - outgoing)
        # Either in-plane direction is a legal rotation axis; pick the side the beam has room on.
        mirror_v = np.asarray(center, dtype=float)
        candidates = [normalize(np.cross(normal, [0, 0, 1])), normalize(np.cross([0, 0, 1], normal))]
        clear = list(zip(candidates, _clearance(candidates, mirror_v, bundle), strict=True))
        # Prefer the side that stands the barrel furthest off the beam.
        axis_v, (gap, shaft) = max(clear, key=lambda item: round(item[1][0], 4))
        if not np.isfinite(shaft) or gap <= 0:
            raise RuntimeError(f"No mounting direction clears the beam for {i + 1}")
        body_center = mirror_v + axis_v * (shaft + d.motor_length / 2)
        stub_near, stub_far = _stub_solid(shaft)
        motors.append({
            "id": f"A{i + 1}", "mirror_center": center,
            "axis": axis_v.tolist(), "body_center": body_center.tolist(),
            "base_normal": normal.tolist(),
            "shaft_length": shaft,
            # The front end draws the drive stub over exactly this span and nothing closer to the
            # mirror, because a beam crosses the rotation axis at the mirror centre by definition.
            "stub_span": [stub_near, stub_far],
            "stub_radius": STUB_DIAMETER / 2,
            # Pedestal reaches from the deck up to the barrel underside, which is what a standoff
            # this long needs. Only the solids in ``rendered_solids`` are checked against the beam,
            # so the front end must not grow the mount past this height on its own.
            "mount_top_z": float(body_center[2] - d.motor_radius),
            "command_index": i if i < 4 else None,
            "status": "assumed_packaging" if i < 4 else "unidentified_kinematics",
            # null rather than Infinity: no other beam comes near this actuator at all.
            "beam_clearance_mm": round(float(gap) * 1000, 1) if np.isfinite(gap) else None,
        })
    return {
        "profile": "precSYS 外形参考 / 可追迹假设光路 v2",
        "units": "m", "dimensions": asdict(d), "motors": motors,
        "optical_demo": {
            "source": source, "direction": [1, 0, 0], "fold_center": fold,
            "fold_normal": normalize(normalize(waypoints[-2] - waypoints[-3]) - np.array([0, 0, -1])).tolist(),
            "fold_radius": 0.010, "lens_center": lens, "lens_radius": 0.006,
            "focal_length": 0.025, "beam_radius": COLLIMATED_BEAM_RADIUS,
            "status": "hypothetical_five_mirror_thin_lens_not_compensation_model",
        },
        "source": {"url": SOURCE_URL, "edition": "02/2026", "drawing_page": 8},
        "confirmed_dimension_keys": [
            "depth", "width", "height", "handle_rise", "exit_drop",
            "exit_flange_diameter", "exit_neck_diameter", "side_extension", "entrance_z",
        ],
        "derived_dimension_keys": ["exit_axis_x", "exit_axis_y", "entrance_y"],
        "assumed_dimension_keys": [
            "panel_thickness", "compartment_split_z", "motor_radius", "motor_length",
            "encoder_length", "mirror_radius",
        ],
        "limitations": [
            "公开尺寸约束外形，不等于厂家内部结构或可制造性验证。",
            "五个旋转振镜轴有公开依据；各轴位置、轴向、外径、长度、轴长及支座为假设。",
            "各轴镜心位于轴上，光束必须落在半径 5 mm 镜面内；因此同轴电机筒只能退到光束包络之外，轴长按该轴与光束夹角逐轴计算，不是选型结果。",
            "五镜演示按装配几何逐级求交反射，初始法向由假设的零位折叠路径推导。",
            "它不是原四镜+qf补偿模型，不证明实机五维独立可控；qf不作用于此固定焦距演示。",
            "A5 仅在假设光路中转动，尚无已辨识的实机第五轴光学模型。",
            "光束只按主光线加 8 条边缘光线校核，未验证动态扫掠、支架与喷嘴遮挡、热变形、线缆弯曲半径及装配公差。",
        ],
    }


def trace_assembly(angles: list[float], config: dict[str, object] | None = None) -> dict[str, object]:
    q = np.asarray(angles, dtype=float)
    if q.shape != (5,) or not np.all(np.isfinite(q)) or np.any(np.abs(q) > np.deg2rad(3.76)):
        raise ValueError("Expected five finite mirror angles within ±3.76 degrees")
    config = config if config is not None else assembly_configuration()
    demo = config["optical_demo"]
    surfaces = [{"name": m["id"], "center": m["mirror_center"],
                 "normal": rotate(m["base_normal"], m["axis"], angle).tolist(),
                 "radius": DIMENSIONS.mirror_radius}
                for m, angle in zip(config["motors"], q, strict=True)]
    surfaces.append({"name": "固定折转镜", "center": demo["fold_center"],
                     "normal": demo["fold_normal"], "radius": demo["fold_radius"]})
    lens = np.asarray(demo["lens_center"])
    focal_length = demo["focal_length"]

    def trace_one(origin: np.ndarray) -> dict[str, object]:
        direction = np.asarray(demo["direction"], dtype=float)
        segments, hits = [], []
        for surface in surfaces:
            try:
                hit, _ = intersect_ray_plane(origin, direction, surface["center"], surface["normal"])
            except GeometryError:
                segments.append({"start": origin.tolist(), "end": (origin + direction * 0.035).tolist(),
                                 "stage": surface["name"], "valid": False})
                return {"segments": segments, "hits": hits, "focus": None, "message": f"无法到达{surface['name']}"}
            valid = np.linalg.norm(hit - surface["center"]) <= surface["radius"]
            endpoint = hit if np.linalg.norm(hit - origin) < 0.6 else origin + direction * 0.035
            segments.append({"start": origin.tolist(), "end": endpoint.tolist(), "stage": surface["name"], "valid": bool(valid)})
            if not valid:
                return {"segments": segments, "hits": hits, "focus": None, "message": f"光束打偏：{surface['name']}口径外"}
            outgoing = reflect(direction, surface["normal"])
            hits.append({"name": surface["name"], "point": hit.tolist(), "normal": surface["normal"],
                         "incoming": direction.tolist(), "outgoing": outgoing.tolist()})
            origin, direction = hit, outgoing
        try:
            hit, _ = intersect_ray_plane(origin, direction, lens, [0, 0, 1])
        except GeometryError:
            return {"segments": segments, "hits": hits, "focus": None, "message": "出射方向未到达物镜"}
        valid = np.linalg.norm(hit[:2] - lens[:2]) <= demo["lens_radius"] and direction[2] < -0.1
        segments.append({"start": origin.tolist(), "end": hit.tolist(), "stage": "物镜", "valid": bool(valid)})
        if not valid:
            return {"segments": segments, "hits": hits, "focus": None, "message": "光束打偏：物镜口径外或超出近轴演示范围"}
        # In downward axial coordinates: u_out = u_in - height / f.
        slope = direction[:2] / -direction[2] - (hit[:2] - lens[:2]) / focal_length
        focus = np.array([*(hit[:2] + focal_length * slope), lens[2] - focal_length])
        segments.append({"start": hit.tolist(), "end": focus.tolist(), "stage": "会聚焦点", "valid": True})
        return {"segments": segments, "hits": hits, "focus": focus.tolist(), "message": "到达固定焦平面（近轴薄透镜示例）"}

    source = np.asarray(demo["source"], dtype=float)
    chief = trace_one(source)
    readout = None
    if chief["focus"] is not None:
        last_segment = chief["segments"][-1]
        readout = focus_readout(chief["focus"], np.asarray(last_segment["end"]) - last_segment["start"], frame="assembly")
    marginal = [trace_one(source + np.array([0, np.cos(t), np.sin(t)]) * demo["beam_radius"])
                for t in np.linspace(0, 2 * np.pi, 8, endpoint=False)]
    return {"chief": chief, "readout": readout, "marginal": marginal, "surfaces": surfaces,
            "transmitted_rays": sum(ray["focus"] is not None for ray in marginal),
            "total_marginal_rays": len(marginal), "model": demo["status"]}
