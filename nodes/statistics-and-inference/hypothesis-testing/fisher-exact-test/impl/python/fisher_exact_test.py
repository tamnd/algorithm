# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fisher-exact-test/. The authors are listed in prov/PNP35A.jsonl.

"""Entry point named after the slug. The code lives in fisher_exact.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from fisher_exact import fisher_exact, hypergeometric_weights

__all__ = ["fisher_exact", "hypergeometric_weights"]
