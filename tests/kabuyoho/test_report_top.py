import os
from datetime import datetime

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
                    "name": "ソニーグループ",
                    "security_code": "6758",
                    "earnings_release_date": datetime(2023, 8, 9),
                    "expected_per": 18.0,
                    "actual_pbr": 2.21,
                    "expected_dividend_yield": None,
                    "market_capitalization": Money("15_845_500_000_000", "JPY"),
                    "actual_roa": 3.00,
                    "actual_roe": 13.04,
                    "equity_ratio": 22.6,
                    "signal": "売り継続",
                    "expected_ordinary_profit": Money("1_140_000_000_000", "JPY"),
                    "consensus_expected_ordinary_profit": Money("1_223_695_000_000", "JPY"),
                    "target_price": Money("16_197", "JPY"),
                    "business_category": "電気機器",
                    "business_description": "世界的なエレクトロニクス企業。エレクトロニクス（半導体・電子デバイス、モバイル、情報通信、テレビ・音響）、"
                    "エンターテインメント（ゲーム、映画、音楽）、金融（銀行・保険）分野でグローバルビジネス。",
                    "products": [
                        "ゲーム＆ネットワークサービス（家庭用ゲーム機「PS5」、ゲームソフト、ネットワークサービス、周辺装置・機器）",
                        "イメージング＆センシングソリューション（CMOSイメージセンサー、LSI/IC/モジュール、レーザーダイオード、ディスプレイデバイス、ボードコンピュータ）",
                    ],
                    "segment_sales_composition": [
                        {
                            "segment": "ｹﾞｰﾑ&ﾈｯﾄﾜｰｸｻｰﾋﾞｽ",
                            "sales": Money("3_644_598_000_000", "JPY"),
                            "proportion": 30.8,
                        },
                        {
                            "segment": "ｴﾝﾀﾃｲﾝﾒﾝﾄ･ﾃｸﾉﾛｼﾞｰ&ｻｰﾋﾞｽ",
                            "sales": Money("2_476_025_000_000", "JPY"),
                            "proportion": 21.0,
                        },
                        {
                            "segment": "金融",
                            "sales": Money("1_454_546_000_000", "JPY"),
                            "proportion": 12.3,
                        },
                        {
                            "segment": "ｲﾒｰｼﾞﾝｸﾞ&ｾﾝｼﾝｸﾞ･ｿﾘｭｰｼｮﾝ",
                            "sales": Money("1_402_187_000_000", "JPY"),
                            "proportion": 11.9,
                        },
                        {
                            "segment": "音楽",
                            "sales": Money("1_380_632_000_000", "JPY"),
                            "proportion": 11.7,
                        },
                        {
                            "segment": "映画",
                            "sales": Money("1_369_422_000_000", "JPY"),
                            "proportion": 11.6,
                        },
                        {
                            "segment": "その他",
                            "sales": Money("87_623_000_000", "JPY"),
                            "proportion": 0.7,
                        },
                    ],
                    "income_statement_amount": Money("11_539_837_000_000", "JPY"),
                    "income_statement_adjustment": Money("-275_196_000_000", "JPY"),
                    "current_term_company_performance_forecast": "減益",
                    "analyst_company_performance_forecast_comparison": "強気",
                    "price_level_to_target": "割安",
                },
            ),
            (
                7837,
                {
                    "price": Money("485", "JPY"),
                    "name": "アールシーコア",
                    "security_code": "7837",
                    "earnings_release_date": datetime(2023, 8, 14),
                    "expected_per": 0.7,
                    "actual_pbr": 2.33,
                    "expected_dividend_yield": 0.00,
                    "market_capitalization": Money("2_200_000_000", "JPY"),
                    "actual_roa": 11.53,
                    "actual_roe": 87.08,
                    "equity_ratio": 7.9,
                    "signal": "売り継続",
                    "expected_ordinary_profit": Money("26_000_000", "JPY"),
                    "consensus_expected_ordinary_profit": None,
                    "target_price": None,
                    "business_category": "その他製品",
                    "business_description": "国内トップのログハウスメーカー。自然材（無垢材）を多用した「BESS」ブランドの自然派個性住宅（ログハウス、エポックス）の"
                    "企画・開発・設計・販売、タイムシェア別荘「フェザント山中湖」の販売・運営。",
                    "products": [
                        "「BESSシリーズ」ログハウス（COUNTRY LOG、G-LOG）",
                        "「BESSシリーズ」エポックス（WONDER DEVICE、倭様「程々の家」、BESS DOME、平小屋「栖ログ」）",
                    ],
                    "segment_sales_composition": [
                        {
                            "segment": "販社",
                            "sales": Money("5_991_000_000", "JPY"),
                            "proportion": 37.2,
                        },
                        {
                            "segment": "BP社",
                            "sales": Money("5_256_000_000", "JPY"),
                            "proportion": 32.6,
                        },
                        {
                            "segment": "直販",
                            "sales": Money("4_874_000_000", "JPY"),
                            "proportion": 30.2,
                        },
                    ],
                    "income_statement_amount": Money("13_940_000_000", "JPY"),
                    "income_statement_adjustment": Money("-2_181_000_000", "JPY"),
                    "current_term_company_performance_forecast": "黒字転換",
                    "analyst_company_performance_forecast_comparison": None,
                    "price_level_to_target": None,
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
