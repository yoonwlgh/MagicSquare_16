"""Blank cell coordinate discovery (FR-02)."""

from __future__ import annotations

from entity.services.constants import BLANK_CELL_VALUE, GRID_SIZE


class BlankFinder:
    """Finds exactly two blank (0) cells in row-major order."""

    def find_blanks(self, grid: list[list[int]]) -> list[tuple[int, int]]:
        """Return two (row, col) coordinates for blank cells.

        Args:
            grid: Validated 4x4 integer matrix with exactly two zeros.

        Returns:
            List of two zero-index (row, col) pairs in row-major order.
        """
        blanks: list[tuple[int, int]] = []
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if grid[row][col] == BLANK_CELL_VALUE:
                    blanks.append((row, col))
        return blanks
