"""Golden Master contract assertions for solver output."""

from __future__ import annotations

from boundary.magic_square.contracts import ErrorResponse, GRID_SIZE
from entity.services.blank_finder import BlankFinder
from entity.services.missing_number_finder import MissingNumberFinder
from tests.golden_master.scenarios import GoldenScenario, SolveStrategy

INT6_LENGTH = 6
MIN_ONE_INDEX = 1


def assert_int6_output_format(result: list[int]) -> None:
    """Assert success payload matches int[6] length and integer element types."""
    assert isinstance(result, list), "Success result must be a list."
    assert len(result) == INT6_LENGTH, (
        f"Success payload must have length {INT6_LENGTH}, got {len(result)}."
    )
    assert all(isinstance(value, int) for value in result), (
        "All int[6] elements must be integers."
    )


def assert_one_index_coordinates(result: list[int]) -> None:
    """Assert blank coordinates in int[6] are 1-indexed within grid bounds."""
    row1, col1, _, row2, col2, _ = result
    for label, coordinate in (
        ("r1", row1),
        ("c1", col1),
        ("r2", row2),
        ("c2", col2),
    ):
        assert MIN_ONE_INDEX <= coordinate <= GRID_SIZE, (
            f"{label} must be 1-indexed within 1..{GRID_SIZE}, got {coordinate}."
        )


def assert_row_major_blank_order(result: list[int], grid: list[list[int]]) -> None:
    """Assert int[6] coordinates follow row-major blank discovery order."""
    blanks = BlankFinder().find_blanks(grid)
    row1, col1, _, row2, col2, _ = result
    expected_first = (blanks[0][0] + 1, blanks[0][1] + 1)
    expected_second = (blanks[1][0] + 1, blanks[1][1] + 1)
    assert (row1, col1) == expected_first, (
        f"First blank must be row-major {expected_first}, got ({row1}, {col1})."
    )
    assert (row2, col2) == expected_second, (
        f"Second blank must be row-major {expected_second}, got ({row2}, {col2})."
    )


def assert_small_first_combination(result: list[int], grid: list[list[int]]) -> None:
    """Assert small missing number maps to blank1 and large to blank2."""
    missing = MissingNumberFinder().find_missing(grid)
    small, large = missing[0], missing[1]
    _, _, n1, _, _, n2 = result
    assert n1 == small and n2 == large, (
        f"Small-first expects ({small}, {large}), got ({n1}, {n2})."
    )


def assert_reverse_fallback_combination(result: list[int], grid: list[list[int]]) -> None:
    """Assert reverse attempt maps large to blank1 and small to blank2."""
    missing = MissingNumberFinder().find_missing(grid)
    small, large = missing[0], missing[1]
    _, _, n1, _, _, n2 = result
    assert n1 == large and n2 == small, (
        f"Reverse fallback expects ({large}, {small}), got ({n1}, {n2})."
    )


def assert_error_contract(result: ErrorResponse, scenario: GoldenScenario) -> None:
    """Assert structured error response matches scenario contract."""
    assert scenario.expected_error_code is not None
    assert scenario.expected_layer is not None
    assert result.code == scenario.expected_error_code, (
        f"Expected error code {scenario.expected_error_code}, got {result.code}."
    )
    assert result.layer == scenario.expected_layer, (
        f"Expected layer {scenario.expected_layer}, got {result.layer}."
    )
    assert result.message.strip(), "Error message must be non-empty."


def assert_success_contract(
    result: list[int],
    grid: list[list[int]],
    scenario: GoldenScenario,
) -> None:
    """Assert int[6] success payload satisfies PRD placement rules."""
    assert_int6_output_format(result)
    assert_one_index_coordinates(result)
    assert_row_major_blank_order(result, grid)
    if scenario.strategy == SolveStrategy.SMALL_FIRST:
        assert_small_first_combination(result, grid)
    elif scenario.strategy == SolveStrategy.REVERSE:
        assert_reverse_fallback_combination(result, grid)
