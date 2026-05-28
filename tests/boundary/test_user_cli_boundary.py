"""Tests for the boundary layer UserCliBoundary."""

from boundary.cli.user_cli_boundary import UserCliBoundary
from control.user_control import UserControl


def test_handle_create_user_returns_serialized_response() -> None:
    """should return serializable user payload when request is valid"""
    # Arrange
    boundary = UserCliBoundary(user_control=UserControl())
    payload = {"user_id": 7, "name": "Carol", "email": "carol@example.com"}

    # Act
    result = boundary.handle_create_user(payload=payload)

    # Assert
    assert result == {
        "user_id": 7,
        "name": "Carol",
        "email": "carol@example.com",
        "is_active": True,
    }
