# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lowe-ratio-test/. The authors are listed in prov/GBD07V.jsonl.

"""Entry point named after the slug. The code is in lowe_ratio.py,
because the tools treat a file whose name ends in _test as a test file."""

from lowe_ratio import nearest_two, ratio_test_match, sqdist

__all__ = ["nearest_two", "ratio_test_match", "sqdist"]
