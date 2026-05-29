"""Missing number discovery for magic square grids (FR-03)."""

from __future__ import annotations

from entity.services.constants import (
    BLANK_CELL_VALUE,
    MAX_CELL_VALUE,
    MIN_CELL_VALUE,
)


class MissingNumberFinder:
    """Computes the two missing values from {1..16} excluding zeros."""

    def find_missing(self, grid: list[list[int]]) -> list[int]:
        """Return missing numbers as [small, large] in ascending order.

        Args:
            grid: Validated 4x4 integer matrix.

        Returns:
            Two missing integers with small < large.
        """
        present = {
            value
            for row in grid
            for value in row
            if value != BLANK_CELL_VALUE
        }
        missing = [
            value
            for value in range(MIN_CELL_VALUE, MAX_CELL_VALUE + 1)
            if value not in present
        ]
        return missing
