import os

import pytest
import requests_mock
from money import Money

import kabupy

url_directory = "reportTop"


class TestReportTop:
    @pytest.mark.parametrize(
        "security_code,expected",
        [(6758, Money("12565", "JPY")), (7837, Money("485", "JPY"))],
    )
    def test_stock_price(self, helpers, security_code, expected):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).price == expected

    @pytest.mark.parametrize(
        "security_code,expected",
        [(6758, 18.0), (7837, 0.7)],
    )
    def test_expected_per(self, helpers, security_code, expected):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).expected_per == expected

    @pytest.mark.parametrize(
        "security_code,expected",
        [(6758, 2.21), (7837, 2.33)],
    )
    def test_actual_pbr(self, helpers, security_code, expected):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).actual_pbr == expected

    @pytest.mark.parametrize(
        "security_code,expected",
        [(6758, 3.00), (7837, 11.53)],
    )
    def test_actual_roa(self, helpers, security_code, expected):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).actual_roa == expected

    @pytest.mark.parametrize(
        "security_code,expected",
        [(6758, Money("15_845_500_000_000", "JPY")), (7837, Money("2_200_000_000", "JPY"))],
    )
    def test_market_capitalization(self, helpers, security_code, expected):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).market_capitalization == expected