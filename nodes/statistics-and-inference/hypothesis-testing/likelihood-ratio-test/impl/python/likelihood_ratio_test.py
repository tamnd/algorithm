# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/likelihood-ratio-test/. The authors are listed in prov/04CJ2P.jsonl.
"""Entry point named after the slug. The code lives in lrt_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from lrt_core import (binomial_lrt, deviance_term, likelihood_ratio_test, most_powerful_test,
                      multinomial_lrt, normal_mean_lrt, poisson_lrt)

__all__ = ["binomial_lrt", "deviance_term", "likelihood_ratio_test", "most_powerful_test",
           "multinomial_lrt", "normal_mean_lrt", "poisson_lrt"]
