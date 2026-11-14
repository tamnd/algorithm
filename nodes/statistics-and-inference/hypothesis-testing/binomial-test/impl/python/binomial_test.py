# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binomial-test/. The authors are listed in prov/P6MXFM.jsonl.

"""Entry point named after the slug. The code lives in binomial_exact.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from binomial_exact import RELATIVE_TOLERANCE, binomial_pmf, binomial_test

__all__ = ["RELATIVE_TOLERANCE", "binomial_pmf", "binomial_test"]
