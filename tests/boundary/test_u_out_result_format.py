"""Track A RED skeleton: U-OUT-01~03 Boundary output contract (FR-05, BR-14)."""

from __future__ import annotations

import pytest

from boundary.result_formatter import ResultFormatter
from entity.services.solver import Solver
from tests.conftest import grid_g3_reverse_success

AC_DOCSTRING = "U-OUT, FR-05, PRD §12.2 — int[6] success output contract."

# TD-01 reverse-success on grid_g3 (SC-DOM-SOL-001)
REVERSE_SUCCESS_INT6 = [3, 3, 7, 4, 4, 1]


class TestUOut01ResultLength:
    """U-OUT-01 — success payload length is 6."""

    # U-OUT-01
    def test_u_out_01_success_payload_length_is_six(self) -> None:
        """U-OUT-01 — formatted result has len == 6 (AC-FR05-04)."""
        # Given
        formatter = ResultFormatter()
        internal = Solver().solve(grid_g3_reverse_success())

        # When
        result = formatter.to_int6(internal)

        # Then
        assert len(result) == 6


class TestUOut02OneIndexedCoordinates:
    """U-OUT-02 — r,c are 1-indexed in 1..4."""

    # U-OUT-02
    def test_u_out_02_coordinates_are_one_indexed(self) -> None:
        """U-OUT-02 — r1,c1,r2,c2 in 1..4 (AC-FR05-05, BS-04)."""
        # Given
        formatter = ResultFormatter()
        internal = Solver().solve(grid_g3_reverse_success())

        # When
        result = formatter.to_int6(internal)

        # Then
        row1, col1, _, row2, col2, _ = result
        for coordinate in (row1, col1, row2, col2):
            assert 1 <= coordinate <= 4


class TestUOut03TupleOrder:
    """U-OUT-03 — [r1,c1,n1,r2,c2,n2] order for reverse success."""

    # U-OUT-03
    def test_u_out_03_reverse_success_tuple_order(self) -> None:
        """U-OUT-03 — reverse success order (AC-FR05-02, TD-01)."""
        # Given
        formatter = ResultFormatter()
        internal = Solver().solve(grid_g3_reverse_success())

        # When
        result = formatter.to_int6(internal)

        # Then
        assert result == REVERSE_SUCCESS_INT6


class TestUOut04FormatterNegativePaths:
    """A-5 / U-OUT — invalid internal payloads raise ValueError."""

    def test_u_out_04_non_list_internal_raises_value_error(self) -> None:
        """A-5 — non-list internal payload rejected."""
        # Given
        formatter = ResultFormatter()

        # When / Then
        with pytest.raises(ValueError, match="must be a list"):
            formatter.to_int6("not-a-list")

    def test_u_out_04_wrong_length_raises_value_error(self) -> None:
        """A-5 — payload length != 6 rejected."""
        # Given
        formatter = ResultFormatter()

        # When / Then
        with pytest.raises(ValueError, match="length 6"):
            formatter.to_int6([1, 2, 3])

    def test_u_out_04_out_of_bounds_coordinate_raises_value_error(self) -> None:
        """A-5 — coordinate outside 1..4 rejected."""
        # Given
        formatter = ResultFormatter()

        # When / Then
        with pytest.raises(ValueError, match="1-indexed"):
            formatter.to_int6([0, 1, 2, 3, 4, 5])
