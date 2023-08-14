"""Scraper for kabuyoho.jp"""
from __future__ import annotations

import functools
import logging
import re
import urllib.parse

from money import Money

from ..base import Page, Website
from ..util import str2float, str2money

logger = logging.getLogger(__name__)


class Kabuyoho(Website):
    """An object for kabuyoho.jp"""

    def __init__(self) -> None:
        self.url = "https://kabuyoho.jp"

    def stock(self, security_code: str | int) -> Stock:
        """Return Stock object"""
        return Stock(self, security_code)


class ReportTopPage(Page):
    """Report target page object."""

    def __init__(self, website: Website, security_code: str | int) -> None:
        self.website = website
        self.security_code = security_code
        self.url = urllib.parse.urljoin(self.website.url, f"sp/reportTop?bcode={self.security_code}")
        super().__init__()


class ReportTargetPage(Page):
    """Report target page object."""

    def __init__(self, website: Website, security_code: str | int) -> None:
        self.website = website
        self.security_code = security_code
        self.url = urllib.parse.urljoin(self.website.url, f"sp/reportTarget?bcode={self.security_code}")
        super().__init__()


class ReportDpsPage(Page):
    """Report target page object."""

    def __init__(self, website: Website, security_code: str | int) -> None:
        self.website = website
        self.security_code = security_code
        self.url = urllib.parse.urljoin(self.website.url, f"sp/reportDps?bcode={self.security_code}")
        super().__init__()


