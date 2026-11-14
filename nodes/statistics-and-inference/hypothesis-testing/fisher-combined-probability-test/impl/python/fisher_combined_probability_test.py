# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fisher-combined-probability-test/. The authors are listed in prov/SR875B.jsonl.
"""Entry point named after the slug. The code lives in fisher_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from fisher_core import fisher_method

__all__ = ["fisher_method"]
