# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mcdonald-kreitman-test/. The authors are listed in prov/4QSXZX.jsonl.

"""Entry point named after the slug. The code lives in mcdonald_kreitman.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from mcdonald_kreitman import MKResult, classify_codons, fisher_exact, mk_summary, mk_test, mk_test_from_counts

__all__ = ["MKResult", "classify_codons", "fisher_exact", "mk_summary", "mk_test", "mk_test_from_counts"]
