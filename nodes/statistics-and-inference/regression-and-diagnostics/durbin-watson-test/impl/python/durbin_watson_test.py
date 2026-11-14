# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/durbin-watson-test/. The authors are listed in prov/TBDQN3.jsonl.
"""Entry point named after the slug. The code lives in durbin_watson_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from durbin_watson_core import (
    DWResult, bound_eigenvalues, bounds_p_values, durbin_watson, dw_statistic, householder_q1, project_out,
)

__all__ = ["DWResult", "bound_eigenvalues", "bounds_p_values", "durbin_watson", "dw_statistic",
           "householder_q1", "project_out"]
