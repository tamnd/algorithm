# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mcnemar-test/. The authors are listed in prov/H919BT.jsonl.

"""Entry point named after the slug. The code lives in mcnemar.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from mcnemar import mcnemar_statistic, mcnemar_test

__all__ = ["mcnemar_statistic", "mcnemar_test"]
