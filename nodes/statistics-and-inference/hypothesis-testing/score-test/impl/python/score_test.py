# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/score-test/. The authors are listed in prov/6H761T.jsonl.
"""Entry point named after the slug. The code lives in score_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from score_core import (binomial_score, multinomial_score, normal_mean_score, poisson_score,
                        score_test, solve)

__all__ = ["binomial_score", "multinomial_score", "normal_mean_score", "poisson_score",
           "score_test", "solve"]
