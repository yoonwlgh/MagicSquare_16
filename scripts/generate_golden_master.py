#!/usr/bin/env python3
"""Generate or refresh tests/golden_master_expected.txt from current solver output."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from boundary.magic_square.boundary_validator import BoundaryValidator
from control.magic_square_control import MagicSquareControl
from control.magic_square_resolver import MagicSquareDomainResolver
from tests.golden_master.approval import (
    GOLDEN_MASTER_PATH,
    build_golden_master_document,
    write_golden_master,
)


def main() -> int:
    """Capture current solver output and write the Golden Master baseline."""
    control = MagicSquareControl(
        boundary_validator=BoundaryValidator(),
        resolver=MagicSquareDomainResolver(),
    )
    document = build_golden_master_document(control)
    write_golden_master(document)
    print(f"Wrote Golden Master baseline: {GOLDEN_MASTER_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
