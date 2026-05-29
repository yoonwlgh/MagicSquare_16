"""Sample 4x4 grids for manual GUI exploration."""

from __future__ import annotations

from boundary.magic_square.contracts import GRID_SIZE


def grid_reverse_success_sample() -> list[list[int]]:
    """TD-01 / SC-DOM-SOL-001 — small-first fails, reverse succeeds."""
    return [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 0, 12],
        [4, 15, 14, 0],
    ]


def grid_small_first_success_sample() -> list[list[int]]:
    """TD-02 — small-first only success."""
    return [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 0, 0, 12],
        [4, 15, 14, 1],
    ]


def grid_invalid_blank_count_sample() -> list[list[int]]:
    """Three blanks — ERR_INVALID_BLANK_COUNT."""
    return [
        [0, 2, 3, 4],
        [5, 0, 7, 8],
        [9, 10, 0, 12],
        [13, 14, 15, 16],
    ]


def empty_grid() -> list[list[int]]:
    """4x4 grid filled with zeros."""
    return [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
