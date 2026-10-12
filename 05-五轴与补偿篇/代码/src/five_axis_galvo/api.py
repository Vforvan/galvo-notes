from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .calibration import generate_calibration_data
from .assembly import assembly_configuration, trace_assembly
from .compensation import PolynomialCompensator
from .geometry import GeometryError, normalize, rotate
from .kinematics import inverse_kinematics, pose_residual
from .model import MachineModel, create_default_machine, create_seeded_real_machine
from .readout import focus_readout
from .verification import verify_compensation
from .api_4p1 import router as four_plus_one_router


class CommandRequest(BaseModel):
    q: list[float] = Field(min_length=5, max_length=5)
    machine: str = "ideal"


class PoseRequest(BaseModel):
    pose: list[float] = Field(min_length=5, max_length=5)
    compensate: bool = False


class AssemblyTraceRequest(BaseModel):
    angles: list[float] = Field(min_length=5, max_length=5)


class CalibrationRequest(BaseModel):
    sample_count: int = Field(default=800, ge=50, le=10000)
    seed: int = 42


app = FastAPI(title="Five-Axis Galvanometer Digital Twin", version="0.1.0")
app.include_router(four_plus_one_router)
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
ideal_machine = create_default_machine()
real_machine = create_seeded_real_machine()
compensator = PolynomialCompensator()


def _model(name: str) -> MachineModel:
    if name == "ideal":
        return ideal_machine
    if name == "real":
        return real_machine
    raise HTTPException(status_code=400, detail="machine must be 'ideal' or 'real'")


def _forward_payload(machine: MachineModel, command: list[float]) -> dict[str, object]:
    result = machine.forward(command)
    objective = result.objective
    if objective is None:
        raise RuntimeError("Optical envelope was not generated")
    return {
        "command": list(command),
        "mirror_angles": (np.asarray(command[:4]) + machine.errors.zero_offsets).tolist(),
        "mirrors": [
            {
                "name": f"M{index + 1}",
                "center": (mirror.center + machine.errors.position_offsets[index]).tolist(),
                "normal": rotate(
                    mirror.normal,
                    normalize(mirror.rotation_axis + machine.errors.axis_tilts[index]),
                    command[index] + machine.errors.zero_offsets[index],
                ).tolist(),
                "axis": normalize(mirror.rotation_axis + machine.errors.axis_tilts[index]).tolist(),
                "radius": mirror.aperture_radius,
            }
            for index, mirror in enumerate(machine.mirrors)
        ],
        "entrance": {
            "center": (machine.source_origin + machine.source_direction * 0.005).tolist(),
            "axis": machine.source_direction.tolist(),
            "radius": machine.specifications.entrance_aperture_diameter_m / 2,
        },
        "pose": result.pose.tolist(),
        "readout": focus_readout(result.focus, result.direction, frame="equivalent_optical"),
        "direction": result.direction.tolist(),
        "intersections": [point.tolist() for point in result.intersections],
        "segments": [
            {"start": segment.start.tolist(), "end": segment.end.tolist()}
            for segment in result.segments
        ],
        "objective": {
            "center": objective.center.tolist(),
            "axis": objective.optical_axis.tolist(),
            "clear_aperture_radius": objective.clear_aperture_radius,
            "beam_radius": objective.beam_radius_at_objective,
            "focus_diameter": objective.waist_radius * 2.0,
            "predicted_focus_diameter": objective.predicted_focus_diameter,
            "rayleigh_range": objective.rayleigh_range,
            "aperture_utilization": objective.aperture_utilization,
            "envelope": [
                {"position": sample.position.tolist(), "radius": sample.radius}
                for sample in objective.samples
            ],
        },
    }


@app.get("/")
def index() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "index_4p1.html")


@app.get("/legacy")
def legacy_index() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get("/api/specifications")
def specifications() -> dict[str, float | str]:
    return ideal_machine.specifications.to_dict()


