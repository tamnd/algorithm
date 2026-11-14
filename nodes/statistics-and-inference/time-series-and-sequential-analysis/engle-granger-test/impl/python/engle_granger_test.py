# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/engle-granger-test/. The authors are listed in prov/33J9EX.jsonl.
"""Entry point named after the slug. The code lives in eg_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from eg_core import (MACKINNON_2010, engle_granger, error_correction, mackinnon_critical_value, ols,
                     residual_adf, select_lags, simulate_null)

__all__ = ["MACKINNON_2010", "engle_granger", "error_correction", "mackinnon_critical_value", "ols",
           "residual_adf", "select_lags", "simulate_null"]
