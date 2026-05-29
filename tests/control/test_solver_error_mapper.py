"""Unit tests for SolverErrorMapper (REFACTOR C-1a)."""

from __future__ import annotations

from control.application_contracts import (
    CONTROL_LAYER,
    ERR_SOLVER_NO_SOLUTION_CODE,
    ERR_SOLVER_NO_SOLUTION_MESSAGE,
    ApplicationError,
)
from control.solver_error_mapper import SolverErrorMapper
from entity.services.exceptions import SolverNoSolutionError


class TestSolverErrorMapper:
    """C-1a — domain solver failures map to application error contracts."""

    def test_from_solver_no_solution_returns_control_layer_error(self) -> None:
        """C-1a — SolverNoSolutionError → ERR_SOLVER_NO_SOLUTION / Control layer."""
        # Given
        mapper = SolverErrorMapper()
        error = SolverNoSolutionError("No valid magic square combination found.")

        # When
        result = mapper.from_solver_no_solution(error)

        # Then
        assert isinstance(result, ApplicationError)
        assert result.code == ERR_SOLVER_NO_SOLUTION_CODE
        assert result.message == ERR_SOLVER_NO_SOLUTION_MESSAGE
        assert result.layer == CONTROL_LAYER
