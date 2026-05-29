"""Domain resolver for magic square solve use-case (FR-02~FR-05)."""

from __future__ import annotations

from boundary.magic_square.contracts import (
    CONTROL_LAYER,
    ERR_SOLVER_NO_SOLUTION_CODE,
    ERR_SOLVER_NO_SOLUTION_MESSAGE,
    ErrorResponse,
)
from entity.services.exceptions import SolverNoSolutionError
from entity.services.solver import Solver


class MagicSquareDomainResolver:
    """Runs the Solver pipeline after Boundary validation succeeds."""

    def __init__(self, solver: Solver | None = None) -> None:
        """Initialize with optional injected solver for testing."""
        self._solver = solver or Solver()

    def resolve(self, grid: list[list[int]]) -> list[int] | ErrorResponse:
        """Attempt small-first then reverse solve on a validated grid.

        Args:
            grid: FR-01-validated 4x4 integer matrix.

        Returns:
            int[6] success payload or structured solver failure response.
        """
        try:
            return self._solver.solve(grid)
        except SolverNoSolutionError:
            return ErrorResponse(
                code=ERR_SOLVER_NO_SOLUTION_CODE,
                message=ERR_SOLVER_NO_SOLUTION_MESSAGE,
                layer=CONTROL_LAYER,
            )
