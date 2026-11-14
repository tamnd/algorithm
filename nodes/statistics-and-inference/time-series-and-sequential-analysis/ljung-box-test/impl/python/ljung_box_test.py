# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ljung-box-test/. The authors are listed in prov/NPBB3C.jsonl.

"""Entry point named after the slug. The code lives in ljung_box.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from ljung_box import ljung_box, residual_autocorrelations

__all__ = ["ljung_box", "residual_autocorrelations"]
