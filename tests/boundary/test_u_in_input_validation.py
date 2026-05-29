"""Track A RED skeleton: U-IN-04~08 Boundary input validation (FR-01, AC-FR01-02~04)."""

from __future__ import annotations

from boundary.input_validator import InputValidator
from boundary.magic_square.contracts import (
    ERR_DUPLICATE_VALUE_CODE,
    ERR_INVALID_BLANK_COUNT_CODE,
    ERR_OUT_OF_RANGE_CODE,
    ErrorResponse,
)
from tests.conftest import (
    grid_duplicate_seven_with_two_blanks,
    grid_g1_filled_no_blanks,
    grid_one_blank,
    grid_three_blanks,
    grid_value_17_with_two_blanks,
)

AC_DOCSTRING = "U-IN, FR-01, PRD §12.1 / §13.2 — Boundary input contract (blank/range/duplicate)."


class TestUIn04BlankCountZero:
    """U-IN-04 — zero blank cells (no 0 in grid)."""

    # U-IN-04
    def test_u_in_04_zero_empty_cells_returns_e002(self) -> None:
        """U-IN-04 — 4x4 with no blanks rejects ERR_INVALID_BLANK_COUNT (E002)."""
        # Given
        validator = InputValidator()
        grid = grid_g1_filled_no_blanks()

        # When
        result = validator.validate(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == ERR_INVALID_BLANK_COUNT_CODE


class TestUIn05BlankCountOne:
    """U-IN-05 — exactly one blank cell."""

    # U-IN-05
    def test_u_in_05_one_blank_cell_returns_e002(self) -> None:
        """U-IN-05 — single 0 cell rejects ERR_INVALID_BLANK_COUNT (E002)."""
        # Given
        validator = InputValidator()
        grid = grid_one_blank()

        # When
        result = validator.validate(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == ERR_INVALID_BLANK_COUNT_CODE


class TestUIn06BlankCountThree:
    """U-IN-06 — three blank cells."""

    # U-IN-06
    def test_u_in_06_three_blank_cells_returns_e002(self) -> None:
        """U-IN-06 — three 0 cells rejects ERR_INVALID_BLANK_COUNT (E002)."""
        # Given
        validator = InputValidator()
        grid = grid_three_blanks()

        # When
        result = validator.validate(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == ERR_INVALID_BLANK_COUNT_CODE


class TestUIn07ValueOutOfRange:
    """U-IN-07 — value outside 0 or 1..16."""

    # U-IN-07
    def test_u_in_07_cell_value_17_returns_e003(self) -> None:
        """U-IN-07 — cell 17 rejects ERR_OUT_OF_RANGE (E003)."""
        # Given
        validator = InputValidator()
        grid = grid_value_17_with_two_blanks()

        # When
        result = validator.validate(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == ERR_OUT_OF_RANGE_CODE


class TestUIn08DuplicateNonZero:
    """U-IN-08 — duplicate non-zero values."""

    # U-IN-08
    def test_u_in_08_duplicate_non_zero_returns_e004(self) -> None:
        """U-IN-08 — duplicate 7 rejects ERR_DUPLICATE_VALUE (E004)."""
        # Given
        validator = InputValidator()
        grid = grid_duplicate_seven_with_two_blanks()

        # When
        result = validator.validate(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == ERR_DUPLICATE_VALUE_CODE
