# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-block-design/. The authors are listed in prov/24Z82C.jsonl.
"""Randomized complete block design: randomization and the two-way additive analysis.

y[i][j] is the response of treatment i (t treatments) in block j (b blocks). The model is
y[i][j] = mu + tau_i + beta_j + e[i][j]: blocks and treatments add, with no interaction.
"""

import random
from collections.abc import Sequence
from typing import NamedTuple


class BlockAnova(NamedTuple):
    ss_treat: float
    ss_block: float
    ss_error: float
    df_treat: int
    df_block: int
    df_error: int
    f_treat: float
    mse: float


def randomize(t: int, b: int, rng: random.Random) -> list[list[int]]:
    """For each block, an independent uniform permutation: plot p of block j gets treatment
    plan[j][p]. Every treatment appears exactly once in every block."""
    plan = []
    for _ in range(b):
        order = list(range(t))
        rng.shuffle(order)  # Fisher-Yates
        plan.append(order)
    return plan


def rcbd_anova(y: Sequence[Sequence[float]]) -> BlockAnova:
    """Sums of squares for treatments, blocks and error, by two passes over the t x b table."""
    t, b = len(y), len(y[0])
    if t < 2 or b < 2 or any(len(r) != b for r in y):
        raise ValueError("need a complete t x b table with t, b >= 2")
    grand = sum(map(sum, y)) / (t * b)
    tm = [sum(r) / b for r in y]
    bm = [sum(y[i][j] for i in range(t)) / t for j in range(b)]
    ss_treat = b * sum((m - grand) ** 2 for m in tm)
    ss_block = t * sum((m - grand) ** 2 for m in bm)
    ss_error = sum((y[i][j] - tm[i] - bm[j] + grand) ** 2 for i in range(t) for j in range(b))
    df_t, df_b, df_e = t - 1, b - 1, (t - 1) * (b - 1)
    mse = ss_error / df_e
    if mse == 0.0:
        raise ValueError("the residuals are all zero")
    return BlockAnova(ss_treat, ss_block, ss_error, df_t, df_b, df_e, (ss_treat / df_t) / mse, mse)


def relative_efficiency(y: Sequence[Sequence[float]]) -> float:
    """Estimated variance of a completely randomized design on the same units over the
    blocked error variance: ((b - 1) MSB + b (t - 1) MSE) / ((tb - 1) MSE)."""
    a = rcbd_anova(y)
    t, b = a.df_treat + 1, a.df_block + 1
    msb = a.ss_block / a.df_block
    return ((b - 1) * msb + b * (t - 1) * a.mse) / ((t * b - 1) * a.mse)
