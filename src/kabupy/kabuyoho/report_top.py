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

    @webpage_property
    def target_price(self) -> Money | None:
        """Target Price: 目標株価."""
        amount = self.soup.select_one('main dt:-soup-contains("目標株価(コ)") + dd>p>span')
        if amount is None:
            return None
        return str2money(amount.text)

    @webpage_property
    def business_category(self) -> str | None:
        """Business category: 事業内容の業種."""
        res = self.soup.select_one('main h1:-soup-contains("基本情報") ~ div h2:-soup-contains("業種")')
        if res is None:
            return None
        return re.sub(r"業種：", "", res.text)

    @webpage_property
    def business_description(self) -> str | None:
        """Business description: 事業内容の説明."""
        res = self.soup.select_one('main h1:-soup-contains("基本情報") ~ div h2:-soup-contains("業種")+p')
        if res is None:
            return None
        return re.sub(r"\s+", "", res.text)

    @webpage_property
    def products(self) -> list[str] | None:
        """Products: 取扱い商品."""
        res = self.soup.select('main div:-soup-contains("取扱い商品") + div > p')
        return [re.sub(r"^・", "", r.text) for r in res]

    @webpage_property
    def segment_sales_composition(self) -> list[dict[str, str | Money | float]] | None:
        """Segment sales composition: セグメント売上構成."""
        rows = self.soup.select('main div:-soup-contains("セグメント売上構成") + div table tr:has(td)')
        return [
            {
                "segment": r.find_all("td")[0].text,
                "sales": str2money(r.find_all("td")[1].text + "百万円"),
                "proportion": str2float(r.find_all("td")[2].text),
            }
            for r in rows
            if r.find("td").text != "損益計算書計上額" and r.find("td").text != "調整額"
        ]

    @webpage_property
    def income_statement_amount(self) -> Money | None:
        """Income statement amount: 損益計算書計上額."""
        amount = self.soup.select_one('main td:-soup-contains("損益計算書計上額") + td')
        if amount is None:
            return None
        return str2money(amount.text + "百万円")

    @webpage_property
    def income_statement_adjustment(self) -> Money | None:
        """Income statement adjustment: 調整額."""
        amount = self.soup.select_one('main td:-soup-contains("調整額") + td')
        if amount is None:
            return None
        return str2money(amount.text + "百万円")

    @webpage_property
    def current_term_company_performance_forecast(self) -> str | None:
        """Current term company performance forecast: 業績予想 会社予想 今期見通し."""
        res = self.soup.select_one(
            'main div:-soup-contains("業績予想") + div h2:-soup-contains("会社予想") + dl > dt:-soup-contains("今期見通し") + dd'
        )
        if res is None:
            return None
        return re.sub(r"\s+", "", res.text)

    @webpage_property
    def analyst_company_performance_forecast_comparison(self) -> str | None:
        """Analyst forecast company forecast comparison: 業績予想 アナリスト予想 会社予想との比較."""
        res = self.soup.select_one(
            'main div:-soup-contains("業績予想") + div h2:-soup-contains("アナリスト予想") + dl '
            '> dt:-soup-contains("会社予想との比較") + dd'
        )
        if res is None:
            return None
        res = re.sub(r"\s+", "", res.text)
        return res if res != "--" else None
