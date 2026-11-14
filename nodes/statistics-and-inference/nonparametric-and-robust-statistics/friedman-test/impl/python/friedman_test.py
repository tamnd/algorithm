# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/friedman-test/. The authors are listed in prov/DRZ1M4.jsonl.
"""Entry point named after the slug. The code lives in friedman_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from friedman_core import doubled_midranks, friedman, q_statistic, rank_sum_counts

__all__ = ["doubled_midranks", "friedman", "q_statistic", "rank_sum_counts"]
