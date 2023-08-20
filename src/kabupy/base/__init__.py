"""Base classes."""
from __future__ import annotations

from .webpage import Webpage
from .website import Website
from .decorators import webpage_property

__all__ = ["Website", "Webpage", "webpage_property"]
