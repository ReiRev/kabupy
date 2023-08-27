"""Scraper for https://kabuyoho.jp/sp/reportTop"""
from __future__ import annotations

import logging
import re
import urllib.parse

from money import Money

from ..base import Website, webpage_property
from ..util import str2float, str2money, str2int
from .kabuyoho_webpage import KabuyohoWebpage

logger = logging.getLogger(__name__)


class ReportTarget(KabuyohoWebpage):
    """Report target page object."""

    def __init__(self, website: Website, security_code: str | int) -> None:
        self.website = website
        self.security_code = str(security_code)
        self.url = urllib.parse.urljoin(self.website.url, f"sp/reportTarget?bcode={self.security_code}")
        super().__init__()

    @webpage_property
    def price_level_to_target(self) -> str | None:
        """Current price level to target price: 目標株価に対する現在の価格が割高か割安か."""
        return None if self.term2description("目標株価から見た株価") == "--" else self.term2description("目標株価から見た株価")

    @webpage_property
    def price_target(self) -> Money | None:
        """Price target: 目標株価(アナリストが発表した目標株価の平均値)"""
        amount = self.soup.select_one('thead:has(>tr>th:-soup-contains("平均")) ~ tbody>tr>td:nth-of-type(1)')
        if amount is None:
            return None
        return str2money(amount.text)

    @webpage_property
    def price_target_ratio_to_previous_week(self) -> float | None:
        """Price target ratio to previous week in %: 目標株価の対前週変化率"""
        amount = self.soup.select_one('thead:has(>tr>th:-soup-contains("平均")) ~ tbody>tr>td:nth-of-type(2)')
        if amount is None:
            return None
        return str2float(amount.text)

    @webpage_property
    def price_target_ratio_to_current_price(self) -> float | None:
        """(price target) / (current price) in %: 目標株価と現在の株価の乖離率"""
        amount = self.soup.select_one('thead:has(>tr>th:-soup-contains("平均")) ~ tbody>tr>td:nth-of-type(3)')
        if amount is None:
            return None
        return str2float(amount.text)

    @webpage_property
    def average_analyst_rating(self) -> float | None:
        """Average analyst rating: レーティング(平均)"""
        amount = self.soup.select_one('main section:has(h1:-soup-contains("レーティング")) th:-soup-contains("平均") + td')
        if amount is None:
            return None
        return str2float(amount.text)

    @webpage_property
    def analyst_count(self) -> int | None:
        """Average count: レーティング(人数)"""
        amount = self.soup.select_one('main section:has(h1:-soup-contains("レーティング")) th:-soup-contains("人数") + td')
        if amount is None:
            return None
        amount = re.sub(r"\D", "", amount.text)
        if amount == "":
            amount = "0"
        return int(amount)

    @webpage_property
    def analyst_rating_composition(self) -> dict[str, int]:
        """Analyst rating composition: レーティング(点数の構成)

        Returns:
            dict[str, int]: key: rating("1", "2", "3", "4", and "5"),
                            which respectively means
                            "strong sell(弱気)", "sell(やや弱気)", "hold(中立)", "buy(やや強気)", and "strong buy(強気)"
                            value: the number of analysts
        """
        ratings = ["1", "2", "3", "4", "5"]
        composition = {}
        for rating in ratings:
            res = self.soup.select_one(
                'main h1:-soup-contains("レーティング") + div '
                f'tbody tr>th:-soup-contains("({rating}点)") + td'
            )
            if res is None:
                continue
            composition[rating] = str2int(res.text)
        return composition

    @webpage_property
    def per_based_theoretical_stock_price(self) -> Money | None:
        """PER based theoretical stock price(理論株価(PER基準))"""
        amount = self.soup.select_one(
            'main h2:-soup-contains("想定株価レンジ") + '
            'table tr>th:-soup-contains("理論株価(PER基準)") + '
            'td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @webpage_property
    def per_based_upside_target(self) -> Money | None:
        """PER based upside target(上値目途(PER基準))"""
        amount = self.soup.select_one(
            'main h2:-soup-contains("想定株価レンジ") + '
            'table tr:has(>th:-soup-contains("理論株価(PER基準)")) ~ '
            'tr:has(>th:-soup-contains("上値目途"))>td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @webpage_property
    def per_based_downside_target(self) -> Money | None:
        """PER based downside target(下値目途(PER基準))"""
        amount = self.soup.select_one(
            'main h2:-soup-contains("想定株価レンジ") + '
            'table tr:has(>th:-soup-contains("理論株価(PER基準)")) ~ '
            'tr:has(>th:-soup-contains("下値目途"))>td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @webpage_property
    def pbr_based_theoretical_stock_price(self) -> Money | None:
        """PBR based theoretical stock price(理論株価(PBR基準))"""
        amount = self.soup.select_one(
            'main h2:-soup-contains("想定株価レンジ") + '
            'table tr>th:-soup-contains("理論株価(PBR基準)") + '
            'td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @webpage_property
    def pbr_based_upside_target(self) -> Money | None:
        """PBR based upside target(上値目途(PBR基準))"""
        amount = self.soup.select_one(
            'main h2:-soup-contains("想定株価レンジ") + '
            'table tr:has(>th:-soup-contains("理論株価(PBR基準)")) ~ '
            'tr:has(>th:-soup-contains("上値目途"))>td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @webpage_property
    def pbr_based_downside_target(self) -> Money | None:
        """PBR based downside target(下値目途(PBR基準))"""
        amount = self.soup.select_one(
            'main h2:-soup-contains("想定株価レンジ") + '
            'table tr:has(>th:-soup-contains("理論株価(PBR基準)")) ~ '
            'tr:has(>th:-soup-contains("下値目途"))>td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @webpage_property
    def actual_bps(self) -> Money | None:
        """Actual BPS: BPS(実績)"""
        amount = self.soup.select_one('main h2:-soup-contains("株価指標") + table th:-soup-contains("BPS(実績)") + td')
        if amount is None:
            return None
        return str2money(amount.text)

    @webpage_property
    def expected_eps(self) -> Money | None:
        """Expected EPS: EPS(予想)"""
        amount = self.soup.select_one('main h2:-soup-contains("株価指標")+table th:-soup-contains("EPS(予想)") + td')
        if amount is None:
            return None
        return str2money(amount.text)

    @webpage_property
    def analyst_expected_eps(self) -> Money | None:
        """Analyst expected EPS: EPS(アナリスト12ヶ月後予想)"""
        amount = self.soup.select_one('main h2:-soup-contains("株価指標")+table th:-soup-contains("EPS ※") + td')
        if amount is None:
            return None
        return str2money(amount.text)

    @webpage_property
    def analyst_expected_epr(self) -> float | None:
        """Analyst expected PER: PER(アナリスト12ヶ月後予想)"""
        amount = self.soup.select_one('main h2:-soup-contains("株価指標")+table th:-soup-contains("PER ※") + td')
        if amount is None:
            return None
        return str2float(amount.text)
