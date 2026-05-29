"""Boundary output formatter for solver success (FR-05, BR-14)."""

from __future__ import annotations


class ResultFormatter:
    """Formats internal solve results to the int[6] output contract."""

    def to_int6(self, internal: object) -> list[int]:
        """Convert internal solve result to [r1, c1, n1, r2, c2, n2] (1-index).

        Args:
            internal: Control/Domain success payload.

        Returns:
            Six-element list matching PRD §12.2.

        Raises:
            NotImplementedError: RED stub — implementation pending GREEN phase.
        """
        _ = internal
        raise NotImplementedError("RED: ResultFormatter.to_int6 not implemented")
