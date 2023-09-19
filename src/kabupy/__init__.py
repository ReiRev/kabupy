"""A Python package for scraping Japanese stock information from various web sites."""

from __future__ import annotations

__version__ = "0.0.7"

from .jpx import Jpx
from .kabuyoho import Kabuyoho
from .minkabu import Minkabu

kabuyoho = Kabuyoho()
minkabu = Minkabu()
jpx = Jpx()
