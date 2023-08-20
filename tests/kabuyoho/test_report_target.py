import os

import pytest
import requests_mock
from money import Money

import kabupy

url_directory = "reportTarget"


class TestReportTarget:
    @pytest.mark.parametrize(
        "security_code,expected_values",
        [
            (
                6758,
                {
                    "per_based_theoretical_stock_price": Money("13438", "JPY"),
                    "per_based_upside_target": Money("14424", "JPY"),
                    "per_based_downside_target": Money("12451", "JPY"),
                    "pbr_based_theoretical_stock_price": Money("12797", "JPY"),
                    "pbr_based_upside_target": Money("13542", "JPY"),
                    "pbr_based_downside_target": Money("12053", "JPY"),
                    "price_target": Money("16197", "JPY"),
                    "average_analyst_rating": 4.75,
                    "analyst_count": 16,
                    "actual_bps": Money("5674", "JPY"),
                    "expected_eps": Money("696.8", "JPY"),
                    "analyst_expected_eps": Money("777.1", "JPY"),
                    "analyst_expected_epr": 16.2,
                },
            ),
            (
                7837,
                {
                    "per_based_theoretical_stock_price": None,
                    "per_based_upside_target": None,
                    "per_based_downside_target": None,
                    "pbr_based_theoretical_stock_price": Money("438", "JPY"),
                    "pbr_based_upside_target": Money("624", "JPY"),
                    "pbr_based_downside_target": Money("253", "JPY"),
                    "price_target": None,
                    "average_analyst_rating": None,
                    "analyst_count": 0,
                    "actual_bps": Money("208", "JPY"),
                    "expected_eps": Money("660.3", "JPY"),
                    "analyst_expected_eps": None,
                    "analyst_expected_epr": None,
                },
            ),
        ],
    )
    def test_properties(self, helpers, security_code, expected_values: dict):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}", text=text)
            for k, v in expected_values.items():
                assert getattr(kabupy.kabuyoho.stock(security_code).report_target, k) == v
