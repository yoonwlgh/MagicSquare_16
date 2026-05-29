"""Track B RED skeleton: D-SOL-01~04 Solver combinations (FR-05)."""

from __future__ import annotations

import copy

import pytest

from entity.services.exceptions import SolverNoSolutionError
from entity.services.solver import Solver
from tests.conftest import (
    grid_g2_small_first_success,
    grid_g3_reverse_success,
    grid_no_solution,
)

AC_DOCSTRING = "D-SOL, FR-05, BR-12~13 — small-first then reverse; EP-02/03/04."

REVERSE_SUCCESS_INT6 = [3, 3, 7, 4, 4, 1]
SMALL_FIRST_SUCCESS_INT6 = [3, 2, 6, 3, 3, 7]


class TestDSol01ReverseSuccess:
    """D-SOL-01 — reverse attempt success (SC-DOM-SOL-001)."""

    # D-SOL-01
    def test_d_sol_01_reverse_attempt_returns_int6_contract(self) -> None:
        """D-SOL-01 — reverse success int[6] (TD-01, AC-FR05-02)."""
        # Given
        solver = Solver()
        grid = grid_g3_reverse_success()

        # When
        result = solver.solve(grid)

        # Then
        assert result == REVERSE_SUCCESS_INT6


class TestDSol02SmallFirstSuccess:
    """D-SOL-02 — small-first attempt success (TD-02 TBD)."""

    # D-SOL-02
    def test_d_sol_02_small_first_success_returns_int6(self) -> None:
        """D-SOL-02 — small→blank1, large→blank2 (AC-FR05-01, G2)."""
        # Given
        solver = Solver()
        grid = grid_g2_small_first_success()

        # When
        result = solver.solve(grid)

        # Then
        assert result == SMALL_FIRST_SUCCESS_INT6


class TestDSol03BothCombinationsFail:
    """D-SOL-03 — both attempts fail → no int[6] (Control error path)."""

    # D-SOL-03
    def test_d_sol_03_both_combinations_fail_no_solution(self) -> None:
        """D-SOL-03 — both attempts invalid → ERR_SOLVER_NO_SOLUTION (AC-FR05-03)."""
        # Given
        solver = Solver()
        grid = grid_no_solution()

        # When / Then
        with pytest.raises(SolverNoSolutionError):
            solver.solve(grid)


class TestDSol04InputImmutability:
    """D-SOL-04 — solver does not mutate input grid (EP-04, NFR-04)."""

    # D-SOL-04
    def test_d_sol_04_input_grid_unchanged_after_solve(self) -> None:
        """D-SOL-04 — grid snapshot before/after solve identical."""
        # Given
        solver = Solver()
        grid = grid_g3_reverse_success()
        snapshot = copy.deepcopy(grid)

        # When
        solver.solve(grid)

        # Then
        assert grid == snapshot
