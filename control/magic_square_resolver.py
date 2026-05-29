"""Domain resolver for magic square solve use-case (FR-02~FR-05)."""

from __future__ import annotations

from control.application_contracts import ApplicationError
from control.solver_error_mapper import SolverErrorMapper
from entity.services.exceptions import SolverNoSolutionError
from entity.services.solver import Solver


class MagicSquareDomainResolver:
    """Runs the Solver pipeline after Boundary validation succeeds."""

    def __init__(
        self,
        solver: Solver | None = None,
        error_mapper: SolverErrorMapper | None = None,
    ) -> None:
        """Initialize with optional injected solver and error mapper for testing."""
        self._solver = solver or Solver()
        self._error_mapper = error_mapper or SolverErrorMapper()

    def resolve(self, grid: list[list[int]]) -> list[int] | ApplicationError:
        """Attempt small-first then reverse solve on a validated grid.

        Args:
            grid: FR-01-validated 4x4 integer matrix.

        Returns:
            int[6] success payload or structured solver failure response.
        """
        try:
            return self._solver.solve(grid)
        except SolverNoSolutionError as error:
            return self._error_mapper.from_solver_no_solution(error)
