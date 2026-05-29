"""Builds PyQt layout widgets for the magic square main window."""

from __future__ import annotations

from dataclasses import dataclass

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from boundary.magic_square.contracts import BLANK_CELL_VALUE, GRID_SIZE, MAX_CELL_VALUE


@dataclass(frozen=True)
class MagicSquareLayoutParts:
    """Widgets produced by the layout builder for event wiring."""

    cells: list[list[QSpinBox]]
    result_label: QLabel
    validate_button: QPushButton
    solve_button: QPushButton


class MagicSquareLayoutBuilder:
    """Assembles the 4×4 grid editor and result panel."""

    def build(self, window: QMainWindow) -> MagicSquareLayoutParts:
        """Construct widgets on the given main window and return handles."""
        window.setWindowTitle("Magic Square 4×4")
        window.setMinimumSize(520, 420)

        central = QWidget()
        window.setCentralWidget(central)
        root = QVBoxLayout(central)

        cells = self._build_grid_group(root)
        result_label = self._build_result_group(root)
        validate_button, solve_button = self._build_action_row(root)

        return MagicSquareLayoutParts(
            cells=cells,
            result_label=result_label,
            validate_button=validate_button,
            solve_button=solve_button,
        )

    def _build_grid_group(self, root: QVBoxLayout) -> list[list[QSpinBox]]:
        grid_group = QGroupBox("4×4 Grid (0 = blank, 1–16 = value)")
        grid_layout = QGridLayout(grid_group)
        cells: list[list[QSpinBox]] = []
        for row in range(GRID_SIZE):
            row_boxes: list[QSpinBox] = []
            for col in range(GRID_SIZE):
                spin = QSpinBox()
                spin.setRange(BLANK_CELL_VALUE, MAX_CELL_VALUE)
                spin.setSpecialValueText("·")
                spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
                grid_layout.addWidget(spin, row, col)
                row_boxes.append(spin)
            cells.append(row_boxes)
        root.addWidget(grid_group)
        return cells

    def _build_action_row(self, root: QVBoxLayout) -> tuple[QPushButton, QPushButton]:
        action_row = QHBoxLayout()
        validate_btn = QPushButton("Validate (FR-01)")
        solve_btn = QPushButton("Solve (FR-05)")
        action_row.addWidget(validate_btn)
        action_row.addWidget(solve_btn)
        root.addLayout(action_row)
        return validate_btn, solve_btn

    def _build_result_group(self, root: QVBoxLayout) -> QLabel:
        result_label = QLabel("Enter a 4×4 grid (0 = blank) and click Validate or Solve.")
        result_label.setWordWrap(True)
        result_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        result_group = QGroupBox("Result")
        result_layout = QVBoxLayout(result_group)
        result_layout.addWidget(result_label)
        root.addWidget(result_group)
        return result_label