class Stock:
    """Stock object for kabuyoho.jp"""

    def __init__(self, website: Kabuyoho, security_code: str | int) -> None:
        self.security_code = str(security_code)
        self.website = website

    def term2description(self, page: Page, term: str) -> str | None:
        res = self.report_top_page.soup.select_one(f'main dt:-soup-contains("{term}") + dd')
        if res is None:
            return None
        return res.text

    @functools.cached_property
    def report_top_page(self) -> Page:
        return ReportTopPage(self.website, self.security_code)

    @functools.cached_property
    def report_target_page(self) -> Page:
        return ReportTargetPage(self.website, self.security_code)

    @functools.cached_property
    def report_dps_page(self) -> Page:
        return ReportDpsPage(self.website, self.security_code)

    @property
    def price(self) -> Money | None:
        """Price of the stock: 価格"""
        amount = self.report_top_page.soup.select_one('main li p:-soup-contains("株価","(","/",")") + p')
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def expected_per(self) -> float | None:
        """Expected PER: PER(予)."""
        amount = self.term2description(self.report_top_page, "PER(予)")
        if amount is None:
            return None
        return str2float(amount)

    @property
    def actual_pbr(self) -> float | None:
        """Actual PBR: PBR(実)."""
        amount = self.term2description(self.report_top_page, "PBR(実)")
        if amount is None:
            return None
        return str2float(amount)

    @property
    def actual_roa(self) -> float | None:
        """Actual ROA: ROA(実)."""
        amount = self.term2description(self.report_top_page, "ROA(実)")
        if amount is None:
            return None
        return str2float(amount)

    @property
    def actual_roe(self) -> float | None:
        """Actual ROE: ROE(実)."""
        amount = self.term2description(self.report_top_page, "ROE(実)")
        if amount is None:
            return None
        return str2float(amount)

    @property
    def equity_ratio(self) -> float | None:
        """Equity ratio: 自己資本率."""
        amount = self.term2description(self.report_top_page, "自己資本比率")
        if amount is None:
            return None
        return str2float(amount)

    @property
    def market_capitalization(self) -> Money | None:
        """Market Capitalization: 時価総額."""
        amount = self.term2description(self.report_top_page, "時価総額")
        if amount is None:
            return None
        return str2money(amount)

    @property
    def signal(self) -> str | None:
        """Signal: シグナル."""
        res = self.term2description(self.report_top_page, "シグナル")
        if res is None:
            return None
        return re.sub(r"\s+", "", res)

    @property
    def expected_ordinary_profit(self) -> Money | None:
        """Market Capitalization: 予想経常利益(予)."""
        amount = self.report_top_page.soup.select_one('main dt:-soup-contains("予想経常利益(予)") + dd>p')
        if amount is None:
            return None
        return str2money(amount.text.split("円")[0])

    @property
    def consensus_expected_ordinary_profit(self) -> Money | None:
        """Market Capitalization: 予想経常利益(コ)."""
        amount = self.report_top_page.soup.select_one('main dt:-soup-contains("予想経常利益(コ)") + dd>p')
        if amount is None:
            return None
        return str2money(amount.text.split("円")[0])

    @property
    def per_based_theoretical_stock_price(self) -> Money | None:
        """PER based theoretical stock price(理論株価(PER基準))"""
        amount = self.report_target_page.soup.select_one(
            'main h2:-soup-contains("想定株価レンジ") + '
            'table tr>th:-soup-contains("理論株価(PER基準)") + '
            'td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def per_based_upside_target(self) -> Money | None:
        """PER based upside target(上値目途(PER基準))"""
        amount = self.report_target_page.soup.select_one(
            'main h2:-soup-contains("想定株価レンジ") + '
            'table tr:has(>th:-soup-contains("理論株価(PER基準)")) ~ '
            'tr:has(>th:-soup-contains("上値目途"))>td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def per_based_downside_target(self) -> Money | None:
        """PER based downside target(下値目途(PER基準))"""
        amount = self.report_target_page.soup.select_one(
            'main h2:-soup-contains("想定株価レンジ") + '
            'table tr:has(>th:-soup-contains("理論株価(PER基準)")) ~ '
            'tr:has(>th:-soup-contains("下値目途"))>td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def pbr_based_theoretical_stock_price(self) -> Money | None:
        """PBR based theoretical stock price(理論株価(PBR基準))"""
        amount = self.report_target_page.soup.select_one(
            'main h2:-soup-contains("想定株価レンジ") + '
            'table tr>th:-soup-contains("理論株価(PBR基準)") + '
            'td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def pbr_based_upside_target(self) -> Money | None:
        """PBR based upside target(上値目途(PBR基準))"""
        amount = self.report_target_page.soup.select_one(
            'main h2:-soup-contains("想定株価レンジ") + '
            'table tr:has(>th:-soup-contains("理論株価(PBR基準)")) ~ '
            'tr:has(>th:-soup-contains("上値目途"))>td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def pbr_based_downside_target(self) -> Money | None:
        """PBR based downside target(下値目途(PBR基準))"""
        amount = self.report_target_page.soup.select_one(
            'main h2:-soup-contains("想定株価レンジ") + '
            'table tr:has(>th:-soup-contains("理論株価(PBR基準)")) ~ '
            'tr:has(>th:-soup-contains("下値目途"))>td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def actual_bps(self) -> Money | None:
        """Actual BPS: BPS(実績)"""
        amount = self.report_target_page.soup.select_one(
            'main h2:-soup-contains("株価指標") + ' 'table th:-soup-contains("BPS(実績)") + td'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def expected_eps(self) -> Money | None:
        """Expected EPS: EPS(予想)"""
        amount = self.report_target_page.soup.select_one(
            'main h2:-soup-contains("株価指標")+table th:-soup-contains("EPS(予想)") + td'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def analyst_expected_eps(self) -> Money | None:
        """Analyst expected EPS: EPS(アナリスト12ヶ月後予想)"""
        amount = self.report_target_page.soup.select_one(
            'main h2:-soup-contains("株価指標")+table th:-soup-contains("EPS ※") + td'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def analyst_expected_epr(self) -> float | None:
        """Analyst expected PER: PER(アナリスト12ヶ月後予想)"""
        amount = self.report_target_page.soup.select_one(
            'main h2:-soup-contains("株価指標")+table th:-soup-contains("PER ※") + td'
        )
        if amount is None:
            return None
        return str2float(amount.text)

    @property
    def price_target(self) -> Money | None:
        """Price target: 目標株価(アナリストが発表した目標株価の平均値)"""
        amount = self.report_target_page.soup.select_one('thead:has(>tr>th:-soup-contains("平均")) ~ tbody>tr>td')
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def average_analyst_rating(self) -> float | None:
        """Average analyst rating: レーティング(平均)"""
        amount = self.report_target_page.soup.select_one(
            'main section:has(h1:-soup-contains("レーティング")) th:-soup-contains("平均") + td'
        )
        if amount is None:
            return None
        return str2float(amount.text)

    @property
    def analyst_count(self) -> int | None:
        """Average count: レーティング(人数)"""
        amount = self.report_target_page.soup.select_one(
            'main section:has(h1:-soup-contains("レーティング")) th:-soup-contains("人数") + td'
        )
        if amount is None:
            return None
        amount = re.sub(r"\D", "", amount.text)
        if amount == "":
            amount = "0"
        return int(amount)

    @property
    def actual_dividend_yield(self) -> float | None:
        """Actual dividend yield(実績配当利回り)."""
        amount = self.report_dps_page.soup.select_one('th:-soup-contains("実績配当利回り") + td')
        if amount is None:
            return None
        return str2float(amount.text)

    @property
    def expected_dividend_yield(self) -> float | None:
        """Expected dividend yield(予想配当利回り)."""
        amount = self.report_dps_page.soup.select_one('th:-soup-contains("予想配当利回り") + td')
        if amount is None:
            return None
        return str2float(amount.text)

    @property
    def dividend_payout_ratio(self) -> float | None:
        """Expected dividend yield(予想配当利回り)."""
        amount = self.report_dps_page.soup.select_one('h2:-soup-contains("前期配当性向") + div td')
        if amount is None:
            return None
        return str2float(amount.text)
