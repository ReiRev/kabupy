"""Scraper for kabuyoho.jp"""
from __future__ import annotations

import functools
import logging
import urllib.parse

from ..base import Website
from .kabuyoho_webpage import KabuyohoWebpage
from .report_dps import ReportDps
from .report_target import ReportTarget
from .report_top import ReportTop

logger = logging.getLogger(__name__)


class Kabuyoho(Website):
    """An object for kabuyoho.jp"""

    def __init__(self) -> None:
        self.url = "https://kabuyoho.jp"

    def stock(self, security_code: str | int) -> Stock:
        """Return Stock object"""
        return Stock(self, security_code)


class ReportDpsPage(KabuyohoWebpage):
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
    def report_top(self) -> KabuyohoWebpage:
        return ReportTop(self.website, self.security_code)

    @functools.cached_property
    def report_target(self) -> KabuyohoWebpage:
        return ReportTarget(self.website, self.security_code)

    @functools.cached_property
    def report_dps(self) -> KabuyohoWebpage:
        return ReportDps(self.website, self.security_code)
