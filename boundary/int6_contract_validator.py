"""Validates solver success payloads against the int[6] output contract (FR-05)."""

from __future__ import annotations

from boundary.magic_square.contracts import GRID_SIZE


class Int6ContractValidator:
    """Checks int[6] length and 1-index coordinate bounds before formatting."""

    def validate(self, internal: object) -> list[int]:
        """Validate and normalize a six-element solver success payload.

        Args:
            internal: Solver success payload (six-element list).

        Returns:
            Six-element list of integers matching PRD §12.2.

        Raises:
            ValueError: When payload type, length, or coordinate bounds are invalid.
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
