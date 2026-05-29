"""Presenter bridging PyQt screen and ECB control/boundary layers."""

from __future__ import annotations

from boundary.magic_square.boundary_validator import BoundaryValidator
from boundary.magic_square.contracts import ErrorResponse
from boundary.result_formatter import ResultFormatter
from boundary.screen.view_formatter import ViewFormatter
from control.application_contracts import ApplicationError
from control.magic_square_control import MagicSquareControl
from control.magic_square_resolver import MagicSquareDomainResolver


class MagicSquareScreenPresenter:
    """Coordinates validation and solve for the desktop UI."""

    def __init__(
        self,
        boundary_validator: BoundaryValidator | None = None,
        control: MagicSquareControl | None = None,
        formatter: ResultFormatter | None = None,
        view_formatter: ViewFormatter | None = None,
    ) -> None:
        """Initialize with optional dependencies for testing."""
        validator = boundary_validator or BoundaryValidator()
        self._validator = validator
        self._control = control or MagicSquareControl(
            boundary_validator=validator,
            resolver=MagicSquareDomainResolver(),
        )
        self._formatter = formatter or ResultFormatter()
        self._view_formatter = view_formatter or ViewFormatter()

    def validate(self, grid: list[list[int]] | None) -> ErrorResponse | None:
        """Run FR-01 boundary validation only."""
        return self._validator.validate(grid)

    def solve(
        self, grid: list[list[int]] | None
    ) -> ApplicationError | ErrorResponse | list[int]:
        """Validate at boundary then run domain solver when valid."""
        return self._control.solve(grid)

    def format_success(self, payload: list[int]) -> list[int]:
        """Normalize solver output to PRD int[6] contract."""
        return self._formatter.to_int6(payload)

    def format_error(self, response: ErrorResponse | ApplicationError) -> str:
        """Render structured failure for the UI."""
        return self._view_formatter.format_error(response)

    def format_success_message(self, result: list[int]) -> str:
        """Render success int[6] for the UI."""
        return self._view_formatter.format_success_message(result)
