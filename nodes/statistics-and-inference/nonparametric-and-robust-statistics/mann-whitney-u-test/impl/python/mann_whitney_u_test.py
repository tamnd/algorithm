# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mann-whitney-u-test/. The authors are listed in prov/9WF4CP.jsonl.
"""Entry point named after the slug. The code lives in mann_whitney_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from mann_whitney_core import (
    ALTERNATIVES, doubled_midranks, mann_whitney, mann_whitney_normal, null_counts_2u, tie_sizes,
    u_statistic,
)

__all__ = ["ALTERNATIVES", "doubled_midranks", "mann_whitney", "mann_whitney_normal",
           "null_counts_2u", "tie_sizes", "u_statistic"]
