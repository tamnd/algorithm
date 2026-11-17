# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/over-representation-analysis/. The authors are listed in prov/4AHTW8.jsonl.
"""Over-representation analysis with the hypergeometric (one-sided Fisher) test.

The universe U holds the N genes that could have been selected. The list D
of selected genes is cut to U, so n = |D|. For a gene set S, cut to U, with
K = |S| members, of which k are selected, the p-value is

    P(X >= k) = sum_{i=k}^{min(K, n)} C(K, i) C(N - K, n - i) / C(N, n),

the upper tail of the hypergeometric distribution. It is computed with
exact integers. The p-values of all sets are then adjusted by the
Benjamini-Hochberg method.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Dict, Hashable, Iterable, List, Mapping, Sequence


def hypergeom_upper_tail(k: int, total: int, good: int, draws: int) -> Fraction:
    """P(X >= k) for X good items among `draws` drawn without replacement from
    `total` items of which `good` are good, as an exact fraction."""
    if not 0 <= good <= total or not 0 <= draws <= total:
        raise ValueError("need 0 <= good, draws <= total")
    lo = max(k, 0, draws - (total - good))
    hi = min(good, draws)
    num = sum(math.comb(good, i) * math.comb(total - good, draws - i) for i in range(lo, hi + 1))  # @line L4
    return Fraction(num, math.comb(total, draws))


def bh_adjust(p: Sequence[float]) -> List[float]:
    """Benjamini-Hochberg adjusted p-values, min over j >= r of m p_(j) / j, capped at 1."""
    m = len(p)
    order = sorted(range(m), key=lambda i: p[i])
    out = [0.0] * m
    run = 1.0
    for r in range(m, 0, -1):
        i = order[r - 1]
        run = min(run, m * p[i] / r)
        out[i] = run
    return out


def ora(selected: Iterable[Hashable], universe: Iterable[Hashable],
        gene_sets: Mapping[str, Iterable[Hashable]], min_size: int = 1) -> Dict[str, dict]:
    """Test every gene set with at least min_size members in the universe.

    Returns, for each tested set: k (selected members), K (members in the
    universe), expected (n K / N), p and q (the BH-adjusted p-value).
    """
    u = set(universe)
    d = set(selected) & u  # @line L1
    total, draws = len(u), len(d)
    rows = {}
    for name, members in gene_sets.items():  # @line L2
        s = set(members) & u  # @line L3
        if len(s) < min_size:
            continue
        k = len(s & d)
        p = hypergeom_upper_tail(k, total, len(s), draws)
        rows[name] = {"k": k, "K": len(s), "expected": draws * len(s) / total if total else 0.0,
                      "p": float(p)}
    names = list(rows)
    q = bh_adjust([rows[x]["p"] for x in names])  # @line L5
    for x, v in zip(names, q):
        rows[x]["q"] = v
    return rows  # @line L6
