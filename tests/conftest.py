"""Shared grid fixtures (G0~G3) for Dual-Track tests."""

from __future__ import annotations

# G1: validated 4x4 shell with two blanks (row-major) for Domain tests
def grid_g1_two_blanks() -> list[list[int]]:
    """4x4 with blanks at (2,2) and (3,3) — reverse-success family (TD-01)."""
    return [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 0, 12],
        [4, 15, 14, 0],
    ]


# G2: small-first-only success (TD-02)
def grid_g2_small_first_success() -> list[list[int]]:
    """4x4 where only small-first placement yields a magic square."""
    return [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 0, 0, 12],
        [4, 15, 14, 1],
    ]


# G3: reverse-success grid — SC-DOM-SOL-001 / TD-01
def grid_g3_reverse_success() -> list[list[int]]:
    """4x4 where small-first fails and reverse succeeds."""
    return grid_g1_two_blanks()


def grid_g1_filled_no_blanks() -> list[list[int]]:
    """4x4 filled 1..16 with zero blank cells (U-IN-04)."""
    return [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]


def grid_one_blank() -> list[list[int]]:
    """4x4 with exactly one blank cell (U-IN-05)."""
    return [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0],
    ]


def grid_three_blanks() -> list[list[int]]:
    """4x4 with three blank cells (U-IN-06, U-FLOW-02)."""
    return [
        [0, 2, 3, 4],
        [5, 0, 7, 8],
        [9, 10, 0, 12],
        [13, 14, 15, 16],
    ]


def grid_value_17_with_two_blanks() -> list[list[int]]:
    """4x4 with cell 17 and two blanks (U-IN-07)."""
    return [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 0],
        [13, 14, 17, 0],
    ]


def grid_duplicate_seven_with_two_blanks() -> list[list[int]]:
    """4x4 with duplicate 7 and two blanks (U-IN-08)."""
    return [
        [7, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 0, 12],
        [13, 14, 15, 0],
    ]


def grid_no_solution() -> list[list[int]]:
    """4x4 where neither solver attempt succeeds (D-SOL-03)."""
    return [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 0, 12],
        [13, 14, 15, 0],
    ]


def grid_valid_magic_square() -> list[list[int]]:
    """Known valid 4x4 magic square (D-VAL-01~05)."""
    return [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]


def grid_invalid_row_sum() -> list[list[int]]:
    """4x4 with one row sum != MAGIC_CONSTANT (D-VAL-06)."""
    return [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 2],
    ]
