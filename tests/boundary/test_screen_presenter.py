"""Boundary tests for MagicSquareScreenPresenter (REFACTOR A-6)."""

from __future__ import annotations

from unittest.mock import MagicMock

from boundary.magic_square.contracts import (
    ERR_INVALID_SHAPE_CODE,
    ERR_INVALID_SHAPE_MESSAGE,
    ErrorResponse,
)
from boundary.result_formatter import ResultFormatter
from boundary.screen.presenter import MagicSquareScreenPresenter
from boundary.screen.view_formatter import ViewFormatter
from control.application_contracts import (
    CONTROL_LAYER,
    ERR_SOLVER_NO_SOLUTION_CODE,
    ERR_SOLVER_NO_SOLUTION_MESSAGE,
    ApplicationError,
)
from control.magic_square_control import MagicSquareControl
from tests.conftest import grid_g3_reverse_success

AC_DOCSTRING = "A-6 — Presenter delegates validate/solve and formats UI strings."


class TestPresenterValidateDelegation:
    """A-6 — validate() forwards to the boundary validator."""

    def test_validate_delegates_to_boundary_validator(self) -> None:
        """A-6 — validator.validate called with the same grid."""
        # Given
        validator = MagicMock()
        validator.validate.return_value = None
        presenter = MagicSquareScreenPresenter(boundary_validator=validator)
        grid = grid_g3_reverse_success()

        # When
        result = presenter.validate(grid)

        # Then
        assert result is None
        validator.validate.assert_called_once_with(grid)

    def test_validate_returns_validator_error_response(self) -> None:
        """A-6 — validator failure is passed through unchanged."""
        # Given
        expected = ErrorResponse(
            code=ERR_INVALID_SHAPE_CODE,
            message=ERR_INVALID_SHAPE_MESSAGE,
        )
        validator = MagicMock()
        validator.validate.return_value = expected
        presenter = MagicSquareScreenPresenter(boundary_validator=validator)

        # When
        result = presenter.validate(None)

        # Then
        assert result is expected


class TestPresenterSolveDelegation:
    """A-6 — solve() forwards to MagicSquareControl."""

    def test_solve_delegates_to_control(self) -> None:
        """A-6 — control.solve called with the same grid."""
        # Given
        control = MagicMock(spec=MagicSquareControl)
        expected = [3, 3, 7, 4, 4, 1]
        control.solve.return_value = expected
        presenter = MagicSquareScreenPresenter(control=control)
        grid = grid_g3_reverse_success()

        # When
        result = presenter.solve(grid)

        # Then
        assert result == expected
        control.solve.assert_called_once_with(grid)

    def test_solve_returns_control_application_error(self) -> None:
        """A-6 — control-layer solver failure is passed through."""
        # Given
        expected = ApplicationError(
            code=ERR_SOLVER_NO_SOLUTION_CODE,
            message=ERR_SOLVER_NO_SOLUTION_MESSAGE,
            layer=CONTROL_LAYER,
        )
        control = MagicMock(spec=MagicSquareControl)
        control.solve.return_value = expected
        presenter = MagicSquareScreenPresenter(control=control)

        # When
        result = presenter.solve(grid_g3_reverse_success())

        # Then
        assert result is expected


class TestPresenterFormatSuccess:
    """A-6 — format_success() delegates to ResultFormatter."""

    def test_format_success_delegates_to_result_formatter(self) -> None:
        """A-6 — formatter.to_int6 called with solver payload."""
        # Given
        formatter = MagicMock(spec=ResultFormatter)
        payload = [3, 3, 7, 4, 4, 1]
        formatter.to_int6.return_value = payload
        presenter = MagicSquareScreenPresenter(formatter=formatter)

        # When
        result = presenter.format_success(payload)

        # Then
        assert result == payload
        formatter.to_int6.assert_called_once_with(payload)


class TestPresenterViewFormatting:
    """A-6 — format_error / format_success_message delegate to ViewFormatter."""

    def test_format_error_delegates_to_view_formatter(self) -> None:
        """A-6 — boundary error rendered as code: message."""
        # Given
        view_formatter = MagicMock(spec=ViewFormatter)
        view_formatter.format_error.return_value = "ERR_INVALID_SHAPE: shape"
        presenter = MagicSquareScreenPresenter(view_formatter=view_formatter)
        error = ErrorResponse(
            code=ERR_INVALID_SHAPE_CODE,
            message=ERR_INVALID_SHAPE_MESSAGE,
        )

        # When
        result = presenter.format_error(error)

        # Then
        assert result == "ERR_INVALID_SHAPE: shape"
        view_formatter.format_error.assert_called_once_with(error)

    def test_format_success_message_delegates_to_view_formatter(self) -> None:
        """A-6 — success int[6] rendered for the UI."""
        # Given
        view_formatter = MagicMock(spec=ViewFormatter)
        int6 = [3, 3, 7, 4, 4, 1]
        view_formatter.format_success_message.return_value = f"Success: {int6}"
        presenter = MagicSquareScreenPresenter(view_formatter=view_formatter)

        # When
        result = presenter.format_success_message(int6)

        # Then
        assert result == f"Success: {int6}"
        view_formatter.format_success_message.assert_called_once_with(int6)

    def test_format_error_with_real_view_formatter(self) -> None:
        """A-6 — default ViewFormatter produces code: message string."""
        # Given
        presenter = MagicSquareScreenPresenter(view_formatter=ViewFormatter())
        error = ApplicationError(
            code=ERR_SOLVER_NO_SOLUTION_CODE,
            message=ERR_SOLVER_NO_SOLUTION_MESSAGE,
            layer=CONTROL_LAYER,
        )

        # When
        result = presenter.format_error(error)

        # Then
        assert result == (
            f"{ERR_SOLVER_NO_SOLUTION_CODE}: {ERR_SOLVER_NO_SOLUTION_MESSAGE}"
        )
