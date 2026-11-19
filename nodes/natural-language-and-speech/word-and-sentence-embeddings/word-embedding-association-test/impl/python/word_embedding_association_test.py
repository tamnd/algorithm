# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/word-embedding-association-test/. The authors are listed in prov/R1EFZ2.jsonl.
"""Entry point named after the slug. The code lives in weat_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from weat_core import association, cosine, effect_size, sampled_p_value, weat, weat_statistic

__all__ = ["association", "cosine", "effect_size", "sampled_p_value", "weat", "weat_statistic"]
