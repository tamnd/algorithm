# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kruskal-wallis-test/. The authors are listed in prov/DCECK4.jsonl.
"""Entry point named after the slug. The code lives in kruskal_wallis_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from kruskal_wallis_core import (
    doubled_midranks, h_statistic, kruskal_wallis, labeling_counts, tie_sizes,
)

__all__ = ["doubled_midranks", "h_statistic", "kruskal_wallis", "labeling_counts", "tie_sizes"]
