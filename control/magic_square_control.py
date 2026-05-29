"""Control orchestration for magic square solve use-case."""

from typing import Any, Protocol

from boundary.magic_square.boundary_validator import BoundaryValidator
from boundary.magic_square.contracts import ErrorResponse


class DomainResolver(Protocol):
    """Domain pipeline entry (FR-02~FR-05); must not run on Boundary failure."""

    def resolve(self, grid: list[list[int]]) -> Any:
        """Run domain solver pipeline on a validated grid."""
        ...


class MagicSquareControl:
    """Coordinates Boundary validation and Domain resolve()."""

    def __init__(
        self,
        boundary_validator: BoundaryValidator,
        resolver: DomainResolver,
    ) -> None:
        self._boundary_validator = boundary_validator
        self._resolver = resolver

    def solve(self, grid: list[list[int]] | None) -> ErrorResponse | Any:
        """Validate grid at Boundary; call resolve only when validation passes.

        RED stub: always invokes resolve() so isolation tests fail until GREEN.
        """
        validation_error = self._boundary_validator.validate(grid)
        if validation_error is not None:
            return validation_error
        return self._resolver.resolve(grid)  # type: ignore[arg-type]
