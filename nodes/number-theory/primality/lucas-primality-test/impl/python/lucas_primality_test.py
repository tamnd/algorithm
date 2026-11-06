# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lucas-primality-test/. The authors are listed in prov/12XYK5.jsonl.

"""Entry point for the Lucas primality test; the code is in lucas.py."""

from lucas import (
    distinct_prime_factors,
    is_prime_lucas,
    lucas_primality_test,
    lucas_witnesses,
    verify_lucas_witnesses,
)

__all__ = [
    "distinct_prime_factors",
    "is_prime_lucas",
    "lucas_primality_test",
    "lucas_witnesses",
    "verify_lucas_witnesses",
]
