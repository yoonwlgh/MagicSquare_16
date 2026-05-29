"""Boundary contracts for magic square validation (FR-01)."""

from control.application_contracts import (
    ApplicationError,
    BOUNDARY_LAYER,
    CONTROL_LAYER,
    ERR_SOLVER_NO_SOLUTION_CODE,
    ERR_SOLVER_NO_SOLUTION_MESSAGE,
)

# Backward-compatible alias; canonical DTO lives in control.application_contracts.
ErrorResponse = ApplicationError

from entity.services.constants import (
    BLANK_CELL_VALUE,
    GRID_SIZE,
    MAX_CELL_VALUE,
    MIN_CELL_VALUE,
    REQUIRED_BLANK_COUNT,
)

ERR_INVALID_SHAPE_CODE = "ERR_INVALID_SHAPE"
ERR_INVALID_SHAPE_MESSAGE = "Input must be a 4x4 integer matrix."

ERR_INVALID_BLANK_COUNT_CODE = "ERR_INVALID_BLANK_COUNT"
ERR_INVALID_BLANK_COUNT_MESSAGE = (
    "Input must contain exactly 2 blank cells (0)."
)

ERR_OUT_OF_RANGE_CODE = "ERR_OUT_OF_RANGE"
ERR_OUT_OF_RANGE_MESSAGE = "Cell values must be 0 or 1..16."

ERR_DUPLICATE_VALUE_CODE = "ERR_DUPLICATE_VALUE"
ERR_DUPLICATE_VALUE_MESSAGE = "Non-zero values must be unique."

FORBIDDEN_OUT_OF_SCOPE_ERROR_CODES = frozenset(
    {
        "ERR_INVALID_BLANK_COUNT",
        "ERR_OUT_OF_RANGE",
        "ERR_DUPLICATE_VALUE",
        "ERR_SOLVER_NO_SOLUTION",
        "ERR_INVALID_SHAPE",
    }
)
