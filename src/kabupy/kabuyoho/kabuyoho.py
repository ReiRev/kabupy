"""Scraper for kabuyoho.jp"""
from __future__ import annotations

import logging
import re

import requests
from bs4 import BeautifulSoup
from money import Money

from ..exceptions import InvalidElementError
from ..util import str2money

logger = logging.getLogger(__name__)


class Kabuyoho:
    """An object for kabuyoho.jp"""

    base_url = "https://kabuyoho.jp"

    def __init__(self) -> None:
        pass

    def stock(self, security_code: str | int) -> Stock:
        """Return Stock object"""
        return Stock(self, security_code)


class Stock:
    """Stock object for kabuyoho.jp"""

    def __init__(self, website: Kabuyoho, security_code: str | int) -> None:
        self.security_code = str(security_code)
        self.website = website

    @property
    def report_top_url(self) -> str:
        """URL of reportTop page"""
        return f"{self.website.base_url}/sp/reportTop?bcode={self.security_code}"

    @property
    def report_target_url(self) -> str:
        """URL of reportTop page"""
        return f"{self.website.base_url}/sp/reportTarget?bcode={self.security_code}"

    @property
    def price(self) -> Money | None:
        """Price of the stock

        Returns:
            float | None: Price if found or None
        """
        response = requests.get(self.report_top_url, timeout=10)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
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
        response = requests.get(self.report_top_url, timeout=10)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
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
        response = requests.get(self.report_target_url, timeout=10)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        amount = soup.select_one('tr>th:-soup-contains("理論株価(PER基準)") + td>span:-soup-contains("円")')
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def per_based_upside_target(self) -> Money | None:
        """PER based upside target(上値目途(PER基準))"""
        response = requests.get(self.report_target_url, timeout=10)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        amount = soup.select_one(
            'tr:has(>th:-soup-contains("理論株価(PER基準)")) ~ tr:has(>th:-soup-contains("上値目途"))>td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def per_based_downside_target(self) -> Money | None:
        """PER based downside target(下値目途(PER基準))"""
        response = requests.get(self.report_target_url, timeout=10)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        amount = soup.select_one(
            'tr:has(>th:-soup-contains("理論株価(PER基準)")) ~ tr:has(>th:-soup-contains("下値目途"))>td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def pbr_based_theoretical_stock_price(self) -> Money | None:
        """PBR based theoretical stock price(理論株価(PBR基準))"""
        response = requests.get(self.report_target_url, timeout=10)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        amount = soup.select_one('tr>th:-soup-contains("理論株価(PBR基準)") + td>span:-soup-contains("円")')
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def pbr_based_upside_target(self) -> Money | None:
        """PBR based upside target(上値目途(PBR基準))"""
        response = requests.get(self.report_target_url, timeout=10)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        amount = soup.select_one(
            'tr:has(>th:-soup-contains("理論株価(PBR基準)")) ~ tr:has(>th:-soup-contains("上値目途"))>td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def pbr_based_downside_target(self) -> Money | None:
        """PBR based downside target(下値目途(PBR基準))"""
        response = requests.get(self.report_target_url, timeout=10)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        amount = soup.select_one(
            'tr:has(>th:-soup-contains("理論株価(PBR基準)")) ~ tr:has(>th:-soup-contains("下値目途"))>td>span:-soup-contains("円")'
        )
        if amount is None:
            return None
        return str2money(amount.text)

    @property
    def price_target(self) -> Money | None:
        """Price target: 目標株価(アナリストが発表した目標株価の平均値)"""
        response = requests.get(self.report_target_url, timeout=10)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        amount = soup.select_one('thead:has(>tr>th:-soup-contains("平均")) ~ tbody>tr>td')
        if amount is None:
            return None
        return str2money(amount.text)
