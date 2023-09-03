import logging
import os
from datetime import datetime

import pytest
import requests_mock

import kabupy
from kabupy.errors import ElementNotFoundError

url_directory = "reportNews"
logger = logging.getLogger(__name__)


class TestReportNews:
    @pytest.mark.parametrize(
        "security_code,expected_values",
        [
            (
                6758,
                [
                    {
                        "date": datetime(2023, 9, 2, 9, 22),
                        "title": "1日のNY市場はまちまち",
                        "category": "外国市場/為替",
                        "weather": None,
                        "url": "https://kabuyoho.jp/sp/fiscoNewsDetail?nid=0005330020230902001&bcode=6758",
                    },
                    {
                        "date": datetime(2023, 9, 2, 9, 20),
                        "title": "米国株式市場はまちまち、経済指標は強弱混在（1日）",
                        "category": "外国市場/為替",
                        "weather": None,
                        "url": "https://kabuyoho.jp/sp/fiscoNewsDetail?nid=0000050020230902001&bcode=6758",
                    },
                    {
                        "date": datetime(2023, 9, 2, 7, 15),
                        "title": "前日に動いた銘柄 part1　内田洋行、JDSC、四電工など",
                        "category": "銘柄/投資戦略",
                        "weather": None,
                        "url": "https://kabuyoho.jp/sp/fiscoNewsDetail?nid=0009350020230902001&bcode=6758",
                    },
                ],
            ),
            (
                7837,
                [
                    {
                        "date": datetime(2023, 5, 12, 17, 10),
                        "title": "ブロンコＢなどがランクイン",
                        "category": "市況・概要",
                        "weather": None,
                        "url": "https://kabuyoho.jp/sp/fiscoNewsDetail?nid=0005550020230512001&bcode=7837",
                    },
                    {
                        "date": datetime(2023, 4, 28, 17, 19),
                        "title": "テラスカイがランクイン",
                        "category": "市況・概要",
                        "weather": None,
                        "url": "https://kabuyoho.jp/sp/fiscoNewsDetail?nid=0005550020230428001&bcode=7837",
                    },
                    {
                        "date": datetime(2023, 4, 14, 17, 29),
                        "title": "正栄食品工業がランクイン",
                        "category": "市況・概要",
                        "weather": None,
                        "url": "https://kabuyoho.jp/sp/fiscoNewsDetail?nid=0005550020230414001&bcode=7837",
                    },
                ],
            ),
        ],
    )
    def test_market_report_single_page(self, helpers, security_code, expected_values: dict):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/market_report/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}&cat=1", text=text)
            assert kabupy.kabuyoho.stock(security_code).report_news.market_report.links == expected_values

    @pytest.mark.parametrize(
        "security_code,expected_values",
        [
            (
                6758,
                [
                    {
                        "date": datetime(2023, 8, 9, 15, 1),
                        "title": "2024年3月期連結第1四半期、税引前損益276,034百万円。IFISコンセンサスを上回る水準。",
                        "category": "決算",
                        "weather": "wthr_clud",
                        "url": "https://kabuyoho.jp/sp/"
                        "consNewsDetail?cat=1&nid=6758_20230809_act_20230809_150126_2&bcode=6758",
                    },
                    {
                        "date": datetime(2023, 4, 28, 15, 2),
                        "title": "2023年3月期連結、5.6%税引前増益。IFISコンセンサスを上回る水準。",
                        "category": "決算",
                        "weather": "wthr_clud",
                        "url": "https://kabuyoho.jp/sp/"
                        "consNewsDetail?cat=1&nid=6758_20230428_act_20230428_150217_1&bcode=6758",
                    },
                    {
                        "date": datetime(2023, 2, 2, 15, 0),
                        "title": "2023年3月期連結第3四半期(累計)、税引前損益1,035,711百万円。",
                        "category": "決算",
                        "weather": "wthr_clud",
                        "url": "https://kabuyoho.jp/sp/"
                        "consNewsDetail?cat=1&nid=6758_20230202_act_20230202_150027_1&bcode=6758",
                    },
                ],
            ),
            (
                7837,
                [
                    {
                        "date": datetime(2023, 8, 14, 15, 1),
                        "title": "2024年3月期連結第1四半期、経常損益62百万円。",
                        "category": "決算",
                        "weather": "wthr_clud",
                        "url": "https://kabuyoho.jp/sp/"
                        "consNewsDetail?cat=1&nid=7837_20230814_act_20230814_150116_1&bcode=7837",
                    },
                    {
                        "date": datetime(2023, 5, 15, 17, 30),
                        "title": "2023年3月期連結、経常赤字幅拡大。事前予想を下回る水準。",
                        "category": "決算",
                        "weather": "wthr_rain",
                        "url": "https://kabuyoho.jp/sp/"
                        "consNewsDetail?cat=1&nid=7837_20230515_act_20230515_173006_1&bcode=7837",
                    },
                    {
                        "date": datetime(2023, 2, 14, 16, 0),
                        "title": "2023年3月期連結第3四半期(累計)、経常損益-591百万円。",
                        "category": "決算",
                        "weather": "wthr_clud",
                        "url": "https://kabuyoho.jp/sp/"
                        "consNewsDetail?cat=1&nid=7837_20230214_act_20230214_160054_1&bcode=7837",
                    },
                ],
            ),
        ],
    )
    def test_flash_report(self, helpers, security_code, expected_values: dict):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/flash_report/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}&cat=2", text=text)
            assert kabupy.kabuyoho.stock(security_code).report_news.flash_report.links == expected_values

    def test_flash_report_raise_element_not_found_error(self, helpers):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "html/no-body.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode=6758&cat=2", text=text)
            with pytest.raises(ElementNotFoundError):
                kabupy.kabuyoho.stock(6758).report_news.flash_report.links
