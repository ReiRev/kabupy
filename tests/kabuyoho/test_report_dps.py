import os

import pytest
import requests_mock

import kabupy

url_directory = "reportDps"


class TestReportDps:
    @pytest.mark.parametrize(
        "security_code,expected_values",
        [
            (
                6758,
                {
                    "actual_dividend_yield": 0.6,
                    "expected_dividend_yield": None,
                    "dividend_payout_ratio": 9.9,
                },
            ),
            (
                7837,
                {
                    "actual_dividend_yield": 0.0,
                    "expected_dividend_yield": 0.0,
                    "dividend_payout_ratio": 0.0,
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
                assert getattr(kabupy.kabuyoho.stock(security_code).report_dps, k) == v
