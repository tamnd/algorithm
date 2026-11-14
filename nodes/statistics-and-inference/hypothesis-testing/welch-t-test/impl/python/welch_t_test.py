# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/welch-t-test/. The authors are listed in prov/C3KW5Q.jsonl.
"""Entry point named after the slug. The code lives in welch_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from welch_core import ALTERNATIVES, welch_df, welch_t_test

__all__ = ["ALTERNATIVES", "welch_df", "welch_t_test"]
