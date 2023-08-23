"""Base class for webpage"""
from __future__ import annotations

from money import Money

from ..base import Webpage, webpage_property
from ..util import str2money


class KabuyohoWebpage(Webpage):
    """Base class for kabuyoho webpage"""

    security_code: str

    def term2description(self, term: str) -> str | None:
        res = self.soup.select_one(f'main dt:-soup-contains("{term}") + dd')
        if res is None:
            return None
        return res.text

    @webpage_property
    def price(self) -> Money | None:
        """Price of the stock: 価格"""
        amount = self.soup.select_one('main li p:-soup-contains("株価","(","/",")") + p')
        if amount is None:
            return None
        return str2money(amount.text)

    @webpage_property
    def name(self) -> str | None:
        """Name of the stock: 銘柄名"""
        res = self.soup.select_one(f"main ul:-soup-contains('{self.security_code}') > li")
        if res is None:
            return None
        return res.text
