# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kolmogorov-smirnov-test/. The authors are listed in prov/DWDQWW.jsonl.
"""Entry point named after the slug. The code lives in ks_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from ks_core import (
    ALTERNATIVES, SMALL_TAIL, kolmogorov_cdf, kolmogorov_sf, ks_1samp, ks_2samp, ks_2samp_stat,
    ks_statistic, smirnov_sf,
)

__all__ = ["ALTERNATIVES", "SMALL_TAIL", "kolmogorov_cdf", "kolmogorov_sf", "ks_1samp",
           "ks_2samp", "ks_2samp_stat", "ks_statistic", "smirnov_sf"]
