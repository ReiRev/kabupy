"""Scraper for https://kabuyoho.jp/sp/reportDps"""
from __future__ import annotations

import functools
import logging
import re
import urllib.parse
from datetime import datetime

import time

from ..base import Website
from ..errors import ElementNotFoundError
from .kabuyoho_webpage import KabuyohoWebpage
from ..constatns import TIME_SLEEP

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
    def market_report(self) -> KabuyohoNewsWebpage:
        """Market report page in a report news page."""
        return KabuyohoNewsWebpage(self.website, self.security_code, 1)

    @functools.cached_property
    def flash_report(self) -> KabuyohoNewsWebpage:
        """Flash report page in a report news page."""
        return KabuyohoNewsWebpage(self.website, self.security_code, 2)

    @functools.cached_property
    def analyst_prediction(self) -> KabuyohoNewsWebpage:
        """Analyst prediction page in a report news page."""
        return KabuyohoNewsWebpage(self.website, self.security_code, 3)

    @functools.cached_property
    def analyst_evaluation(self) -> KabuyohoNewsWebpage:
        """Analyst evaluation page in a report news page."""
        return KabuyohoNewsWebpage(self.website, self.security_code, 4)


class KabuyohoNewsWebpage(KabuyohoWebpage):
    """Kabuyoho news page object."""

    def __init__(self, website: Website, security_code: str | int, category: int) -> None:
        self.website = website
        self.security_code = str(security_code)
        self.category = category
        self.url = urllib.parse.urljoin(
            self.website.url, f"sp/reportNews?bcode={self.security_code}&cat={self.category}"
        )
        super().__init__()

    def get_max_page(self) -> int:
        """Max page number."""
        try:
            page = self.select_one("div.pager > ul > li.interval + li")
        except ElementNotFoundError:
            return 1
        return int(re.sub(r"[\D]", "", page.text))

    def get_links(self, max_page: int | None = 1, time_sleep: float = TIME_SLEEP) -> list[dict]:
        """list of links.

        Args:
            max_page (int | None, optional): Max page number. Defaults to 1. If None, all pages are scraped.

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
        res = []
        if max_page is None:
            max_page = self.get_max_page()
        else:
            max_page = min(max_page, self.get_max_page())
        for p in range(1, max_page + 1):
            if p > 1:
                time.sleep(time_sleep)
                self.url = self.url + f"&page={p}"
                self.load()
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
                    weathers[i] = weather if weather != "wthr" else None
            urls = self.select("div.sp_news_list > ul a")
            urls = [u.get("href") for u in urls]
            urls = [urllib.parse.urljoin(self.website.url, u) for u in urls if isinstance(u, str)]
            res = res + [
                {"date": date, "title": title, "category": category, "weather": weather, "url": url}
                for date, title, category, weather, url in zip(dates, titles, categories, weathers, urls)
            ]
        return res
