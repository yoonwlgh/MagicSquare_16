"""Maps domain solver failures to application-layer error contracts."""

from __future__ import annotations

from control.application_contracts import (
    CONTROL_LAYER,
    ERR_SOLVER_NO_SOLUTION_CODE,
    ERR_SOLVER_NO_SOLUTION_MESSAGE,
    ApplicationError,
)
from entity.services.exceptions import SolverNoSolutionError


class SolverErrorMapper:
    """Translates Solver domain exceptions into structured application errors."""

    def from_solver_no_solution(
        self, error: SolverNoSolutionError
    ) -> ApplicationError:
        """Map exhausted solve attempts to the Control-layer error contract."""
        _ = error
        return ApplicationError(
            code=ERR_SOLVER_NO_SOLUTION_CODE,
            message=ERR_SOLVER_NO_SOLUTION_MESSAGE,
            layer=CONTROL_LAYER,
        )
