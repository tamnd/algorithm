# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/li-stephens-model/. The authors are listed in prov/QN36N8.jsonl.
"""The Li-Stephens haplotype copying model (Li and Stephens 2003).

A new haplotype h over m biallelic sites is built as a mosaic of K known
haplotypes (the panel). The hidden state X_j in 0..K-1 is the panel
haplotype copied at site j.

  X_1 is uniform on the panel.
  Between sites j and j+1, with s_j = 1 - exp(-rho_j / K), where rho_j is
  the scaled recombination rate 4 Ne r times the distance between the
  sites, the chain switches with probability s_j to a haplotype drawn
  uniformly from the panel (which may be the same one):
      P(X_{j+1} = y | X_j = x) = (1 - s_j) [x == y] + s_j / K.
  At site j, the copy has the allele of the copied haplotype with
  probability (K + theta / 2) / (K + theta), and the other allele with
  probability (theta / 2) / (K + theta).

The default theta is Watterson's 1 / (1 + 1/2 + ... + 1/(K-1)).

The forward algorithm gives P(h | panel) in O(mK) time, because each
transition is a mix of "stay" and "jump to a uniform state". Posterior
copying probabilities come from forward and backward passes.
"""

from __future__ import annotations

import itertools
import math
from typing import Sequence


def watterson_theta(k: int) -> float:
    if k < 2:
        raise ValueError("need at least two panel haplotypes for the default theta")
    return 1.0 / sum(1.0 / i for i in range(1, k))


def emission(k: int, theta: float) -> tuple[float, float]:
    """(probability of copying the allele, probability of the other allele)."""
    return (k + theta / 2.0) / (k + theta), (theta / 2.0) / (k + theta)


def switch_probabilities(rho: Sequence[float], k: int) -> list[float]:
    """s_j = 1 - exp(-rho_j / K) for each of the m - 1 gaps."""
    return [1.0 - math.exp(-r / k) for r in rho]


def check(panel: Sequence[Sequence[int]], h: Sequence[int], rho: Sequence[float], theta: float) -> tuple[int, int]:
    k = len(panel)
    if k == 0:
        raise ValueError("empty panel")
    m = len(h)
    if m == 0:
        raise ValueError("empty haplotype")
    for row in list(panel) + [h]:
        if len(row) != m or any(v not in (0, 1) for v in row):
            raise ValueError("haplotypes must be 0/1 rows of equal length")
    if len(rho) != m - 1 or any(r < 0 for r in rho):
        raise ValueError("need m - 1 nonnegative recombination rates")
    if theta <= 0:
        raise ValueError("theta must be positive, so that every haplotype has positive probability")
    return k, m


def forward(panel: Sequence[Sequence[int]], h: Sequence[int], rho: Sequence[float],
            theta: float | None = None) -> tuple[float, list[list[float]], list[float]]:
    """Scaled forward pass. Returns log P(h | panel), the scaled forward
    vectors (each sums to 1) and the scale factors c_j."""
    if theta is None:
        theta = watterson_theta(len(panel))
    k, m = check(panel, h, rho, theta)
    same, diff = emission(k, theta)
    s = switch_probabilities(rho, k)
    alpha = [(same if panel[x][0] == h[0] else diff) / k for x in range(k)]  # @line L1
    c = sum(alpha)  # @line L2
    alpha = [v / c for v in alpha]
    alphas, scales = [alpha], [c]
    for j in range(1, m):  # @line L3
        jump = s[j - 1] / k  # @line L4
        alpha = [((1.0 - s[j - 1]) * alpha[x] + jump) * (same if panel[x][j] == h[j] else diff)
                 for x in range(k)]  # @line L5
        c = sum(alpha)  # @line L6
        alpha = [v / c for v in alpha]  # @line L7
        alphas.append(alpha)
        scales.append(c)
    return sum(math.log(v) for v in scales), alphas, scales  # @line L8


