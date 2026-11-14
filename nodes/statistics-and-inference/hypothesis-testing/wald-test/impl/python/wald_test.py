# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wald-test/. The authors are listed in prov/QP1T8S.jsonl.
"""Entry point named after the slug. The code lives in wald_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from wald_core import (binomial_wald, logit_binomial_wald, normal_mean_wald, poisson_wald,
                       solve, wald_test)

__all__ = ["binomial_wald", "logit_binomial_wald", "normal_mean_wald", "poisson_wald",
           "solve", "wald_test"]
