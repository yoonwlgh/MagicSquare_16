"""Magic square invariant validation (FR-04)."""

from __future__ import annotations

from entity.services.constants import MAGIC_CONSTANT


class MagicSquareValidator:
    """Checks row, column, and diagonal sums against the magic constant."""

    def is_valid(self, grid: list[list[int]]) -> bool:
        """Return True only when all magic-square line sums match.

        Args:
            grid: Filled 4x4 integer matrix.

        Returns:
            True if the grid satisfies magic-square rules.

        Raises:
            NotImplementedError: RED stub — implementation pending GREEN phase.
        """
        _ = grid
        _ = MAGIC_CONSTANT
        raise NotImplementedError(
            "RED: MagicSquareValidator.is_valid not implemented"
        )
