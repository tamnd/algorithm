# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/power-of-d-choices-theorem/. The authors are listed in prov/AKHE82.jsonl.

"""Numbers of the layered induction proof of the power of d choices theorem.

betas gives the thresholds beta_6 = n / (2e), beta_{i+1} = e * beta_i^d / n^(d-1).
i_star is the first level where the expected number of high balls n p_i falls
below 2 ln n; the proof bounds the maximum load by i_star + 2.
greedy_max_load simulates the d-choice process to compare with the bound.
"""

import math
import random


def betas(n: int, d: int) -> dict[int, float]:
    """The thresholds beta_i for i = 6, 7, ..., up to and including level i_star."""
    if n < 2 or d < 2:
        raise ValueError("need n >= 2 and d >= 2")
    out = {6: n / (2 * math.e)}
    i = 6
    while n * (out[i] / n) ** d >= 2 * math.log(n):
        out[i + 1] = math.e * out[i] ** d / n ** (d - 1)
        i += 1
    return out


def i_star(n: int, d: int) -> int:
    """The least i >= 6 with n (beta_i / n)^d < 2 ln n."""
    return max(betas(n, d))


def proof_bound(n: int, d: int) -> int:
    """The maximum load bound i_star + 2 of the proof."""
    return i_star(n, d) + 2


def closed_form_bound(n: int, d: int) -> float:
    """beta_{6+j} <= n / 2^(d^j); this returns the right side for each level of betas."""
    return min(n / 2 ** (d ** (i - 6)) for i in betas(n, d))


def failure_bound(n: int, d: int) -> float:
    """The failure probability of the proof: (i_star + 1)/n^2 + C(n,2) (6 ln n / n)^(2d)."""
    return (i_star(n, d) + 1) / n ** 2 + math.comb(n, 2) * (6 * math.log(n) / n) ** (2 * d)


def greedy_max_load(n: int, m: int, d: int, rng: random.Random) -> int:
    """Place m balls into n bins, each into the least loaded of d uniform samples."""
    loads = [0] * n
    for _ in range(m):
        best = rng.randrange(n)
        for _ in range(d - 1):
            b = rng.randrange(n)
            if loads[b] < loads[best]:
                best = b
        loads[best] += 1
    return max(loads)


def leading_term(n: int, d: int) -> float:
    """ln ln n / ln d."""
    return math.log(math.log(n)) / math.log(d)
