"""Missing number discovery for magic square grids (FR-03)."""

from __future__ import annotations


class MissingNumberFinder:
    """Computes the two missing values from {1..16} excluding zeros."""

    def find_missing(self, grid: list[list[int]]) -> list[int]:
        """Return missing numbers as [small, large] in ascending order.

        Args:
            grid: Validated 4x4 integer matrix.

        Returns:
            Two missing integers with small < large.

        Raises:
            NotImplementedError: RED stub — implementation pending GREEN phase.
        """
        _ = grid
        raise NotImplementedError(
            "RED: MissingNumberFinder.find_missing not implemented"
        )
