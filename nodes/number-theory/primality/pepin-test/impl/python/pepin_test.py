# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pepin-test/. The authors are listed in prov/SM5V45.jsonl.
"""Entry point named after the slug. The code is in pepin.py,
because the tools treat a file whose name ends in _test as a test file."""

from pepin import is_fermat_number_prime, pepin_residue, pepin_test, reduce_fermat

__all__ = ["is_fermat_number_prime", "pepin_residue", "pepin_test", "reduce_fermat"]
