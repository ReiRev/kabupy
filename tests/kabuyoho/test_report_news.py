import logging
import os
from datetime import datetime

import pytest
import requests_mock

import kabupy
from kabupy.base.decorators import webpage_property
from kabupy.errors import ElementNotFoundError

url_directory = "reportNews"
logger = logging.getLogger(__name__)


class TestReportNews:
    @pytest.mark.parametrize(
        "security_code,expected_values",
        [
            (
                6758,
                {
                    "news": [
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
                },
            ),
            (
                7837,
                {
                    "news": [
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
                assert getattr(kabupy.kabuyoho.stock(security_code).report_news, k) == v

    def test_raise_element_not_found_error(self, helpers):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "html/no-body.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get("https://kabuyoho.jp/sp/reportNews?bcode=6758", text=text)
            page = kabupy.kabuyoho.stock(6758).report_news
            for k, v in page.__class__.__dict__.items():
                if isinstance(v, webpage_property):
                    logger.debug(f"Testing {k}")
                    with pytest.raises(ElementNotFoundError):
                        getattr(page, k)
