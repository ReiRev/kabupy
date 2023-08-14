import os

import pytest
import requests_mock
from money import Money

import kabupy

url_directory = "reportTarget"


class TestReportTarget:
    @pytest.mark.parametrize(
        "security_code,expected",
        [(6758, Money("13438", "JPY")), (7837, None)],
    )
    def test_per_based_theoretical_stock_price(self, helpers, security_code, expected):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/reportTarget?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).per_based_theoretical_stock_price == expected

    @pytest.mark.parametrize(
        "security_code,expected",
        [(6758, Money("14424", "JPY")), (7837, None)],
    )
    def test_per_based_upside_target(self, helpers, security_code, expected):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).per_based_upside_target == expected

    @pytest.mark.parametrize(
        "security_code,expected",
        [(6758, Money("12451", "JPY")), (7837, None)],
    )
    def test_per_based_downside_target(self, helpers, security_code, expected):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).per_based_downside_target == expected

    @pytest.mark.parametrize(
        "security_code,expected",
        [(6758, Money("12797", "JPY")), (7837, Money("438", "JPY"))],
    )
    def test_pbr_based_theoretical_stock_price(self, helpers, security_code, expected):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).pbr_based_theoretical_stock_price == expected

    @pytest.mark.parametrize(
        "security_code,expected",
        [(6758, Money("13542", "JPY")), (7837, Money("624", "JPY"))],
    )
    def test_pbr_based_upside_target(self, helpers, security_code, expected):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).pbr_based_upside_target == expected

    @pytest.mark.parametrize(
        "security_code,expected",
        [(6758, Money("12053", "JPY")), (7837, Money("253", "JPY"))],
    )
    def test_pbr_based_downside_target(self, helpers, security_code, expected):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).pbr_based_downside_target == expected

    @pytest.mark.parametrize(
        "security_code,expected",
        [(6758, Money("16197", "JPY")), (7837, None)],
    )
    def test_price_target(self, helpers, security_code, expected):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).price_target == expected

    @pytest.mark.parametrize(
        "security_code,expected",
        [(6758, 4.75), (7837, None)],
    )
    def test_average_analyst_rating(self, helpers, security_code, expected):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).average_analyst_rating == expected

    @pytest.mark.parametrize(
        "security_code,expected",
        [(6758, 16), (7837, 0)],
    )
    def test_analyst_count(self, helpers, security_code, expected):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).analyst_count == expected

    @pytest.mark.parametrize(
        "security_code,expected",
        [(6758, Money("5674", "JPY")), (7837, Money("208", "JPY"))],
    )
    def test_actual_bps(self, helpers, security_code, expected):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).actual_bps == expected

    @pytest.mark.parametrize(
        "security_code,expected",
        [(6758, Money("696.8", "JPY")), (7837, Money("660.3", "JPY"))],
    )
    def test_expected_eps(self, helpers, security_code, expected):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).expected_eps == expected

    @pytest.mark.parametrize(
        "security_code,expected",
        [(6758, Money("777.1", "JPY")), (7837, None)],
    )
    def test_analyst_expected_eps(self, helpers, security_code, expected):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).analyst_expected_eps == expected

    @pytest.mark.parametrize(
        "security_code,expected",
        [(6758, 16.2), (7837, None)],
    )
    def test_analyst_expected_epr(self, helpers, security_code, expected):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).analyst_expected_epr == expected
