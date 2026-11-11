# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gossip-averaging/. The authors are listed in prov/ZSVD30.jsonl.

"""Randomized pairwise gossip averaging (Boyd, Ghosh, Prabhakar and Shah 2006).

Time is counted in clock ticks. In the asynchronous model of the paper each
node has a rate 1 Poisson clock, so the ticks of all clocks form one rate n
Poisson process and each tick belongs to a uniform random node. At a tick
of node i, node i picks j with probability P[i][j] and both nodes replace
their values by the mean. Here P is the natural random walk, P[i][j] = 1/d_i.
"""

import math
import random
from fractions import Fraction


def complete(n: int) -> list[list[int]]:
    return [[j for j in range(n) if j != i] for i in range(n)]


def cycle(n: int) -> list[list[int]]:
    return [[(i - 1) % n, (i + 1) % n] for i in range(n)]


def torus(s: int) -> list[list[int]]:
    """The s by s grid with wrap around, so every degree is 4 (s >= 3)."""
    adj = []
    for a in range(s):
        for b in range(s):
            adj.append([((a + 1) % s) * s + b, ((a - 1) % s) * s + b,
                        a * s + (b + 1) % s, a * s + (b - 1) % s])
    return adj


def tick(adj: list[list[int]], x: list, rng: random.Random) -> tuple[int, int]:
    i = rng.randrange(len(adj))                  # @line L2
    j = adj[i][rng.randrange(len(adj[i]))]       # @line L3
    xi, xj = x[i], x[j]                          # @line L4
    m = (xi + xj) / 2                            # @line L5
    x[i] = m                                     # @line L6
    x[j] = m
    return i, j


def ticks_to_eps(adj: list[list[int]], x0: list[float], eps: float, rng: random.Random,
                 limit: int = 10**7) -> int:
    """The number of ticks until ||x - avg 1|| <= eps ||x(0) - avg 1||. The
    squared error is updated in O(1) per tick."""
    x = list(x0)
    avg = sum(x) / len(x)
    err2 = sum((v - avg) ** 2 for v in x)
    goal = eps * eps * err2
    t = 0
    while err2 > goal and t < limit:
        i = rng.randrange(len(adj))
        j = adj[i][rng.randrange(len(adj[i]))]
        before = (x[i] - avg) ** 2 + (x[j] - avg) ** 2
        m = (x[i] + x[j]) / 2
        x[i] = x[j] = m
        err2 += 2 * (m - avg) ** 2 - before
        t += 1
    return t


def expected_matrix(adj: list[list[int]]) -> list[list[float]]:
    """W-bar = I - D/(2n) + (P + P^T)/(2n), with D_i = sum_j (P_ij + P_ji)."""
    n = len(adj)
    p = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in adj[i]:
            p[i][j] += 1.0 / len(adj[i])
    w = [[(p[i][j] + p[j][i]) / (2 * n) for j in range(n)] for i in range(n)]
    for i in range(n):
        d = sum(p[i][j] + p[j][i] for j in range(n))
        w[i][i] += 1.0 - d / (2 * n)
    return w


def lambda2(w: list[list[float]], iters: int = 4000, seed: int = 1) -> float:
    """The largest eigenvalue of W on the vectors orthogonal to 1, by power
    iteration. W-bar is symmetric and positive semidefinite (an average of
    projections), so this eigenvalue is lambda_2 and also the SLEM."""
    n = len(w)
    rng = random.Random(seed)
    x = [rng.gauss(0.0, 1.0) for _ in range(n)]
    est = 0.0
    for _ in range(iters):
        a = sum(x) / n
        x = [v - a for v in x]
        norm = math.sqrt(sum(v * v for v in x))
        x = [v / norm for v in x]
        y = [sum(r[k] * x[k] for k in range(n)) for r in w]
        est = sum(a * b for a, b in zip(x, y))
        x = y
    return est


def lambda2_closed_form(kind: str, n: int) -> float:
    """lambda_2(W-bar) = 1 - (1 - lambda_2(P)) / n for a symmetric P."""
    if kind == "complete":
        lp = -1.0 / (n - 1)
    elif kind == "cycle":
        lp = math.cos(2 * math.pi / n)
    else:
        s = math.isqrt(n)
        lp = (1 + math.cos(2 * math.pi / s)) / 2
    return 1 - (1 - lp) / n


def predicted_ticks(lam2: float, eps: float) -> float:
    """log(1/eps) / log(1/lambda_2): Theorem 3 of Boyd et al. puts the
    eps-averaging time between 0.5 and 3 times this many ticks."""
    return math.log(1 / eps) / math.log(1 / lam2)


def exact_run(adj: list[list[int]], x0: list[int], ticks: int, seed: int) -> list[Fraction]:
    rng = random.Random(seed)
    x = [Fraction(v) for v in x0]
    for _ in range(ticks):                       # @line L1
        tick(adj, x, rng)
    return x