@app.post("/api/forward")
def forward(request: CommandRequest) -> dict[str, object]:
    try:
        return _forward_payload(_model(request.machine), request.q)
    except (ValueError, GeometryError) as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@app.get("/api/assembly")
def assembly() -> dict[str, object]:
    return assembly_configuration()


@app.post("/api/assembly/trace")
def assembly_trace(request: AssemblyTraceRequest) -> dict[str, object]:
    try:
        return trace_assembly(request.angles)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@app.post("/api/inverse")
def inverse(request: PoseRequest) -> dict[str, object]:
    try:
        if request.compensate:
            if not compensator.fitted:
                raise HTTPException(status_code=409, detail="Run calibration before compensation")
            result = compensator.solve_command(ideal_machine, request.pose)
        else:
            result = inverse_kinematics(ideal_machine, request.pose)
        actual = real_machine.forward(result.command).pose
        return {
            "success": result.success,
            "command": result.command.tolist(),
            "ideal_pose": result.achieved_pose.tolist(),
            "actual_pose": actual.tolist(),
            "residual": (actual - np.asarray(request.pose)).tolist(),
            "iterations": result.iterations,
            "message": result.message,
        }
    except (ValueError, GeometryError) as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@app.post("/api/compare")
def compare(request: CommandRequest) -> dict[str, object]:
    try:
        target = _forward_payload(ideal_machine, request.q)
        before = _forward_payload(real_machine, request.q)
        model = compensator
        in_workspace = ideal_machine.is_pose_within_workspace(target["pose"])
        after = None
        corrected_command = None
        message = "请先训练补偿模型"
        if not in_workspace:
            message = "当前目标超出标定工作域，补偿对比已停用；请复位或减小转角"
        elif model.fitted:
            solution = model.solve_command(
                ideal_machine, target["pose"], initial_command=request.q
            )
            if solution.success:
                try:
                    after = _forward_payload(real_machine, solution.command.tolist())
                    corrected_command = solution.command.tolist()
                    message = "同一目标的补偿前后对比（确定性仿真）"
                except ValueError as error:
                    message = f"补偿后光路无效：{error}"
            else:
                message = "补偿逆解未收敛，未显示补偿后结果"

        def errors(payload: dict[str, object]) -> dict[str, object]:
            delta = pose_residual(payload["pose"], target["pose"])
            return {
                "position_um": (delta[:3] * 1e6).tolist(),
                "angles_urad": (delta[3:] * 1e6).tolist(),
                "position_norm_um": float(np.linalg.norm(delta[:3]) * 1e6),
                "angle_norm_urad": float(np.linalg.norm(delta[3:]) * 1e6),
            }

        return {
            "target": target, "before": before, "after": after,
            "errors_before": errors(before),
            "errors_after": errors(after) if after is not None else None,
            "corrected_command": corrected_command,
            "fitted": model.fitted, "in_workspace": in_workspace,
            "message": message,
        }
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@app.post("/api/calibrate")
def calibrate(request: CalibrationRequest) -> dict[str, object]:
    global compensator
    data = generate_calibration_data(
        ideal_machine,
        real_machine,
        sample_count=request.sample_count,
        seed=request.seed,
    )
    candidate = PolynomialCompensator().fit(data)
    split = max(20, request.sample_count // 5)
    commands = generate_calibration_data(
        ideal_machine, real_machine, sample_count=split, seed=request.seed + 1
    ).commands
    metrics = verify_compensation(ideal_machine, real_machine, candidate, commands)
    compensator = candidate
    return asdict(metrics) | {
        "requested_validation_samples": split,
        "failed_validation_samples": split - metrics.sample_count,
        "position_improvement_percent": metrics.position_improvement_percent,
        "orientation_improvement_percent": metrics.orientation_improvement_percent,
    }


def main() -> None:
    import uvicorn

    uvicorn.run("five_axis_galvo.api:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()
