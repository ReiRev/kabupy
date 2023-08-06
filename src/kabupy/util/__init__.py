"""util functions"""
import re

from money import Money

__all__ = ["str2money"]

jpy_unit = str.maketrans({"千": "0" * 3, "万": "0" * 5, "億": "0" * 8})


def str2money(price: str) -> Money:
    """Convert str to JPY Money object"""
    amount = price.translate(jpy_unit)
    amount = re.sub(r"\D", "", amount)
    return Money(amount, "JPY")
