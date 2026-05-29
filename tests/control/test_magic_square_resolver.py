"""Control layer unit tests for MagicSquareDomainResolver."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from boundary.magic_square.contracts import (
    CONTROL_LAYER,
    ERR_SOLVER_NO_SOLUTION_CODE,
    ERR_SOLVER_NO_SOLUTION_MESSAGE,
    ErrorResponse,
)
from control.magic_square_resolver import MagicSquareDomainResolver
from entity.services.exceptions import SolverNoSolutionError
from tests.conftest import grid_g3_reverse_success, grid_no_solution

AC_DOCSTRING = "Control — MagicSquareDomainResolver maps Solver outcomes to contracts."


class TestMagicSquareDomainResolverSuccess:
    """A-2 — solver success returns int[6] payload."""

    def test_resolve_returns_solver_success_payload(self) -> None:
        """A-2 — mock solver success passthrough."""
        # Given
        solver = MagicMock()
        expected = [3, 3, 7, 4, 4, 1]
        solver.solve.return_value = expected
        resolver = MagicSquareDomainResolver(solver=solver)
        grid = grid_g3_reverse_success()

        # When
        result = resolver.resolve(grid)

        # Then
        assert result == expected
        solver.solve.assert_called_once_with(grid)


class TestMagicSquareDomainResolverNoSolution:
    """A-2 — SolverNoSolutionError maps to Control-layer ErrorResponse."""

    def test_resolve_maps_solver_no_solution_to_control_error(self) -> None:
        """A-2 — SolverNoSolutionError → ERR_SOLVER_NO_SOLUTION / Control layer."""
        # Given
        solver = MagicMock()
        solver.solve.side_effect = SolverNoSolutionError("No valid magic square combination found.")
        resolver = MagicSquareDomainResolver(solver=solver)
        grid = grid_no_solution()

        # When
        result = resolver.resolve(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == ERR_SOLVER_NO_SOLUTION_CODE
        assert result.message == ERR_SOLVER_NO_SOLUTION_MESSAGE
        assert result.layer == CONTROL_LAYER
