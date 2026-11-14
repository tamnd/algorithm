# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chi-squared-goodness-of-fit-test/. The authors are listed in prov/B43M8J.jsonl.

"""Entry point named after the slug. The code lives in chi_squared_gof.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from chi_squared_gof import chi_squared_gof

__all__ = ["chi_squared_gof"]
