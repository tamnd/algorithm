# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anderson-darling-test/. The authors are listed in prov/7ZCNKW.jsonl.
"""Entry point named after the slug. The code lives in ad_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from ad_core import ad_statistic, ad_statistic_u, ad_test, adinf_cdf

__all__ = ["ad_statistic", "ad_statistic_u", "ad_test", "adinf_cdf"]