def backward(panel: Sequence[Sequence[int]], h: Sequence[int], rho: Sequence[float],
             scales: Sequence[float], theta: float) -> list[list[float]]:
    """Backward vectors scaled with the forward factors."""
    k, m = check(panel, h, rho, theta)
    same, diff = emission(k, theta)
    s = switch_probabilities(rho, k)
    beta = [1.0] * k
    betas = [beta]
    for j in range(m - 1, 0, -1):
        e = [(same if panel[y][j] == h[j] else diff) * beta[y] for y in range(k)]
        total = sum(e) / k
        beta = [((1.0 - s[j - 1]) * e[x] + s[j - 1] * total) / scales[j] for x in range(k)]
        betas.append(beta)
    betas.reverse()
    return betas


def posterior(panel: Sequence[Sequence[int]], h: Sequence[int], rho: Sequence[float],
              theta: float | None = None) -> list[list[float]]:
    """P(X_j = x | h, panel) for each site j and panel haplotype x."""
    if theta is None:
        theta = watterson_theta(len(panel))
    _, alphas, scales = forward(panel, h, rho, theta)
    betas = backward(panel, h, rho, scales, theta)
    return [[a * b for a, b in zip(al, be)] for al, be in zip(alphas, betas)]


def path_probability(path: Sequence[int], panel: Sequence[Sequence[int]], h: Sequence[int],
                     rho: Sequence[float], theta: float) -> float:
    """Joint probability of one copying path and the haplotype h."""
    k, m = check(panel, h, rho, theta)
    same, diff = emission(k, theta)
    s = switch_probabilities(rho, k)
    p = 1.0 / k
    for j, x in enumerate(path):
        if j > 0:
            p *= (1.0 - s[j - 1]) * (path[j - 1] == x) + s[j - 1] / k
        p *= same if panel[x][j] == h[j] else diff
    return p


def enumerate_likelihood(panel: Sequence[Sequence[int]], h: Sequence[int], rho: Sequence[float],
                         theta: float) -> tuple[float, list[list[float]]]:
    """P(h | panel) and the posterior copying probabilities, by summing over all K^m paths."""
    k, m = check(panel, h, rho, theta)
    total = 0.0
    marg = [[0.0] * k for _ in range(m)]
    for path in itertools.product(range(k), repeat=m):
        p = path_probability(path, panel, h, rho, theta)
        total += p
        for j, x in enumerate(path):
            marg[j][x] += p
    return total, [[v / total for v in row] for row in marg]


def most_likely_path(panel: Sequence[Sequence[int]], h: Sequence[int], rho: Sequence[float],
                     theta: float | None = None) -> list[int]:
    """Viterbi path in O(mK) time, using the same stay-or-jump structure."""
    if theta is None:
        theta = watterson_theta(len(panel))
    k, m = check(panel, h, rho, theta)
    same, diff = emission(k, theta)
    s = switch_probabilities(rho, k)
    neg = -math.inf

    def lg(v: float) -> float:
        return math.log(v) if v > 0 else neg

    score = [lg(1.0 / k) + lg(same if panel[x][0] == h[0] else diff) for x in range(k)]
    back: list[list[int]] = []
    for j in range(1, m):
        best = max(range(k), key=lambda y: score[y])
        stay, jump = lg(1.0 - s[j - 1] + s[j - 1] / k), lg(s[j - 1] / k)
        new, ptr = [], []
        for x in range(k):
            a, b = score[x] + stay, score[best] + jump
            if a >= b:
                new.append(a)
                ptr.append(x)
            else:
                new.append(b)
                ptr.append(best)
            new[-1] += lg(same if panel[x][j] == h[j] else diff)
        score = new
        back.append(ptr)
    x = max(range(k), key=lambda y: score[y])
    path = [x]
    for ptr in reversed(back):
        x = ptr[x]
        path.append(x)
    path.reverse()
    return path
