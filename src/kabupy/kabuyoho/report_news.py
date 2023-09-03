"""Scraper for https://kabuyoho.jp/sp/reportDps"""
from __future__ import annotations

import logging
import re
import urllib.parse
from datetime import datetime
import functools

from ..base import Website, webpage_property
from .kabuyoho_webpage import KabuyohoWebpage

logger = logging.getLogger(__name__)


class ReportNews(KabuyohoWebpage):
    """Report news page object."""

    def __init__(self, website: Website, security_code: str | int) -> None:
        self.website = website
        self.security_code = str(security_code)
        self.url = urllib.parse.urljoin(self.website.url, f"sp/reportNews?bcode={self.security_code}")
        # No need to call super().__init__() because this class does not have any webpage property.
        super().__init__(load=False)

    @functools.cached_property
    def flash_report(self) -> FlashReport:
        """Flash report page in a report news page."""
        return FlashReport(self.website, self.security_code)

    @functools.cached_property
    def market_report(self) -> MarketReport:
        """Market report page in a report news page."""
        return MarketReport(self.website, self.security_code)


class MarketReport(KabuyohoWebpage):
    """Market report page in a report news page."""

    def __init__(self, website: Website, security_code: str | int) -> None:
        self.website = website
        self.security_code = str(security_code)
        self.url = urllib.parse.urljoin(self.website.url, f"sp/reportNews?bcode={self.security_code}&cat=1")
        super().__init__()

    @webpage_property
    def links(self) -> list[dict]:
        """list of market reports(マーケット).

        Returns:
            list[dict]: List of news.

        Note:
            The example of the return value is as follows:
            [
                {
                    "date": datetime(2021, 3, 1, 12, 34),
                    "title": "FooBar",
                    "category": "決算",
                    "weather": "wthr_clud",
                    "url": "https://kabuyoho.jp/sp/example"
                },
                ...
            ]
        """
        dates = self.select("div.sp_news_list > ul span.time")
        dates = [datetime.strptime(re.sub(r"[\D]", "", d.text), "%Y%m%d%H%M") for d in dates]
        titles = self.select("div.sp_news_list > ul p.list_title")
        titles = [t.text for t in titles]
        categories = self.select("div.sp_news_list > ul span.ctgr")
        categories = [c.text for c in categories]
        weathers = self.select("div.sp_news_list > ul span.wthr")
        weathers = [w.get("class") for w in weathers]
        for i, weather in enumerate(weathers):
            if weather is None:
                weathers[i] = None
            elif isinstance(weather, list):
                _extracted = [w for w in weather if w != "wthr"]
                weathers[i] = _extracted[0] if len(_extracted) > 0 else None
            elif isinstance(weather, str):
                weathers[i] = weather
        urls = self.select("div.sp_news_list > ul a")
        urls = [u.get("href") for u in urls]
        urls = [urllib.parse.urljoin(self.website.url, u) for u in urls if isinstance(u, str)]
        return [
            {"date": date, "title": title, "category": category, "weather": weather, "url": url}
            for date, title, category, weather, url in zip(dates, titles, categories, weathers, urls)
        ]


class FlashReport(KabuyohoWebpage):
    """Flash report page in a report news page."""

    def __init__(self, website: Website, security_code: str | int) -> None:
        self.website = website
        self.security_code = str(security_code)
        self.url = urllib.parse.urljoin(self.website.url, f"sp/reportNews?bcode={self.security_code}&cat=2")
        super().__init__()

    @webpage_property
    def links(self) -> list[dict]:
        """list of flash reports(業績速報).

        Returns:
            list[dict]: List of news.

        Note:
            The example of the return value is as follows:
            [
                {
                    "date": datetime(2021, 3, 1, 12, 34),
                    "title": "FooBar",
                    "category": "決算",
                    "weather": "wthr_clud",
                    "url": "https://kabuyoho.jp/sp/example"
                },
                ...
            ]
        """
        dates = self.select("div.sp_news_list > ul span.time")
        dates = [datetime.strptime(re.sub(r"[\D]", "", d.text), "%Y%m%d%H%M") for d in dates]
        titles = self.select("div.sp_news_list > ul p.list_title")
        titles = [t.text for t in titles]
        categories = self.select("div.sp_news_list > ul span.ctgr")
        categories = [c.text for c in categories]
        weathers = self.select("div.sp_news_list > ul span.wthr")
        weathers = [w.get("class") for w in weathers]
        weathers = [[w for w in ws if w != "wthr"][0] for ws in weathers if isinstance(ws, list)]
        urls = self.select("div.sp_news_list > ul a")
        urls = [u.get("href") for u in urls]
        urls = [urllib.parse.urljoin(self.website.url, u) for u in urls if isinstance(u, str)]
        return [
            {"date": date, "title": title, "category": category, "weather": weather, "url": url}
            for date, title, category, weather, url in zip(dates, titles, categories, weathers, urls)
        ]
