"""Scenario definitions for Golden Master solver regression tests."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum

from boundary.magic_square.contracts import (
    BOUNDARY_LAYER,
    CONTROL_LAYER,
    ERR_DUPLICATE_VALUE_CODE,
    ERR_INVALID_BLANK_COUNT_CODE,
    ERR_SOLVER_NO_SOLUTION_CODE,
)
from tests.conftest import (
    grid_duplicate_seven_with_two_blanks,
    grid_g2_small_first_success,
    grid_g3_reverse_success,
    grid_no_solution,
    grid_three_blanks,
)

GridFactory = Callable[[], list[list[int]]]


class SolveStrategy(Enum):
    """Which solver attempt is expected to succeed for a scenario."""

    SMALL_FIRST = "small_first"
    REVERSE = "reverse"
    ERROR = "error"


@dataclass(frozen=True)
class GoldenScenario:
    """One solver scenario captured in the Golden Master baseline."""

    test_case_id: str
    section_id: str
    title: str
    grid_factory: GridFactory
    strategy: SolveStrategy
    expected_error_code: str | None = None
    expected_layer: str | None = None


GOLDEN_SCENARIOS: tuple[GoldenScenario, ...] = (
    GoldenScenario(
        test_case_id="GM-TC-01",
        section_id="GM-TC-01",
        title="normal_success",
        grid_factory=grid_g2_small_first_success,
        strategy=SolveStrategy.SMALL_FIRST,
    ),
    GoldenScenario(
        test_case_id="GM-TC-02",
        section_id="GM-TC-02",
        title="reverse_success",
        grid_factory=grid_g3_reverse_success,
        strategy=SolveStrategy.REVERSE,
    ),
    GoldenScenario(
        test_case_id="GM-TC-03",
        section_id="GM-TC-03",
        title="invalid_blank_count",
        grid_factory=grid_three_blanks,
        strategy=SolveStrategy.ERROR,
        expected_error_code=ERR_INVALID_BLANK_COUNT_CODE,
        expected_layer=BOUNDARY_LAYER,
    ),
    GoldenScenario(
        test_case_id="GM-TC-04",
        section_id="GM-TC-04",
        title="duplicate_number",
        grid_factory=grid_duplicate_seven_with_two_blanks,
        strategy=SolveStrategy.ERROR,
        expected_error_code=ERR_DUPLICATE_VALUE_CODE,
        expected_layer=BOUNDARY_LAYER,
    ),
    GoldenScenario(
        test_case_id="GM-TC-05",
        section_id="GM-TC-05",
        title="no_valid_magic_square",
        grid_factory=grid_no_solution,
        strategy=SolveStrategy.ERROR,
        expected_error_code=ERR_SOLVER_NO_SOLUTION_CODE,
        expected_layer=CONTROL_LAYER,
    ),
)

SCENARIO_BY_TEST_CASE: dict[str, GoldenScenario] = {
    scenario.test_case_id: scenario for scenario in GOLDEN_SCENARIOS
}
