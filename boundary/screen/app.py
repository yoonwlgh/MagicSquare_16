"""Application entry for the PyQt magic square screen."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from boundary.screen.main_window import MagicSquareMainWindow


def main() -> int:
    """Launch the desktop GUI and return the Qt exit code."""
    app = QApplication(sys.argv)
    window = MagicSquareMainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
