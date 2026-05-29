"""AC-FR-01-01 RED tests: invalid grid shape / None input (FR-01, I-1)."""

from __future__ import annotations

import importlib
import inspect
from unittest.mock import MagicMock

import pytest

from boundary.magic_square.boundary_validator import BoundaryValidator
from boundary.magic_square.contracts import (
    FORBIDDEN_OUT_OF_SCOPE_ERROR_CODES,
    ERR_INVALID_SHAPE_CODE,
    ERR_INVALID_SHAPE_MESSAGE,
    BOUNDARY_LAYER,
    ErrorResponse,
)
from control.magic_square_control import MagicSquareControl
from tests.boundary.conftest import grid_3x4, grid_empty_rows_four

AC_DOCSTRING = (
    "AC-FR-01-01, PRD §8.1 INVALID_SIZE — grid shape must be 4x4 before Domain resolve()."
)


class TestAcFr0101NormalFailureReturn:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — happy path of failure for invalid grid."""

    # AC-FR-01-01
    def test_grid_none_returns_invalid_size_error_response(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — None grid returns structured failure."""
        # Given
        grid = None

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == ERR_INVALID_SHAPE_CODE
        assert result.message == ERR_INVALID_SHAPE_MESSAGE

    # AC-FR-01-01
    def test_grid_none_failure_code_is_invalid_size_string(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — failure code literal match."""
        # Given
        grid = None

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.code == "ERR_INVALID_SHAPE"

    # AC-FR-01-01
    def test_grid_none_failure_message_is_grid_must_be_4x4(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — failure message literal match."""
        # Given
        grid = None

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.message == "Input must be a 4x4 integer matrix."

    # AC-FR-01-01
    def test_grid_none_failure_layer_is_boundary(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — failure attributed to Boundary layer."""
        # Given
        grid = None

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.layer == BOUNDARY_LAYER

    # AC-FR-01-01
    def test_grid_none_returns_pydantic_error_response_model(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — failure type is ErrorResponse contract."""
        # Given
        grid = None

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert isinstance(result, ErrorResponse)


class TestAcFr0101BoundaryValues:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — boundary value grids rejected as invalid size."""

    # AC-FR-01-01
    def test_grid_empty_list_returns_invalid_size_failure(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — empty list is not 4x4."""
        # Given
        grid: list[list[int]] = []

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == ERR_INVALID_SHAPE_CODE
        assert result.message == ERR_INVALID_SHAPE_MESSAGE

    # AC-FR-01-01
    def test_grid_four_empty_rows_returns_invalid_size_failure(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — four rows with no columns rejected."""
        # Given
        grid = grid_empty_rows_four()

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == ERR_INVALID_SHAPE_CODE

    # AC-FR-01-01
    def test_grid_four_empty_rows_via_repeat_pattern_returns_invalid_size(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — [[]] * 4 shape rejected."""
        # Given
        grid = [[]] * 4

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.message == ERR_INVALID_SHAPE_MESSAGE

    # AC-FR-01-01
    def test_grid_3x4_matrix_returns_invalid_size_failure(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — three by four matrix rejected."""
        # Given
        grid = grid_3x4()

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == ERR_INVALID_SHAPE_CODE
        assert result.message == ERR_INVALID_SHAPE_MESSAGE

    # AC-FR-01-01
    def test_grid_4x3_matrix_returns_invalid_size_failure(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — four by three matrix rejected."""
        # Given
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == ERR_INVALID_SHAPE_CODE


class TestAcFr0101DomainIsolation:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — resolve() must not run on shape failure."""

    # AC-FR-01-01
    def test_grid_none_resolve_call_count_zero(
        self,
        magic_square_control: MagicSquareControl,
        domain_resolver_mock: MagicMock,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — None grid does not invoke resolve()."""
        # Given
        grid = None

        # When
        magic_square_control.solve(grid)

        # Then
        assert domain_resolver_mock.resolve.call_count == 0

    # AC-FR-01-01
    def test_grid_empty_list_resolve_never_called(
        self,
        magic_square_control: MagicSquareControl,
        domain_resolver_mock: MagicMock,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — empty grid blocks resolve()."""
        # Given
        grid: list[list[int]] = []

        # When
        magic_square_control.solve(grid)

        # Then
        domain_resolver_mock.resolve.assert_not_called()

    # AC-FR-01-01
    def test_grid_four_empty_rows_resolve_call_count_zero(
        self,
        magic_square_control: MagicSquareControl,
        domain_resolver_mock: MagicMock,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — zero-width rows block resolve()."""
        # Given
        grid = grid_empty_rows_four()

        # When
        magic_square_control.solve(grid)

        # Then
        assert domain_resolver_mock.resolve.call_count == 0

    # AC-FR-01-01
    def test_grid_3x4_resolve_call_count_zero(
        self,
        magic_square_control: MagicSquareControl,
        domain_resolver_mock: MagicMock,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 3x4 grid blocks resolve()."""
        # Given
        grid = grid_3x4()

        # When
        magic_square_control.solve(grid)

        # Then
        assert domain_resolver_mock.resolve.call_count == 0

    # AC-FR-01-01
    def test_grid_none_solve_returns_boundary_error_without_resolve(
        self,
        magic_square_control: MagicSquareControl,
        domain_resolver_mock: MagicMock,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — solve returns error and skips resolve()."""
        # Given
        grid = None

        # When
        result = magic_square_control.solve(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == ERR_INVALID_SHAPE_CODE
        assert domain_resolver_mock.resolve.call_count == 0


class TestAcFr0101MessageIdentity:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — message string identity (character-level)."""

    # AC-FR-01-01
    def test_grid_none_message_exact_prd_contract_string(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — message equals contract constant."""
        # Given
        grid = None
        expected = "Input must be a 4x4 integer matrix."

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.message == expected
        assert len(result.message) == len(expected)

    # AC-FR-01-01
    def test_grid_empty_list_message_character_for_character_match(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — empty grid message identity."""
        # Given
        grid: list[list[int]] = []

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert list(result.message) == list(ERR_INVALID_SHAPE_MESSAGE)

    # AC-FR-01-01
    def test_grid_four_empty_rows_message_no_extra_whitespace(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — no leading or trailing whitespace."""
        # Given
        grid = grid_empty_rows_four()

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.message.strip() == result.message
        assert result.message == ERR_INVALID_SHAPE_MESSAGE

    # AC-FR-01-01
    def test_grid_3x4_message_equals_invalid_size_constant(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 3x4 uses same message as None case."""
        # Given
        grid = grid_3x4()

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.message == ERR_INVALID_SHAPE_MESSAGE
        assert repr(result.message) == repr("Input must be a 4x4 integer matrix.")

    # AC-FR-01-01
    def test_grid_repeat_empty_rows_message_byte_identity(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — [[]]*4 message byte-for-byte match."""
        # Given
        grid = [[]] * 4

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.message.encode("utf-8") == ERR_INVALID_SHAPE_MESSAGE.encode("utf-8")


class TestAcFr0101ScopeRestriction:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — AC-FR-01-02~05 / FR-02~05 out of scope."""

    # AC-FR-01-01
    def test_grid_none_does_not_return_blank_count_error_code(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — not AC-FR-01-02 blank count error."""
        # Given
        grid = None

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.code != "ERR_INVALID_BLANK_COUNT"

    # AC-FR-01-01
    def test_grid_none_does_not_return_out_of_range_error_code(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — not AC-FR-01-03 value range error."""
        # Given
        grid = None

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.code != "ERR_OUT_OF_RANGE"

    # AC-FR-01-01
    def test_grid_none_does_not_return_duplicate_value_error_code(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — not AC-FR-01-04 duplicate error."""
        # Given
        grid = None

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.code != "ERR_DUPLICATE_VALUE"

    # AC-FR-01-01
    def test_grid_none_invalid_size_not_in_forbidden_solver_codes(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — not FR-05 solver failure code."""
        # Given
        grid = None

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert result is not None
        assert result.code == ERR_INVALID_SHAPE_CODE
        assert result.code not in FORBIDDEN_OUT_OF_SCOPE_ERROR_CODES

    # AC-FR-01-01
    def test_ac_fr01_01_module_has_no_fr02_fr05_domain_test_names(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — this RED module excludes FR-02~05 tests."""
        # Given
        module = importlib.import_module("tests.boundary.test_ac_fr01_01_invalid_size")
        forbidden_fragments = (
            "blank_count",
            "blank_finder",
            "missing_number",
            "magic_square_validator",
            "solver_no_solution",
            "valid_4x4",
            "int_six",
        )

        # When
        test_names = [
            name
            for name, obj in inspect.getmembers(module)
            if name.startswith("test_") and inspect.isfunction(obj)
        ]

        # Then
        for test_name in test_names:
            lowered = test_name.lower()
            for fragment in forbidden_fragments:
                assert fragment not in lowered, (
                    f"AC-FR-01-01 scope violation: {test_name} suggests FR-02~05"
                )


def grid_5x5() -> list[list[int]]:
    """Five rows and five columns — shape violation (TC-BND-006)."""
    return [[1, 2, 3, 4, 5] for _ in range(5)]


class TestAcFr0101ExtendedBoundaryContract:
    """TC-BND-006, TC-BND-DET-001, TC-BND-IMM-001 — shape edge and invariants."""

    # TC-BND-006
    def test_tc_bnd_006_five_by_five_matrix_returns_invalid_size(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """TC-BND-006 — 5×5 matrix rejects INVALID_SIZE before Domain."""
        # Given
        grid = grid_5x5()

        # When
        result = boundary_validator.validate(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == ERR_INVALID_SHAPE_CODE
        assert result.message == ERR_INVALID_SHAPE_MESSAGE
        assert result.layer == BOUNDARY_LAYER

    # TC-BND-DET-001
    def test_tc_bnd_det_001_validate_twice_returns_identical_error(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """TC-BND-DET-001 — same invalid grid validated twice yields identical response."""
        # Given
        grid = None

        # When
        first = boundary_validator.validate(grid)
        second = boundary_validator.validate(grid)

        # Then
        assert first is not None and second is not None
        assert first.code == second.code
        assert first.message == second.message
        assert first.layer == second.layer

    # TC-BND-IMM-001
    def test_tc_bnd_imm_001_validate_does_not_mutate_input_grid(
        self,
        boundary_validator: BoundaryValidator,
    ) -> None:
        """TC-BND-IMM-001 — validate leaves mutable grid snapshot unchanged."""
        # Given
        import copy

        grid = grid_3x4()
        before = copy.deepcopy(grid)

        # When
        boundary_validator.validate(grid)

        # Then
        assert grid == before
