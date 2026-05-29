"""Boundary input validator facade (FR-01, OPEN-04).

Canonical implementation: ``boundary.magic_square.boundary_validator.BoundaryValidator``.
"""

from __future__ import annotations

from boundary.magic_square.boundary_validator import BoundaryValidator

InputValidator = BoundaryValidator

__all__ = ["BoundaryValidator", "InputValidator"]
