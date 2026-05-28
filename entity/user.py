"""User entity for the MagicSquare ECB architecture."""

from __future__ import annotations

from dataclasses import dataclass
import re


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class User:
    """Represents a domain user with validation rules.

    Attributes:
        user_id: Positive identifier for the user.
        name: Display name with at least 2 non-space characters.
        email: Valid email address used as a unique contact point.
        is_active: Indicates whether the user can use the system.
    """

    user_id: int
    name: str
    email: str
    is_active: bool = True

    def __post_init__(self) -> None:
        """Validate invariant rules after dataclass initialization.

        Raises:
            ValueError: If any domain invariant is violated.
        """
        self._validate_user_id(self.user_id)
        self._validate_name(self.name)
        self._validate_email(self.email)

    def activate(self) -> None:
        """Activate this user.

        This operation changes only the active-state flag.
        """
        self.is_active = True

    def deactivate(self) -> None:
        """Deactivate this user.

        This operation changes only the active-state flag.
        """
        self.is_active = False

    @staticmethod
    def _validate_user_id(user_id: int) -> None:
        """Validate user id.

        Args:
            user_id: Identifier candidate.

        Raises:
            ValueError: If id is not a positive integer.
        """
        if user_id <= 0:
            raise ValueError("user_id must be a positive integer.")

    @staticmethod
    def _validate_name(name: str) -> None:
        """Validate name.

        Args:
            name: Name candidate.

        Raises:
            ValueError: If name is too short after trimming.
        """
        if len(name.strip()) < 2:
            raise ValueError("name must contain at least 2 characters.")

    @staticmethod
    def _validate_email(email: str) -> None:
        """Validate email format.

        Args:
            email: Email candidate.

        Raises:
            ValueError: If email format is invalid.
        """
        if not EMAIL_PATTERN.match(email):
            raise ValueError("email must be a valid email format.")
