"""Boundary output formatter for solver success (FR-05, BR-14)."""

from __future__ import annotations

from boundary.int6_contract_validator import Int6ContractValidator


class ResultFormatter:
    """Formats internal solve results to the int[6] output contract."""

    def __init__(self, validator: Int6ContractValidator | None = None) -> None:
        """Initialize with optional injected validator for testing."""
        self._validator = validator or Int6ContractValidator()

    def to_int6(self, internal: object) -> list[int]:
        """Convert internal solve result to [r1, c1, n1, r2, c2, n2] (1-index).

        Args:
            internal: Solver success payload (six-element list).

        Returns:
            Six-element list matching PRD §12.2.

        Raises:
            ValueError: When payload length or coordinate bounds are invalid.
        """
        return self._validator.validate(internal)
