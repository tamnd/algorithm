# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gelman-rubin-diagnostic/. The authors are listed in prov/T7ND6C.jsonl.

import math
from statistics import NormalDist
from typing import Sequence

Chains = Sequence[Sequence[float]]


def potential_scale_reduction(chains: Chains) -> float:
    """Classic R-hat = sqrt(var_plus / W) for m >= 2 chains of equal length n >= 2.

    W is the mean within-chain variance, B / n the variance of the chain means,
    and var_plus = (n - 1) / n * W + B / n. No degrees-of-freedom correction.
    """
    m = len(chains)
    if m < 2:
        raise ValueError("need at least 2 chains")
    n = len(chains[0])
    if n < 2 or any(len(c) != n for c in chains):
        raise ValueError("need chains of equal length, at least 2")
    means = [sum(c) / n for c in chains]
    grand = sum(means) / m
    w = sum(sum((x - mu) ** 2 for x in c) / (n - 1) for c, mu in zip(chains, means)) / m
    b = n * sum((mu - grand) ** 2 for mu in means) / (m - 1)
    if w == 0:
        return math.inf if b > 0 else 1.0
    var_plus = (n - 1) / n * w + b / n
    return math.sqrt(var_plus / w)


def split_chains(chains: Chains) -> list[list[float]]:
    """Split each chain into its first and second half; drop the middle draw if n is odd."""
    out = []
    for c in chains:
        h = len(c) // 2
        out.append(list(c[:h]))
        out.append(list(c[len(c) - h:]))
    return out


def split_rhat(chains: Chains) -> float:
    """R-hat on the 2m half-chains, which also detects trends inside each chain."""
    return potential_scale_reduction(split_chains(chains))


def rank_normalize(chains: Chains) -> list[list[float]]:
    """Replace each draw by Phi^-1((r - 3/8) / (S + 1/4)), r its pooled rank (ties averaged)."""
    flat = [(x, j, t) for j, c in enumerate(chains) for t, x in enumerate(c)]
    flat.sort(key=lambda e: e[0])
    s = len(flat)
    ranks = [0.0] * s
    i = 0
    while i < s:
        k = i
        while k + 1 < s and flat[k + 1][0] == flat[i][0]:
            k += 1
        avg = (i + k) / 2 + 1
        for p in range(i, k + 1):
            ranks[p] = avg
        i = k + 1
    nd = NormalDist()
    out = [[0.0] * len(c) for c in chains]
    for (_, j, t), r in zip(flat, ranks):
        out[j][t] = nd.inv_cdf((r - 0.375) / (s + 0.25))
    return out


def rank_normalized_split_rhat(chains: Chains) -> float:
    """Vehtari et al. (2021): max of the bulk and folded rank-normalized split R-hat."""
    halves = split_chains(chains)
    bulk = potential_scale_reduction(rank_normalize(halves))
    pooled = sorted(x for c in halves for x in c)
    s = len(pooled)
    med = (pooled[(s - 1) // 2] + pooled[s // 2]) / 2
    folded = [[abs(x - med) for x in c] for c in halves]
    tail = potential_scale_reduction(rank_normalize(folded))
    return max(bulk, tail)
