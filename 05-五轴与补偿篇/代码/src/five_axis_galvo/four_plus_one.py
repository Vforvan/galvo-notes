"""Assumed 4+1 pre-focus architecture; not a manufacturer's optical prescription."""
from dataclasses import dataclass

import numpy as np

from .geometry import GeometryError, normalize, rotate
from .model import MachineErrors
from .readout import focus_readout
from .specifications import STANDARD_515_NM


@dataclass
class OpticalResult:
    pose: np.ndarray
    focus: np.ndarray
    direction: np.ndarray
    paths: np.ndarray
    surfaces: list
    geometric_rms: float


def cylinder_hit(start, end, center, axis, radius, length):
    """Exact segment versus closed finite cylinder (no capsule approximation)."""
    p, v = np.asarray(start) - center, np.asarray(end) - start
    z, dz = float(p @ axis), float(v @ axis)
    lo, hi = 0.0, 1.0
    if abs(dz) < 1e-14:
        if abs(z) > length / 2:
            return False
    else:
        bounds = sorted(((-length / 2 - z) / dz, (length / 2 - z) / dz))
        lo, hi = max(lo, bounds[0]), min(hi, bounds[1])
    pp, vv = p - z * axis, v - dz * axis
    a, b, c = float(vv @ vv), float(2 * pp @ vv), float(pp @ pp - radius**2)
    if a < 1e-20:
        return c <= 0 and hi - lo > 1e-9
    discriminant = b*b - 4*a*c
    if discriminant < 0:
        return False
    roots = ((-b - np.sqrt(discriminant)) / (2*a), (-b + np.sqrt(discriminant)) / (2*a))
    return min(hi, roots[1]) - max(lo, roots[0]) > 1e-9


def box_hit(start, end, center, size):
    p, d = np.asarray(start)-center, np.asarray(end)-start
    lo, hi = 0., 1.
    for i in range(3):
        if abs(d[i]) < 1e-14:
            if abs(p[i]) > size[i]/2:
                return False
        else:
            a,b = sorted(((-size[i]/2-p[i])/d[i], (size[i]/2-p[i])/d[i]))
            lo,hi = max(lo,a),min(hi,b)
    return hi-lo > 1e-9


