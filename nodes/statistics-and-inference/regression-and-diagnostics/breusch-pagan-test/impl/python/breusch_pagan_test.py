# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/breusch-pagan-test/. The authors are listed in prov/R9XRKX.jsonl.
"""Entry point named after the slug. The code lives in breusch_pagan_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from breusch_pagan_core import (
    BPResult, breusch_pagan, householder_qr, monte_carlo_p_values, residuals, statistics_from_residuals,
)

__all__ = ["BPResult", "breusch_pagan", "householder_qr", "monte_carlo_p_values", "residuals",
           "statistics_from_residuals"]
