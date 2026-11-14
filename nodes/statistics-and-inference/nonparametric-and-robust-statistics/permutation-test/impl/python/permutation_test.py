# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/permutation-test/. The authors are listed in prov/KSN49K.jsonl.
"""Entry point named after the slug. The code lives in permutation_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from permutation_core import ALTERNATIVES, mean_difference, permutation_test, sign_flip_test

__all__ = ["ALTERNATIVES", "mean_difference", "permutation_test", "sign_flip_test"]
