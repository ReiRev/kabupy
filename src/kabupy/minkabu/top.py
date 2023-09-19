"""Scraper for https://kabuyoho.jp/sp/reportDps"""
from __future__ import annotations

import logging
import re
import urllib.parse
from typing import Literal

from money import Money

from ..base import Website, webpage_property
from ..util import str2float, str2int, str2money
from .minkabu_webpage import MinkabuWebpage

logger = logging.getLogger(__name__)


class Top(MinkabuWebpage):
    """Report target page object."""

    def __init__(self, website: Website, security_code: str | int) -> None:
        self.website = website
        self.security_code = str(security_code)
        self.url = urllib.parse.urljoin(self.website.url, f"stock/{self.security_code}")
        super().__init__()

    @webpage_property
    def business_category(self) -> str:
        """Business category, 業種."""
        return self.select_one('span:-soup-contains("業種") + a').text

    @webpage_property
    def business_description(self) -> str:
        """Business description, 事業内容."""
        return re.sub(r"\s+", "", self.select_one('div:-soup-contains("業種") + div').text)

    @webpage_property
    def related_themes(self) -> list[str]:
        """Related themes, 関連テーマ."""
        return [re.sub(r"\s+", "", t.text) for t in self.select('ul > li:-soup-contains("関連テーマ") ~ li')]

    @webpage_property
    def previous_close_price(self) -> Money | None:
        """Previous day close price, 前日終値."""
        return str2money(self.th2td("前日終値"))

    @webpage_property
    def open_price(self) -> Money | None:
        """Open price, 始値."""
        return str2money(self.th2td("始値"))

    @webpage_property
    def daily_highest_price(self) -> Money | None:
        """Daily highest price, 高値."""
        return str2money(self.th2td("高値"))

    @webpage_property
    def daily_lowest_price(self) -> Money | None:
        """Daily lowest price, 安値."""
        return str2money(self.th2td("安値"))

    @webpage_property
    def dividend_yield(self) -> float | None:
        """Dividend yield, 配当利回り."""
        return str2float(self.th2td("配当利回り"))

    @webpage_property
    def share_unit(self) -> int | None:
        """Share unit, 単元株数."""
        return str2int(self.th2td("単元株数"))

    @webpage_property
    def adjusted_per(self) -> float | None:
        """Adjusted PER, PER(調整後)."""
        return str2float(self.th2td("PER(調整後)"))

    @webpage_property
    def psr(self) -> float | None:
        """PSR, PSR."""
        return str2float(self.th2td("PSR"))

    @webpage_property
    def pbr(self) -> float | None:
        """PBR, PBR."""
        return str2float(self.th2td("PBR"))

    @webpage_property
    def volume(self) -> int | None:
        """Volume, 出来高."""
        return str2int(self.th2td("出来高"))

    @webpage_property
    def market_capitalization(self) -> Money | None:
        """Market capitalization, 時価総額."""
        return str2money(self.th2td("時価総額"))

    @webpage_property
    def issued_shares(self) -> int | None:
        """Issued shares, 発行済株数."""
        return str2int(self.th2td("発行済株数"))

    @webpage_property
    def shareholder_benefits(self) -> str | None:
        """Shareholder benefits, 株主優待."""
        return self.th2td("株主優待")

    @webpage_property
    def lowest_purchase_price(self) -> Money | None:
        """The purchase price with the cheapest fee, 手数料の一番安いネット証券で取引した時の購入金額."""
        return str2money(self.th2td("購入金額"))

    @webpage_property
    def performance_weather_rating(self) -> Literal["sunny", "partly_sunny", "cloudy", "rainy", "thunderstorm"] | None:
        """Performance weather rating, 業績評価.

        This expresses the comprehensive evaluation of sales, operating profit, and net profit with weather conditions.
        The closer it is to sunny, the higher the rating is. Sunny, partly sunny, cloudy, rainy, or thunderstorm.

        Note:
            Here is the original description in Japanese.
            売上高・経常利益・最終利益の総合的な評価をお天気で表現しています。「晴れ」に近づくほど高評価となります。
            「晴れ」、「曇り時々晴れ」、「曇り」、「雨」、「雷」。
        """
        weather = self.select_one('div:-soup-contains("業績評価") + div').text
        if weather == "晴れ":
            return "sunny"
        if weather == "曇り時々晴れ":
            return "partly_sunny"
        if weather == "曇り":
            return "cloudy"
        if weather == "雨":
            return "rainy"
        if weather == "雷":
            return "thunderstorm"
        return None
