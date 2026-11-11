# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/push-sum/. The authors are listed in prov/X9WP5N.jsonl.

"""Push-sum (Kempe, Dobra and Gehrke 2003) in synchronous rounds.

Every node keeps a pair (s, w). In each round it sends half of the pair to a
target chosen uniformly from all n nodes (itself included, as in the paper)
and the other half to itself, then sums what it received. The estimate of
node i is s_i / w_i. With exact=True the pairs are Fractions, so the sum of
the s values and the sum of the w values can be compared exactly.
"""

import math
import random
from fractions import Fraction
from typing import Sequence


def round_step(s: list, w: list, targets: Sequence[int]) -> tuple[list, list]:
    """One round with the given targets: node i sends half to targets[i]."""
    n = len(s)
    ns = [s[i] / 2 for i in range(n)]            # @line L4
    nw = [w[i] / 2 for i in range(n)]
    for i in range(n):
        f = targets[i]
        ns[f] += s[i] / 2                        # @line L5
        nw[f] += w[i] / 2
    return ns, nw                                # @line L6


def run(x: Sequence, rounds: int, seed: int, exact: bool = False) -> list[tuple[list, list]]:
    """The pairs (s, w) after each round, starting from (x_i, 1)."""
    rng = random.Random(seed)
    n = len(x)
    if exact:
        s = [Fraction(v) for v in x]             # @line L1
        w = [Fraction(1)] * n
    else:
        s = [float(v) for v in x]
        w = [1.0] * n
    hist = [(s, w)]
    for _ in range(rounds):                      # @line L2
        targets = [rng.randrange(n) for _ in range(n)]   # @line L3
        s, w = round_step(s, w, targets)
        hist.append((s, w))
    return hist


def estimates(s: list, w: list) -> list:
    return [a / b for a, b in zip(s, w)]         # @line L7


def relative_error(x: Sequence[float], s: list, w: list) -> float:
    """The largest |s_i/w_i - mean| over nodes, divided by the mean of |x_j|.
    This is the error that Theorem 3.1 of Kempe et al. bounds by eps."""
    n = len(x)
    mean = sum(x) / n
    scale = sum(abs(v) for v in x) / n
    return max(abs(a / b - mean) for a, b in zip(s, w)) / scale


def potential(v: list[list], w: list) -> object:
    """Phi = sum_i sum_j (v_ij - w_i / n)^2 for contribution vectors v_i."""
    n = len(w)
    return sum((v[i][j] - w[i] / n) ** 2 for i in range(n) for j in range(n))


def contribution_step(v: list[list], w: list, targets: Sequence[int]) -> tuple[list[list], list]:
    """Push-sum run on the contribution vectors: node i holds v_i, with
    s_i = sum_j v_ij x_j, and w_i = sum_j v_ij."""
    n = len(w)
    nv = [[c / 2 for c in v[i]] for i in range(n)]
    nw = [w[i] / 2 for i in range(n)]
    for i in range(n):
        f = targets[i]
        for j in range(n):
            nv[f][j] += v[i][j] / 2
        nw[f] += w[i] / 2
    return nv, nw


def kdg_rounds(n: int, eps: float, delta: float) -> int:
    """The explicit round count of the proof on the page:
    tau = 4 log2 n + log2(2/delta) rounds of push rumor spreading, and
    t = 3 log2 n + 2 log2(1/eps) + log2(2/delta) + 2 tau."""
    tau = math.ceil(4 * math.log2(n) + math.log2(2 / delta))
    return math.ceil(3 * math.log2(n) + 2 * math.log2(1 / eps) + math.log2(2 / delta) + 2 * tau)


def rounds_to_eps(x: Sequence[float], eps: float, seed: int, limit: int = 1000) -> int:
    rng = random.Random(seed)
    n = len(x)
    s = [float(v) for v in x]
    w = [1.0] * n
    t = 0
    while relative_error(x, s, w) > eps and t < limit:
        s, w = round_step(s, w, [rng.randrange(n) for _ in range(n)])
        t += 1
    return t
