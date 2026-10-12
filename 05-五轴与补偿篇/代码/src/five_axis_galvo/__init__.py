"""Five-axis galvanometer digital twin."""

from .compensation import PolynomialCompensator
from .kinematics import InverseKinematicsResult, inverse_kinematics, numerical_jacobian
from .model import ForwardResult, MachineModel, create_default_machine
from .optics import EquivalentObjectiveResult, predicted_gaussian_focus_diameter
from .specifications import OpticalSpecifications, STANDARD_515_NM

__all__ = [
    "ForwardResult",
    "InverseKinematicsResult",
    "MachineModel",
    "EquivalentObjectiveResult",
    "OpticalSpecifications",
    "PolynomialCompensator",
    "STANDARD_515_NM",
    "create_default_machine",
    "inverse_kinematics",
    "numerical_jacobian",
    "predicted_gaussian_focus_diameter",
]
