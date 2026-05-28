"""Control layer for user-related use-cases."""

from __future__ import annotations

from entity.user import User


class UserControl:
    """Coordinates user use-cases between boundary and entity layers."""

    def create_user(self, user_id: int, name: str, email: str) -> User:
        """Create a user entity with validated domain values.

        Args:
            user_id: Positive user identifier.
            name: User display name.
            email: User email address.

        Returns:
            User: Newly created user entity.

        Raises:
            ValueError: If domain validation fails.
        """
        return User(user_id=user_id, name=name, email=email)
