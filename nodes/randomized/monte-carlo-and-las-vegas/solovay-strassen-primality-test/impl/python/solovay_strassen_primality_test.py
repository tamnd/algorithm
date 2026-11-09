# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/solovay-strassen-primality-test/. The authors are listed in prov/XD7T81.jsonl.
"""Entry point named after the slug. The code is in solovay_strassen.py,
because the tools treat a file whose name ends in _test as a test file."""

from solovay_strassen import is_euler_probable_prime, jacobi, solovay_strassen

__all__ = ["is_euler_probable_prime", "jacobi", "solovay_strassen"]
