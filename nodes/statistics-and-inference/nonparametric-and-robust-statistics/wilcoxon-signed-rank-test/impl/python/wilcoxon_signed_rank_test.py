# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wilcoxon-signed-rank-test/. The authors are listed in prov/8KPP1Q.jsonl.
"""Entry point named after the slug. The code lives in wilcoxon_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from wilcoxon_core import (
    ALTERNATIVES, doubled_midranks, signed_rank_counts, tie_sizes, wilcoxon_normal,
    wilcoxon_signed_rank,
)

__all__ = ["ALTERNATIVES", "doubled_midranks", "signed_rank_counts", "tie_sizes",
           "wilcoxon_normal", "wilcoxon_signed_rank"]
