"""Scraper for kabuyoho.jp"""
from __future__ import annotations

import functools
import logging

from ..base import Website
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


class Stock:
    """Stock object for kabuyoho.jp"""

    def __init__(self, website: Kabuyoho, security_code: str | int) -> None:
        self.security_code = str(security_code)
        self.website = website

    @functools.cached_property
    def report_top(self) -> ReportTop:
        return ReportTop(self.website, self.security_code)

    @functools.cached_property
    def report_target(self) -> ReportTarget:
        return ReportTarget(self.website, self.security_code)

    @functools.cached_property
    def report_dps(self) -> ReportDps:
        return ReportDps(self.website, self.security_code)
