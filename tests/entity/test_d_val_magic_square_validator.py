"""Track B RED skeleton: D-VAL-01~06 MagicSquareValidator line sums (FR-04)."""

from __future__ import annotations

from entity.services.constants import MAGIC_CONSTANT
from entity.services.magic_square_validator import MagicSquareValidator
from tests.conftest import grid_invalid_row_sum, grid_valid_magic_square

AC_DOCSTRING = "D-VAL, FR-04, BR-09/10/11 — MAGIC_CONSTANT=34 line validation."


class TestDVal01RowSums:
    """D-VAL-01 — each row sums to 34."""

    # D-VAL-01
    def test_d_val_01_all_row_sums_equal_magic_constant(self) -> None:
        """D-VAL-01 — four row sums == 34."""
        # Given
        validator = MagicSquareValidator()
        grid = grid_valid_magic_square()

        # When
        valid = validator.is_valid(grid)

        # Then
        assert all(sum(row) == MAGIC_CONSTANT for row in grid)
        assert valid is True


class TestDVal02ColumnSums:
    """D-VAL-02 — each column sums to 34."""

    # D-VAL-02
    def test_d_val_02_all_column_sums_equal_magic_constant(self) -> None:
        """D-VAL-02 — four column sums == 34."""
        # Given
        validator = MagicSquareValidator()
        grid = grid_valid_magic_square()

        # When
        valid = validator.is_valid(grid)

        # Then
        assert all(
            sum(grid[row][col] for row in range(4)) == MAGIC_CONSTANT for col in range(4)
        )
        assert valid is True


class TestDVal03MainDiagonal:
    """D-VAL-03 — main diagonal sum is 34."""

    # D-VAL-03
    def test_d_val_03_main_diagonal_sum_equals_magic_constant(self) -> None:
        """D-VAL-03 — primary diagonal sum == 34."""
        # Given
        validator = MagicSquareValidator()
        grid = grid_valid_magic_square()

        # When
        valid = validator.is_valid(grid)

        # Then
        assert sum(grid[index][index] for index in range(4)) == MAGIC_CONSTANT
        assert valid is True


class TestDVal04AntiDiagonal:
    """D-VAL-04 — anti-diagonal sum is 34."""

    # D-VAL-04
    def test_d_val_04_anti_diagonal_sum_equals_magic_constant(self) -> None:
        """D-VAL-04 — secondary diagonal sum == 34."""
        # Given
        validator = MagicSquareValidator()
        grid = grid_valid_magic_square()

        # When
        valid = validator.is_valid(grid)

        # Then
        assert sum(grid[index][3 - index] for index in range(4)) == MAGIC_CONSTANT
        assert valid is True


class TestDVal05FullyValidGrid:
    """D-VAL-05 — complete magic square returns true."""

    # D-VAL-05
    def test_d_val_05_complete_magic_square_is_valid(self) -> None:
        """D-VAL-05 — all lines + uniqueness → is_valid True (AC-FR04-01)."""
        # Given
        validator = MagicSquareValidator()
        grid = grid_valid_magic_square()

        # When
        valid = validator.is_valid(grid)

        # Then
        assert valid is True


class TestDVal06InvalidLineSum:
    """D-VAL-06 — one line not 34 returns false."""

    # D-VAL-06
    def test_d_val_06_one_row_wrong_sum_is_invalid(self) -> None:
        """D-VAL-06 — single row sum != 34 → False (AC-FR04-02)."""
        # Given
        validator = MagicSquareValidator()
        grid = grid_invalid_row_sum()

        # When
        valid = validator.is_valid(grid)

        # Then
        assert valid is False
