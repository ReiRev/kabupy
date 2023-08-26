"""Scraper for https://kabuyoho.jp/sp/reportTop"""
from __future__ import annotations

import logging
import re
import urllib.parse

from money import Money

from ..base import Website, webpage_property
from ..util import str2float, str2money
from .kabuyoho_webpage import KabuyohoWebpage

logger = logging.getLogger(__name__)


class ReportTop(KabuyohoWebpage):
    """Report target page object."""

    def __init__(self, website: Website, security_code: str | int) -> None:
        self.website = website
        self.security_code = security_code
        self.url = urllib.parse.urljoin(self.website.url, f"sp/reportTop?bcode={self.security_code}")
        super().__init__()

    @webpage_property
    def expected_per(self) -> float | None:
        """Expected PER: PER(予)."""
        amount = self.term2description("PER(予)")
        if amount is None:
            return None
        return str2float(amount)

    @webpage_property
    def actual_pbr(self) -> float | None:
        """Actual PBR: PBR(実)."""
        amount = self.term2description("PBR(実)")
        if amount is None:
            return None
        return str2float(amount)

    @webpage_property
    def expected_dividend_yield(self) -> float | None:
        """Expected dividend yield: 配当利回り(予)."""
        amount = self.term2description("配当利回り(予)")
        if amount is None:
            return None
        return str2float(amount)

    @webpage_property
    def market_capitalization(self) -> Money | None:
        """Market Capitalization: 時価総額."""
        amount = self.term2description("時価総額")
        if amount is None:
            return None
        return str2money(amount)

    @webpage_property
    def actual_roa(self) -> float | None:
        """Actual ROA: ROA(実)."""
        amount = self.term2description("ROA(実)")
        if amount is None:
            return None
        return str2float(amount)

    @webpage_property
    def actual_roe(self) -> float | None:
        """Actual ROE: ROE(実)."""
        amount = self.term2description("ROE(実)")
        if amount is None:
            return None
        return str2float(amount)

    @webpage_property
    def equity_ratio(self) -> float | None:
        """Equity ratio: 自己資本率."""
        amount = self.term2description("自己資本比率")
        if amount is None:
            return None
        return str2float(amount)

    @webpage_property
    def signal(self) -> str | None:
        """Signal: シグナル."""
        res = self.term2description("シグナル")
        if res is None:
            return None
        return re.sub(r"\s+", "", res)

    @webpage_property
    def expected_ordinary_profit(self) -> Money | None:
        """Market Capitalization: 予想経常利益(予)."""
        amount = self.soup.select_one('main dt:-soup-contains("予想経常利益(予)") + dd>p')
        if amount is None:
            return None
        return str2money(amount.text.split("円")[0])

    @webpage_property
    def consensus_expected_ordinary_profit(self) -> Money | None:
        """Market Capitalization: 予想経常利益(コ)."""
        amount = self.soup.select_one('main dt:-soup-contains("予想経常利益(コ)") + dd>p')
        if amount is None:
            return None
        return str2money(amount.text.split("円")[0])
