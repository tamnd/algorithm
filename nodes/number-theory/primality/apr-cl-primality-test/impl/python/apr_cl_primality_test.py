# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/apr-cl-primality-test/. The authors are listed in prov/MW7HYF.jsonl.
"""Entry point named after the slug. The code is in apr_cl.py,
because the tools treat a file whose name ends in _test as a test file."""

from apr_cl import (
    T_TABLE,
    Plan,
    Report,
    aprcl,
    candidate_primes,
    divisor_search,
    extra_check,
    gauss_jacobi_check,
    jacobi_power,
    jacobi_sums,
    jacobi_symbol,
    make_plan,
    plan,
    primitive_root,
    trace,
    unit_w,
)

__all__ = [
    "T_TABLE",
    "Plan",
    "Report",
    "aprcl",
    "candidate_primes",
    "divisor_search",
    "extra_check",
    "gauss_jacobi_check",
    "jacobi_power",
    "jacobi_sums",
    "jacobi_symbol",
    "make_plan",
    "plan",
    "primitive_root",
    "trace",
    "unit_w",
]
