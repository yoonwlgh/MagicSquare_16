"""Two-combination solver for 4x4 magic squares (FR-05)."""

from __future__ import annotations

from copy import deepcopy

from entity.services.blank_finder import BlankFinder
from entity.services.exceptions import SolverNoSolutionError
from entity.services.magic_square_validator import MagicSquareValidator
from entity.services.missing_number_finder import MissingNumberFinder


class Solver:
    """Attempts small-first then reverse number placement on blank cells."""

    def __init__(
        self,
        blank_finder: BlankFinder | None = None,
        missing_finder: MissingNumberFinder | None = None,
        validator: MagicSquareValidator | None = None,
    ) -> None:
        """Initialize with optional collaborators for testing."""
        self._blank_finder = blank_finder or BlankFinder()
        self._missing_finder = missing_finder or MissingNumberFinder()
        self._validator = validator or MagicSquareValidator()

    def solve(self, grid: list[list[int]]) -> list[int]:
        """Solve blanks and return int[6] success payload (1-index coordinates).

        Args:
            grid: Validated 4x4 matrix with two blank cells.

        Returns:
            ``[r1, c1, n1, r2, c2, n2]`` with 1-indexed coordinates.

        Raises:
            SolverNoSolutionError: When neither attempt produces a magic square.
        """
        blanks = self._blank_finder.find_blanks(grid)
        if len(blanks) != 2:
            raise SolverNoSolutionError("Expected exactly two blank cells.")

        missing = self._missing_finder.find_missing(grid)
        if len(missing) != 2:
            raise SolverNoSolutionError("Expected exactly two missing numbers.")

        small, large = missing[0], missing[1]
        (row1, col1), (row2, col2) = blanks

        small_first = self._attempt(grid, blanks, small, large)
        if small_first is not None:
            return [
                row1 + 1,
                col1 + 1,
                small,
                row2 + 1,
                col2 + 1,
                large,
            ]

        reverse = self._attempt(grid, blanks, large, small)
        if reverse is not None:
            return [
                row1 + 1,
                col1 + 1,
                large,
                row2 + 1,
                col2 + 1,
                small,
            ]

        raise SolverNoSolutionError("No valid magic square combination found.")

    def _attempt(
        self,
        grid: list[list[int]],
        blanks: list[tuple[int, int]],
        first_value: int,
        second_value: int,
    ) -> list[list[int]] | None:
        """Place values on blanks and validate; return filled grid or None."""
        candidate = deepcopy(grid)
        (row1, col1), (row2, col2) = blanks
        candidate[row1][col1] = first_value
        candidate[row2][col2] = second_value
        if self._validator.is_valid(candidate):
            return candidate
        return None
