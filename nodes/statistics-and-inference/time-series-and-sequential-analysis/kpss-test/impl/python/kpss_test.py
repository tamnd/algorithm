# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kpss-test/. The authors are listed in prov/AWK28P.jsonl.
"""Entry point named after the slug. The code lives in kpss_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from kpss_core import (KPSS_TABLE, autocovariances, bandwidth, bartlett, cvm_limit_sf, detrend,
                       kpss, long_run_variance, simulate_null, table_p_value)

__all__ = ["KPSS_TABLE", "autocovariances", "bandwidth", "bartlett", "cvm_limit_sf", "detrend",
           "kpss", "long_run_variance", "simulate_null", "table_p_value"]
