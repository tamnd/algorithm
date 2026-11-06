# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fermat-primality-test/. The authors are listed in prov/8TFPRS.jsonl.
"""Entry point named after the slug. The code is in fermat_primality.py,
because the tools treat a file whose name ends in _test as a test file."""

from fermat_primality import fermat_primality_test, fermat_test_bases, is_fermat_witness

__all__ = ["fermat_primality_test", "fermat_test_bases", "is_fermat_witness"]
