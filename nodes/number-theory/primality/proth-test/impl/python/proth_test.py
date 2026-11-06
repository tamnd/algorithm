# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proth-test/. The authors are listed in prov/ACSTC1.jsonl.
"""Entry point named after the slug. The code is in proth.py,
because the tools treat a file whose name ends in _test as a test file."""

from proth import is_proth_number, jacobi, proth_split, proth_test

__all__ = ["is_proth_number", "jacobi", "proth_split", "proth_test"]
