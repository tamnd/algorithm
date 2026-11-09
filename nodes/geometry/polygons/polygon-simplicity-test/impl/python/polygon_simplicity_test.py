# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polygon-simplicity-test/. The authors are listed in prov/HSYKXN.jsonl.

"""Entry point named after the slug. The code lives in simplicity_check.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from simplicity_check import find_violation, is_simple, orient, segments_intersect

__all__ = ["find_violation", "is_simple", "orient", "segments_intersect"]
