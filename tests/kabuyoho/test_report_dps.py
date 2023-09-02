import logging
import os
from datetime import datetime

import pytest
import requests_mock
from money import Money

import kabupy
from kabupy.base.decorators import webpage_property
from kabupy.errors import ElementNotFoundError

url_directory = "reportDps"
logger = logging.getLogger(__name__)


class TestReportDps:
    @pytest.mark.parametrize(
        "security_code,expected_values",
        [
            (
                6758,
                {
                    "dividend_history": [
                        {"date": datetime(2021, 3, 1), "dividend": Money("55.0", "JPY")},
                        {"date": datetime(2022, 3, 1), "dividend": Money("65.0", "JPY")},
                        {"date": datetime(2023, 3, 1), "dividend": Money("75.0", "JPY")},
                        {"date": datetime(2024, 3, 1), "dividend": None},
                    ],
                    "actual_dividend_yield": 0.6,
                    "expected_dividend_yield": None,
                    "dividend_payout_ratio": 9.9,
                },
            ),
            (
                7837,
                {
                    "dividend_history": [
                        {"date": datetime(2021, 3, 1), "dividend": Money("20.0", "JPY")},
                        {"date": datetime(2022, 3, 1), "dividend": Money("15.0", "JPY")},
                        {"date": datetime(2023, 3, 1), "dividend": Money("0.0", "JPY")},
                        {"date": datetime(2024, 3, 1), "dividend": Money("0.0", "JPY")},
                    ],
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

    def test_raise_element_not_found_error(self, helpers):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "html/no-body.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get("https://kabuyoho.jp/sp/reportDps?bcode=6758", text=text)
            page = kabupy.kabuyoho.stock(6758).report_dps
            for k, v in page.__class__.__dict__.items():
                if isinstance(v, webpage_property):
                    logger.debug(f"Testing {k}")
                    with pytest.raises(ElementNotFoundError):
                        getattr(page, k)
