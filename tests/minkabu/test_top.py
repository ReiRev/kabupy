import logging
import os

import pytest
import requests_mock
from money import Money

import kabupy

url_directory = "top"
logger = logging.getLogger(__name__)


class TestReportDps:
    @pytest.mark.parametrize(
        "security_code,expected_values",
        [
            (
                6758,
                {
                    "name": "ソニーグループ",
                    "market_segment": "tse_prime",
                    "price": Money("12930.0", "JPY"),
                    "business_category": "電気機器",
                    "business_description": "AV機器世界大手。映画、ゲーム、音楽、金融を展開。センサー等デバイス事業も拡大。",
                    "related_themes": [
                        "電気機器",
                        "国際優良株",
                        "ブルーレイ",
                        "プレイステーション",
                        "CMOSセンサー",
                        "ウェアラブル端末",
                        "4K・8Kテレビ",
                        "VR",
                        "一眼レフカメラ",
                        "AIスピーカー",
                    ],
                    "previous_close_price": Money("12645.0", "JPY"),
                    "open_price": Money("12840.0", "JPY"),
                    "daily_highest_price": Money("12980.0", "JPY"),
                    "daily_lowest_price": Money("12765.0", "JPY"),
                    "dividend_yield": None,
                    "share_unit": 100,
                    "adjusted_per": 17.04,
                    "psr": 1.41,
                    "pbr": 2.44,
                    "volume": 5199800,
                    "market_capitalization": Money("16_305_787_000_000", "JPY"),
                    "issued_shares": 1_261_081_000,
                    "shareholder_benefits": "自社商品割引券",
                    "lowest_purchase_price": Money("1_293_440", "JPY"),
                    "performance_weather_rating": "cloudy",
                },
            ),
            (
                7837,
                {
                    "name": "アールシーコア",
                    "market_segment": "tse_standard",
                    "price": Money("501.0", "JPY"),
                    "business_category": "その他製品",
                    "business_description": "丸太組み工法のログハウスで首位。自然派の提案型住宅に強み。別荘運営も。",
                    "related_themes": ["建設", "建設資材"],
                    "previous_close_price": Money("495.0", "JPY"),
                    "open_price": Money("500.0", "JPY"),
                    "daily_highest_price": Money("504.0", "JPY"),
                    "daily_lowest_price": Money("494.0", "JPY"),
                    "dividend_yield": 0.0,
                    "share_unit": 100,
                    "adjusted_per": None,
                    "psr": 0.16,
                    "pbr": 2.57,
                    "volume": 13700,
                    "market_capitalization": Money("2_272_000_000", "JPY"),
                    "issued_shares": 4_536_000,
                    "shareholder_benefits": "ホテル宿泊割引券、オリジナルカレンダー",
                    "lowest_purchase_price": Money("50_188", "JPY"),
                    "performance_weather_rating": "sunny",
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
            m.get(f"https://minkabu.jp/stock/{security_code}", text=text)
            for k, v in expected_values.items():
                assert getattr(kabupy.minkabu.stock(security_code).top, k) == v

    def test_raise_element_not_found_error(self, helpers):
        pass
