import logging
import os

import pytest
import requests_mock

import kabupy
from kabupy.base.decorators import webpage_property
from kabupy.errors import ElementNotFoundError

url_directory = "reportTrendSignal"

logger = logging.Logger(__name__)


class TestTrendSignal:
    @pytest.mark.parametrize(
        "security_code,expected_values",
        [
            (
                6758,
                {
                    "trend_signal": "買い継続",
                    "coincident_index": 0.05,
                    "leading_index": 0.08,
                    "risk_on_relative_index_level": "底値圏突入",
                },
            ),
            (
                7837,
                {
                    "trend_signal": "ニュートラル",
                    "coincident_index": 0.75,
                    "leading_index": 0.74,
                    "risk_on_relative_index_level": None,
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
                assert getattr(kabupy.kabuyoho.stock(security_code).report_trend_signal, k) == v

    def test_raise_element_not_found_error(self, helpers):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "html/no-body.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode=6758", text=text)
            page = kabupy.kabuyoho.stock(6758).report_trend_signal
            for k, v in page.__class__.__dict__.items():
                if isinstance(v, webpage_property):
                    logger.debug(f"Testing {k}")
                    with pytest.raises(ElementNotFoundError):
                        getattr(page, k)
