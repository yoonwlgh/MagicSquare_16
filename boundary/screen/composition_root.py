"""Composition root for the PyQt magic square desktop screen."""

from __future__ import annotations

from boundary.screen.main_window import MagicSquareMainWindow
from boundary.screen.presenter import MagicSquareScreenPresenter


def create_magic_square_presenter() -> MagicSquareScreenPresenter:
    """Wire default ECB dependencies for the screen presenter."""
    return MagicSquareScreenPresenter()


def create_magic_square_main_window(
    presenter: MagicSquareScreenPresenter | None = None,
) -> MagicSquareMainWindow:
    """Create the main window with an optional injected presenter."""
    return MagicSquareMainWindow(
        presenter=presenter or create_magic_square_presenter(),
    )
