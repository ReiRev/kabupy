import os

import pytest
import requests_mock
from money import Money

import kabupy


class TestStock:
    @pytest.mark.parametrize(
        "security_code,price",
        [(3260, Money("692", "JPY")), (5210, Money("1192", "JPY"))],
    )
    def test_stock_price(self, helpers, security_code, price):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/reportTop/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/reportTop?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).price == price

    @pytest.mark.parametrize(
        "security_code,market_capitalization",
        [(3260, 1_200_000_000), (5210, 13_300_000_000)],
    )
    def test_market_capitalization(self, helpers, security_code, market_capitalization):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/reportTop/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/reportTop?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).market_capitalization == Money(market_capitalization, "JPY")

    @pytest.mark.parametrize(
        "security_code,per_based_theoretical_stock_price",
        [(6758, Money("13438", "JPY")), (7837, None)],
    )
    def test_theoretical_stock_price(self, helpers, security_code, per_based_theoretical_stock_price):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/reportTarget/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/reportTarget?bcode={security_code}", text=text)
            assert (
                kabupy.kabuyoho.stock(security_code).per_based_theoretical_stock_price
                == per_based_theoretical_stock_price
            )
