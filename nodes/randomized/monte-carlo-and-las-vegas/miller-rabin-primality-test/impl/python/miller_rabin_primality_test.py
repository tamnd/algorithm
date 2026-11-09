# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/miller-rabin-primality-test/. The authors are listed in prov/HSYVA5.jsonl.
"""Entry point named after the slug. The code is in miller_rabin.py,
because the tools treat a file whose name ends in _test as a test file."""

from miller_rabin import decompose, is_strong_probable_prime, miller_rabin, strong_sequence

__all__ = ["decompose", "is_strong_probable_prime", "miller_rabin", "strong_sequence"]
