"""Control layer unit tests for MagicSquareControl orchestration."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from boundary.magic_square.boundary_validator import BoundaryValidator
from boundary.magic_square.contracts import (
    ERR_INVALID_BLANK_COUNT_CODE,
    ErrorResponse,
)
from control.magic_square_control import MagicSquareControl
from tests.conftest import grid_g3_reverse_success, grid_three_blanks

AC_DOCSTRING = "Control — MagicSquareControl.solve validate-then-resolve orchestration."


class TestMagicSquareControlValidationFailure:
    """A-1 — validation failure must not invoke Domain resolver."""

    def test_solve_validation_failure_returns_error_without_resolver(
        self,
    ) -> None:
        """A-1 — invalid blank count: ErrorResponse and resolver.call_count == 0."""
        # Given
        validator = BoundaryValidator()
        resolver = MagicMock()
        control = MagicSquareControl(boundary_validator=validator, resolver=resolver)
        grid = grid_three_blanks()

        # When
        result = control.solve(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == ERR_INVALID_BLANK_COUNT_CODE
        assert resolver.resolve.call_count == 0


class TestMagicSquareControlValidationSuccess:
    """A-1 — validation success delegates to resolver once."""

    def test_solve_validation_success_invokes_resolver_once(
        self,
    ) -> None:
        """A-1 — valid grid: resolver.resolve called exactly once with same grid."""
        # Given
        validator = BoundaryValidator()
        resolver = MagicMock()
        resolver.resolve.return_value = [3, 3, 7, 4, 4, 1]
        control = MagicSquareControl(boundary_validator=validator, resolver=resolver)
        grid = grid_g3_reverse_success()

        # When
        result = control.solve(grid)

        # Then
        assert result == [3, 3, 7, 4, 4, 1]
        resolver.resolve.assert_called_once_with(grid)
