"""Boundary input validator for 4x4 magic square grids (FR-01)."""

from typing import Any

from boundary.magic_square.contracts import ErrorResponse


class BoundaryValidator:
    """Validates grid shape before Control invokes Domain resolve()."""

    def validate(self, grid: list[list[int]] | None) -> ErrorResponse | None:
        """Return ErrorResponse on shape failure; None when validation passes.

        RED stub: not implemented — always returns None so AC-FR-01-01 tests fail.
        """
        _ = grid
        return None
