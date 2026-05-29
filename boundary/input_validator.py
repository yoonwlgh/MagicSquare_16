"""Boundary input validator facade (FR-01).

Delegates to ``BoundaryValidator`` until OPEN-04 naming is unified.
"""

from __future__ import annotations

from boundary.magic_square.boundary_validator import BoundaryValidator
from boundary.magic_square.contracts import ErrorResponse


class InputValidator:
    """Validates 4x4 grid input contract before Control invokes Domain."""

    def __init__(self, validator: BoundaryValidator | None = None) -> None:
        """Initialize with optional injected validator for testing.

        Args:
            validator: Boundary validator implementation; defaults to production stub.
        """
        self._validator = validator or BoundaryValidator()

    def validate(self, grid: list[list[int]] | None) -> ErrorResponse | None:
        """Return ErrorResponse on failure; None when input passes FR-01 checks.

        Args:
            grid: Candidate 4x4 integer matrix.

        Returns:
            Structured error on failure, or None if validation passes.
        """
        return self._validator.validate(grid)
