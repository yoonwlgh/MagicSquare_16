"""CLI boundary adapters for user flows."""

from __future__ import annotations

from typing import Any

from control.user_control import UserControl


class UserCliBoundary:
    """Adapts external payloads to user control use-cases."""

    def __init__(self, user_control: UserControl) -> None:
        """Initialize boundary with control dependency.

        Args:
            user_control: Control layer coordinator for user flows.
        """
        self._user_control = user_control

    def handle_create_user(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Create a user and return a serializable response payload.

        Args:
            payload: External input containing user fields.

        Returns:
            dict[str, Any]: Serialized user data for boundary response.
        """
        user = self._user_control.create_user(
            user_id=int(payload["user_id"]),
            name=str(payload["name"]),
            email=str(payload["email"]),
        )
        return {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "is_active": user.is_active,
        }
