"""Approve-pattern Golden Master comparison for solver output regression."""

from __future__ import annotations

import difflib
import os
from pathlib import Path

from boundary.magic_square.contracts import ErrorResponse
from control.application_contracts import ApplicationError
from control.magic_square_control import MagicSquareControl
from tests.golden_master.scenarios import GOLDEN_SCENARIOS, GoldenScenario

GOLDEN_MASTER_PATH = Path(__file__).resolve().parent.parent / "golden_master_expected.txt"
APPROVE_ENV_VAR = "GOLDEN_MASTER_APPROVE"
SECTION_SEPARATOR = "\n________________________________________\n"
DIFF_EXPECTED_LABEL = "expected"
DIFF_ACTUAL_LABEL = "actual"


def format_grid_lines(grid: list[list[int]]) -> str:
    """Render a 4x4 grid as space-separated rows."""
    return "\n".join(" ".join(str(cell) for cell in row) for row in grid)


def serialize_success_section(section_id: str, grid: list[list[int]], result: list[int]) -> str:
    """Serialize a successful solve scenario for Golden Master comparison."""
    return (
        f"[{section_id}]\n"
        f"Input:\n"
        f"{format_grid_lines(grid)}\n"
        f"Output:\n"
        f"{result}"
    )


def serialize_error_section(section_id: str, grid: list[list[int]], error_code: str) -> str:
    """Serialize a boundary/control error scenario for Golden Master comparison."""
    return (
        f"[{section_id}]\n"
        f"Input:\n"
        f"{format_grid_lines(grid)}\n"
        f"Error:\n"
        f"{error_code}"
    )


def capture_scenario_section(
    control: MagicSquareControl,
    scenario: GoldenScenario,
) -> str:
    """Run one scenario through Control and serialize its Golden Master section."""
    grid = scenario.grid_factory()
    result = control.solve(grid)
    if isinstance(result, (ErrorResponse, ApplicationError)):
        return serialize_error_section(scenario.section_id, grid, result.code)
    return serialize_success_section(scenario.section_id, grid, result)


def build_golden_master_document(control: MagicSquareControl) -> str:
    """Build the full Golden Master document from all configured scenarios."""
    sections = [
        capture_scenario_section(control, scenario) for scenario in GOLDEN_SCENARIOS
    ]
    body = SECTION_SEPARATOR.join(sections)
    return f"{body}\n"


def parse_golden_master_sections(document: str) -> dict[str, str]:
    """Parse a Golden Master document into section_id -> body mappings."""
    sections: dict[str, str] = {}
    for chunk in document.strip().split(SECTION_SEPARATOR):
        chunk = chunk.strip()
        if not chunk:
            continue
        header, _, body = chunk.partition("\n")
        if not header.startswith("[") or not header.endswith("]"):
            continue
        section_id = header[1:-1]
        sections[section_id] = body.strip()
    return sections


def read_expected_document(path: Path = GOLDEN_MASTER_PATH) -> str:
    """Read committed Golden Master baseline text."""
    return path.read_text(encoding="utf-8")


def should_approve_golden_master() -> bool:
    """Return True when the caller explicitly requests baseline regeneration."""
    return os.environ.get(APPROVE_ENV_VAR, "").strip().lower() in {"1", "true", "yes"}


def write_golden_master(document: str, path: Path = GOLDEN_MASTER_PATH) -> None:
    """Persist the Golden Master baseline document."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(document, encoding="utf-8", newline="\n")


def unified_diff(expected: str, actual: str, label: str) -> str:
    """Build a unified diff with --- expected / +++ actual headers."""
    return "".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile=f"--- {DIFF_EXPECTED_LABEL}",
            tofile=f"+++ {DIFF_ACTUAL_LABEL}",
            lineterm="",
        )
    )


def assert_text_matches_baseline(
    expected: str,
    actual: str,
    *,
    label: str,
    path: Path,
    approve: bool,
) -> None:
    """Compare expected vs actual text using the approve pattern."""
    if approve or not path.exists():
        write_golden_master(actual, path)
        return

    if expected == actual:
        return

    diff = unified_diff(expected, actual, label)
    raise AssertionError(
        "Golden Master output mismatch.\n"
        f"Baseline: {path}\n"
        f"Re-approve with: set {APPROVE_ENV_VAR}=1 or run scripts/generate_golden_master.py\n"
        f"{diff}"
    )


def assert_golden_master_matches(
    control: MagicSquareControl,
    *,
    path: Path = GOLDEN_MASTER_PATH,
    approve: bool | None = None,
) -> None:
    """Approve-pattern verification for the full solver Golden Master baseline."""
    actual_document = build_golden_master_document(control)
    approve_requested = should_approve_golden_master() if approve is None else approve

    if approve_requested or not path.exists():
        write_golden_master(actual_document, path)
        return

    expected_document = read_expected_document(path)
    assert_text_matches_baseline(
        expected_document,
        actual_document,
        label=path.name,
        path=path,
        approve=False,
    )


def assert_golden_section_matches(
    control: MagicSquareControl,
    scenario: GoldenScenario,
    *,
    path: Path = GOLDEN_MASTER_PATH,
    approve: bool | None = None,
) -> None:
    """Approve-pattern verification for one Golden Master scenario section."""
    actual_section = capture_scenario_section(control, scenario)
    _, _, actual_body = actual_section.partition("\n")
    actual_body = actual_body.strip()
    approve_requested = should_approve_golden_master() if approve is None else approve

    if approve_requested or not path.exists():
        write_golden_master(build_golden_master_document(control), path)
        return

    expected_sections = parse_golden_master_sections(read_expected_document(path))
    if scenario.section_id not in expected_sections:
        write_golden_master(build_golden_master_document(control), path)
        return

    expected_body = expected_sections[scenario.section_id]
    if expected_body == actual_body:
        return

    diff = unified_diff(expected_body, actual_body, scenario.section_id)
    raise AssertionError(
        f"Golden Master section mismatch [{scenario.section_id}].\n"
        f"Baseline: {path}\n"
        f"Re-approve with: set {APPROVE_ENV_VAR}=1 or run scripts/generate_golden_master.py\n"
        f"{diff}"
    )
