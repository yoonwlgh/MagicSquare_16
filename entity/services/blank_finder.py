"""Blank cell coordinate discovery (FR-02)."""

from __future__ import annotations


class BlankFinder:
    """Finds exactly two blank (0) cells in row-major order."""

    def find_blanks(self, grid: list[list[int]]) -> list[tuple[int, int]]:
        """Return two (row, col) coordinates for blank cells.

        Args:
            grid: Validated 4x4 integer matrix with exactly two zeros.

        Returns:
            List of two zero-index (row, col) pairs in row-major order.

        Raises:
            NotImplementedError: RED stub — implementation pending GREEN phase.
        """
        _ = grid
        raise NotImplementedError("RED: BlankFinder.find_blanks not implemented")
