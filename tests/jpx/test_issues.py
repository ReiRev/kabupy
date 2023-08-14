import os

import requests_mock

import kabupy


class TestIssues:
    def test_issues_link(self, helpers):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "html/issues.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get("https://www.jpx.co.jp/markets/statistics-equities/misc/01.html", text=text)
            assert (
                kabupy.jpx.issues_link
                == "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
            )

    def test_actual_dividend_yield(self, helpers):
        bytes = helpers.excel2bytes(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "excel/issues.xls",
            )
        )
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "html/issues.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get("https://www.jpx.co.jp/markets/statistics-equities/misc/01.html", text=text)
            m.get(
                "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls", content=bytes
            )
            assert kabupy.jpx.issues
            assert kabupy.jpx.issues[0]['security_code'] == 1234
            assert kabupy.jpx.issues[1]['security_code'] == 1333
            assert kabupy.jpx.issues[0]['name'] == 'Foo'
            assert kabupy.jpx.issues[1]['name'] == 'Bar'
