"""Scraper for kabuyoho.jp"""
from __future__ import annotations

import functools
import logging
import re
import urllib.parse

from money import Money

from ..base import Page, Website
from ..exceptions import InvalidElementError
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
        """Price of the stock

        Returns:
            float | None: Price if found or None
        """
        soup = self.report_top_page.soup
        titles = soup.find_all("dt")
        descriptions = soup.find_all("dd")
        titles = [re.sub(r"\s", "", t.text) for t in titles]
        descriptions = [re.sub(r"\s", "", d.text) for d in descriptions]
        if len(titles) != len(descriptions):
            raise InvalidElementError("The number of dd and dt is not same.")
        for title, description in zip(titles, descriptions):
            if "株価" not in title:
                continue
            return str2money(description)
        return None

    @property
    def market_capitalization(self) -> Money | None:
        """Market Capitalization(時価総額)"""
        soup = self.report_top_page.soup
        titles = soup.find_all("dt")
        descriptions = soup.find_all("dd")
        titles = [re.sub(r"\s", "", t.text) for t in titles]
        descriptions = [re.sub(r"\s", "", d.text) for d in descriptions]
        if len(titles) != len(descriptions):
            raise InvalidElementError("The number of dd and dt is not same.")
        for title, description in zip(titles, descriptions):
            if "時価総額" not in title:
                continue
            return str2money(description)
        return None

    @property
    def per_based_theoretical_stock_price(self) -> Money | None:
        """PER based theoretical stock price(理論株価(PER基準))"""
        amount = self.report_target_page.soup.select_one(
            'tr>th:-soup-contains("理論株価(PER基準)") + td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def per_based_upside_target(self) -> Money | None:
        """PER based upside target(上値目途(PER基準))"""
        amount = self.report_target_page.soup.select_one(
            'tr:has(>th:-soup-contains("理論株価(PER基準)")) ~ tr:has(>th:-soup-contains("上値目途"))>td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def per_based_downside_target(self) -> Money | None:
        """PER based downside target(下値目途(PER基準))"""
        amount = self.report_target_page.soup.select_one(
            'tr:has(>th:-soup-contains("理論株価(PER基準)")) ~ tr:has(>th:-soup-contains("下値目途"))>td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def pbr_based_theoretical_stock_price(self) -> Money | None:
        """PBR based theoretical stock price(理論株価(PBR基準))"""
        amount = self.report_target_page.soup.select_one(
            'tr>th:-soup-contains("理論株価(PBR基準)") + td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def pbr_based_upside_target(self) -> Money | None:
        """PBR based upside target(上値目途(PBR基準))"""
        amount = self.report_target_page.soup.select_one(
            'tr:has(>th:-soup-contains("理論株価(PBR基準)")) ~ tr:has(>th:-soup-contains("上値目途"))>td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def pbr_based_downside_target(self) -> Money | None:
        """PBR based downside target(下値目途(PBR基準))"""
        amount = self.report_target_page.soup.select_one(
            'tr:has(>th:-soup-contains("理論株価(PBR基準)")) ~ tr:has(>th:-soup-contains("下値目途"))>td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def price_target(self) -> Money | None:
        """Price target: 目標株価(アナリストが発表した目標株価の平均値)"""
        amount = self.report_target_page.soup.select_one('thead:has(>tr>th:-soup-contains("平均")) ~ tbody>tr>td')
        if amount is None:
            return None
        return str2money(amount.text)

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
