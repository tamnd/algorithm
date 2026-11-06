# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lucas-lehmer-test/. The authors are listed in prov/X19VXC.jsonl.
"""Entry point named after the slug. The code is in lucas_lehmer.py,
because the tools treat a file whose name ends in _test as a test file."""

from lucas_lehmer import is_mersenne_number_prime, lucas_lehmer_residues, lucas_lehmer_test, reduce_mersenne

__all__ = ["is_mersenne_number_prime", "lucas_lehmer_residues", "lucas_lehmer_test", "reduce_mersenne"]
