"""Boundary contracts for magic square validation (FR-01)."""

from pydantic import BaseModel, ConfigDict

# PRD §8.1 / test_plan sample contract (OPEN-01: map to ERR_INVALID_SHAPE later).
GRID_SIZE = 4
BLANK_CELL_VALUE = 0
REQUIRED_BLANK_COUNT = 2
MIN_CELL_VALUE = 1
MAX_CELL_VALUE = 16

INVALID_SIZE_CODE = "INVALID_SIZE"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."

ERR_INVALID_BLANK_COUNT_CODE = "ERR_INVALID_BLANK_COUNT"
ERR_INVALID_BLANK_COUNT_MESSAGE = (
    "Input must contain exactly 2 blank cells (0)."
)

ERR_OUT_OF_RANGE_CODE = "ERR_OUT_OF_RANGE"
ERR_OUT_OF_RANGE_MESSAGE = "Cell values must be 0 or 1..16."

ERR_DUPLICATE_VALUE_CODE = "ERR_DUPLICATE_VALUE"
ERR_DUPLICATE_VALUE_MESSAGE = "Non-zero values must be unique."

ERR_SOLVER_NO_SOLUTION_CODE = "ERR_SOLVER_NO_SOLUTION"
ERR_SOLVER_NO_SOLUTION_MESSAGE = "No valid magic square combination found."

BOUNDARY_LAYER = "Boundary"
CONTROL_LAYER = "Control"

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
