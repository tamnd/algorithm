# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chi-squared-test-of-independence/. The authors are listed in prov/E5V169.jsonl.

"""Entry point named after the slug. The code lives in chi_squared_independence.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from chi_squared_independence import chi_squared_independence

__all__ = ["chi_squared_independence"]
