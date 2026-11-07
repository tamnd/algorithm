# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rabin-irreducibility-test/. The authors are listed in prov/6CAYMS.jsonl.
"""Entry point named after the slug. The code is in rabin_irreducibility.py,
because the tools treat a file whose name ends in _test as a test file."""

from rabin_irreducibility import is_irreducible

__all__ = ["is_irreducible"]
