import pytest
from money import Money

from kabupy.util import str2money


class TestStr2Money:
    @pytest.mark.parametrize(
        "price,expected",
        [("692円", Money("692", "JPY")), ("5,210円", Money("5210", "JPY")), ("1億円", Money("100_000_000", "JPY"))],
    )
    def test_str2money(self, price, expected):
        assert str2money(price) == expected
