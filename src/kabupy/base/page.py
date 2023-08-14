"""Base class for website"""
from __future__ import annotations

from abc import ABC

import requests
from bs4 import BeautifulSoup


class Page(ABC):
    """Base class for website"""

    url: str
    html: str
    soup: BeautifulSoup

    def __init__(self):
        self.load()

    def load(self):
        response = requests.get(self.url, timeout=10)
        response.raise_for_status()
        self.html = response.text
        self.soup = BeautifulSoup(self.html, "html.parser")
