"""Boundary contracts for magic square validation (FR-01)."""

from pydantic import BaseModel, ConfigDict

# PRD §8.1 / test_plan sample contract (OPEN-01: map to ERR_INVALID_SHAPE later).
GRID_SIZE = 4
INVALID_SIZE_CODE = "INVALID_SIZE"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."
BOUNDARY_LAYER = "Boundary"

FORBIDDEN_OUT_OF_SCOPE_ERROR_CODES = frozenset(
    {
        "ERR_INVALID_BLANK_COUNT",
        "ERR_OUT_OF_RANGE",
        "ERR_DUPLICATE_VALUE",
        "ERR_SOLVER_NO_SOLUTION",
        "ERR_INVALID_SHAPE",
    }
)


class ErrorResponse(BaseModel):
    """Structured failure response from Boundary validation."""

    model_config = ConfigDict(frozen=True)

    code: str
    message: str
    layer: str = BOUNDARY_LAYER
