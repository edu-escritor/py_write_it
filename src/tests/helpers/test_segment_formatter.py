import pytest

from writeit.enums.locales import Locales
from writeit.errors.validation_error import ValidationError
from writeit.helpers.segment_formatter import SegmentFormatter


class TestSegmentFormatter:

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (1, "p01"),
            (12, "p12"),
            (99, "p99"),
            ("5", "p05"),
            (0, ""),
            ("0", ""),
        ],
    )
    def test_part(self, value: int | str, expected: str) -> None:
        assert SegmentFormatter.part(value) == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (0, "00"),
            (1, "01"),
            (12, "12"),
            (99, "99"),
            ("5", "05"),
        ],
    )
    def test_part_value(self, value: int | str, expected: str) -> None:
        assert SegmentFormatter.part_value(value) == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (1, "parte-01"),
            (5, "parte-05"),
            (12, "parte-12"),
            ("3", "parte-03"),
        ],
    )
    def test_part_slug(self, value: int | str, expected: str) -> None:
        assert (
            SegmentFormatter.part_slug(
                value,
                Locales.PORTUGUESE_EUROPEAN,
            )
            == expected
        )

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (1, "Parte um"),
            (2, "Parte dois"),
            (10, "Parte dez"),
        ],
    )
    def test_part_title(self, value: int | str, expected: str) -> None:
        assert (
            SegmentFormatter.part_title(
                value,
                Locales.PORTUGUESE_EUROPEAN,
            )
            == expected
        )

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (1, "i0001"),
            (10, "i0010"),
            (100, "i0100"),
            (9999, "i9999"),
            ("20", "i0020"),
            (0, ""),
            ("0", ""),
        ],
    )
    def test_index(self, value: int | str, expected: str) -> None:
        assert SegmentFormatter.index(value) == expected

    def test_index_allow_zero(self) -> None:
        assert SegmentFormatter.index(0, allow_zero=True) == "i0000"

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (0, "0000"),
            (1, "0001"),
            (20, "0020"),
            (9999, "9999"),
            ("5", "0005"),
        ],
    )
    def test_index_value(self, value: int | str, expected: str) -> None:
        assert SegmentFormatter.index_value(value) == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (1, "v01"),
            (5, "v05"),
            (10, "v10"),
            (99, "v99"),
            ("7", "v07"),
            (0, ""),
            ("0", ""),
        ],
    )
    def test_version(self, value: int | str, expected: str) -> None:
        assert SegmentFormatter.version(value) == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (0, "00"),
            (1, "01"),
            (5, "05"),
            (10, "10"),
            (99, "99"),
            ("7", "07"),
        ],
    )
    def test_version_value(self, value: int | str, expected: str) -> None:
        assert SegmentFormatter.version_value(value) == expected

    @pytest.mark.parametrize(
        ("method", "value"),
        [
            (SegmentFormatter.part, -1),
            (SegmentFormatter.part_value, -1),
            (SegmentFormatter.index, -1),
            (SegmentFormatter.index_value, -1),
            (SegmentFormatter.version, -1),
            (SegmentFormatter.version_value, -1),
        ],
    )
    def test_negative_value_raises_validation_error(
        self,
        method,
        value: int,
    ) -> None:
        with pytest.raises(ValidationError):
            method(value)

    @pytest.mark.parametrize(
        ("method", "value"),
        [
            (SegmentFormatter.part, 100),
            (SegmentFormatter.part_value, 100),
            (SegmentFormatter.index, 10000),
            (SegmentFormatter.index_value, 10000),
            (SegmentFormatter.version, 100),
            (SegmentFormatter.version_value, 100),
        ],
    )
    def test_value_exceeding_digits_raises_validation_error(
        self,
        method,
        value: int,
    ) -> None:
        with pytest.raises(ValidationError):
            method(value)