class FourPlusOneModel:
    specifications = STANDARD_515_NM
    nominal_command = np.zeros(5)
    angle_limit = np.deg2rad(0.8)
    focus_limits = (-0.00065, 0.00065)
    work_origin = np.array([0.275, 0.200, -0.060])
    centers = np.array([[.095,.060,.065],[.095,.130,.065],[.185,.130,.065],[.185,.200,.065]])
    route = np.array([[1.,0,0],[0,1.,0],[1.,0,0],[0,1.,0],[1.,0,0]])

    def __init__(self, errors=None):
        self.errors = errors if errors is not None else MachineErrors()
        self.lower_bounds = np.array([-self.angle_limit]*4 + [self.focus_limits[0]])
        self.upper_bounds = -self.lower_bounds

    @property
    def nominal_pose(self):
        return self.forward(self.nominal_command, include_optics=False).pose

    def is_pose_within_workspace(self, pose, **kwargs):
        p = np.asarray(pose)
        return bool(np.linalg.norm(p[:2]) <= .0025 and abs(p[2]) <= .001
                    and np.hypot(np.tan(p[3]), np.tan(p[4])) <= np.tan(np.deg2rad(7.5)))

    def surfaces(self, command):
        shift = command[4] * self.errors.focal_scale + self.errors.focal_offset
        surfaces = [
            dict(name="L1 移动负透镜 / Z5", kind="lens", center=[.020+shift,.060,.065], normal=[1.,0,0], radius=.002, focal=-.020),
            dict(name="L2 固定准直镜", kind="lens", center=[.060,.060,.065], normal=[1.,0,0], radius=.005, focal=.060),
        ]
        for i, center in enumerate(self.centers):
            normal = normalize(self.route[i+1] - self.route[i])
            axis = np.array([0.,0,1.]) if i % 2 == 0 else normalize([1.,1.,0.])
            if i == 3:
                axis = -axis
            axis = normalize(axis + self.errors.axis_tilts[i])
            pivot = center+self.errors.position_offsets[i]-normal*.0028
            angle = command[i] + self.errors.zero_offsets[i]
            moved_center = pivot + rotate(normal*.0028, axis, angle)
            normal = rotate(normal, axis, angle)
            surfaces.append(dict(name=f"M{i+1} / A{i+1}", kind="mirror", center=moved_center.tolist(),
                                 normal=normal.tolist(), axis=axis.tolist(), pivot=pivot.tolist(), radius=.008))
        surfaces.extend([
            dict(name="F 固定折转镜", kind="mirror", center=[.275,.200,.065], normal=normalize([-1.,0,-1.]).tolist(), radius=.010),
            dict(name="O 固定物镜", kind="lens", center=[.275,.200,.015], normal=[0.,0,-1.], radius=.012, focal=.075),
        ])
        return surfaces

    def forward(self, command, *, include_optics=True):
        q = np.asarray(command, dtype=float)
        if q.shape != (5,) or not np.all(np.isfinite(q)) or np.any(q < self.lower_bounds-1e-12) or np.any(q > self.upper_bounds+1e-12):
            raise GeometryError("指令超限：A1–A4 ±0.8°，Z5 镜片位移 ±0.65 mm")
        theta = np.arange(8) * np.pi / 4
        origins = np.tile([-.015,.060,.065], (9,1)).astype(float)
        origins[1:,1] += .001 * np.cos(theta)
        origins[1:,2] += .001 * np.sin(theta)
        directions = np.tile([1.,0,0], (9,1))
        paths = [origins.copy()]
        surfaces = self.surfaces(q)
        for surface in surfaces:
            center, normal = np.array(surface["center"]), np.array(surface["normal"])
            denominator = directions @ normal
            if np.any(abs(denominator) < 1e-9):
                raise GeometryError(surface["name"] + "：光线平行于光学面")
            distance = ((center-origins) @ normal) / denominator
            if np.any(distance <= 0):
                raise GeometryError(surface["name"] + "：交点位于光线后方")
            origins = origins + distance[:,None]*directions
            if np.any(np.linalg.norm(origins-center, axis=1) > surface["radius"]):
                raise GeometryError(surface["name"] + "：采样光束超出口径")
            paths.append(origins.copy())
            if surface["kind"] == "mirror":
                directions = directions - 2*(directions @ normal)[:,None]*normal
            else:
                directions = directions / (directions @ normal)[:,None] - (origins-center)/surface["focal"]
            directions /= np.linalg.norm(directions, axis=1)[:,None]
        # Minimise pupil-ray variance in a plane parallel to the workpiece.
        slopes = directions[:,:2] / directions[:,2,None]
        intercepts = origins[:,:2] - slopes*origins[:,2,None]
        ds, db = slopes[1:]-slopes[1:].mean(axis=0), intercepts[1:]-intercepts[1:].mean(axis=0)
        denominator = float(np.sum(ds*ds))
        if denominator < 1e-12:
            raise GeometryError("物镜后无有限聚焦平面")
        z = -float(np.sum(ds*db)) / denominator
        distance = (z-origins[:,2])/directions[:,2]
        if np.any(distance <= 0):
            raise GeometryError("焦点位于物镜前方")
        endpoints = origins + distance[:,None]*directions
        paths.append(endpoints)
        focus = endpoints[0]
        direction = directions[0]
        pose = np.r_[focus-self.work_origin, np.arctan2(direction[:2], -direction[2])]
        rms = float(np.sqrt(np.mean(np.sum((endpoints[1:,:2]-endpoints[1:,:2].mean(axis=0))**2, axis=1))))
        return OpticalResult(pose, focus, direction, np.stack(paths,axis=1), surfaces, rms)

    def solids(self, result):
        solids = []
        for surface in result.surfaces:
            if surface["kind"] != "mirror":
                continue
            c, n = np.array(surface["center"]), np.array(surface["normal"])
            solids.append(dict(name=surface["name"]+" 背板", center=(c-n*.0011).tolist(), axis=n.tolist(), radius=surface["radius"], length=.002, role="backing"))
            if "axis" in surface:
                axis = np.array(surface["axis"])
                for label, offset, length, radius, role in [("侧轴", .012, .012, .0015,"shaft"),("电机",.032,.028,.009,"motor"),("编码器",.049,.006,.008,"encoder")]:
                    solids.append(dict(name=surface["name"]+" "+label, center=(np.array(surface["pivot"])+axis*offset).tolist(), axis=axis.tolist(), radius=radius, length=length, role=role))
        return solids

    def supports(self, result):
        x = result.surfaces[0]["center"][0]
        parts = [dict(name="基板 左",center=[.130,.132,.020],size=[.260,.264,.010]),
                 dict(name="基板 右",center=[.300,.132,.020],size=[.020,.264,.010]),
                 dict(name="基板 前",center=[.275,.0925,.020],size=[.030,.185,.010]),
                 dict(name="基板 后",center=[.275,.2395,.020],size=[.030,.049,.010]),
                 dict(name="Z5 动子",center=[x,.060,.048],size=[.012,.036,.006]),
                 dict(name="Z5 镜托",center=[x,.060,.056],size=[.003,.004,.011]),
                 dict(name="Z5 执行器",center=[.026,.087,.042],size=[.040,.013,.019]),
                 dict(name="L2 镜托",center=[.060,.060,.0425],size=[.014,.014,.035])]
        for y in [.045,.075]:
            parts.append(dict(name="Z5 导轨",center=[.026,y,.043],size=[.043,.003,.004]))
        for i,s in enumerate(result.surfaces[2:6]):
            c,n,a = np.array(s["center"]),np.array(s["normal"]),np.array(s["axis"])
            motor = np.array(s["pivot"])+a*.032
            if i % 2 == 0:
                parts.extend([dict(name=f"A{i+1} 支承板",center=[motor[0],motor[1],.080],size=[.026,.046,.005]),
                              dict(name=f"A{i+1} 支承柱",center=[motor[0],motor[1]-.020,.05125],size=[.007,.006,.0525])])
            else:
                parts.extend([dict(name=f"A{i+1} 支承板",center=[motor[0],motor[1],.0535],size=[.025,.025,.005]),
                              dict(name=f"A{i+1} 支承柱",center=[motor[0],motor[1],.038],size=[.012,.012,.026])])
        return parts

    def payload(self, command):
        result = self.forward(command)
        solids = self.solids(result)
        supports = self.supports(result)
        collisions = set()
        for path in result.paths:
            for start,end in zip(path[:-1], path[1:]):
                for solid in solids:
                    if cylinder_hit(start,end,np.array(solid["center"]),np.array(solid["axis"]),solid["radius"],solid["length"]):
                        collisions.add(solid["name"])
                for part in supports:
                    if box_hit(start,end,np.array(part["center"]),np.array(part["size"])):
                        collisions.add(part["name"])
        return dict(command=list(command), pose=result.pose.tolist(), focus_world=result.focus.tolist(),
                    z5_actual_displacement_m=result.surfaces[0]["center"][0]-.020,
                    readout=focus_readout(result.pose[:3],result.direction,frame="workpiece_4p1"),
                    paths=result.paths.tolist(), surfaces=result.surfaces, solids=solids, supports=supports,
                    geometric_rms_um=result.geometric_rms*1e6, collisions=sorted(collisions),
                    collision_scope="当前指令的 1 条主光线 + 8 条瞳边缘采样线；镜背板、侧轴、电机、编码器、基板与支承；不含连续束体、透镜压圈厚度、安装公差、外壳与线缆")


def create_real_four_plus_one():
    rng = np.random.default_rng(2026)
    return FourPlusOneModel(MachineErrors(position_offsets=rng.normal(0,8e-6,(4,3)),
                                         axis_tilts=rng.normal(0,50e-6,(4,3)),
                                         zero_offsets=rng.normal(0,30e-6,4),
                                         focal_scale=1.0002, focal_offset=8e-6))
