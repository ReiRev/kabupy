from __future__ import annotations

import pytest


class Helpers:
    @staticmethod
    def html2text(filename: str):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def excel2bytes(filename: str):
        with open(filename, "rb") as f:
            return f.read()


@pytest.fixture
def helpers():
    return Helpers
