# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extremal-optimization/. The authors are listed in prov/ZRWP63.jsonl.

import itertools
import random
from typing import Sequence

Couplings = Sequence[Sequence[float]]


def local_fitness(s: Sequence[int], J: Couplings) -> list[float]:
    """lambda_i = s_i * sum_j J_ij s_j. A large value means spin i agrees with its bonds."""
    n = len(s)
    return [s[i] * sum(J[i][j] * s[j] for j in range(n) if j != i) for i in range(n)]


def energy(s: Sequence[int], J: Couplings) -> float:
    """E(s) = -sum_{i<j} J_ij s_i s_j, which equals -1/2 * sum_i lambda_i."""
    n = len(s)
    return -sum(J[i][j] * s[i] * s[j] for i in range(n) for j in range(i + 1, n))


def rank_probabilities(n: int, tau: float) -> list[float]:
    """P(k) proportional to k^(-tau) for the ranks k = 1..n, as a list indexed by k - 1."""
    w = [k ** (-tau) for k in range(1, n + 1)]
    z = sum(w)
    return [x / z for x in w]


def draw_rank(cum: Sequence[float], rng: random.Random) -> int:
    """Draw a rank k in 1..n from the cumulative probabilities cum."""
    u = rng.random()
    for k, c in enumerate(cum, start=1):
        if u < c:
            return k
    return len(cum)


def tau_eo(
    s0: Sequence[int],
    J: Couplings,
    tau: float,
    steps: int,
    rng: random.Random,
    trace: list | None = None,
) -> tuple[list[int], float]:
    """tau-extremal optimization for the spin glass energy. Return (best spins, best energy).

    At each step, rank the spins from the worst local fitness (rank 1) to the best
    (rank n), with ties broken by the index, draw a rank k with probability
    proportional to k^(-tau), and flip that spin without any test. If trace is a
    list, append (k, i, lambda_i, energy before the flip) for each step.
    """
    n = len(s0)
    cum = list(itertools.accumulate(rank_probabilities(n, tau)))
    s = list(s0)
    e = energy(s, J)
    best, eb = list(s), e  # @line L1
    for _ in range(steps):  # @line L2
        lam = local_fitness(s, J)  # @line L3
        order = sorted(range(n), key=lambda i: (lam[i], i))  # @line L4
        k = draw_rank(cum, rng)  # @line L5
        i = order[k - 1]
        if trace is not None:
            trace.append((k, i, lam[i], e))
        s[i] = -s[i]  # @line L6
        e += 2 * lam[i]
        if e < eb:  # @line L7
            best, eb = list(s), e
    return best, eb  # @line L8


def ground_state(J: Couplings) -> tuple[list[int], float]:
    """Exhaustive search over all 2^n spin vectors, for small n."""
    n = len(J)
    best, eb = None, float("inf")
    for bits in itertools.product((1, -1), repeat=n):
        e = energy(bits, J)
        if e < eb:
            best, eb = list(bits), e
    return best, eb


def random_pm_j(n: int, rng: random.Random) -> list[list[int]]:
    """Symmetric couplings J_ij in {-1, +1} on all pairs, with J_ii = 0."""
    J = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            J[i][j] = J[j][i] = rng.choice((-1, 1))
    return J
