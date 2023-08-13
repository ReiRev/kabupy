import pytest

from kabupy.util import str2float


class TestStr2Money:
    @pytest.mark.parametrize(
        "value,expected",
        [("0.00%", 0.0)],
    )
    def test_str2money(self, value, expected):
        assert str2float(value) == expected
