# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jury-stability-test/. The authors are listed in prov/7A0696.jsonl.

"""The Jury stability test. The code is in jury.py; this module re-exports it
under the name of the page (a file name ending in _test is read as a test file
by some tools, so the implementation itself lives in jury.py)."""

from jury import (  # noqa: F401
    JuryResult,
    is_schur,
    jury_classic,
    jury_table,
    outside_count,
)
