# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regression-f-test/. The authors are listed in prov/KE7D2K.jsonl.
"""Entry point named after the slug. The code lives in regression_f_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from regression_f_core import (
    RANK_TOL, back_substitute, coefficient_t_tests, householder_qr, linear_hypothesis_f_test,
    nested_f_test, ols_fit, overall_f_test, r_inverse,
)

__all__ = ["RANK_TOL", "back_substitute", "coefficient_t_tests", "householder_qr",
           "linear_hypothesis_f_test", "nested_f_test", "ols_fit", "overall_f_test", "r_inverse"]
