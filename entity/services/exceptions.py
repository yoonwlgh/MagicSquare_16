"""Solver domain exceptions (FR-05)."""


class SolverNoSolutionError(Exception):
    """Raised when neither small-first nor reverse placement yields a magic square."""
