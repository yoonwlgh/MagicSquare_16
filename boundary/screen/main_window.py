"""PyQt main window for 4x4 magic square validation and solve."""

from __future__ import annotations

from collections.abc import Callable

from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget

from boundary.magic_square.contracts import (
    BLANK_CELL_VALUE,
    GRID_SIZE,
    ErrorResponse,
)
from control.application_contracts import ApplicationError
from boundary.screen.layout_builder import MagicSquareLayoutBuilder
from boundary.screen.presenter import MagicSquareScreenPresenter
from boundary.screen.sample_grids import (
    grid_invalid_blank_count_sample,
    grid_reverse_success_sample,
    grid_small_first_success_sample,
)


class MagicSquareMainWindow(QMainWindow):
    """Desktop UI for FR-01 validation and FR-05 solve flows."""

    def __init__(self, presenter: MagicSquareScreenPresenter) -> None:
        """Build the grid editor and wire actions to the presenter."""
        super().__init__()
        self._presenter = presenter
        parts = MagicSquareLayoutBuilder().build(self)
        self._cells = parts.cells
        self._result_label = parts.result_label
        parts.validate_button.clicked.connect(self._on_validate)
        parts.solve_button.clicked.connect(self._on_solve)
        self._wire_sample_buttons()

    def _wire_sample_buttons(self) -> None:
        """Attach sample-load actions below the grid editor."""
        central = self.centralWidget()
        assert central is not None
        root = central.layout()
        assert isinstance(root, QVBoxLayout)

        sample_row = QHBoxLayout()
        sample_row.addWidget(self._make_button("Reverse sample", grid_reverse_success_sample))
        sample_row.addWidget(
            self._make_button("Small-first sample", grid_small_first_success_sample)
        )
        sample_row.addWidget(
            self._make_button("Invalid blanks (×3)", grid_invalid_blank_count_sample)
        )
        sample_row.addWidget(self._make_button("Clear", self._clear_grid))
        root.insertLayout(1, sample_row)

    def _make_button(
        self, label: str, loader: Callable[[], list[list[int]]]
    ) -> QPushButton:
        """Create a sample-load button."""
        button = QPushButton(label)
        button.clicked.connect(lambda: self._load_grid(loader()))
        return button

    def _clear_grid(self) -> list[list[int]]:
        """Return an empty 4x4 grid for the Clear sample action."""
        return [[BLANK_CELL_VALUE for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def _load_grid(self, grid: list[list[int]]) -> None:
        """Fill spin boxes from a 4x4 matrix."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self._cells[row][col].setValue(grid[row][col])
        self._show_info("Grid loaded. Click Validate or Solve.")

    def _read_grid(self) -> list[list[int]]:
        """Read current spin box values as int[][]."""
        return [
            [self._cells[row][col].value() for col in range(GRID_SIZE)]
            for row in range(GRID_SIZE)
        ]

    def _on_validate(self) -> None:
        """Handle Validate button — boundary checks only."""
        result = self._presenter.validate(self._read_grid())
        if isinstance(result, (ErrorResponse, ApplicationError)):
            self._show_error(self._presenter.format_error(result))
            return
        self._show_success("Validation passed (FR-01). Grid is ready for solve.")

    def _on_solve(self) -> None:
        """Handle Solve button — validate then domain solver."""
        outcome = self._presenter.solve(self._read_grid())
        if isinstance(outcome, (ErrorResponse, ApplicationError)):
            self._show_error(self._presenter.format_error(outcome))
            return
        formatted = self._presenter.format_success(outcome)
        self._show_success(self._presenter.format_success_message(formatted))

    def _show_error(self, message: str) -> None:
        """Display failure styling and message."""
        self._result_label.setStyleSheet("color: #b00020; font-weight: bold;")
        self._result_label.setText(message)

    def _show_success(self, message: str) -> None:
        """Display success styling and message."""
        self._result_label.setStyleSheet("color: #1b5e20; font-weight: bold;")
        self._result_label.setText(message)

    def _show_info(self, message: str) -> None:
        """Display neutral status message."""
        self._result_label.setStyleSheet("color: #333333;")
        self._result_label.setText(message)
