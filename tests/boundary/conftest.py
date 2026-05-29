"""Shared fixtures for magic square boundary tests (AC-FR-01-01)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from boundary.magic_square.boundary_validator import BoundaryValidator
from control.magic_square_control import MagicSquareControl


@pytest.fixture
def boundary_validator() -> BoundaryValidator:
    """BoundaryValidator under test (RED: validate not implemented)."""
    return BoundaryValidator()


@pytest.fixture
def domain_resolver_mock() -> MagicMock:
    """Spy for Domain resolve() entry point."""
    return MagicMock()


@pytest.fixture
def magic_square_control(
    boundary_validator: BoundaryValidator,
    domain_resolver_mock: MagicMock,
) -> MagicSquareControl:
    """Control with injected Boundary validator and Domain resolver spy."""
    return MagicSquareControl(
        boundary_validator=boundary_validator,
        resolver=domain_resolver_mock,
    )


def grid_3x4() -> list[list[int]]:
    """Three rows, four columns — shape violation (BV-004)."""
    return [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]


def grid_empty_rows_four() -> list[list[int]]:
    """Four rows with zero columns — [[]] * 4 pattern (BV-003)."""
    return [[] for _ in range(4)]
