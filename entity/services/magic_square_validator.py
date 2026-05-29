"""Magic square invariant validation (FR-04)."""

from __future__ import annotations

from entity.services.constants import GRID_SIZE, MAGIC_CONSTANT


class MagicSquareValidator:
    """Checks row, column, and diagonal sums against the magic constant."""

    def is_valid(self, grid: list[list[int]]) -> bool:
        """Return True only when all magic-square line sums match.

        Args:
            grid: Filled 4x4 integer matrix.

        Returns:
            True if the grid satisfies magic-square rules.
        """
        for row in range(GRID_SIZE):
            if sum(grid[row][col] for col in range(GRID_SIZE)) != MAGIC_CONSTANT:
                return False

        for col in range(GRID_SIZE):
            if sum(grid[row][col] for row in range(GRID_SIZE)) != MAGIC_CONSTANT:
                return False

        if sum(grid[index][index] for index in range(GRID_SIZE)) != MAGIC_CONSTANT:
            return False

        if (
            sum(grid[index][GRID_SIZE - 1 - index] for index in range(GRID_SIZE))
            != MAGIC_CONSTANT
        ):
            return False

        return True
