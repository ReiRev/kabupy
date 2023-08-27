import os

import pytest
import requests_mock
from money import Money

import kabupy

url_directory = "reportTarget"


class TestReportTarget:
    @pytest.mark.parametrize(
        "security_code,forward_values",
        [
            (
                6758,
                {
                    # Properties in "price target(目標株価)"
                    "price_level_to_target": "割安",
                    "price_target": Money("16197", "JPY"),
                    "price_target_ratio_to_previous_week": -0.21,
                    "price_target_ratio_to_current_price": 28.90,
                    # Properties in "rating(レーティング)"
                    "average_analyst_rating": 4.75,
                    "analyst_count": 16,
                    "analyst_rating_composition": {
                        "1": 0,
                        "2": 0,
                        "3": 2,
                        "4": 0,
                        "5": 14,
                    },
                    # Properties in "stock index(株価指標)"
                    "bps": Money("5674", "JPY"),
                    "forward_eps": Money("696.8", "JPY"),
                    "forward_eps_by_analysts": Money("777.1", "JPY"),
                    "pbr": 2.21,
                    "forward_per": 18.0,
                    "forward_per_by_analysts": 16.2,
                    # Properties in "target price range(想定株価レンジ)"
                    "pbr_based_fair_value": Money("12_797", "JPY"),
                    "pbr_fair": 2.26,
                    "pbr_based_ceiling": Money("13_542", "JPY"),
                    "pbr_ceiling": 2.39,
                    "pbr_based_floor": Money("12_053", "JPY"),
                    "pbr_floor": 2.12,
                    "per_based_fair_value": Money("13438", "JPY"),
                    "per_fair": 17.3,
                    "per_based_ceiling": Money("14_424", "JPY"),
                    "ceiling_per": 18.6,
                    "per_based_floor": Money("12_451", "JPY"),
                    "per_floor": 16.0,
                },
            ),
            (
                7837,
                {
                    # Properties in "price target(目標株価)"
                    "price_level_to_target": None,
                    "price_target": None,
                    "price_target_ratio_to_previous_week": None,
                    "price_target_ratio_to_current_price": None,
                    # Properties in "rating(レーティング)"
                    "average_analyst_rating": None,
                    "analyst_count": 0,
                    "analyst_rating_composition": {
                        "1": 0,
                        "2": 0,
                        "3": 0,
                        "4": 0,
                        "5": 0,
                    },
                    # Properties in "stock index(株価指標)"
                    "bps": Money("208", "JPY"),
                    "forward_eps": Money("660.3", "JPY"),
                    "forward_eps_by_analysts": None,
                    "pbr": 2.33,
                    "forward_per": 0.7,
                    "forward_per_by_analysts": None,
                    # Properties in "target price range(想定株価レンジ)"
                    "pbr_based_fair_value": Money("438", "JPY"),
                    "pbr_fair": 2.11,
                    "pbr_based_ceiling": Money("624", "JPY"),
                    "pbr_ceiling": 3.00,
                    "pbr_based_floor": Money("253", "JPY"),
                    "pbr_floor": 1.22,
                    "per_based_fair_value": None,
                    "per_fair": None,
                    "per_based_ceiling": None,
                    "ceiling_per": None,
                    "per_based_floor": None,
                    "per_floor": None,
                },
            ),
        ],
    )
    def test_properties(self, helpers, security_code, forward_values: dict):
        text = helpers.html2text(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"html/{url_directory}/{security_code}.html",
            )
        )
        with requests_mock.Mocker() as m:
            m.get(f"https://kabuyoho.jp/sp/{url_directory}?bcode={security_code}", text=text)
            for k, v in forward_values.items():
                assert getattr(kabupy.kabuyoho.stock(security_code).report_target, k) == v
