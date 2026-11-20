# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fourier-amplitude-sensitivity-test/. The authors are listed in prov/VVPHQA.jsonl.
"""Entry point named after the slug. The code lives in efast.py, because tools treat
a file whose name ends in _test.py as a test file and skip its line markers."""

from efast import efast, frequencies, search_points, spectrum

__all__ = ["efast", "frequencies", "search_points", "spectrum"]
