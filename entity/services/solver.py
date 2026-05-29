"""Two-combination solver for 4x4 magic squares (FR-05)."""

from __future__ import annotations


class Solver:
    """Attempts small-first then reverse number placement on blank cells."""

    def solve(self, grid: list[list[int]]) -> list[int]:
        """Solve blanks and return internal result for formatting.

        Args:
            grid: Validated 4x4 matrix with two blank cells.

        Returns:
            Internal solve payload (formatted to int[6] at Boundary).

        Raises:
            NotImplementedError: RED stub — implementation pending GREEN phase.
        """
        _ = grid
        raise NotImplementedError("RED: Solver.solve not implemented")
