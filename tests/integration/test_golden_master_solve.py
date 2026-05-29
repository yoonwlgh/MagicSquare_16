"""GM-1 Golden Master regression tests for Magic Square Solver output."""

from __future__ import annotations

from pathlib import Path

import pytest

from boundary.magic_square.boundary_validator import BoundaryValidator
from control.magic_square_control import MagicSquareControl
from control.magic_square_resolver import MagicSquareDomainResolver
from tests.golden_master.approval import (
    GOLDEN_MASTER_PATH,
    assert_golden_master_matches,
    build_golden_master_document,
    parse_golden_master_sections,
    read_expected_document,
)
from tests.golden_master.scenarios import GOLDEN_SCENARIOS

AC_DOCSTRING = "GM-1 — solver stdout/DTO Golden Master regression (approve pattern)."
pytestmark = pytest.mark.golden_master


@pytest.fixture
def magic_square_control() -> MagicSquareControl:
    """Production Control wiring for end-to-end Golden Master capture."""
    return MagicSquareControl(
        boundary_validator=BoundaryValidator(),
        resolver=MagicSquareDomainResolver(),
    )


class TestGoldenMasterSolveScenarios:
    """GM-1 — five solver scenarios captured as Golden Master sections."""

    # GM-1
    def test_gm_01_full_document_matches_baseline(
        self,
        magic_square_control: MagicSquareControl,
        tmp_path: Path,
    ) -> None:
        """GM-1 — full Golden Master document matches committed baseline."""
        # Given
        baseline = tmp_path / "golden_master_expected.txt"
        if GOLDEN_MASTER_PATH.exists():
            baseline.write_text(read_expected_document(), encoding="utf-8")

        # When / Then
        assert_golden_master_matches(
            magic_square_control,
            path=baseline,
            approve=False,
        )

    # GM-1
    @pytest.mark.parametrize(
        "section_id",
        [scenario.section_id for scenario in GOLDEN_SCENARIOS],
        ids=[scenario.title for scenario in GOLDEN_SCENARIOS],
    )
    def test_gm_02_each_section_present_in_baseline(
        self,
        magic_square_control: MagicSquareControl,
        section_id: str,
    ) -> None:
        """GM-1 — each configured scenario has a section in the baseline."""
        # Given
        assert GOLDEN_MASTER_PATH.exists(), (
            f"Missing baseline {GOLDEN_MASTER_PATH}. "
            "Run scripts/generate_golden_master.py first."
        )
        expected_sections = parse_golden_master_sections(read_expected_document())
        actual_sections = parse_golden_master_sections(
            build_golden_master_document(magic_square_control)
        )

        # Then
        assert section_id in expected_sections
        assert section_id in actual_sections
        assert expected_sections[section_id] == actual_sections[section_id]
