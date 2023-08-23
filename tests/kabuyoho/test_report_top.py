import os

import pytest
import requests_mock
from money import Money

import kabupy

url_directory = "reportTop"


class TestReportTop:
    @pytest.mark.parametrize(
        "security_code,expected_values",
        [
            (
                6758,
                {
                    "price": Money("12565", "JPY"),
                    "expected_per": 18.0,
                    "actual_pbr": 2.21,
                    "actual_roa": 3.00,
                    "actual_roe": 13.04,
                    "equity_ratio": 22.6,
                    "market_capitalization": Money("15_845_500_000_000", "JPY"),
                    "signal": "売り継続",
                    "expected_ordinary_profit": Money("1_140_000_000_000", "JPY"),
                    "consensus_expected_ordinary_profit": Money("1_223_695_000_000", "JPY"),
                },
            ),
            (
                7837,
                {
                    "price": Money("485", "JPY"),
                    "expected_per": 0.7,
                    "actual_pbr": 2.33,
                    "actual_roa": 11.53,
                    "actual_roe": 87.08,
                    "equity_ratio": 7.9,
                    "market_capitalization": Money("2_200_000_000", "JPY"),
                    "signal": "売り継続",
                    "expected_ordinary_profit": Money("26_000_000", "JPY"),
                    "consensus_expected_ordinary_profit": None,
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
                assert getattr(kabupy.kabuyoho.stock(security_code).report_top, k) == v
