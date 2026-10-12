from dataclasses import asdict

import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .calibration import generate_calibration_data
from .compensation import PolynomialCompensator
from .four_plus_one import FourPlusOneModel, create_real_four_plus_one
from .kinematics import inverse_kinematics, numerical_jacobian, pose_residual
from .verification import verify_compensation

router = APIRouter(prefix="/api/4p1")
ideal = FourPlusOneModel()
real = create_real_four_plus_one()
compensator = PolynomialCompensator()


class Command(BaseModel):
    q: list[float] = Field(min_length=5, max_length=5)


class TargetPose(BaseModel):
    pose: list[float] = Field(min_length=5, max_length=5, description="工件 XYZ (m)，αβ (rad)")


def _pose_error(actual, target):
    delta = pose_residual(actual, target)
    return dict(position_um=(delta[:3]*1e6).tolist(), angles_urad=(delta[3:]*1e6).tolist(),
                norm_um=float(np.linalg.norm(delta[:3])*1e6))


def _inverse_branch(machine, target, *, calibration=None, initial=None):
    try:
        solution = (calibration.solve_command(machine, target, initial_command=initial)
                    if calibration is not None else inverse_kinematics(machine, target, initial_command=initial))
        if not solution.success:
            return dict(success=False, command=None, payload=None,
                        message="目标不可达或逆解未收敛：检查机械行程、角度组合和光学口径", iterations=solution.iterations)
        command = solution.command.tolist()
        payload = real.payload(command)
        if payload["collisions"]:
            return dict(success=False, command=None, payload=None,
                        message="逆解存在遮挡：" + "、".join(payload["collisions"]), iterations=solution.iterations)
        return dict(success=True, command=command, payload=payload,
                    errors=_pose_error(payload["pose"], target), iterations=solution.iterations,
                    message="逆解收敛；指令仅作用于仿真模型，未连接实机")
    except (ValueError, RuntimeError) as exc:
        return dict(success=False, command=None, payload=None, message=f"逆解失败：{exc}", iterations=0)


@router.post("/inverse")
def inverse(request: TargetPose):
    target = np.asarray(request.pose, dtype=float)
    if not np.all(np.isfinite(target)):
        raise HTTPException(422, "XYZαβ 必须是有限数值")
    if np.any(np.abs(target[3:]) > np.deg2rad(7.5)) or not ideal.is_pose_within_workspace(target):
        raise HTTPException(422, "目标超出工作域：XY 半径 ≤2.5 mm、Z ±1 mm、合成 AOI ≤7.5°；αβ 不是 AOI/RotZ")
    candidate = compensator
    baseline = _inverse_branch(ideal, target)
    seed = baseline["command"]
    truth = _inverse_branch(real, target, initial=seed)
    calibrated = (_inverse_branch(ideal, target, calibration=candidate, initial=seed)
                  if candidate.fitted else dict(success=False, command=None, payload=None,
                                               message="尚未标定，请先训练 4+1 仿真补偿", iterations=0))
    target_payload = ideal.payload(seed) if baseline["success"] else None
    return dict(mode="inverse", requested_pose=target.tolist(), branches=dict(baseline=baseline,truth=truth,calibrated=calibrated),
                target=target_payload, before=baseline["payload"], after=calibrated["payload"], truth=truth["payload"],
                errors_before=baseline.get("errors"), errors_after=calibrated.get("errors"),
                corrected_command=calibrated["command"], fitted=candidate.fitted, in_workspace=True,
                message="误差均相对手动输入的目标。真实模型直接逆解是已知误差的仿真参考；校准逆解只使用拟合补偿模型。")


@router.get("/configuration")
def configuration():
    return dict(lower=ideal.lower_bounds.tolist(), upper=ideal.upper_bounds.tolist(),
                work_origin=ideal.work_origin.tolist(), envelope_mm=[310,264,271],
                jacobian_rank=int(np.linalg.matrix_rank(numerical_jacobian(ideal, np.zeros(5)))),
                prescription="假设处方：L1 −20 mm / L2 +60 mm / 间距 40 mm / 物镜 +75 mm；名义扩束 3×",
                reference="https://www.scanlab.de/en/products/z-axes-3d-add-ons/varioscan-ii")


@router.post("/compare")
def compare(request: Command):
    try:
        target, before = ideal.payload(request.q), real.payload(request.q)
        after, corrected = None, None
        candidate = compensator
        valid = ideal.is_pose_within_workspace(target["pose"])
        message = "同一套 4+1 结构、追迹与补偿模型；请先训练仿真补偿"
        if not valid:
            message = "超出目标工作域（XY 半径 2.5 mm / Z ±1 mm / AOI 7.5°），不执行补偿"
        elif candidate.fitted:
            solution = candidate.solve_command(ideal, target["pose"], initial_command=request.q)
            if solution.success:
                corrected = solution.command.tolist()
                after = real.payload(corrected)
                message = "仿真补偿已应用；第五个指令是镜片机械位移，不是焦距或第五面振镜角度"
            else:
                message = "补偿逆解未收敛，不显示补偿后结果"
        def error(payload):
            delta = pose_residual(payload["pose"], target["pose"])
            return dict(position_um=(delta[:3]*1e6).tolist(), angles_urad=(delta[3:]*1e6).tolist(),
                        norm_um=float(np.linalg.norm(delta[:3])*1e6))
        return dict(target=target,before=before,after=after,corrected_command=corrected,
                    errors_before=error(before),errors_after=error(after) if after else None,
                    message=message,in_workspace=valid,fitted=candidate.fitted)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@router.post("/calibrate")
def calibrate():
    global compensator
    try:
        data = generate_calibration_data(ideal, real, sample_count=400, seed=42)
        candidate = PolynomialCompensator().fit(data)
        commands = generate_calibration_data(ideal, real, sample_count=80, seed=43).commands
        metrics = verify_compensation(ideal, real, candidate, commands)
        compensator = candidate
        return asdict(metrics) | dict(requested_validation_samples=80,failed_validation_samples=80-metrics.sample_count)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(422, str(exc)) from exc
