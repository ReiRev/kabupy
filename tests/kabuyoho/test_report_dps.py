import os

import pytest
import requests_mock

import kabupy


class TestReportDps:
    @pytest.mark.parametrize(
        "security_code,actual_dividend_yield",
        [(6758, 0.6), (7837, 0.0)],
    )
    def test_actual_dividend_yield(self, helpers, security_code, actual_dividend_yield):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/reportDps/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/reportDps?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).actual_dividend_yield == actual_dividend_yield

    @pytest.mark.parametrize(
        "security_code,expected_dividend_yield",
        [(6758, None), (7837, 0.0)],
    )
    def test_expected_dividend_yield(self, helpers, security_code, expected_dividend_yield):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/reportDps/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/reportDps?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).expected_dividend_yield == expected_dividend_yield

    @pytest.mark.parametrize(
        "security_code,dividend_payout_ratio",
        [(6758, 9.9), (7837, 0.0)],
    )
    def test_dividend_payout_ratio(self, helpers, security_code, dividend_payout_ratio):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/reportDps/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/reportDps?bcode={security_code}", text=text)
            assert kabupy.kabuyoho.stock(security_code).dividend_payout_ratio == dividend_payout_ratio
