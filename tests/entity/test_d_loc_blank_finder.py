"""Track B RED skeleton: D-LOC-01 BlankFinder row-major coordinates (FR-02)."""

from __future__ import annotations

import pytest

from entity.services.blank_finder import BlankFinder

AC_DOCSTRING = "D-LOC-01, FR-02, AC-FR02-01/02 — two blank coords row-major (0-index)."


class TestDLoc01BlankFinderRowMajor:
    """D-LOC-01 — BlankFinder returns two (r,c) in row-major order."""

    # D-LOC-01
    def test_d_loc_01_blank_finder_row_major_two_coords(self) -> None:
        """D-LOC-01 — row-major first and second 0 cell coordinates."""
        # Given
        # finder = BlankFinder()
        # grid = grid_g1_two_blanks()  # tests/conftest G1 placeholder

        # When
        # blanks = finder.find_blanks(grid)

        # Then
        pytest.fail("RED: D-LOC-01 — BlankFinder row-major two (r,c) coordinates")
