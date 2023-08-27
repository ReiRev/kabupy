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
                    "price_level_to_target": "割安",
                    "price_target": Money("16197", "JPY"),
                    "price_target_ratio_to_previous_week": -0.21,
                    "price_target_ratio_to_current_price": 28.90,
                    "average_analyst_rating": 4.75,
                    "analyst_count": 16,
                    "analyst_rating_composition": {
                        "1": 0,
                        "2": 0,
                        "3": 2,
                        "4": 0,
                        "5": 14,
                    },
                    "per_based_theoretical_stock_price": Money("13438", "JPY"),
                    "per_based_upside_target": Money("14424", "JPY"),
                    "per_based_downside_target": Money("12451", "JPY"),
                    "pbr_based_theoretical_stock_price": Money("12797", "JPY"),
                    "pbr_based_upside_target": Money("13542", "JPY"),
                    "pbr_based_downside_target": Money("12053", "JPY"),
                    "actual_bps": Money("5674", "JPY"),
                    "expected_eps": Money("696.8", "JPY"),
                    "analyst_expected_eps": Money("777.1", "JPY"),
                    "analyst_expected_epr": 16.2,
                },
            ),
            (
                7837,
                {
                    "price_level_to_target": None,
                    "price_target": None,
                    "price_target_ratio_to_previous_week": None,
                    "price_target_ratio_to_current_price": None,
                    "average_analyst_rating": None,
                    "analyst_count": 0,
                    "analyst_rating_composition": {
                        "1": 0,
                        "2": 0,
                        "3": 0,
                        "4": 0,
                        "5": 0,
                    },
                    "per_based_theoretical_stock_price": None,
                    "per_based_upside_target": None,
                    "per_based_downside_target": None,
                    "pbr_based_theoretical_stock_price": Money("438", "JPY"),
                    "pbr_based_upside_target": Money("624", "JPY"),
                    "pbr_based_downside_target": Money("253", "JPY"),
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
