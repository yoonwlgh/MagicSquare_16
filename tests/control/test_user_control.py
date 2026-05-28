"""Tests for the control layer UserControl."""

import pytest

from control.user_control import UserControl


def test_create_user_returns_entity_with_input_values() -> None:
    """should create active user when valid values are provided"""
    # Arrange
    user_control = UserControl()

    # Act
    user = user_control.create_user(user_id=10, name="Bob", email="bob@example.com")

    # Assert
    assert user.user_id == 10
    assert user.name == "Bob"
    assert user.email == "bob@example.com"
    assert user.is_active is True


def test_create_user_raises_error_when_domain_validation_fails() -> None:
    """should raise ValueError when email format is invalid"""
    # Arrange
    user_control = UserControl()

    # Act / Assert
    with pytest.raises(ValueError, match="email must be a valid email format."):
        user_control.create_user(user_id=1, name="Bob", email="invalid-email")
