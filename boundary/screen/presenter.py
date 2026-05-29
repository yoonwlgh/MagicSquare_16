"""Presenter bridging PyQt screen and ECB control/boundary layers."""

from __future__ import annotations

from boundary.magic_square.boundary_validator import BoundaryValidator
from boundary.magic_square.contracts import ErrorResponse
from boundary.result_formatter import ResultFormatter
from control.magic_square_control import MagicSquareControl
from control.magic_square_resolver import MagicSquareDomainResolver


class MagicSquareScreenPresenter:
    """Coordinates validation and solve for the desktop UI."""

    def __init__(
        self,
        boundary_validator: BoundaryValidator | None = None,
        control: MagicSquareControl | None = None,
        formatter: ResultFormatter | None = None,
    ) -> None:
        """Initialize with optional dependencies for testing."""
        validator = boundary_validator or BoundaryValidator()
        self._validator = validator
        self._control = control or MagicSquareControl(
            boundary_validator=validator,
            resolver=MagicSquareDomainResolver(),
        )
        self._formatter = formatter or ResultFormatter()

    def validate(self, grid: list[list[int]] | None) -> ErrorResponse | None:
        """Run FR-01 boundary validation only."""
        return self._validator.validate(grid)

    def solve(
        self, grid: list[list[int]] | None
    ) -> ErrorResponse | list[int]:
        """Validate at boundary then run domain solver when valid."""
        return self._control.solve(grid)

    def format_success(self, payload: list[int]) -> list[int]:
        """Normalize solver output to PRD int[6] contract."""
        return self._formatter.to_int6(payload)

    @staticmethod
    def format_error(response: ErrorResponse) -> str:
        """Render structured failure for the UI."""
        return f"{response.code}: {response.message}"

    @staticmethod
    def format_success_message(result: list[int]) -> str:
        """Render success int[6] for the UI."""
        return f"Success: {result}"
