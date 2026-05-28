"""Tests for the User entity."""

import pytest

from entity.user import User


def test_create_user_with_valid_data() -> None:
    """should create user when input satisfies domain rules"""
    # Arrange
    user_id = 1
    name = "Alice"
    email = "alice@example.com"

    # Act
    user = User(user_id=user_id, name=name, email=email)

    # Assert
    assert user.user_id == 1
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.is_active is True


@pytest.mark.parametrize("invalid_user_id", [0, -1, -99])
def test_raise_error_when_user_id_is_not_positive(invalid_user_id: int) -> None:
    """should raise ValueError when user_id is not positive"""
    # Arrange
    name = "Alice"
    email = "alice@example.com"

    # Act / Assert
    with pytest.raises(ValueError, match="user_id must be a positive integer."):
        User(user_id=invalid_user_id, name=name, email=email)


@pytest.mark.parametrize("invalid_name", ["", " ", "A"])
def test_raise_error_when_name_is_too_short(invalid_name: str) -> None:
    """should raise ValueError when trimmed name length is below minimum"""
    # Arrange
    user_id = 1
    email = "alice@example.com"

    # Act / Assert
    with pytest.raises(ValueError, match="name must contain at least 2 characters."):
        User(user_id=user_id, name=invalid_name, email=email)


@pytest.mark.parametrize("invalid_email", ["invalid", "a@", "@example.com", "a b@c.com"])
def test_raise_error_when_email_format_is_invalid(invalid_email: str) -> None:
    """should raise ValueError when email format does not match rule"""
    # Arrange
    user_id = 1
    name = "Alice"

    # Act / Assert
    with pytest.raises(ValueError, match="email must be a valid email format."):
        User(user_id=user_id, name=name, email=invalid_email)


def test_deactivate_user() -> None:
    """should deactivate user when deactivate is called"""
    # Arrange
    user = User(user_id=1, name="Alice", email="alice@example.com")

    # Act
    user.deactivate()

    # Assert
    assert user.is_active is False


def test_activate_user() -> None:
    """should activate user when activate is called"""
    # Arrange
    user = User(user_id=1, name="Alice", email="alice@example.com", is_active=False)

    # Act
    user.activate()

    # Assert
    assert user.is_active is True
