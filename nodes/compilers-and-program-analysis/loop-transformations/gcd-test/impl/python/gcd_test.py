# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gcd-test/. The authors are listed in prov/M4BM5N.jsonl.
"""Entry point named after the slug. The code is in gcd_dependence.py,
because the tools treat a file whose name ends in _test as a test file."""

from gcd_dependence import equation, ext_gcd, gcd_test, gcd_test_subscript, solve_linear

__all__ = ["equation", "ext_gcd", "gcd_test", "gcd_test_subscript", "solve_linear"]
