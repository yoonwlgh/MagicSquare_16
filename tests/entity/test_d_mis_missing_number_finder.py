"""Track B RED skeleton: D-MIS-01 MissingNumberFinder (FR-03)."""

from __future__ import annotations

from entity.services.missing_number_finder import MissingNumberFinder
from tests.conftest import grid_g1_two_blanks

AC_DOCSTRING = "D-MIS-01, FR-03, AC-FR03-01/02 — [small, large] ascending, 0 excluded."


class TestDMis01MissingNumbersAscending:
    """D-MIS-01 — missing pair from {1..16} \\ input, sorted ascending."""

    # D-MIS-01
    def test_d_mis_01_missing_numbers_ascending_pair(self) -> None:
        """D-MIS-01 — returns [small, large] with small < large."""
        # Given
        finder = MissingNumberFinder()
        grid = grid_g1_two_blanks()

        # When
        missing = finder.find_missing(grid)

        # Then
        assert missing == [1, 7]
        assert missing[0] < missing[1]
