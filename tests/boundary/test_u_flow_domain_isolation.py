"""Track A RED skeleton: U-FLOW-02 — Control flow blocks Domain on FR-01 failures (extended)."""

from __future__ import annotations

from unittest.mock import MagicMock

from boundary.magic_square.boundary_validator import BoundaryValidator
from boundary.magic_square.contracts import (
    ERR_DUPLICATE_VALUE_CODE,
    ERR_INVALID_BLANK_COUNT_CODE,
    ERR_OUT_OF_RANGE_CODE,
    ErrorResponse,
)
from control.magic_square_control import MagicSquareControl
from tests.conftest import (
    grid_duplicate_seven_with_two_blanks,
    grid_three_blanks,
    grid_value_17_with_two_blanks,
)

AC_DOCSTRING = (
    "U-FLOW-02, BR-05, EP-01 — blank-count / range / duplicate failure "
    "must not invoke Domain pipeline (extends shape-only U-FLOW-01)."
)


class TestUFlow02BlankCountBlocksDomain:
    """U-FLOW-02 — FR-01 blank-count failure skips Domain resolve/spy."""

    # U-FLOW-02
    def test_u_flow_02_blank_count_error_domain_pipeline_zero_calls(
        self,
    ) -> None:
        """U-FLOW-02 — three blanks: Control.solve, Domain spy call_count == 0."""
        # Given
        validator = BoundaryValidator()
        resolver = MagicMock()
        control = MagicSquareControl(boundary_validator=validator, resolver=resolver)
        grid = grid_three_blanks()

        # When
        result = control.solve(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == ERR_INVALID_BLANK_COUNT_CODE
        assert resolver.resolve.call_count == 0


class TestUFlow02OutOfRangeBlocksDomain:
    """U-FLOW-02 — FR-01 range failure skips Domain resolve/spy."""

    def test_u_flow_02_out_of_range_error_domain_pipeline_zero_calls(
        self,
    ) -> None:
        """U-FLOW-02 — cell value 17: resolver.call_count == 0."""
        # Given
        validator = BoundaryValidator()
        resolver = MagicMock()
        control = MagicSquareControl(boundary_validator=validator, resolver=resolver)
        grid = grid_value_17_with_two_blanks()

        # When
        result = control.solve(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == ERR_OUT_OF_RANGE_CODE
        assert resolver.resolve.call_count == 0


class TestUFlow02DuplicateBlocksDomain:
    """U-FLOW-02 — FR-01 duplicate failure skips Domain resolve/spy."""

    def test_u_flow_02_duplicate_value_error_domain_pipeline_zero_calls(
        self,
    ) -> None:
        """U-FLOW-02 — duplicate non-zero: resolver.call_count == 0."""
        # Given
        validator = BoundaryValidator()
        resolver = MagicMock()
        control = MagicSquareControl(boundary_validator=validator, resolver=resolver)
        grid = grid_duplicate_seven_with_two_blanks()

        # When
        result = control.solve(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == ERR_DUPLICATE_VALUE_CODE
        assert resolver.resolve.call_count == 0
