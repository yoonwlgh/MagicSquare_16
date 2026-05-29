"""Boundary output formatter for solver success (FR-05, BR-14)."""

from __future__ import annotations

from boundary.magic_square.contracts import GRID_SIZE


class ResultFormatter:
    """Formats internal solve results to the int[6] output contract."""

    def to_int6(self, internal: object) -> list[int]:
        """Convert internal solve result to [r1, c1, n1, r2, c2, n2] (1-index).

        Args:
            internal: Solver success payload (six-element list).

        Returns:
            Six-element list matching PRD §12.2.

        Raises:
            ValueError: When payload length or coordinate bounds are invalid.
        """
        if not isinstance(internal, list):
            raise ValueError("Internal result must be a list.")

        result = [int(value) for value in internal]
        if len(result) != 6:
            raise ValueError("Success payload must have length 6.")

        row1, col1, _, row2, col2, _ = result
        for coordinate in (row1, col1, row2, col2):
            if coordinate < 1 or coordinate > GRID_SIZE:
                raise ValueError("Coordinates must be 1-indexed within grid bounds.")

        return result
