"""Base class for webpage"""
from __future__ import annotations

import re
from typing import Literal

from money import Money

from ..base import Webpage, webpage_property
from ..errors import ElementNotFoundError
from ..util import str2money


class MinkabuWebpage(Webpage):
    """Base class for minkabu webpage."""

    security_code: str

    @webpage_property
    def name(self) -> str | None:
        """Name of the stock, 銘柄名."""
        return self.select_one("p.md_stockBoard_stockName").text

    @webpage_property
    def market_segment(self) -> Literal["tse_prime", "tse_standard", "tse_growth"] | None:
        """Market segment, 市場区分."""
        segment = self.select_one("div.stock_label").text
        segment = re.sub(r"[\d+\s+]", "", segment)
        if segment == "東証プライム":
            return "tse_prime"
        if segment == "東証スタンダード":
            return "tse_standard"
        if segment == "東証グロース":
            return "tse_growth"
        return None

    @webpage_property
    def price(self) -> Money | None:
        """Price of the stock, 株価."""
        tag = self.select_one("div#stock-for-securities-company")
        amount = tag.get("data-price")
        if isinstance(amount, str):
            return str2money(amount)
        raise ElementNotFoundError("price")
