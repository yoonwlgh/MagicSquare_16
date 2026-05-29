"""Application-layer contracts for magic square use-cases (Control ports)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

BOUNDARY_LAYER = "Boundary"
CONTROL_LAYER = "Control"

ERR_SOLVER_NO_SOLUTION_CODE = "ERR_SOLVER_NO_SOLUTION"
ERR_SOLVER_NO_SOLUTION_MESSAGE = "No valid magic square combination found."


class ApplicationError(BaseModel):
    """Structured failure response from Control or Boundary adapters."""

    model_config = ConfigDict(frozen=True)

    code: str
    message: str
    layer: str = BOUNDARY_LAYER
