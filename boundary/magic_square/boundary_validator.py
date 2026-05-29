"""Boundary input validator for 4x4 magic square grids (FR-01)."""

from boundary.magic_square.contracts import (
    GRID_SIZE,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    ErrorResponse,
)


class BoundaryValidator:
    """Validates grid shape before Control invokes Domain resolve()."""

    def validate(self, grid: list[list[int]] | None) -> ErrorResponse | None:
        """Return ErrorResponse on shape failure; None when validation passes.

        GREEN (AC-FR-01-01): None and non-4x4 shape (I-1); blank/range/duplicate RED.
        """
        if grid is None or not self._is_4x4_shape(grid):
            return ErrorResponse(
                code=INVALID_SIZE_CODE,
                message=INVALID_SIZE_MESSAGE,
            )
        return None

    @staticmethod
    def _is_4x4_shape(grid: list[list[int]]) -> bool:
        """True when grid has exactly GRID_SIZE rows and GRID_SIZE columns per row."""
        if len(grid) != GRID_SIZE:
            return False
        return all(len(row) == GRID_SIZE for row in grid)
