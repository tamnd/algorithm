# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schur-cohn-test/. The authors are listed in prov/AXFQZ4.jsonl.

"""The Schur-Cohn test. The code is in schur_cohn.py; this module re-exports it
under the name of the page (a file name ending in _test is read as a test file
by some tools, so the implementation itself lives in schur_cohn.py)."""

from schur_cohn import (  # noqa: F401
    SchurCohnResult,
    is_schur_stable,
    poly_from_roots,
    schur_cohn,
    taylor_shift_scale,
    to_gq,
)
