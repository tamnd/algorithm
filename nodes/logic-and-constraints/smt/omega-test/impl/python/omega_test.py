# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/omega-test/. The authors are listed in prov/8M5CJY.jsonl.

"""Entry point for the omega test, under the file name of the slug.

The code is in omega.py. A file name that ends in "_test" is read as a test
file by the tools, so the line markers of the pseudocode live in omega.py.
"""

from omega import Omega, bounds_on, dark_shadow, holds, mod_hat, normalize_ineq, real_shadow, solve, splinters

__all__ = ["Omega", "bounds_on", "dark_shadow", "holds", "mod_hat", "normalize_ineq", "real_shadow", "solve", "splinters"]
