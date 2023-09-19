"""Scraper for minkabu.jp"""
from __future__ import annotations

import functools
import logging

from ..base import Website
from .top import Top

logger = logging.getLogger(__name__)


class Minkabu(Website):
    """An object for minkabu.jp"""

    def __init__(self) -> None:
        self.url = "https://minkabu.jp"

    def stock(self, security_code: str | int) -> Stock:
        """Return Stock object"""
        return Stock(self, security_code)


class Stock:
    """Stock object for minkabu.jp"""

    def __init__(self, website: Minkabu, security_code: str | int) -> None:
        self.security_code = str(security_code)
        self.website = website

    @functools.cached_property
    def top(self) -> Top:
        """Top page object"""
        return Top(self.website, self.security_code)
