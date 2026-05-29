"""Control-layer port protocols for magic square orchestration."""

from __future__ import annotations

from typing import Any, Protocol

from control.application_contracts import ApplicationError


class ValidationPort(Protocol):
    """FR-01 validation entry; implemented by Boundary adapters."""

    def validate(self, grid: list[list[int]] | None) -> ApplicationError | None:
        """Return application error on failure; None when validation passes."""
        ...


class DomainResolver(Protocol):
    """Domain pipeline entry (FR-02~FR-05); must not run on validation failure."""

    def resolve(self, grid: list[list[int]]) -> Any:
        """Run domain solver pipeline on a validated grid."""
        ...
