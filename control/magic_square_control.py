"""Control orchestration for magic square solve use-case."""

from typing import Any

from control.application_contracts import ApplicationError
from control.ports import DomainResolver, ValidationPort


class MagicSquareControl:
    """Coordinates Boundary validation and Domain resolve()."""

    def __init__(
        self,
        boundary_validator: ValidationPort,
        resolver: DomainResolver,
    ) -> None:
        self._boundary_validator = boundary_validator
        self._resolver = resolver

    def solve(self, grid: list[list[int]] | None) -> ApplicationError | Any:
        """Validate grid at Boundary; call resolve only when validation passes."""
        validation_error = self._boundary_validator.validate(grid)
        if validation_error is not None:
            return validation_error
        return self._resolver.resolve(grid)