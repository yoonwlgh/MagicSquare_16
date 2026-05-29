"""Renders magic-square use-case outcomes for the desktop UI."""

from __future__ import annotations

from boundary.magic_square.contracts import ErrorResponse
from control.application_contracts import ApplicationError


class ViewFormatter:
    """Formats structured DTOs and success payloads into user-visible strings."""

    def format_error(self, response: ErrorResponse | ApplicationError) -> str:
        """Render structured failure for the UI."""
        return f"{response.code}: {response.message}"

    def format_success_message(self, result: list[int]) -> str:
        """Render success int[6] for the UI."""
        return f"Success: {result}"
