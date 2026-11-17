# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pooling-size-factors/. The authors are listed in prov/EQZ9B0.jsonl.
"""Size factors of single cells by pooling and deconvolution (Lun, Bach and Marioni 2016).

counts[g][j] is the count of gene g in cell j. With t_j the library size of
cell j and Z[g][j] = counts[g][j] / t_j, the reference pseudo-cell is
U[g] = the mean of Z[g][j] over all cells. For a pool S of cells,
V[g] = the sum of Z[g][j] over S, and the pool factor is the median over genes
of V[g] / U[g]. Under the model of the paper this estimates the sum over S of
x_j = theta_j / t_j, up to one constant. The pools are windows of w
consecutive cells on a ring of the cells ordered by library size, for several
window sizes. The equations "sum of x over S = pool factor", together with
weak equations "x_j = single-cell estimate", are solved by weighted least
squares, and theta_j = x_j t_j. The factors are scaled to mean 1.

An optional clustering step normalizes each cluster on its own and then
scales the clusters to each other by the median ratio of their average
normalized profiles, as in scran.
"""

from __future__ import annotations

import statistics
from typing import Dict, List, Optional, Sequence, Tuple

from rq3lin import solve

DEFAULT_SIZES = (20, 40, 60, 80, 100)
WEAK = 1e-6


def ring_order(lib_sizes: Sequence[float]) -> List[int]:
    """Cells by library size; ranks 1, 3, 5, ... go up one side of the ring and ranks 2, 4, 6, ... come down the other."""
    order = sorted(range(len(lib_sizes)), key=lambda j: (lib_sizes[j], j))
    return order[0::2] + order[1::2][::-1]  # @line L3


def ring_pools(n: int, sizes: Sequence[int]) -> List[List[int]]:
    """All windows of w consecutive positions on a ring of n, for each w in sizes, as position lists."""
    pools = []
    for w in sizes:
        if not 1 <= w <= n:
            raise ValueError("each pool size must be between 1 and the number of cells")
        for s in range(n):
            pools.append([(s + i) % n for i in range(w)])  # @line L4
    return pools


def median_ratio(values: Sequence[float], ref: Sequence[float]) -> float:
    """The median over genes with ref > 0 of values / ref."""
    ratios = [v / u for v, u in zip(values, ref) if u > 0]
    if not ratios:
        raise ValueError("no gene has a positive reference")
    return statistics.median(ratios)


def build_system(counts: Sequence[Sequence[float]], sizes: Sequence[int] = DEFAULT_SIZES,
                 weak: float = WEAK) -> Tuple[List[List[int]], List[float], List[float], List[float]]:
    """(pools as cell lists, pool factors, single-cell estimates, library sizes) for one group of cells."""
    G, n = len(counts), len(counts[0])
    t = [sum(counts[g][j] for g in range(G)) for j in range(n)]
    if min(t) <= 0:
        raise ValueError("every cell needs a positive library size")
    Z = [[counts[g][j] / t[j] for j in range(n)] for g in range(G)]  # @line L1
    U = [sum(row) / n for row in Z]  # @line L2
    ring = ring_order(t)
    pools = [[ring[p] for p in pool] for pool in ring_pools(n, sizes)]
    factors = []
    for S in pools:
        V = [sum(Z[g][j] for j in S) for g in range(G)]
        factors.append(median_ratio(V, U))  # @line L5
    single = [median_ratio([Z[g][j] for g in range(G)], U) for j in range(n)]
    return pools, factors, single, t


def solve_pools(n: int, pools: Sequence[Sequence[int]], factors: Sequence[float],
                single: Sequence[float], weak: float = WEAK) -> List[float]:
    """Weighted least squares for x: the pool equations with weight 1 and x_j = single_j with weight weak.

    The normal equations (A^T W A) x = A^T W b are solved by Gaussian elimination.
    """
    N = [[0.0] * n for _ in range(n)]
    rhs = [0.0] * n
    for S, f in zip(pools, factors):  # @line L6
        for a in S:
            rhs[a] += f
            row = N[a]
            for b in S:
                row[b] += 1.0
    for j in range(n):  # @line L7
        N[j][j] += weak
        rhs[j] += weak * single[j]
    return solve(N, rhs)  # @line L8


def deconvolve(counts: Sequence[Sequence[float]], sizes: Sequence[int] = DEFAULT_SIZES,
               weak: float = WEAK) -> List[float]:
    """Size factors theta_j = x_j t_j of one group of cells, before centering."""
    n = len(counts[0])
    pools, factors, single, t = build_system(counts, sizes, weak)
    x = solve_pools(n, pools, factors, single, weak)
    return [x[j] * t[j] for j in range(n)]  # @line L9


def pooled_size_factors(counts: Sequence[Sequence[float]], sizes: Sequence[int] = DEFAULT_SIZES,
                        clusters: Optional[Sequence[int]] = None, weak: float = WEAK) -> List[float]:
    """Size factors of all cells, scaled to mean 1.

    With clusters, each cluster is deconvolved on its own (all pool sizes must fit
    in each cluster), and cluster c is then multiplied by the median over genes of
    its mean normalized profile divided by that of the largest cluster.
    """
    G, n = len(counts), len(counts[0])
    if clusters is None:
        clusters = [0] * n
    groups: Dict[int, List[int]] = {}
    for j, c in enumerate(clusters):
        groups.setdefault(c, []).append(j)
    theta = [0.0] * n
    profile = {}
    for c, cells in groups.items():
        sub = [[counts[g][j] for j in cells] for g in range(G)]
        th = deconvolve(sub, sizes, weak)
        for j, v in zip(cells, th):
            theta[j] = v
        profile[c] = [sum(counts[g][j] / theta[j] for j in cells) / len(cells) for g in range(G)]
    ref = max(groups, key=lambda c: (len(groups[c]), -c))
    for c, cells in groups.items():
        if c == ref:
            continue
        both = [(p, q) for p, q in zip(profile[c], profile[ref]) if p > 0 and q > 0]
        tau = statistics.median(p / q for p, q in both) if both else 1.0  # @line L10
        for j in cells:
            theta[j] *= tau
    mean = sum(theta) / n
    return [v / mean for v in theta]  # @line L11
