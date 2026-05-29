"""GM-2 Golden Master regression tests for Magic Square Solver output."""

from __future__ import annotations

import pytest

from boundary.magic_square.boundary_validator import BoundaryValidator
from boundary.magic_square.contracts import ErrorResponse
from control.magic_square_control import MagicSquareControl
from control.magic_square_resolver import MagicSquareDomainResolver
from tests.golden_master.approval import (
    GOLDEN_MASTER_PATH,
    assert_golden_master_matches,
    assert_golden_section_matches,
    build_golden_master_document,
    parse_golden_master_sections,
    read_expected_document,
)
from tests.golden_master.contracts import (
    assert_error_contract,
    assert_success_contract,
)
from tests.golden_master.scenarios import (
    GOLDEN_SCENARIOS,
    SCENARIO_BY_TEST_CASE,
    SolveStrategy,
)

AC_DOCSTRING = "GM-2 — int[6]/Error Golden Master regression with approve pattern."
pytestmark = pytest.mark.golden_master


@pytest.fixture
def magic_square_control() -> MagicSquareControl:
    """Production Control wiring for end-to-end Golden Master capture."""
    return MagicSquareControl(
        boundary_validator=BoundaryValidator(),
        resolver=MagicSquareDomainResolver(),
    )


@pytest.mark.parametrize(
    "test_case_id",
    [scenario.test_case_id for scenario in GOLDEN_SCENARIOS],
    ids=[scenario.title for scenario in GOLDEN_SCENARIOS],
)
class TestGoldenMasterMagicSquare:
    """[TAG][GoldenMaster] — GM-TC-01~05 solver output approval tests."""

    # GM-TC-01~05
    def test_golden_master_section_matches_baseline(
        self,
        magic_square_control: MagicSquareControl,
        test_case_id: str,
    ) -> None:
        """[GoldenMaster] section body matches golden_master_expected.txt."""
        # Given
        scenario = SCENARIO_BY_TEST_CASE[test_case_id]

        # When / Then — approve pattern: create baseline if missing, else compare
        assert_golden_section_matches(
            magic_square_control,
            scenario,
            path=GOLDEN_MASTER_PATH,
            approve=False,
        )

    # GM-TC-01~05
    def test_golden_master_output_contract(
        self,
        magic_square_control: MagicSquareControl,
        test_case_id: str,
    ) -> None:
        """[GoldenMaster] verify int[6], row-major, 1-index, strategy, error contract."""
        # Given
        scenario = SCENARIO_BY_TEST_CASE[test_case_id]
        grid = scenario.grid_factory()

        # When
        result = magic_square_control.solve(grid)

        # Then
        if scenario.strategy == SolveStrategy.ERROR:
            assert isinstance(result, ErrorResponse)
            assert_error_contract(result, scenario)
        else:
            assert isinstance(result, list)
            assert_success_contract(result, grid, scenario)


class TestGoldenMasterMagicSquareDocument:
    """Full baseline document regression for all GM-TC sections."""

    # GM-2
    def test_golden_master_full_document_matches_baseline(
        self,
        magic_square_control: MagicSquareControl,
    ) -> None:
        """[GoldenMaster] open(expected).read() vs actual for full baseline file."""
        # Given / When / Then
        assert_golden_master_matches(
            magic_square_control,
            path=GOLDEN_MASTER_PATH,
            approve=False,
        )

    # GM-2
    def test_golden_master_serialized_sections_match_file(
        self,
        magic_square_control: MagicSquareControl,
    ) -> None:
        """[GoldenMaster] API result serialization matches parsed baseline sections."""
        # Given
        assert GOLDEN_MASTER_PATH.exists(), (
            f"Missing baseline {GOLDEN_MASTER_PATH}. "
            "Run scripts/generate_golden_master.py first."
        )
        expected_sections = parse_golden_master_sections(read_expected_document())
        actual_sections = parse_golden_master_sections(
            build_golden_master_document(magic_square_control)
        )

        # When / Then
        for scenario in GOLDEN_SCENARIOS:
            assert scenario.section_id in expected_sections
            assert scenario.section_id in actual_sections
            assert (
                expected_sections[scenario.section_id]
                == actual_sections[scenario.section_id]
            )
