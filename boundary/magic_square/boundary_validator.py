"""Boundary input validator for 4x4 magic square grids (FR-01)."""

from boundary.magic_square.contracts import (
    BLANK_CELL_VALUE,
    ERR_DUPLICATE_VALUE_CODE,
    ERR_DUPLICATE_VALUE_MESSAGE,
    ERR_INVALID_BLANK_COUNT_CODE,
    ERR_INVALID_BLANK_COUNT_MESSAGE,
    ERR_INVALID_SHAPE_CODE,
    ERR_INVALID_SHAPE_MESSAGE,
    ERR_OUT_OF_RANGE_CODE,
    ERR_OUT_OF_RANGE_MESSAGE,
    GRID_SIZE,
    MAX_CELL_VALUE,
    MIN_CELL_VALUE,
    REQUIRED_BLANK_COUNT,
    ErrorResponse,
)


class BoundaryValidator:
    """Validates grid shape before Control invokes Domain resolve()."""

    def validate(self, grid: list[list[int]] | None) -> ErrorResponse | None:
        """Return ErrorResponse on failure; None when validation passes.

        GREEN (AC-FR-01-01~04): shape, blank count, range, duplicate checks.
        """
        shape_error = self._validate_shape(grid)
        if shape_error is not None:
            return shape_error

        blank_error = self._validate_blank_count(grid)
        if blank_error is not None:
            return blank_error

        return self._validate_values(grid)

    def _validate_shape(self, grid: list[list[int]] | None) -> ErrorResponse | None:
        """Return shape failure when grid is not a 4x4 matrix."""
        if grid is None or not self._is_4x4_shape(grid):
            return ErrorResponse(
                code=ERR_INVALID_SHAPE_CODE,
                message=ERR_INVALID_SHAPE_MESSAGE,
            )
        return None

    def _validate_blank_count(self, grid: list[list[int]]) -> ErrorResponse | None:
        """Return failure when blank cell count is not exactly two."""
        blank_count = sum(
            1 for row in grid for value in row if value == BLANK_CELL_VALUE
        )
        if blank_count != REQUIRED_BLANK_COUNT:
            return ErrorResponse(
                code=ERR_INVALID_BLANK_COUNT_CODE,
                message=ERR_INVALID_BLANK_COUNT_MESSAGE,
            )
        return None

    def _validate_values(self, grid: list[list[int]]) -> ErrorResponse | None:
        """Return failure on out-of-range or duplicate non-zero cell values."""
        seen_non_zero: set[int] = set()
        for row in grid:
            for value in row:
                if value == BLANK_CELL_VALUE:
                    continue
                if value < MIN_CELL_VALUE or value > MAX_CELL_VALUE:
                    return ErrorResponse(
                        code=ERR_OUT_OF_RANGE_CODE,
                        message=ERR_OUT_OF_RANGE_MESSAGE,
                    )
                if value in seen_non_zero:
                    return ErrorResponse(
                        code=ERR_DUPLICATE_VALUE_CODE,
                        message=ERR_DUPLICATE_VALUE_MESSAGE,
                    )
                seen_non_zero.add(value)
        return None

    @staticmethod
    def _is_4x4_shape(grid: list[list[int]]) -> bool:
        """True when grid has exactly GRID_SIZE rows and GRID_SIZE columns per row."""
        if len(grid) != GRID_SIZE:
            return False
        return all(len(row) == GRID_SIZE for row in grid)
