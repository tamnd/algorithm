# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shapiro-wilk-test/. The authors are listed in prov/F6R58F.jsonl.
"""Entry point named after the slug. The code lives in sw_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from sw_core import shapiro_wilk, shapiro_wilk_coefficients

__all__ = ["shapiro_wilk", "shapiro_wilk_coefficients"]
